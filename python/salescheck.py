"""SalesCheck reference engine and CSV CLI, Python 3.10+, standard library only."""
import argparse
import csv
import io
import re
from decimal import Decimal
from pathlib import Path

MAX_SAFE = 2**53 - 1


def cents(value):
    text = str(value).strip()
    if not re.fullmatch(r'-?\d+(?:\.\d{1,2})?', text, flags=re.ASCII):
        return None
    number = int(Decimal(text) * 100)
    return number if abs(number) <= MAX_SAFE else None


def read_csv(path, required):
    text = Path(path).read_text(encoding='utf-8-sig')
    reader = csv.reader(io.StringIO(text), strict=True)
    records = [r for r in reader if any(v.strip() for v in r)]
    if not records:
        raise ValueError('CSV is empty')
    headers = [v.strip().lower() for v in records.pop(0)]
    if len(set(headers)) != len(headers) or any(not h for h in headers):
        raise ValueError('CSV headers must be unique and non-empty')
    if not set(required).issubset(headers) or not records:
        raise ValueError('Missing required columns or data rows')
    result = []
    for i, r in enumerate(records, 2):
        if len(r) != len(headers):
            raise ValueError(f'Record {i}: incorrect field count')
        result.append(dict(zip(headers, (v.strip() for v in r))))
    return result


def load_prices(records, overrides=False):
    result = {}
    for r in records:
        value = cents(r['unit_price'])
        key = (r['department'], r['item']) if overrides else r['item']
        if not r['item'] or (overrides and not r['department']) or value is None or value < 0 or key in result:
            raise ValueError('Invalid or duplicate price entry')
        result[key] = value
    return result


def validate(records, prices, patches=None):
    patches = patches or {}
    output = []
    for row_number, r in enumerate(records, 2):
        key = (r['department'], r['item'])
        unit = patches.get(key, prices.get(r['item']))
        quantity = int(r['quantity']) if re.fullmatch(r'\d+', r['quantity'], flags=re.ASCII) else None
        recorded = cents(r['sale_total'])
        expected, issue = None, ''
        if not r['department'] or not r['item']:
            issue = 'Missing field'
        elif quantity is None or not 0 < quantity <= MAX_SAFE:
            issue = 'Invalid quantity'
        elif recorded is None or recorded < 0:
            issue = 'Invalid amount'
        elif unit is None:
            issue = 'Unknown item'
        elif unit * quantity > MAX_SAFE:
            issue = 'Amount too large'
        else:
            expected = unit * quantity
            if expected != recorded:
                issue = 'Price mismatch'
        output.append(dict(r, row=row_number, recorded=recorded, expected=expected,
                           issue=issue, valid=not issue, override=key in patches))
    return output


def safe_cell(value):
    text = str(value)
    return "'" + text if text.startswith(('=', '+', '-', '@', '\t', '\r')) else text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sales', required=True)
    parser.add_argument('--prices', required=True)
    parser.add_argument('--overrides')
    parser.add_argument('--output', default='salescheck-report.csv')
    args = parser.parse_args()
    try:
        prices = load_prices(read_csv(args.prices, ['item', 'unit_price']))
        patches = load_prices(read_csv(args.overrides, ['department', 'item', 'unit_price']), True) if args.overrides else {}
        rows = validate(read_csv(args.sales, ['department', 'item', 'quantity', 'sale_total']), prices, patches)
        revenue = sum(r['recorded'] for r in rows if r['valid'])
        if revenue > MAX_SAFE:
            raise ValueError('Combined sales exceed supported amount')
        with open(args.output, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['row', 'department', 'item', 'quantity', 'recorded', 'expected', 'status'])
            for r in rows:
                writer.writerow([safe_cell(v) for v in [r['row'], r['department'], r['item'], r['quantity'],
                    r['sale_total'], '' if r['expected'] is None else f"{Decimal(r['expected']) / 100:.2f}",
                    'Valid' if r['valid'] else r['issue']]])
        valid = sum(r['valid'] for r in rows)
        print(f'{len(rows)} records | {valid} valid | {len(rows)-valid} flagged | AUD {Decimal(revenue)/100:.2f} valid sales')
        print(f'Report: {args.output}')
    except (ValueError, KeyError, OSError, csv.Error) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
