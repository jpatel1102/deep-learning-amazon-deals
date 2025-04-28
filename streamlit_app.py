import streamlit as st
import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler

st.title("🏡📺 Amazon Home and Electrical Deals Advisor")

# Load
df = pd.read_csv("../data/cleaned_deals.csv")
model = tf.keras.models.load_model("../models/price_predictor_lstm.h5")

# Show Table
st.subheader("Top Deals Today!")
st.dataframe(df.sort_values(by="Drop Percentage", ascending=False).head(10))

# Prediction Area
st.subheader("Predict Future Price")

product = st.selectbox("Select Product", df["Title"])

idx = df[df["Title"] == product].index[0]
price = df.iloc[idx]["Current Price"]
prices = np.array([price]*5).reshape(-1,1)

scaler = MinMaxScaler()
prices_scaled = scaler.fit_transform(prices)

X_input = prices_scaled.reshape((1, prices_scaled.shape[0], 1))
predicted_price_scaled = model.predict(X_input)
predicted_price = scaler.inverse_transform(predicted_price_scaled)

st.success(f"Predicted next price: **${predicted_price.flatten()[0]:.2f}**")
