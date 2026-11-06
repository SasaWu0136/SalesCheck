# SalesCheck

A sales validation workspace by **Sasa Wu**. Upload a sales CSV, reconcile each transaction against base and department prices, investigate discrepancies, and export actionable reports.

Developed from my personal Python projects [Sale-Reporting](https://github.com/SasaWu0136/Sale-Reporting) and [Sales Validation & Multi-Department Reporting](https://github.com/SasaWu0136/Sales-Validation-Multi-Department-Reporting-System). This edition adds an accessible responsive dashboard, CSV import/export, traceable error reasons, filtering, price-list replacement, exact-cent calculations, and automated regression checks.

## Project evolution

| Version | Purpose | Added capabilities |
| --- | --- | --- |
| Sale-Reporting | Original personal Python project | Validate sales and summarize by item |
| Multi-Department Reporting | Extended personal Python project | Group by department and apply department price overrides |
| **SalesCheck** | Current portfolio edition | Interactive dashboard, CSV workflows, traceable discrepancies, exports, and exact-cent validation |

The two original repositories are retained as the project's history. **SalesCheck is the main maintained portfolio repository.**

## 中文快速開始

這個專案會核對銷售紀錄是否符合商品價格與部門專屬價格，找出金額不符、未知商品或無效數量，再整理成部門報表。

下載本 repo 後，用 Chrome 開啟 `dist/index.html` 即可操作，不必安裝套件。畫面預設提供 240 筆示範交易。先到 **Price lists** 匯入價格，再到 **Upload data** 上傳自己的銷售 CSV，最後於 **Validation results** 檢查異常與下載結果。重新整理頁面會清除匯入資料。

## Run the web application

No dependency installation or build step is required. Open `dist/index.html` directly in a browser, or serve the directory:

```sh
python3 -m http.server 8000 --directory dist
```

Visit http://localhost:8000. The dashboard starts with **clearly labelled demo data**: 240 records, 232 valid and 8 flagged. Every displayed total and chart is calculated from the underlying rows; there are no fixed KPI values. Use the supplied CSV examples or download the larger sample in the app.

## Workflow

1. View the demo overview and inspect the flagged records.
2. Import your base prices and optional department overrides in **Price lists**.
3. Upload your sales CSV and select **Validate sales**.
4. Filter transactions by issue, department, or search text; switch between flagged records and all transactions.
5. Export the complete result, all flagged records, or the department summary.

Importing prices replaces the corresponding list and immediately revalidates the current sales. Failed imports leave the previous dataset intact. Reset demo restores both sample sales and sample prices.

## CSV formats

Sales: `department,item,quantity,sale_total`

Base prices: `item,unit_price`

Department overrides: `department,item,unit_price`

Names are case-sensitive after trimming whitespace. Header names are case-insensitive. CSV supports UTF-8 BOM, CRLF/LF, quoted commas, escaped quotes, and quoted multiline fields. Extra columns are accepted; duplicate/empty headers and inconsistent field counts are rejected. The browser accepts CSVs up to 5 MB and 20,000 records. A price file must contain at least one row; use Reset demo to restore sample overrides.

## Business rules

- All amounts are **AUD**. Inputs use plain decimal notation with up to two decimal places, without currency symbols or thousands separators.
- Expected amount = applicable unit price × a positive whole-number quantity.
- A matching department override takes priority over the base price and can introduce a new item.
- **Exact cents, no tolerance.** JavaScript uses safe integer cents; Python uses Decimal conversion to integer cents. Unsafe amounts are rejected.
- Missing fields, invalid quantities, invalid amounts, unknown items, and price mismatches are flagged in that order. The first applicable error is reported.
- Only valid transactions contribute to revenue and department totals. Record validation rate = valid records / all records.
- All records are retained. Duplicate sales are not automatically removed.
- CSV record numbers include the header and are independent of physical lines in quoted multiline fields.
- CSV exports neutralize formula-leading text for spreadsheet safety. This can prefix negative values with an apostrophe.

Refunds, discounts, tax calculations, historical effective-date prices, duplicate detection, saved accounts, and multi-currency reconciliation are outside v1 scope. This is a portfolio validation tool, not an accounting ledger.

## Python CLI

The reference Python engine preserves the original Python focus and offers a standard-library command-line workflow:

```sh
python3 python/salescheck.py --sales examples/sales.csv --prices examples/base-prices.csv --overrides examples/department-prices.csv --output salescheck-report.csv
```

Requires Python 3.10+. Browser CSV processing is implemented in JavaScript and does not call the Python engine. The two engines share the same business rules and sample fixture expectations; they are maintained separately. Python's standard CSV parser may differ from the browser parser on malformed quote syntax.

## Validation

```sh
node --test tests/core.test.js
python3 -m unittest discover -s tests -p 'test_*.py'
```

Node.js 18+ is needed only to run JavaScript tests. Checks cover exact-cent money, overrides, unknown products, invalid quantities and amounts, malformed CSV, formula-safe exports, and department aggregation.

## Privacy and deployment

Sales and prices are held **in browser memory**. The app does not upload CSVs, create user accounts, or persist imported sales after reload. Hosted access control belongs to the hosting provider. Google Fonts is an optional external request; the interface has local font fallbacks. UI assets are buildless HTML/CSS/JavaScript and can be deployed to a static host using `dist/`.

## Structure

- `dist/`: deployable dashboard, styles, browser application, and validation engine.
- `python/`: Python reference engine and CSV CLI.
- `examples/`: CSV fixtures for a quick demonstration.
- `tests/`: JavaScript and Python regression checks.

Created and independently extended by Sasa Wu. The two original repositories remain the historical starting point; this edition does not overwrite either repository.
