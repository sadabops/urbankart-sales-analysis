# Data Quality Note — UrbanKart Sales Export (Jan–Jun 2026)

Pulled in 5,150 raw order lines for UrbanKart's Jan–Jun 2026 export. Found four main issue types:

1. **150 exact duplicate rows** from the double-export during migration.
2. **208 rows with inconsistent date formats** — slash (`DD/MM/YYYY`), dash-YY (`DD-MM-YY`), and `Mon D, YYYY` mixed in with ISO dates.
3. **102 rows with revenue stored as text** — ₹ symbols, "INR" suffix, comma separators (e.g. `₹1,782`, `3500 INR`, `1,751.00`).
4. **Inconsistent city/product spelling and casing** across dozens of rows — city aliases (Bombay, GGN, BLR, Calcutta, Madras, Cochin, New Delhi), ALL CAPS entries, and stray whitespace.

Per finance's rule, dropped:
- **120 rows** with blank quantity or blank revenue (60 each, no overlap) — not recomputed or guessed, per instruction.
- **60 rows** with quantity ≤ 0 (known system errors: zero and negative values).

Filled:
- **60 blank regions** using the city→region mapping table.

**Final file:** 4,820 clean rows, 11 columns unchanged, every row verified to satisfy `quantity × unit_price = total_revenue`.

**Verdict: data is analysis-ready.**

## Cleaning order (matters — do not reorder)

1. Deduplicate on the raw file first.
2. Standardize dates.
3. Standardize city names *before* filling blank regions (the region map only recognizes official city names).
4. Standardize product names (exact-match against official spellings — no blanket title-case, since names like `43-inch Smart TV` and `Power Bank 20000mAh` use deliberate casing).
5. Parse revenue text to plain numbers.
6. Apply missing-value rules (drop blank qty/revenue, fill blank region).
7. Remove invalid quantities (≤ 0).
8. Trim whitespace and fix any remaining casing issues against official lists.

## Self-check

Before shipping, every surviving row was validated against: `quantity × unit_price == total_revenue`. Zero mismatches.
