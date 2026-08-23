import pandas as pd
import re

df = pd.read_csv('../data/urbankart_sales_messy.csv', dtype=str)
start_rows = len(df)

log = {}

# Step 1: Remove exact duplicate rows (on raw file)
before = len(df)
df = df.drop_duplicates(keep='first').reset_index(drop=True)
log['exact_duplicates_removed'] = before - len(df)

# Step 2: Standardize dates to YYYY-MM-DD
def parse_date(s):
    s = s.strip()
    # already ISO
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', s)
    if m:
        return s
    # DD/MM/YYYY
    m = re.match(r'^(\d{2})/(\d{2})/(\d{4})$', s)
    if m:
        d, mo, y = m.groups()
        return f"{y}-{mo}-{d}"
    # DD-MM-YY
    m = re.match(r'^(\d{2})-(\d{2})-(\d{2})$', s)
    if m:
        d, mo, y = m.groups()
        return f"20{y}-{mo}-{d}"
    # "Mon D, YYYY" or "Mon DD, YYYY"
    m = re.match(r'^([A-Za-z]{3})\s+(\d{1,2}),\s*(\d{4})$', s)
    if m:
        mon, d, y = m.groups()
        dt = pd.to_datetime(f"{mon} {d} {y}", format="%b %d %Y")
        return dt.strftime("%Y-%m-%d")
    raise ValueError(f"Unrecognized date format: {s}")

df['order_date'] = df['order_date'].apply(parse_date)

# Step 3: Standardize city names
city_map = {
    'GURGAON': 'Gurugram', 'GGN': 'Gurugram',
    'BANGALORE': 'Bengaluru', 'BLR': 'Bengaluru',
    'BOMBAY': 'Mumbai',
    'CALCUTTA': 'Kolkata',
    'MADRAS': 'Chennai',
    'COCHIN': 'Kochi',
    'NEW DELHI': 'Delhi',
}
official_cities = ['Delhi','Gurugram','Noida','Chandigarh','Bengaluru','Chennai','Hyderabad',
                    'Kochi','Mumbai','Pune','Ahmedabad','Surat','Kolkata','Bhubaneswar',
                    'Guwahati','Patna','Indore','Bhopal','Nagpur','Raipur']
official_city_upper = {c.upper(): c for c in official_cities}

def clean_city(s):
    s = s.strip()
    key = s.upper()
    if key in city_map:
        return city_map[key]
    if key in official_city_upper:
        return official_city_upper[key]
    return s  # fallback, shouldn't happen

df['city'] = df['city'].apply(clean_city)

# Step 3b: Standardize product names
official_products = [
    "43-inch Smart TV","Bluetooth Speaker Mini","Mirrorless Camera Lite","Noise-Cancelling Headphones",
    "Power Bank 20000mAh","Smart Watch X2","Ultrabook Air 14","Wireless Earbuds Pro",
    "Cotton Kurta Set","Denim Jacket","Ethnic Dupatta","Formal Shirt","Leather Wallet",
    "Running Sneakers","Silk Saree","Slim Fit Jeans",
    "Air Fryer 5L","Cotton Bedsheet Set","Dinner Set 24pc","Electric Kettle 1.5L",
    "Mixer Grinder 750W","Modern Wall Clock","Non-Stick Cookware Set","Robot Vacuum R7",
    "Beard Grooming Kit","Eau de Parfum 100ml","Face Wash Combo","Ionic Hair Dryer",
    "Makeup Brush Set","Matte Lipstick Set","Sunscreen SPF50","Vitamin C Serum",
    "Adjustable Dumbbells 15kg","Badminton Racket Set","Cricket Bat English Willow",
    "Cycling Helmet","Foldable Treadmill T2","Football Size 5","Gym Gloves","Yoga Mat Pro"
]
product_upper_map = {p.upper(): p for p in official_products}

def clean_product(s):
    s = s.strip()
    key = s.upper()
    if key in product_upper_map:
        return product_upper_map[key]
    return s

df['product_name'] = df['product_name'].apply(clean_product)

# Step 4: Fix total_revenue stored as text -> plain numbers
def clean_revenue(s):
    if pd.isna(s):
        return s
    s = str(s).strip()
    s = s.replace('₹', '').replace('INR', '').strip()
    s = s.replace(',', '')
    if s == '':
        return None
    val = float(s)
    return val

df['total_revenue'] = df['total_revenue'].apply(clean_revenue)
df['quantity'] = df['quantity'].apply(lambda x: float(x) if pd.notna(x) and str(x).strip()!='' else None)
df['unit_price'] = df['unit_price'].apply(lambda x: float(x))

# Step 5a: Drop rows with blank quantity or blank total_revenue
before = len(df)
blank_mask = df['quantity'].isna() | df['total_revenue'].isna()
log['dropped_blank_qty_or_revenue'] = int(blank_mask.sum())
df = df[~blank_mask].reset_index(drop=True)

# Step 5b: Fill blank region using city->region map
region_map = {
    'Delhi':'North','Gurugram':'North','Noida':'North','Chandigarh':'North',
    'Bengaluru':'South','Chennai':'South','Hyderabad':'South','Kochi':'South',
    'Mumbai':'West','Pune':'West','Ahmedabad':'West','Surat':'West',
    'Kolkata':'East','Bhubaneswar':'East','Guwahati':'East','Patna':'East',
    'Indore':'Central','Bhopal':'Central','Nagpur':'Central','Raipur':'Central',
}
blank_region_mask = df['region'].isna() | (df['region'].astype(str).str.strip()=='')
log['blank_region_filled'] = int(blank_region_mask.sum())
df.loc[blank_region_mask, 'region'] = df.loc[blank_region_mask, 'city'].map(region_map)

# Step 6: Remove invalid quantities (<=0)
before = len(df)
invalid_qty_mask = df['quantity'] <= 0
log['invalid_quantity_removed'] = int(invalid_qty_mask.sum())
df = df[~invalid_qty_mask].reset_index(drop=True)

# Step 7: Fix whitespace/casing on region, category, customer_id, sales_channel, order_id (trim)
for col in ['order_id','region','category','customer_id','sales_channel']:
    df[col] = df[col].astype(str).str.strip()

# quantity/total_revenue to int/plain numbers
df['quantity'] = df['quantity'].astype(int)
df['total_revenue'] = df['total_revenue'].round(2)
# if total_revenue is whole number, drop decimal
df['total_revenue'] = df['total_revenue'].apply(lambda x: int(x) if float(x).is_integer() else x)
df['unit_price'] = df['unit_price'].apply(lambda x: int(x) if float(x).is_integer() else x)

# Self-check: quantity * unit_price == total_revenue
check = (df['quantity'] * df['unit_price'] - df['total_revenue']).abs()
mismatch = df[check > 0.01]
print("Mismatched rows (qty*price != revenue):", len(mismatch))
if len(mismatch) > 0:
    print(mismatch.head(20))

# Reorder columns to original order
cols = ['order_id','order_date','region','city','product_name','category',
        'quantity','unit_price','total_revenue','customer_id','sales_channel']
df = df[cols]

df.to_csv('../data/urbankart_sales_clean.csv', index=False)

print("=== LOG ===")
for k,v in log.items():
    print(k, v)
print("Start rows:", start_rows)
print("Final rows:", len(df))
print("Total dropped:", start_rows - len(df))
