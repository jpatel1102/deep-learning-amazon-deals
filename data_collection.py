# 01_data_collection.py

import keepa
import pandas as pd
import time
import os

# ---------------
# SETTINGS
# ---------------
API_KEY = "3kj4vv6neism9vvejf9515cva29hhcr2td3qfumps2o329p0j5jvdffm8oldkfaq"   # <-- Replace this with your real Keepa API key
ASIN_LIST = [
    "B07PGL2ZSL",  # Echo Dot (Electronics)
    "B08N5WRWNW",  # Fire TV Stick
    "B07XJ8C8F5",  # Instant Pot
    "B08V83JZH4"    # Air Fryer
]
OUTPUT_CSV = "data/collected_deals.csv"

# ---------------
# FETCH DATA
# ---------------
def fetch_deals():
    try:
        print("Connecting to Keepa...")
        api = keepa.Keepa(API_KEY)
        print("Querying ASINs...")
        products = api.query(ASIN_LIST, domain='US')

        df = pd.json_normalize(products['products'])
        return df

    except Exception as e:
        print(f"Error fetching from Keepa: {e}")
        if os.path.exists(OUTPUT_CSV):
            print("Loading existing cached CSV...")
            return pd.read_csv(OUTPUT_CSV)
        else:
            print("No cached data found. Exiting.")
            exit(1)

# ---------------
# SAVE TO CSV
# ---------------
def save_deals(df):
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Deals saved to {OUTPUT_CSV}")

# ---------------
# MAIN
# ---------------
if __name__ == "__main__":
    deals_df = fetch_deals()
    save_deals(deals_df)
    print("✅ Data Collection Complete!")
