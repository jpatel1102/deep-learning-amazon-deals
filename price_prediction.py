# 02_price_prediction_model.py

import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# ---------------
# SETTINGS
# ---------------
INPUT_CSV = "data/collected_deals.csv"
MODEL_OUTPUT = "models/price_predictor_lstm.h5"

# ---------------
# LOAD DATA
# ---------------
def load_data():
    if not os.path.exists(INPUT_CSV):
        print("❗ Please run 01_data_collection.py first!")
        exit(1)
    df = pd.read_csv(INPUT_CSV)
    return df

# ---------------
# PREPARE DATA
# ---------------
def prepare_data(df):
    # For demo purposes, fake historical prices
    price = df['currentPrices.CURRENT'].dropna().values[:50]
    price = price.reshape(-1, 1)

    scaler = MinMaxScaler()
    price_scaled = scaler.fit_transform(price)

    X, y = [], []
    for i in range(5, len(price_scaled)):
        X.append(price_scaled[i-5:i])
        y.append(price_scaled[i])

    X, y = np.array(X), np.array(y)
    return X, y, scaler

# ---------------
# BUILD MODEL
# ---------------
def build_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=input_shape))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

# ---------------
# MAIN
# ---------------
if __name__ == "__main__":
    df = load_data()
    X, y, scaler = prepare_data(df)

    model = build_model((X.shape[1], X.shape[2]))
    print("Training model...")
    model.fit(X, y, epochs=50, verbose=1)

    os.makedirs(os.path.dirname(MODEL_OUTPUT), exist_ok=True)
    model.save(MODEL_OUTPUT)
    print(f"✅ Model saved to {MODEL_OUTPUT}")
