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

# Paths
DATA_PATH = '../crypto_data/hourly/ETH_hourly.csv'
MODEL_PATH = 'eth_hourly_simple_lstm.h5'
XGB_MODEL_PATH = 'eth_hourly_simple_xgb.pkl'
SCALER_PATH = 'eth_hourly_simple_scaler.pkl'

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
    
    # Convert to INR if needed
    avg_price = np.mean(prices)
    if avg_price < 50000:
        prices = prices * 82
        print("Data converted from USD to INR")
    
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
    model.add(LSTM(64, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.3))
    model.add(LSTM(32))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def build_xgb_model():
    return XGBRegressor(n_estimators=50, learning_rate=0.1, max_depth=4, random_state=42)

def plot_results(actual, predicted, title):
    plt.figure(figsize=(12,6))
    plt.plot(actual[-100:], label='Actual Prices', alpha=0.7)
    plt.plot(predicted[-100:], label='Ensemble Predictions', alpha=0.7)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Price (INR)')
    plt.legend()
    plt.show()

def train_models():
    look_back = 24
    print("Training ETH ensemble model...")
    X, y, scaler = load_and_preprocess_data(DATA_PATH, look_back)
    
    # Split data
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Train LSTM
    lstm_model = build_lstm_model((X.shape[1], 1))
    callbacks_list = [
        EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True),
        ModelCheckpoint(MODEL_PATH, save_best_only=True)
    ]
    
    lstm_model.fit(X_train, y_train, epochs=30, batch_size=32, 
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
    
    # Evaluate
    lstm_model = load_model(MODEL_PATH)
    lstm_pred = lstm_model.predict(X_test, verbose=0)
    xgb_pred = xgb_model.predict(X_test_flat).reshape(-1, 1)
    
    # Ensemble prediction (60% LSTM, 40% XGBoost)
    ensemble_pred = 0.6 * lstm_pred + 0.4 * xgb_pred
    
    # Convert back to original scale
    actual_prices = scaler.inverse_transform(y_test.reshape(-1, 1))
    predicted_prices = scaler.inverse_transform(ensemble_pred)
    
    mse = mean_squared_error(actual_prices, predicted_prices)
    print(f'Training complete!')
    print(f'Ensemble RMSE: {np.sqrt(mse):.2f} INR')
    
    plot_results(actual_prices, predicted_prices, 'ETH Hourly Price Prediction - Ensemble Model')
    return lstm_model, xgb_model, scaler, look_back

def predict_live(lstm_model, xgb_model, scaler, look_back, recent_prices):
    scaled_input = scaler.transform(np.array(recent_prices).reshape(-1, 1))
    
    # LSTM prediction
    lstm_input = scaled_input.reshape(1, look_back, 1)
    lstm_pred = lstm_model.predict(lstm_input, verbose=0)
    
    # XGBoost prediction
    xgb_input = scaled_input.flatten().reshape(1, -1)
    xgb_pred = xgb_model.predict(xgb_input).reshape(-1, 1)
    
    # Ensemble
    ensemble_pred = 0.6 * lstm_pred + 0.4 * xgb_pred
    final_price = scaler.inverse_transform(ensemble_pred)
    
    return final_price[0, 0]

if __name__ == '__main__':
    # Use different model names to avoid conflicts
    models_exist = (os.path.exists(MODEL_PATH) and 
                   os.path.exists(XGB_MODEL_PATH) and 
                   os.path.exists(SCALER_PATH))
    
    if not models_exist:
        print("Training new ETH ensemble model...")
        lstm_model, xgb_model, scaler, look_back = train_models()
    else:
        print("Loading saved ETH ensemble model...")
        lstm_model = load_model(MODEL_PATH)
        with open(XGB_MODEL_PATH, 'rb') as f:
            xgb_model = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        look_back = 24
    
    print(f"\nEnter the last {look_back} ETH hourly closing prices in INR:")
    prices_input = input()
    try:
        recent_prices = list(map(float, prices_input.strip().split()))
        if len(recent_prices) != look_back:
            raise ValueError(f"Expected exactly {look_back} values.")
        predicted_price = predict_live(lstm_model, xgb_model, scaler, look_back, recent_prices)
        print(f"\n✅ Predicted next ETH hourly price (INR): {predicted_price:.2f}")
    except Exception as e:
        print("Error:", e)
