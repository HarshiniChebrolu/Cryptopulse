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


# Config
DATA_PATH = '../crypto_data/hourly/ADA_hourly.csv'
MODEL_PATH_LSTM = "ada_hourly_lstm_xgb_model.h5"
MODEL_PATH_XGB = "ada_hourly_xgb_model.pkl"
SCALER_PATH = "ada_hourly_scaler.pkl"
LOOK_BACK = 24  # Number of hours as predictors


def load_and_preprocess(filepath, look_back=LOOK_BACK):
    df = pd.read_csv(filepath)
    col0 = df.columns[0]
    if not np.issubdtype(df[col0].dtype, np.number):
        df.set_index(col0, inplace=True)
        df.index = pd.to_datetime(df.index, errors='coerce')
        df = df[df.index.notnull()]
        df = df.sort_index()
    close_col = [col for col in df.columns if 'close' in col.lower()]
    assert close_col, "No close column found!"
    prices = df[close_col[0]].values.reshape(-1, 1)
    
    print(f"Training data price range: {prices.min():.2f} - {prices.max():.2f} INR")
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)
    
    # Create sequences
    X, y = [], []
    for i in range(len(scaled_prices) - look_back):
        X.append(scaled_prices[i:i + look_back, 0])
        y.append(scaled_prices[i + look_back, 0])
    X_seq = np.array(X).reshape(-1, look_back, 1)            # LSTM input
    X_flat = np.array(X)                                     # XGB input
    y = np.array(y)
    return X_seq, X_flat, y, scaler, prices


def build_lstm(input_shape):
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(32))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def train_and_save_models():
    X_seq, X_flat, y, scaler, orig_prices = load_and_preprocess(DATA_PATH, LOOK_BACK)
    
    # Split for validation
    split_idx = int(0.8 * len(X_seq))
    X_seq_train, X_seq_val = X_seq[:split_idx], X_seq[split_idx:]
    X_flat_train, X_flat_val = X_flat[:split_idx], X_flat[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]
    
    # LSTM Model
    lstm_model = build_lstm((LOOK_BACK, 1))
    lstm_callbacks = [
        EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True),
        ModelCheckpoint(MODEL_PATH_LSTM, save_best_only=True)
    ]
    lstm_model.fit(
        X_seq_train, y_train,
        epochs=40,
        batch_size=32,
        validation_data=(X_seq_val, y_val),
        callbacks=lstm_callbacks,
        verbose=1,
        shuffle=False
    )
    
    # XGBoost Model
    xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.07, max_depth=5, random_state=42)
    xgb_model.fit(X_flat_train, y_train)
    
    # Save models and scaler
    with open(SCALER_PATH, 'wb') as f: 
        pickle.dump(scaler, f)
    with open(MODEL_PATH_XGB, 'wb') as f: 
        pickle.dump(xgb_model, f)
    
    # Evaluate both
    lstm_pred_scaled = lstm_model.predict(X_seq)
    xgb_pred_scaled = xgb_model.predict(X_flat).reshape(-1, 1)
    
    # Ensemble: better match with actuals
    ensemble_scaled = 0.6 * lstm_pred_scaled + 0.4 * xgb_pred_scaled
    predicted = scaler.inverse_transform(ensemble_scaled).flatten()
    actual = scaler.inverse_transform(y.reshape(-1, 1)).flatten()
    mse = mean_squared_error(actual, predicted)
    print(f"Ensemble Training RMSE: {np.sqrt(mse):.4f} INR")
    
    # Plot
    plt.figure(figsize=(14, 7))
    plt.plot(actual[-200:], label='Actual Price', alpha=0.7)
    plt.plot(predicted[-200:], label='Predicted Price', alpha=0.8)
    plt.title("ADA Hourly LSTM+XGBoost Ensemble Prediction")
    plt.xlabel("Hours")
    plt.ylabel("Price (INR)")
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return lstm_model, xgb_model, scaler


