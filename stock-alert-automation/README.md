# Stock Alert Automation

A Python CLI that reads an inventory CSV, flags products at or below their reorder point and generates an HTML report plus machine-readable JSON.

Inspired by retail ordering workflows. Personal portfolio project for **Deepak Puligilla**, developed with AI assistance. Uses fictional inventory, not OTR data or a workplace integration. Python 3.10+; standard library only.

## Run the demo

From this project folder:

```bash
python stock_alert.py examples/inventory.csv
python -m unittest discover -s tests -v
```

Use `py` on Windows or `python3` if needed. Open `reports/stock-alerts.html` in a browser. JSON is at `reports/stock-alerts.json`. Choose a different folder with `--output another-folder`; repeated runs overwrite the two named report files.

Expected: **5 products checked, 3 alerts**.

| Product | Stock | Reorder point | Target | Suggested order |
| --- | --- | --- | --- | --- |
| Paper cups pack | 0 | 4 | 12 | 12 |
| Coffee beans 1kg | 3 | 5 | 15 | 12 |
| Chocolate bars | 6 | 6 | 20 | 14 |

## Logic explained

`quantity <= reorder_point` triggers an alert, including the exact boundary. Zero quantity is classified out_of_stock; other alerts are low_stock. A suggested order is `max(0, target_stock - quantity)`. A product can trigger an alert but need zero units if its target equals its current quantity.

Example: Coffee has 3 units, a reorder point of 5 and a target of 15. Since 3 <= 5, it needs attention. The suggested order is 15 - 3 = 12 units.

## Walk through the code

1. `csv.DictReader` converts each CSV row into a dictionary using the header names.
2. Validation checks required columns, non-empty values, unique SKUs (case-insensitive) and non-negative whole numbers.
3. `analyze_inventory()` applies the rule and builds a list of alert dictionaries.
4. Alerts are sorted with zero-stock products first, then quantity and SKU.
5. `render_html()` escapes text before placing it in the HTML report. JSON retains the structured values.
6. The CLI prints a summary. Invalid input exits with code 2 and does not generate a new report. Existing reports from a previous run remain, so check that the command succeeded before using them.

## CSV format

Required unique headers: `sku,name,quantity,reorder_point,target_stock`.

Headers are case-sensitive. SKUs and names are trimmed; SKUs must be unique ignoring case. Quantities must be whole non-negative numbers. Target stock must be at least the reorder point. Extra named columns are ignored; unnamed extra values are rejected. Inventory with valid headers and no rows produces zero counts.

## Limits

This is a manual, on-demand automation tool. It does not run a background schedule, send messages or place orders. It does not account for pending deliveries, demand forecasts, pack sizes, prices, spoilage or stock reserved for customers. Confirm recommendations before ordering. Output contains product names and SKUs; use synthetic data for public demonstrations.

## Skills demonstrated

Business rules, CSV validation, dictionaries and lists, filtering and sorting, report generation, HTML escaping and automated tests.

## Learn it / interview practice

Explain the difference between reorder point and target stock, why duplicate SKUs must be rejected and why an alert is not an automatic purchase. Your first extension: add a supplier field and group alerts by supplier. Run and understand this AI-assisted project before presenting implementation experience.
