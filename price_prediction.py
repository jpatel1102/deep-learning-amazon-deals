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
df = pd.read_csv(INPUT_CSV)
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
# --------------

def extract_prices_from_column(df, column_name):
    prices = []
    if column_name not in df.columns:
        return prices
    
    for entry in df[column_name].dropna():
        try:
            if isinstance(entry, str):
                price_list = eval(entry)
            else:
                price_list = entry

            # Remove NaN, zeros, and invalid values
            price_list = [p for p in price_list if not (pd.isna(p) or p == 0)]

            if isinstance(price_list, list) and len(price_list) > 0:
                last_price = price_list[-1]
                if last_price > 0:
                    prices.append(last_price)
        except:
            continue

    return prices

def prepare_data(df):
    # Try multiple possible price fields
    possible_price_columns = ['data.NEW', 'data.AMAZON', 'data.LISTPRICE']

    prices = []
    for col in possible_price_columns:
        prices = extract_prices_from_column(df, col)
        if len(prices) > 0:
            print(f"✅ Found valid prices in column: {col}")
            break

    if len(prices) == 0:
        raise ValueError("❗ No valid prices found in any of ['data.NEW', 'data.AMAZON', 'data.LISTPRICE']. Check your collected data.")

    prices = np.array(prices[:50])

    scaler = MinMaxScaler()
    prices = scaler.fit_transform(prices.reshape(-1, 1))

    X = []
    y = []
    sequence_length = 2

    for i in range(len(prices) - sequence_length):
        X.append(prices[i:i+sequence_length])
        y.append(prices[i+sequence_length])

    X = np.array(X)
    y = np.array(y)

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

    if X.shape[0] == 0 or y.shape[0] == 0:
        print("❗ Not enough data to train the model. Please collect more deals with valid price history.")
        exit(1)

    print(f"✅ X shape: {X.shape}")
    print(f"✅ y shape: {y.shape}")

    model = build_model((X.shape[1], X.shape[2]))
    print("Training model...")
    model.fit(X, y, epochs=50, verbose=1)

    os.makedirs(os.path.dirname(MODEL_OUTPUT), exist_ok=True)
    model.save(MODEL_OUTPUT)
    print(f"✅ Model saved to {MODEL_OUTPUT}")
