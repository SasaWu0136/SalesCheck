import importlib.util
import unittest
from pathlib import Path
spec = importlib.util.spec_from_file_location('salescheck', Path(__file__).parents[1] / 'python/salescheck.py')
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)

class ValidationTests(unittest.TestCase):
    def test_exact_cents(self):
        self.assertEqual(engine.cents('0.30'), 30)
        self.assertIsNone(engine.cents('0.301'))
        self.assertIsNone(engine.cents('NaN'))

    def test_shared_sample(self):
        root = Path(__file__).parents[1] / 'examples'
        prices = engine.load_prices(engine.read_csv(root/'base-prices.csv', ['item','unit_price']))
        patches = engine.load_prices(engine.read_csv(root/'department-prices.csv', ['department','item','unit_price']), True)
        rows = engine.validate(engine.read_csv(root/'sales.csv', ['department','item','quantity','sale_total']), prices, patches)
        self.assertEqual([r['issue'] for r in rows], ['', 'Price mismatch', '', '', 'Unknown item', 'Invalid quantity'])
        self.assertEqual(sum(r['recorded'] for r in rows if r['valid']), 2000)
        self.assertTrue(rows[2]['override'])

    def test_formula_escape(self):
        self.assertEqual(engine.safe_cell('=1+1'), "'=1+1")

if __name__ == '__main__':
    unittest.main()
