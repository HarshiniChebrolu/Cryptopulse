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

DATA_PATH = '../crypto_data/daily/SOL_daily.csv'
MODEL_PATH = 'sol_daily_lstm_model.h5'
SCALER_PATH = 'sol_daily_scaler.pkl'
LOOK_BACK = 30

def load_and_preprocess_data(filepath, look_back=LOOK_BACK):
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

    # Optional currency conversion if needed
    avg_price = np.mean(prices)
    if avg_price < 200:  
        prices = prices * 82
        print("Data converted from USD to INR")

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)

    X, y = [], []
    for i in range(len(scaled_prices) - look_back):
        X.append(scaled_prices[i:i + look_back, 0])
        y.append(scaled_prices[i + look_back, 0])

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    return X, y, scaler

def build_model(input_shape):
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.3))
    model.add(LSTM(32))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def plot_results(actual, predicted):
    plt.figure(figsize=(14, 7))
    plt.plot(actual, label='Actual Prices')
    plt.plot(predicted, label='Predicted Prices')
    plt.title('SOL Daily Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Price (INR)')
    plt.legend()
    plt.show()

def train_model():
    X, y, scaler = load_and_preprocess_data(DATA_PATH, LOOK_BACK)
    model = build_model((X.shape[1], 1))
    callbacks_list = [
        EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        ModelCheckpoint(MODEL_PATH, save_best_only=True)
    ]
    model.fit(
        X, y,
        epochs=50,
        batch_size=32,
        validation_split=0.1,
        callbacks=callbacks_list,
        verbose=1,
        shuffle=False
    )

    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)

    model = load_model(MODEL_PATH)
    predictions = model.predict(X)
    predicted_prices = scaler.inverse_transform(predictions)
    actual_prices = scaler.inverse_transform(y.reshape(-1, 1))
    mse = mean_squared_error(actual_prices, predicted_prices)
    print(f'Mean Squared Error on training data: {mse}')
    plot_results(actual_prices, predicted_prices)
    return model, scaler, LOOK_BACK

def predict_live(model, scaler, look_back, recent_prices):
    if len(recent_prices) != look_back:
        raise ValueError(f"Expected exactly {look_back} values, got {len(recent_prices)}")

    scaled_input = scaler.transform(np.array(recent_prices).reshape(-1, 1))
    input_seq = np.reshape(scaled_input, (1, look_back, 1))
    scaled_pred = model.predict(input_seq)
    pred_price = scaler.inverse_transform(scaled_pred)
    return pred_price[0, 0]

if __name__ == '__main__':
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        print("Training SOL daily LSTM model...")
        model, scaler, look_back = train_model()
    else:
        print("Loading saved SOL daily model and scaler...")
        model = load_model(MODEL_PATH)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        look_back = LOOK_BACK

    print(f"\nEnter the last {look_back} SOL daily closing prices separated by spaces for live prediction:")
    prices_input = input()
    try:
        recent_prices = list(map(float, prices_input.strip().split()))
        if len(recent_prices) != look_back:
            raise ValueError(f"Expected exactly {look_back} values, but got {len(recent_prices)}.")
        predicted_price = predict_live(model, scaler, look_back, recent_prices)
        print(f"Predicted next SOL daily price (INR): {predicted_price:.2f}")
    except Exception as e:
        print("Error:", e)