def predict_next(lstm_model, xgb_model, scaler, input_prices):
    """Prediction function with diagnostics and validation"""
    if len(input_prices) != LOOK_BACK:
        raise ValueError(f"Expected {LOOK_BACK} prices, got {len(input_prices)}")
    
    # Debug: Check scaler's training range
    print(f"\n--- Prediction Diagnostics ---")
    print(f"Input prices range: {min(input_prices):.2f} - {max(input_prices):.2f} INR")
    print(f"Scaler trained range: {scaler.data_min_[0]:.2f} - {scaler.data_max_[0]:.2f} INR")
    
    # Check if input is within reasonable range of training data
    input_min, input_max = min(input_prices), max(input_prices)
    scaler_min, scaler_max = scaler.data_min_[0], scaler.data_max_[0]
    
    if input_min < scaler_min * 0.5 or input_max > scaler_max * 2.0:
        print(f"WARNING: Input range significantly different from training range!")
        print(f"This may cause poor predictions. Consider retraining the model.")
    
    # Transform input using the saved scaler
    arr = np.array(input_prices).reshape(-1, 1)
    scaled = scaler.transform(arr)
    
    # Debug: Check scaled values
    print(f"Scaled input range: {scaled.min():.4f} - {scaled.max():.4f}")
    
    # Prepare inputs for both models
    lstm_in = scaled.reshape(1, LOOK_BACK, 1)
    xgb_in = scaled.flatten().reshape(1, -1)
    
    # Get predictions from both models (scaled)
    lstm_pred = lstm_model.predict(lstm_in, verbose=0)
    xgb_pred = xgb_model.predict(xgb_in).reshape(-1, 1)
    
    print(f"LSTM prediction (scaled): {lstm_pred[0][0]:.4f}")
    print(f"XGB prediction (scaled): {xgb_pred[0][0]:.4f}")
    
    # Ensemble prediction (still in scaled space)
    ensemble_scaled = 0.6 * lstm_pred + 0.4 * xgb_pred
    print(f"Ensemble prediction (scaled): {ensemble_scaled[0][0]:.4f}")
    
    # Transform back to original price scale
    final_pred = scaler.inverse_transform(ensemble_scaled)
    print(f"Final prediction (INR): {final_pred[0][0]:.2f}")
    print("--- End Diagnostics ---\n")
    
    return float(final_pred[0, 0])


def check_scaler_validity():
    """Check if existing scaler has reasonable range for ADA prices"""
    if not os.path.exists(SCALER_PATH):
        return False
    
    try:
        with open(SCALER_PATH, 'rb') as f:
            test_scaler = pickle.load(f)
        
        # ADA prices typically range from 20-500 INR, check if scaler is reasonable
        scaler_min, scaler_max = test_scaler.data_min_[0], test_scaler.data_max_[0]
        
        # If scaler range is way off from typical ADA range, force retrain
        if scaler_min > 1000 or scaler_max < 10 or scaler_max > 2000:
            print(f"Scaler range ({scaler_min:.2f} - {scaler_max:.2f}) seems incorrect for ADA prices")
            return False
        
        return True
    except:
        return False


if __name__ == "__main__":
    # Check if models exist and scaler is valid
    need_training = (not os.path.exists(MODEL_PATH_LSTM) or 
                    not os.path.exists(MODEL_PATH_XGB) or 
                    not check_scaler_validity())
    
    if need_training:
        print("Training/retraining ADA hourly LSTM+XGBoost models...")
        # Remove old files if they exist
        for file_path in [MODEL_PATH_LSTM, MODEL_PATH_XGB, SCALER_PATH]:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        lstm_model, xgb_model, scaler = train_and_save_models()
    else:
        print("Loading trained models and scaler...")
        lstm_model = load_model(MODEL_PATH_LSTM)
        with open(MODEL_PATH_XGB, 'rb') as f: 
            xgb_model = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f: 
            scaler = pickle.load(f)
    
    print(f"\nEnter the last {LOOK_BACK} ADA hourly closing prices (space-separated):")
    user_input = input()
    try:
        prices = list(map(float, user_input.strip().split()))
        if len(prices) != LOOK_BACK:
            raise ValueError(f"Must input exactly {LOOK_BACK} prices, got {len(prices)}.")
        
        pred = predict_next(lstm_model, xgb_model, scaler, prices)
        print(f"Next ADA hourly price prediction: ₹{pred:.2f}")
        
    except Exception as e:
        print("Error:", e)
