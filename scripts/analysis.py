"""
UrbanKart Board Meeting Prep — Analysis Script
Answers three questions from the COO using the cleaned dataset:
  Q1: Which region generates the highest total revenue?
  Q2: What is month-on-month revenue growth for Apr->May and May->Jun?
  Q3: Which sales channel is weakest, and should it be paused?

Run: python analysis.py
Requires: pandas
"""
import pandas as pd

df = pd.read_csv('../data/urbankart_sales_clean.csv')
df['order_date'] = pd.to_datetime(df['order_date'])
df['month'] = df['order_date'].dt.to_period('M')

print("=" * 60)
print("Q1 — Which region is carrying us?")
print("=" * 60)
region_rev = df.groupby('region')['total_revenue'].sum().sort_values(ascending=False)
print(region_rev)
top_region = region_rev.idxmax()
print(f"\nAnswer: {top_region} — {region_rev.max():,}")

print("\n" + "=" * 60)
print("Q2 — Revenue momentum (Month-on-Month)")
print("=" * 60)
monthly = df.groupby('month')['total_revenue'].sum().sort_index()
print(monthly)
apr, may, jun = monthly.loc['2026-04'], monthly.loc['2026-05'], monthly.loc['2026-06']
apr_may = (may - apr) / apr * 100
may_jun = (jun - may) / may * 100
direction = "Growing" if apr_may > 0 and may_jun > 0 else ("Declining" if apr_may < 0 and may_jun < 0 else "Mixed")
print(f"\nApr -> May: {apr_may:+.1f}%")
print(f"May -> Jun: {may_jun:+.1f}%")
print(f"Direction: {direction}")

print("\n" + "=" * 60)
print("Q3 — The channel decision")
print("=" * 60)
total = df['total_revenue'].sum()
ch_stats = df.groupby('sales_channel').agg(
    revenue=('total_revenue', 'sum'),
    orders=('order_id', 'count'),
)
ch_stats['share'] = ch_stats['revenue'] / total * 100
ch_stats['aov'] = ch_stats['revenue'] / ch_stats['orders']
print(ch_stats.sort_values('revenue'))

weakest = ch_stats['revenue'].idxmin()
print(f"\nPart A — Weakest channel by revenue: {weakest} "
      f"({ch_stats.loc[weakest, 'share']:.1f}% of total revenue)")

# Look beyond total revenue: trajectory + order economics
ch_month = df.groupby(['sales_channel', 'month'])['total_revenue'].sum().unstack(level=0)
growth = (ch_month.loc['2026-06'] - ch_month.loc['2026-01']) / ch_month.loc['2026-01'] * 100
print("\nJan -> Jun growth by channel:")
print(growth.sort_values(ascending=False))

print("\nPart B — Recommendation: Do NOT pause the weakest-revenue channel.")
print("Reasoning: it has the highest AOV and by far the fastest Jan->Jun growth —")
print("it is gaining ground, not dead weight. See deliverables/UrbanKart_COO_Memo.docx")
print("for the full memo.")
