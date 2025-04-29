import keepa 
import pandas as pd
import time

# ----------------------------
    # Keepa API Connection
    # ----------------------------
API_KEY = "3kj4vv6neism9vvejf9515cva29hhcr2td3qfumps2o329p0j5jvdffm8oldkfaq"
api = keepa.Keepa(API_KEY)

    # Example ASINs (you can expand)
# Read ASINs from file instead of manually typing
with open("collected_asins.txt", "r") as f:
    asin_list = [line.strip() for line in f if line.strip()]
    # ----------------------------
    # Function to Fetch Deals
    # ----------------------------
def fetch_deals(asins):
    print("Fetching products...")
    products = api.query(asins, domain='US', history=True, buybox=True, offers=20)
    print(f"Fetched {len(products)} products.")
    return products

    # ----------------------------
    # Main
    # ----------------------------
try:
    deals_df = fetch_deals(asin_list)  # ✅ Pass asin_list correctly
    df = pd.json_normalize(deals_df)
    df.to_csv("collected_deals.csv", index=False)
    print("✅ Deals saved to 'collected_deals.csv'")

except Exception as e:
    print(f"❌ Error fetching: {e}")
