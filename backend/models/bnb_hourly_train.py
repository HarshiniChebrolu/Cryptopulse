import numpy as np
import pandas as pd
import os
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt

# Config for BNB
DATA_PATH = '../crypto_data/hourly/BNB_hourly.csv'
MODEL_PATH_LSTM = 'models/bnb_lstm_best.h5'
MODEL_PATH_XGB = 'models/bnb_xgb_best.pkl'
SCALER_PATH = 'models/bnb_scaler_best.pkl'
LOOK_BACK = 24  # Use 24 hours of price history
EPOCHS = 100
BATCH_SIZE = 32

def load_and_preprocess(filepath, look_back=LOOK_BACK):
    df = pd.read_csv(filepath)
    time_col = df.columns[0]
    if not np.issubdtype(df[time_col].dtype, np.number):
        df.set_index(time_col, inplace=True)
        df.index = pd.to_datetime(df.index, errors='coerce')
        df = df[df.index.notnull()]
        df = df.sort_index()
    close_col = [col for col in df.columns if col.lower() == 'close']
    assert close_col, "No close price column found!"
    prices = df[close_col[0]].values.reshape(-1, 1)

    print(f"Data price range: {prices.min():.2f} to {prices.max():.2f} INR")

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(prices)

    X, y = [], []
    for i in range(len(scaled) - look_back):
        X.append(scaled[i:i + look_back, 0])
        y.append(scaled[i + look_back, 0])
    X_seq = np.array(X).reshape(-1, look_back, 1)
    X_flat = np.array(X)
    y = np.array(y)

    return X_seq, X_flat, y, scaler, prices

def build_lstm(input_shape):
    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.3))
    model.add(LSTM(64))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_models():
    X_seq, X_flat, y, scaler, orig_prices = load_and_preprocess(DATA_PATH, LOOK_BACK)
    split = int(0.8 * len(X_seq))
    X_seq_train, X_seq_val = X_seq[:split], X_seq[split:]
    X_flat_train, X_flat_val = X_flat[:split], X_flat[split:]
    y_train, y_val = y[:split], y[split:]

    lstm = build_lstm((LOOK_BACK, 1))
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
        ModelCheckpoint(MODEL_PATH_LSTM, save_best_only=True)
    ]
    lstm.fit(X_seq_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE,
             validation_data=(X_seq_val, y_val), callbacks=callbacks, verbose=1, shuffle=False)

    xgb = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=6, random_state=42)
    xgb.fit(X_flat_train, y_train)

    with open(MODEL_PATH_XGB, 'wb') as f:
        pickle.dump(xgb, f)

    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)

    lstm_preds = lstm.predict(X_seq)
    xgb_preds = xgb.predict(X_flat).reshape(-1, 1)

    ensemble_preds = 0.6 * lstm_preds + 0.4 * xgb_preds
    actual = scaler.inverse_transform(y.reshape(-1, 1))
    predicted = scaler.inverse_transform(ensemble_preds)

    rmse = np.sqrt(mean_squared_error(actual, predicted))
    print(f"Training RMSE: {rmse:.4f} INR")

    plt.figure(figsize=(14, 7))
    plt.plot(actual[-200:], label='Actual Price')
    plt.plot(predicted[-200:], label='Predicted Price')
    plt.title('BNB Hourly Price Prediction (Ensemble)')
    plt.xlabel('Time')
    plt.ylabel('Price INR')
    plt.legend()
    plt.show()

    return lstm, xgb, scaler

def predict_next(lstm, xgb, scaler, input_prices):
    if len(input_prices) != LOOK_BACK:
        raise ValueError(f"Expected {LOOK_BACK} prices, got {len(input_prices)}.")

    arr = np.array(input_prices).reshape(-1, 1)
    scaled = scaler.transform(arr)

    lstm_in = scaled.reshape(1, LOOK_BACK, 1)
    xgb_in = scaled.flatten().reshape(1, -1)

    lstm_pred = lstm.predict(lstm_in, verbose=0)
    xgb_pred = xgb.predict(xgb_in).reshape(-1, 1)

    ensemble_pred = 0.6 * lstm_pred + 0.4 * xgb_pred
    final_pred = scaler.inverse_transform(ensemble_pred)

    return float(final_pred[0, 0])

if __name__ == "__main__":
    need_train = not (os.path.exists(MODEL_PATH_LSTM) and os.path.exists(MODEL_PATH_XGB) and os.path.exists(SCALER_PATH))

    if need_train:
        print("Training models, please wait...")
        lstm_model, xgb_model, scaler = train_models()
    else:
        print("Loading saved models...")
        lstm_model = load_model(MODEL_PATH_LSTM)
        with open(MODEL_PATH_XGB, 'rb') as f:
            xgb_model = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)

    print(f"\nEnter the last {LOOK_BACK} BNB hourly closing prices (space-separated):")
    inp = input()
    try:
        prices = list(map(float, inp.strip().split()))
        pred_price = predict_next(lstm_model, xgb_model, scaler, prices)
        print(f"Next predicted BNB price: ₹{pred_price:.2f}")
    except Exception as e:
        print("Error:", e)
