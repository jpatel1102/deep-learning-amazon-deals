# streamlit_app.py (FINAL VERSION)

import streamlit as st
import os
import pandas as pd
import time
from datetime import datetime
from transformers import pipeline

# --------------------
# Page Configuration
# --------------------
st.set_page_config(page_title="Amazon Home & Electronics Deals", layout="wide")
st.markdown(
    '''
    <div style="text-align: center;">
        <img src="https://st3.depositphotos.com/1001860/16375/i/450/depositphotos_163757632-stock-photo-amazon-logo-on-a-white.jpg" width="120">
        <h1 style="font-size: 2.5em;">Amazon Deals Advisor</h1>
    </div>
    ''',
    unsafe_allow_html=True
)

# --------------------
# Helper Functions
# --------------------

def fetch_deals():
    if os.path.exists("collected_deals.csv"):
        df = pd.read_csv("collected_deals.csv")
        st.success("✅ Loaded deals from collected_deals.csv!")
        return df
    else:
        st.error("❌ collected_deals.csv not found. Please collect data first!")
        st.stop()

def mock_predict_future_price(current_price):
    drop_percent = 0.05 + 0.1 * (time.time() % 1)
    future_price = current_price * (1 - drop_percent)
    return round(future_price, 2)

@st.cache_resource
def load_llm():
    return pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")


def recommend_deal(llm_pipeline, title):
    result = llm_pipeline(title)
    return result[0]['label']

# --------------------
# Main App
# --------------------

st.sidebar.header("Settings")
refresh = st.sidebar.button("🔄 Refresh Deals")

# Fetch deals
with st.spinner('Fetching Amazon deals...'):
    deals_df = fetch_deals()

# Focus on Home & Electronics
categories_of_interest = ['Electronics', 'Home & Kitchen', 'Appliances']
if 'categoryTree' in deals_df.columns:
    deals_df = deals_df[deals_df['categoryTree'].astype(str).str.contains('|'.join(categories_of_interest), case=False, na=False)]

# Basic filters
min_price = st.sidebar.slider('Minimum Price ($)', 0, 500, 20)
max_price = st.sidebar.slider('Maximum Price ($)', 50, 2000, 500)
min_rating = st.sidebar.slider('Minimum Rating', 0.0, 5.0, 3.5, 0.1)

# Process pricing
if 'currentPrices.CURRENT' in deals_df.columns:
    deals_df['current_price'] = deals_df['currentPrices.CURRENT']
elif 'price' in deals_df.columns:
    deals_df['current_price'] = deals_df['price']
else:
    deals_df['current_price'] = 100  # fallback mock price

# Filter
deals_df = deals_df[(deals_df['current_price'] >= min_price) & (deals_df['current_price'] <= max_price)]

# Mock rating field (temporary if no real rating)
deals_df['rating'] = 3.5 + (deals_df.index % 2) * 1.0

# Further rating filter
deals_df = deals_df[deals_df['rating'] >= min_rating]

# Load LLM
llm = load_llm()

st.subheader("🔥 Top Home & Electronics Deals")

cols = st.columns(2)
for idx, row in deals_df.iterrows():
    with cols[idx % 2]:
        # Title handling
        title = row.get('title', 'No Title')
        st.markdown(f"### {title[:70]}..." if pd.notna(title) else "No Title")

        # Current Price
        st.markdown(f"**Current Price:** ${row.get('current_price', 'N/A')}")

        # Predicted Future Price
        future_price = mock_predict_future_price(row.get('current_price', 0))
        st.markdown(f"**Predicted Future Price:** ${future_price}")

        # ➡️ Add Product Link
        asin = row.get('asin', None)
        if asin:
            amazon_url = f"https://www.amazon.com/dp/{asin}"
            st.markdown(f"[🔗 View on Amazon]({amazon_url})")
        else:
            st.markdown("❌ ASIN not available")

        # Recommendation
        recommendation = recommend_deal(llm, title)
        if recommendation == 'POSITIVE':
            st.success("✅ Recommended Deal!")
        else:
            st.warning("⚠️ Not Highly Recommended")
        
        st.markdown("---")
