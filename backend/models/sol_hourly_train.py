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

# File paths (unique, SAFE)
DATA_PATH = '../crypto_data/hourly/SOL_hourly.csv'
MODEL_PATH = 'sol_hourly_ultrasafe_lstm.h5'
XGB_MODEL_PATH = 'sol_hourly_ultrasafe_xgb.pkl'
SCALER_PATH = 'sol_hourly_ultrasafe_scaler.pkl'

def load_and_preprocess_data(filepath, look_back=24):
    # Load data
    data = pd.read_csv(filepath)
    print(f"Loaded {len(data)} rows from {filepath}")
    
    # Check if first column is date/time and set as index
    if not pd.api.types.is_numeric_dtype(data.iloc[:, 0]):
        data.set_index(data.columns[0], inplace=True)
        try:
            data.index = pd.to_datetime(data.index)
            data = data.sort_index()  # Ensure chronological order
        except:
            pass
    
    # Find the close price column (case insensitive)
    price_col = None
    for col in data.columns:
        if 'close' in col.lower():
            price_col = col
            break
    
    if price_col is None:
        raise ValueError("No 'Close' column found.")
    
    # Extract and clean prices
    prices = data[price_col].values.astype(float)
    
    # Remove non-finite values and ensure positive
    valid_mask = np.isfinite(prices) & (prices > 0)
    prices = prices[valid_mask]
    
    if len(prices) <= look_back:
        raise ValueError(f"Not enough valid rows in data for look_back={look_back}. Found: {len(prices)}")
    
    # Convert to INR if needed (assuming USD prices are typically below 500)
    avg_price = np.mean(prices)
    if avg_price < 500:
        print(f"Converting from USD to INR (multiplying by 82)")
        prices = prices * 82
    else:
        print("Prices already in INR")
    
    prices = prices.reshape(-1, 1)
    
    # Scale the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)
    
    # Build X and y
    X, y = [], []
    for i in range(len(scaled_prices) - look_back):
        X.append(scaled_prices[i:i + look_back, 0])
        y.append(scaled_prices[i + look_back, 0])
    
    X = np.array(X)
    y = np.array(y)
    
    if X.shape[0] == 0 or y.shape[0] == 0:
        raise ValueError(f"No samples generated for training with {look_back}=look_back!")
    
    # Reshape for LSTM [samples, time steps, features]
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
    print(f"Training shapes: X: {X.shape}, y: {y.shape}")
    return X, y, scaler

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.3))
    model.add(LSTM(32, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(16))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def build_xgb_model():
    return XGBRegressor(n_estimators=30, learning_rate=0.1, max_depth=4, random_state=42)

def train_models():
    look_back = 24
    print("\n=== Training UltraSafe SOL Hourly Model ===")
    
    # Load and preprocess data
    X, y, scaler = load_and_preprocess_data(DATA_PATH, look_back)
    
    # Split data
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Train LSTM model
    lstm_model = build_lstm_model((X.shape[1], 1))
    callbacks_list = [
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ModelCheckpoint(MODEL_PATH, save_best_only=True)
    ]
    history = lstm_model.fit(
        X_train, y_train, 
        epochs=50, 
        batch_size=32,
        validation_data=(X_test, y_test), 
        callbacks=callbacks_list, 
        verbose=1
    )
    
    # Train XGBoost model
    X_train_flat = X_train.reshape(X_train.shape[0], -1)
    X_test_flat = X_test.reshape(X_test.shape[0], -1)
    
    xgb_model = build_xgb_model()
    xgb_model.fit(X_train_flat, y_train)
    
    # Save models
    with open(XGB_MODEL_PATH, 'wb') as f:
        pickle.dump(xgb_model, f)
    
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    
    # Evaluate ensemble model
    lstm_model = load_model(MODEL_PATH)  # Load best saved model
    lstm_pred = lstm_model.predict(X_test, verbose=0)
    xgb_pred = xgb_model.predict(X_test_flat).reshape(-1, 1)
    # Ensemble prediction (weighted average)
    ensemble_pred = 0.7 * lstm_pred + 0.3 * xgb_pred
    # Ensemble prediction (weighted average)
    ensemble_pred = 0.6 * lstm_pred + 0.4 * xgb_pred
    
    # Inverse transform to original scale
    actual_prices = scaler.inverse_transform(y_test.reshape(-1, 1))
    predicted_prices = scaler.inverse_transform(ensemble_pred)
    
    # Calculate error
    mse = mean_squared_error(actual_prices, predicted_prices)
    rmse = np.sqrt(mse)
    
    print(f'✅ Training Complete! RMSE: {rmse:.2f} INR')
    print(f"Sample last 3 actuals: {actual_prices[-3:].flatten()}")
    print(f"Sample last 3 preds:   {predicted_prices[-3:].flatten()}")
    
    # Plot results for visual inspection
    plt.figure(figsize=(12, 6))
    plt.plot(actual_prices[-100:], label='Actual Prices')
    plt.plot(predicted_prices[-100:], label='Predicted Prices')
    plt.title('SOL Price Prediction (Last 100 Hours)')
    plt.xlabel('Time')
    plt.ylabel('Price (INR)')
    plt.legend()
    plt.savefig('prediction_plot.png')
    plt.close()
    
    return lstm_model, xgb_model, scaler, look_back, rmse

def predict_live(lstm_model, xgb_model, scaler, look_back, recent_prices):
    print("\n=== Live Prediction ===")
    
    # Convert input to numpy array and validate
    prices = np.array(recent_prices).reshape(-1, 1)
    
    if len(prices) != look_back:
        raise ValueError(f"Need exactly {look_back} values for prediction! Got {len(prices)}")
    
    if np.any(prices <= 0):
        raise ValueError("All prices must be positive.")
    
    print(f"Input prices (INR): {prices.flatten()}")
    print(f"Average input price: {np.mean(prices):.2f} INR")
    
    # Scale the input using the same scaler
    scaled_input = scaler.transform(prices)
    
    # Prepare input for LSTM
    lstm_input = scaled_input.reshape(1, look_back, 1)
    
    # Make predictions
    lstm_pred = lstm_model.predict(lstm_input, verbose=0)
    
    # Prepare input for XGBoost
    xgb_input = scaled_input.flatten().reshape(1, -1)
    xgb_pred = xgb_model.predict(xgb_input).reshape(-1, 1)
    
    # Ensemble prediction
    ensemble_pred = 0.6 * lstm_pred + 0.4 * xgb_pred
    
    # Convert back to original scale
    final_price = scaler.inverse_transform(ensemble_pred)
    
    print(f"LSTM scaled prediction: {lstm_pred[0, 0]:.6f}")
    print(f"XGBoost scaled prediction: {xgb_pred[0, 0]:.6f}")
    print(f"Ensemble scaled prediction: {ensemble_pred[0, 0]:.6f}")
    print(f"Final INR prediction: {final_price[0, 0]:.2f}")
    
    return final_price[0, 0]

if __name__ == '__main__':
    # Remove old models to force fresh training
    for fpath in [MODEL_PATH, XGB_MODEL_PATH, SCALER_PATH]:
        if os.path.exists(fpath):
            os.remove(fpath)
    
    print("Forcing fresh training for SOL hourly model...")
    
    try:
        # Train models
        lstm_model, xgb_model, scaler, look_back, rmse = train_models()
        
        print(f"\nModel trained with RMSE: {rmse:.2f} INR")
        print(f"Enter the last {look_back} SOL hourly closing prices in INR:")
        print("Example: 14980 15060 15010 15100 15140 14960 15070 15130 15200 15170 15100 15120 15080 14960 15120 15140 15010 15070 15130 15190 14990 15020 15090 15180")
        
        # Get user input
        prices_input = input().strip()
        
        if not prices_input:
            # Use example data if no input provided
            prices_input = "14980 15060 15010 15100 15140 14960 15070 15130 15200 15170 15100 15120 15080 14960 15120 15140 15010 15070 15130 15190 14990 15020 15090 15180"
            print(f"Using example data: {prices_input}")
        
        # Process input and make prediction
        recent_prices = list(map(float, prices_input.split()))
        pred = predict_live(lstm_model, xgb_model, scaler, look_back, recent_prices)
        print(f"\n✅ Predicted next SOL hourly price (INR): {pred:.2f}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your data file and try again.")