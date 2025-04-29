# Deep Learning Amazon Deals Advisor

Welcome to the **Amazon Deals Advisor**! 🚀

This project builds a system that:
- 📦 Collects real-time Amazon product data (via Keepa API)
- 🔢 Predicts future prices using a deep learning LSTM model
- 🧑‍💻 Generates product recommendations using an LLM (or fallback)
- 📈 Displays deals via an interactive Streamlit web app

---

## 📂 Folder Structure
```
- data_collection.py            # Collect Amazon deals and save to CSV
- price_prediction.py           # Train LSTM price predictor
- llm_recommendations.py        # Generate product recommendations
- streamlit_app.py              # Streamlit web app for final display
- collected_ains.txt            # ASINs list (Product IDs)
- collected_deals.csv           # Collected products data
- models/                       # Trained LSTM model saved here
  - price_predictor_lstm.h5
```

---

## 🔧 How to Run the Full Project

### Step 1: Clone Repository
```bash
git clone https://github.com/your_username/deep-learning-amazon-deals.git
cd deep-learning-amazon-deals
```

### Step 2: Create and Activate Environment
```bash
conda create -n deals_env python=3.9
conda activate deals_env
```

### Step 3: Install Requirements
```bash
pip install -r requirements.txt
```
(*If no requirements.txt, install manually: pandas, numpy, scikit-learn, tensorflow, transformers, keepa, streamlit*)

### Step 4: Collect Amazon Deals
```bash
python data_collection.py
```
- This will fetch products using Keepa API and save them in `collected_deals.csv`.

### Step 5: Train Price Prediction Model
```bash
python price_prediction.py
```
- This will train an LSTM model to predict future prices.
- Model is saved in `models/price_predictor_lstm.h5`

### Step 6: Generate Product Recommendations
```bash
python llm_recommendations.py
```
- Adds a "POSITIVE" or "NEGATIVE" recommendation for each product.

### Step 7: Run the Streamlit App
```bash
streamlit run streamlit_app.py
```
- Open your browser at `http://localhost:8501`
- View products, future prices, recommendations

---

## 📈 Features
- 💪 Real Amazon product fetching (Keepa API)
- 📊 Deep Learning (LSTM) for price forecasting
- 🧬 LLM-powered product recommendations
- 📅 Daily updated deals
- 🔗 Direct Amazon product links

---

## ⚠️ Important Notes
- **Keepa API Key**: You must have your own Keepa API Key (free or paid account)
- **Limitations**: If LLM cannot load locally, a Mock recommender is used.
- **Data Volume**: Better results if 100+ products are collected.
- **Images**: Currently, images are disabled in the app for stability.

---

## 💪 Future Improvements
- Use real LLM models (e.g., GPT-2/3)
- Add user authentication
- Display live charts of price history
- Improve UI/UX with buttons & advanced filters

---

# Happy Deal Hunting! 📈🚀

