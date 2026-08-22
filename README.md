# UrbanKart Sales Data — Cleaning & Board-Level Analysis

End-to-end data analyst project: cleaned a messy 6-month e-commerce sales export, then answered three business questions for a company's leadership team ahead of a board meeting — including pushing back on a decision-maker's assumption with data.

## Project context

UrbanKart is a Delhi NCR–based e-commerce company that migrated to a new order management system. The migration export (5,150 order lines, Jan–Jun 2026) had duplicate rows, three inconsistent date formats, city names spelled multiple ways, revenue stored as text, and blank/invalid values. Leadership needed clean, trustworthy numbers before a Friday board meeting.

## Part 1 — Data Cleaning

**Task:** Turn the raw export into an analysis-ready dataset following seven specific cleaning rules (exact duplicate removal, date standardization, city/product name standardization, currency parsing, business-rule-based handling of missing values, invalid-quantity removal, and casing fixes — without blanket transformations that would destroy deliberate formatting like `43-inch Smart TV` or `SPF50`).

**Result:** 5,150 → 4,820 rows. Every surviving row passes `quantity × unit_price = total_revenue`.

| Issue found | Rows affected |
|---|---|
| Exact duplicate rows | 150 |
| Blank `quantity` (dropped per finance rule) | 60 |
| Blank `total_revenue` (dropped per finance rule) | 60 |
| Invalid quantity (≤ 0) | 60 |
| Blank `region` (filled from city→region map) | 60 |
| Mixed date formats | 208 |
| Revenue stored as text (₹, INR, commas) | 102 |
| City/product name & casing inconsistencies | multiple |

Full write-up: [`docs/data_quality_note.md`](docs/data_quality_note.md)

## Part 2 — Business Analysis

The COO asked three questions ahead of the board meeting. The third was a trap: he'd already decided to pause the company's lowest-revenue sales channel to cut costs, and wanted the data to confirm it.

**Q1 — Which region is carrying us?**
South leads with ₹1,06,05,827 in total revenue — but North is only ~15% behind, so the lead is real but not dominant.

**Q2 — Revenue momentum?**
Growing every month, Jan–Jun. April→May: +7.8%. May→June: +4.5%.

**Q3 — Should we pause the weakest channel?**
Marketplace has the lowest total revenue (26.0% share) — but total revenue alone is misleading. Marketplace also has:
- The **highest average order value** (₹10,366 vs. ₹7,900 Website, ₹6,938 App)
- **158% revenue growth** Jan→Jun — by far the fastest-growing channel, while Website grew just 0.9% and actually declined 14.9% month-on-month in its most recent transition

**Recommendation: Do not pause Marketplace.** It's a channel gaining ground, not dead weight. Website is the one that actually warrants scrutiny. Full reasoning in the memo below.

## Repository structure

```
├── data/
│   ├── urbankart_sales_messy.csv     # Original export (as received)
│   └── urbankart_sales_clean.csv     # Cleaned, analysis-ready dataset
├── scripts/
│   ├── clean.py                      # Cleaning pipeline (Part 1)
│   ├── analysis.py                   # Q1–Q3 analysis (Part 2)
│   └── build_xlsx.py                 # Generates the Excel workbook deliverable
├── deliverables/
│   ├── UrbanKart_Board_Analysis.xlsx # Full workbook: data, formulas, charts, answer summary
│   └── UrbanKart_COO_Memo.docx       # One-page memo to the COO
├── docs/
│   └── data_quality_note.md          # Cleaning summary written for leadership
└── screenshots/                      # Before/after and chart screenshots
```

## Tools used

Python (pandas) for cleaning and analysis · openpyxl for the Excel deliverable with live formulas and charts · Excel/Google Sheets equivalent formulas documented in `docs/data_quality_note.md` for non-Python workflows.

## How to reproduce

```bash
cd scripts
python clean.py       # produces ../data/urbankart_sales_clean.csv
python analysis.py    # prints Q1–Q3 answers
```

---
*This project was completed as part of an analytics training/assignment series. Data is illustrative/exercise data, not real UrbanKart business records.*
