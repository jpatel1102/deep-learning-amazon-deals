import streamlit as st
import keepa
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
    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/a/ab/Logo_TV_2015.png" width="120">
        <h1 style="padding-left: 20px; font-size: 2.5em;">Deep Learning Amazon Deals Advisor</h1>
    </div>
    ''',
    unsafe_allow_html=True
)

# --------------------
# Helper Functions
# --------------------

def fetch_deals():
    api_key = "your-keepa-api-key-here"

    try:
        api = keepa.Keepa(api_key)
        asin_list = [
            "B07PGL2ZSL",  # Echo Dot
            "B08N5WRWNW",  # Fire TV Stick
            "B07XJ8C8F5",  # Instant Pot
            "B08V83JZH4"   # Air Fryer
        ]
        product_data = api.query(asin_list, domain='US')
        df = pd.json_normalize(product_data['products'])
        return df

    except Exception as e:
        st.error(f"⚠️ Live data fetch failed: {e}")
        st.warning("Loading mock data instead...")

        # Fallback mock data
        data = {
            "title": ["Mock Echo Dot", "Mock Fire Stick", "Mock Instant Pot", "Mock Air Fryer"],
            "current_price": [49.99, 39.99, 89.99, 129.99],
            "imagesCSV": [
                "https://via.placeholder.com/150",
                "https://via.placeholder.com/150",
                "https://via.placeholder.com/150",
                "https://via.placeholder.com/150"
            ],
            "categoryTree": ["Electronics", "Electronics", "Home & Kitchen", "Appliances"]
        }
        df = pd.DataFrame(data)
        return df


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
with st.spinner('Fetching live Amazon deals...'):
    deals_df = fetch_deals()

# Focus on Home & Electronics categories
categories_of_interest = ['Electronics', 'Home & Kitchen', 'Appliances']
deals_df = deals_df[deals_df['categoryTree'].astype(str).str.contains('|'.join(categories_of_interest))]

# Basic filters
min_price = st.sidebar.slider('Minimum Price ($)', 0, 500, 20)
max_price = st.sidebar.slider('Maximum Price ($)', 50, 2000, 500)
min_rating = st.sidebar.slider('Minimum Rating', 0.0, 5.0, 3.5, 0.1)

# Filter deals
try:
    # try real Keepa field
    deals_df['current_price'] = deals_df['currentPrices.CURRENT']
except KeyError:
    # fallback: already using mock 'current_price'
    pass
deals_df = deals_df[(deals_df['current_price'] >= min_price) & (deals_df['current_price'] <= max_price)]

# Mock rating field
deals_df['rating'] = 3.5 + (deals_df.index % 2) * 1.0
deals_df = deals_df[deals_df['rating'] >= min_rating]

# Load LLM for recommendation
llm = load_llm()

st.subheader("🔥 Top Home & Electronics Deals")

# Display deals
cols = st.columns(2)
for idx, row in deals_df.iterrows():
    with cols[idx % 2]:
        st.image(row['imagesCSV'].split(',')[0] if pd.notna(row['imagesCSV']) else "https://via.placeholder.com/150", width=150)
        st.markdown(f"### {row['title'][:60]}...")
        st.markdown(f"**Current Price:** ${row['current_price']}")
        future_price = mock_predict_future_price(row['current_price'])
        st.markdown(f"**Predicted Future Price:** ${future_price}")
        recommendation = recommend_deal(llm, row['title'])
        if recommendation == 'POSITIVE':
            st.success("✅ Recommended Deal!")
        else:
            st.warning("⚠️ Not Highly Recommended")
        st.markdown("---")

st.success("Data loaded and displayed successfully!")
