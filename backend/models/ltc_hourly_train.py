import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import os
import pickle
from xgboost import XGBRegressor

# Brand new file names to avoid any conflicts
DATA_PATH = '../crypto_data/hourly/LTC_hourly.csv'
MODEL_PATH = 'ltc_hourly_v2_lstm.h5'
XGB_MODEL_PATH = 'ltc_hourly_v2_xgb.pkl'
SCALER_PATH = 'ltc_hourly_v2_scaler.pkl'

def load_and_preprocess_data(filepath, look_back=24):
    data = pd.read_csv(filepath)
    col0 = data.columns[0]
    if not np.issubdtype(data[col0].dtype, np.number):
        data.set_index(col0, inplace=True)
        try:
            data.index = pd.to_datetime(data.index, errors='coerce')
            data = data[data.index.notnull()]
        except Exception:
            pass
    
    price_col = [col for col in data.columns if col.lower() == 'close']
    if not price_col:
        raise ValueError("No 'Close' column found in data.")
    prices = data[price_col[0]].values.reshape(-1, 1)
    
    # Clean data - remove invalid prices
    prices = prices[prices > 0]
    prices = prices[~np.isnan(prices)]
    prices = prices[~np.isinf(prices)]
    prices = prices.reshape(-1, 1)
    
    # Convert to INR if needed
    avg_price = np.mean(prices)
    print(f"Original data average: {avg_price:.2f}")
    
    if avg_price < 1000:  # USD range for LTC
        prices = prices * 82
        print(f"Converted USD to INR")
    
    print(f"Final training range: {prices.min():.0f} - {prices.max():.0f} INR")
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)
    
    X, y = [], []
    for i in range(len(scaled_prices) - look_back):
        X.append(scaled_prices[i:i + look_back, 0])
        y.append(scaled_prices[i + look_back, 0])
    
    X = np.array(X)
    y = np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    return X, y, scaler

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(32, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(16))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def build_xgb_model():
    return XGBRegressor(n_estimators=30, learning_rate=0.1, max_depth=3, random_state=42)

def train_models():
    look_back = 24
    print("=== Training Brand New LTC Hourly Model ===")
    X, y, scaler = load_and_preprocess_data(DATA_PATH, look_back)
    
    print(f"Training data shape: {X.shape}")
    print(f"Scaler min/max: {scaler.data_min_[0]:.2f} / {scaler.data_max_[0]:.2f}")
    
    # Split data
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Train LSTM (smaller, simpler model)
    lstm_model = build_lstm_model((X.shape[1], 1))
    callbacks_list = [
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ModelCheckpoint(MODEL_PATH, save_best_only=True)
    ]
    
    lstm_model.fit(X_train, y_train, epochs=15, batch_size=16, 
                   validation_data=(X_test, y_test), callbacks=callbacks_list, verbose=1)
    
    # Train XGBoost
    X_train_flat = X_train.reshape(X_train.shape[0], -1)
    X_test_flat = X_test.reshape(X_test.shape[0], -1)
    
    xgb_model = build_xgb_model()
    xgb_model.fit(X_train_flat, y_train.flatten())
    
    # Save models
    with open(XGB_MODEL_PATH, 'wb') as f:
        pickle.dump(xgb_model, f)
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    
    print("=== Testing Model ===")
    # Test on some data
    lstm_model = load_model(MODEL_PATH)
    test_pred_lstm = lstm_model.predict(X_test[:5], verbose=0)
    test_pred_xgb = xgb_model.predict(X_test_flat[:5]).reshape(-1, 1)
    ensemble_test = 0.6 * test_pred_lstm + 0.4 * test_pred_xgb
    
    # Inverse transform to check sanity
    actual_test = scaler.inverse_transform(y_test[:5].reshape(-1, 1))
    predicted_test = scaler.inverse_transform(ensemble_test)
    
    print("Sample predictions vs actual:")
    for i in range(5):
        print(f"  Actual: {actual_test[i,0]:.2f}, Predicted: {predicted_test[i,0]:.2f}")
    
    return lstm_model, xgb_model, scaler, look_back

def predict_live(lstm_model, xgb_model, scaler, look_back, recent_prices):
    print(f"\n=== Live Prediction Debug ===")
    print(f"Input prices: {recent_prices}")
    print(f"Input range: {min(recent_prices):.2f} - {max(recent_prices):.2f}")
    
    # Validate prices
    if any(p <= 0 for p in recent_prices):
        raise ValueError("All prices must be positive!")
    
    if not (5000 <= np.mean(recent_prices) <= 15000):
        print(f"⚠️ Warning: Prices seem unusual for LTC INR")
    
    # Scale input
    input_array = np.array(recent_prices).reshape(-1, 1)
    scaled_input = scaler.transform(input_array)
    print(f"Scaled input range: {scaled_input.min():.6f} - {scaled_input.max():.6f}")
    
    # LSTM prediction
    lstm_input = scaled_input.reshape(1, look_back, 1)
    lstm_pred = lstm_model.predict(lstm_input, verbose=0)
    print(f"LSTM scaled prediction: {lstm_pred[0,0]:.6f}")
    
    # XGBoost prediction
    xgb_input = scaled_input.flatten().reshape(1, -1)
    xgb_pred = xgb_model.predict(xgb_input).reshape(-1, 1)
    print(f"XGBoost scaled prediction: {xgb_pred[0,0]:.6f}")
    
    # Ensemble
    ensemble_pred = 0.6 * lstm_pred + 0.4 * xgb_pred
    print(f"Ensemble scaled prediction: {ensemble_pred[0,0]:.6f}")
    
    # Inverse transform
    final_price = scaler.inverse_transform(ensemble_pred)
    print(f"Final price: {final_price[0,0]:.2f}")
    
    return final_price[0, 0]

if __name__ == '__main__':
    # ALWAYS train new model (no loading)
    print("🔥 Training completely fresh model...")
    lstm_model, xgb_model, scaler, look_back = train_models()
    
    print(f"\n=== Model Ready ===")
    print(f"Scaler trained on: {scaler.data_min_[0]:.2f} - {scaler.data_max_[0]:.2f} INR")
    print(f"Enter the last {look_back} LTC hourly closing prices in INR:")
    
    prices_input = input()
    try:
        recent_prices = list(map(float, prices_input.strip().split()))
        if len(recent_prices) != look_back:
            raise ValueError(f"Expected exactly {look_back} values.")
            
        predicted_price = predict_live(lstm_model, xgb_model, scaler, look_back, recent_prices)
        print(f"\n✅ Predicted next LTC hourly price (INR): {predicted_price:.2f}")
        
    except Exception as e:
        print("Error:", e)
