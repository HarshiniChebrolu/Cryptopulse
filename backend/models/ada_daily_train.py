import numpy as np
import pandas as pd
import os
import pickle
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# ---- PATHS for ADA DAILY ----
DATA_PATH = '../crypto_data/daily/ADA_daily.csv'
MODEL_PATH = 'ada_daily_lstm_model.h5'
SCALER_PATH = 'ada_daily_scaler.pkl'
SCALE_FACTOR = 1e6  # Set as appropriate for ADA daily range

def load_and_preprocess_data(filepath, look_back=60):
    df = pd.read_csv(filepath)
    if not np.issubdtype(df[df.columns[0]].dtype, np.number):
        df.set_index(df.columns[0], inplace=True)
        try:
            df.index = pd.to_datetime(df.index, errors='coerce')
            df = df[df.index.notnull()]
        except Exception:
            pass
    close_col = [col for col in df.columns if col.lower() == 'close']
    if not close_col:
        raise ValueError("No 'Close' column found in the dataset.")
    close_prices = df[close_col[0]].values.reshape(-1, 1)
    close_prices = close_prices[~np.isnan(close_prices).flatten()]
    scaled_down_prices = close_prices / SCALE_FACTOR
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(scaled_down_prices)
    X, y = [], []
    for i in range(len(scaled_prices) - look_back):
        X.append(scaled_prices[i:i + look_back, 0])
        y.append(scaled_prices[i + look_back, 0])
    X, y = np.array(X), np.array(y)
    X = X.reshape(X.shape[0], X.shape[1], 1)
    return X, y, scaler

def build_model(input_shape):
    model = Sequential([
        LSTM(128, return_sequences=True, input_shape=input_shape),
        Dropout(0.3),
        LSTM(64),
        Dropout(0.3),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model():
    look_back = 60
    X, y, scaler = load_and_preprocess_data(DATA_PATH, look_back)
    model = build_model((look_back, 1))
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        ModelCheckpoint(MODEL_PATH, save_best_only=True),
    ]
    model.fit(
        X, y,
        epochs=50,
        batch_size=64,
        validation_split=0.1,
        callbacks=callbacks,
        verbose=1
    )
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    model = load_model(MODEL_PATH)
    pred_scaled = model.predict(X)
    pred_prices = scaler.inverse_transform(pred_scaled) * SCALE_FACTOR
    actual_prices = scaler.inverse_transform(y.reshape(-1, 1)) * SCALE_FACTOR
    mse = mean_squared_error(actual_prices, pred_prices)
    print(f'Training MSE: {mse}')
    print(f'Training RMSE: {np.sqrt(mse)}')
    plt.figure(figsize=(14,7))
    plt.plot(actual_prices, label='Actual')
    plt.plot(pred_prices, label='Predicted')
    plt.title('ADA Daily Price Prediction')
    plt.xlabel('Samples')
    plt.ylabel('Price (INR)')
    plt.legend()
    plt.show()
    return model, scaler, look_back

def predict_live(model, scaler, look_back, input_prices):
    if len(input_prices) != look_back:
        raise ValueError(f'Input price count must be {look_back}, got {len(input_prices)}')
    input_array = np.array(input_prices).reshape(-1, 1) / SCALE_FACTOR
    input_scaled = scaler.transform(input_array).reshape(1, look_back, 1)
    scaled_pred = model.predict(input_scaled)
    pred_price = scaler.inverse_transform(scaled_pred) * SCALE_FACTOR
    return float(pred_price[0, 0])

if __name__ == '__main__':
    if os.path.exists(MODEL_PATH):
        os.remove(MODEL_PATH)
    if os.path.exists(SCALER_PATH):
        os.remove(SCALER_PATH)
    print('Training ADA daily LSTM model...')
    model, scaler, look_back = train_model()
    print(f'\nEnter the last {look_back} ADA daily closing prices in INR, separated by spaces:')
    user_input = input()
    try:
        prices = list(map(float, user_input.strip().split()))
        prediction = predict_live(model, scaler, look_back, prices)
        print(f'Predicted next ADA closing price (INR): {prediction:.2f}')
    except Exception as e:
        print(f'Error: {e}')
