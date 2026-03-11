import os
import numpy as np
import pandas as pd
from keras.models import load_model
import pickle
import logging

logger = logging.getLogger(__name__)

MODEL_FOLDER = 'models'
LOOKBACKS = {'hourly': 24, 'daily': 60}
FEATURE_LENGTH_XGB = {'hourly': 24, 'daily': 30}

MODEL_FILES = {
    'ada': {
        'daily': {'lstm': 'ada_daily_lstm.h5', 'scaler': 'ada_daily_scaler.pkl', 'xgb': 'ada_daily_xgb.pkl'},
        'hourly': {'lstm': 'ada_hourly_lstm_xgb.h5', 'scaler': 'ada_hourly_scaler.pkl', 'xgb': 'ada_hourly_xgb.pkl'}
    },
    'bnb': {
        'daily': {'lstm': 'bnb_daily_lstm.h5', 'scaler': 'bnb_daily_scaler.pkl'},
        'hourly': {'lstm': 'bnb_hourly_lstm_xgb.h5', 'scaler': 'bnb_hourly_scaler.pkl', 'xgb': 'bnb_hourly_xgb.pkl'}
    },
    'btc': {
        'daily': {'lstm': 'btc_daily_lstm.h5', 'scaler': 'btc_daily_scaler.pkl'},
        'hourly': {'lstm': 'btc_hourly_lstm.h5', 'scaler': 'btc_hourly_scaler.pkl'}
    },
    'eth': {
        'daily': {'lstm': 'eth_daily_lstm.h5', 'scaler': 'eth_daily_scaler.pkl', 'xgb': 'eth_daily_xgb.pkl'},
        'hourly': {'lstm': 'eth_hourly_lstm_simple.h5', 'scaler': 'eth_hourly_scaler_simple.pkl', 'xgb': 'eth_hourly_xgb_simple.pkl'}
    },
    'ltc': {
        'daily': {'lstm': 'ltc_daily_lstm.h5', 'scaler': 'ltc_daily_scaler.pkl', 'xgb': 'ltc_daily_xgb.pkl'},
        'hourly': {'lstm': 'ltc_hourly_lstm.h5', 'scaler': 'ltc_hourly_scaler.pkl', 'xgb': 'ltc_hourly_xgb.pkl'}
    },
    'sol': {
        'daily': {'lstm': 'sol_daily_lstm.h5', 'scaler': 'sol_daily_scaler.pkl', 'xgb': 'sol_daily_xgb.pkl'},
        'hourly': {'lstm': 'sol_hourly_lstm_ultrasafe.h5', 'scaler': 'sol_hourly_scaler_ultrasafe.pkl', 'xgb': 'sol_hourly_xgb_ultrasafe.pkl'}
    },
    'xrp': {
        'daily': {'lstm': 'xrp_daily_lstm.h5', 'scaler': 'xrp_daily_scaler.pkl', 'xgb': 'xrp_daily_xgb.pkl'},
        'hourly': {'lstm': 'xrp_hourly_lstm.h5', 'scaler': 'xrp_hourly_scaler.pkl', 'xgb': 'xrp_hourly_xgb.pkl'}
    }
}

def load_any_model(path):
    if not path or not os.path.exists(path):
        return None
    if path.endswith('.h5'):
        return load_model(path)
    else:
        with open(path, 'rb') as f:
            return pickle.load(f)

def generate_demo_prices(lookback, base=30000, vol=0.02):
    prices = [float(base)]
    for _ in range(lookback - 1):
        change = np.random.uniform(-vol, vol)
        prices.append(prices[-1] * (1 + change))
    return prices

def preload_models():
    models = {}
    for coin, freqs in MODEL_FILES.items():
        models[coin] = {}
        for freq, files in freqs.items():
            try:
                lstm = load_any_model(os.path.join(MODEL_FOLDER, files.get('lstm')))
                scaler = load_any_model(os.path.join(MODEL_FOLDER, files.get('scaler')))
                xgb = load_any_model(os.path.join(MODEL_FOLDER, files.get('xgb')))
                models[coin][freq] = {'lstm': lstm, 'scaler': scaler, 'xgb': xgb}
                logger.info(f"Loaded models for {coin} {freq}")
            except Exception as e:
                logger.error(f"Failed loading models for {coin} {freq}: {e}")
    return models
