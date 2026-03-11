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

DATA_PATH = '../crypto_data/daily/XRP_daily.csv'
MODEL_PATH = 'xrp_daily_lstm_model.h5'
SCALER_PATH = 'xrp_daily_scaler.pkl'
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

    # Convert USD to INR if average price low
    avg_price = np.mean(prices)
    if avg_price < 2:
        prices = prices * 82
        print(f"Converted USD to INR range: {prices.min():.2f} - {prices.max():.2f}")
    else:
        print(f"Data in INR range: {prices.min():.2f} - {prices.max():.2f}")

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

def build_model(input_shape):
    model = Sequential()
    model.add(LSTM(32, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(16))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def plot_results(actual, predicted):
    plt.figure(figsize=(14,7))
    plt.plot(actual, label='Actual Prices')
    plt.plot(predicted, label='Predicted Prices')
    plt.title('XRP Daily Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

def train_model():
    X, y, scaler = load_and_preprocess_data(DATA_PATH, LOOK_BACK)
    model = build_model((X.shape[1], 1))
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        ModelCheckpoint(MODEL_PATH, save_best_only=True)
    ]
    model.fit(
        X, y,
        epochs=40,
        batch_size=32,
        validation_split=0.1,
        shuffle=False,
        callbacks=callbacks,
        verbose=1
    )
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)

    model = load_model(MODEL_PATH)
    predictions = model.predict(X)
    predicted_prices = scaler.inverse_transform(predictions)
    actual_prices = scaler.inverse_transform(y.reshape(-1, 1))
    mse = mean_squared_error(actual_prices, predicted_prices)
    print(f'Training Mean Squared Error: {mse}')
    plot_results(actual_prices, predicted_prices)

    return model, scaler, LOOK_BACK

def predict_live(model, scaler, look_back, recent_prices):
    if len(recent_prices) != look_back:
        raise ValueError(f"Expected {look_back} inputs, got {len(recent_prices)}")
    scaled_input = scaler.transform(np.array(recent_prices).reshape(-1, 1))
    input_seq = scaled_input.reshape(1, look_back, 1)
    scaled_pred = model.predict(input_seq)
    pred = scaler.inverse_transform(scaled_pred)
    return pred[0, 0]

if __name__ == '__main__':
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        print("Training XRP LSTM model...")
        model, scaler, look_back = train_model()
    else:
        print("Loading saved XRP LSTM model and scaler...")
        model = load_model(MODEL_PATH)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        look_back = LOOK_BACK

    print(f"\nEnter the last {look_back} XRP daily closing prices separated by spaces for live prediction:")
    prices_input = input()
    try:
        recent_prices = list(map(float, prices_input.strip().split()))
        if len(recent_prices) != look_back:
            raise ValueError(f"Expected exactly {look_back} values.")
        prediction = predict_live(model, scaler, look_back, recent_prices)
        print(f"Predicted next XRP daily price (INR): {prediction:.2f}")
    except Exception as e:
        print(f"Error during prediction: {e}")
