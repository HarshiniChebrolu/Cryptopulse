#!/usr/bin/env python3
"""
CryptoPulse Database Setup Script

This script initializes the SQLite database for CryptoPulse Analytics with all required tables,
indexes, and sample data for testing.

Run this script before starting the Flask application for the first time.
"""

import sqlite3
import json
from datetime import datetime, timedelta
import os

DATABASE = 'cryptopulse.db'

def create_database():
    """Create and initialize the CryptoPulse database"""
    print("🗄️  Initializing CryptoPulse Database...")
    
    # Remove existing database if it exists
    if os.path.exists(DATABASE):
        print(f"📋 Removing existing database: {DATABASE}")
        os.remove(DATABASE)
    
    # Create new database connection
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # Create Users table
        print("👥 Creating Users table...")
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                user_preferences TEXT, -- JSON string for user settings
                total_predictions INTEGER DEFAULT 0,
                accurate_predictions INTEGER DEFAULT 0
            )
        ''')
        
        # Create Prediction History table
        print("📊 Creating Prediction History table...")
        cursor.execute('''
            CREATE TABLE prediction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_email TEXT,
                coin TEXT NOT NULL,
                current_price REAL NOT NULL,
                predicted_price REAL NOT NULL,
                prediction_change REAL,
                prediction_change_percent REAL,
                timeframe TEXT NOT NULL, -- '24h', '7d', '30d'
                confidence_score REAL,
                model_used TEXT,
                prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                actual_price REAL, -- Filled later for accuracy tracking
                accuracy_score REAL, -- Calculated after actual outcome
                market_data TEXT, -- JSON string of additional market data
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create User Sessions table
        print("🔐 Creating User Sessions table...")
        cursor.execute('''
            CREATE TABLE user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                user_id INTEGER,
                user_email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create Price Alerts table
        print("🔔 Creating Price Alerts table...")
        cursor.execute('''
            CREATE TABLE price_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_email TEXT,
                coin TEXT NOT NULL,
                alert_type TEXT NOT NULL, -- 'above', 'below', 'change'
                target_price REAL,
                target_percentage REAL,
                current_price REAL,
                is_active BOOLEAN DEFAULT 1,
                triggered BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                triggered_at TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create Market Data Cache table
        print("💾 Creating Market Data Cache table...")
        cursor.execute('''
            CREATE TABLE market_data_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coin TEXT NOT NULL,
                price REAL,
                change_24h REAL,
                volume_24h REAL,
                market_cap REAL,
                high_24h REAL,
                low_24h REAL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_source TEXT DEFAULT 'api',
                raw_data TEXT -- JSON string of full API response
            )
        ''')
        
        # Create System Logs table
        print("📋 Creating System Logs table...")
        cursor.execute('''
            CREATE TABLE system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_level TEXT NOT NULL, -- 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
                message TEXT NOT NULL,
                user_email TEXT,
                ip_address TEXT,
                endpoint TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                additional_data TEXT -- JSON string
            )
        ''')
        
        # Create Database Indexes for Performance
        print("🔍 Creating database indexes...")
        
        # Prediction History indexes
        cursor.execute('CREATE INDEX idx_prediction_user_email ON prediction_history(user_email)')
        cursor.execute('CREATE INDEX idx_prediction_coin ON prediction_history(coin)')
        cursor.execute('CREATE INDEX idx_prediction_timestamp ON prediction_history(prediction_timestamp)')
        cursor.execute('CREATE INDEX idx_prediction_user_coin ON prediction_history(user_email, coin)')
        cursor.execute('CREATE INDEX idx_prediction_timeframe ON prediction_history(timeframe)')
        
        # User Sessions indexes
        cursor.execute('CREATE INDEX idx_session_id ON user_sessions(session_id)')
        cursor.execute('CREATE INDEX idx_session_user_email ON user_sessions(user_email)')
        cursor.execute('CREATE INDEX idx_session_expires ON user_sessions(expires_at)')
        cursor.execute('CREATE INDEX idx_session_active ON user_sessions(is_active)')
        
        # Price Alerts indexes
        cursor.execute('CREATE INDEX idx_alerts_user_email ON price_alerts(user_email)')
        cursor.execute('CREATE INDEX idx_alerts_coin ON price_alerts(coin)')
        cursor.execute('CREATE INDEX idx_alerts_active ON price_alerts(is_active)')
        cursor.execute('CREATE INDEX idx_alerts_triggered ON price_alerts(triggered)')
        
        # Market Data Cache indexes
        cursor.execute('CREATE INDEX idx_market_coin ON market_data_cache(coin)')
        cursor.execute('CREATE INDEX idx_market_updated ON market_data_cache(last_updated)')
        
        # System Logs indexes
        cursor.execute('CREATE INDEX idx_logs_timestamp ON system_logs(timestamp)')
        cursor.execute('CREATE INDEX idx_logs_level ON system_logs(log_level)')
        cursor.execute('CREATE INDEX idx_logs_user ON system_logs(user_email)')
        
        # Insert Sample Data
        print("📋 Inserting sample data...")
        insert_sample_data(cursor)
        
        # Commit all changes
        conn.commit()
        print("✅ Database created successfully!")
        
        # Display database statistics
        show_database_stats(cursor)
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        conn.rollback()
        
    finally:
        conn.close()

def insert_sample_data(cursor):
    """Insert sample data for testing"""
    
    # Sample users
    sample_users = [
        ('demo@cryptopulse.com', datetime.now(), '{"theme": "dark", "notifications": true}'),
        ('alice@example.com', datetime.now() - timedelta(days=5), '{"theme": "light", "notifications": false}'),
        ('bob@example.com', datetime.now() - timedelta(days=10), '{"theme": "dark", "notifications": true}'),
    ]
    
    for email, created, prefs in sample_users:
        cursor.execute('''
            INSERT INTO users (email, created_at, last_login, user_preferences, total_predictions)
            VALUES (?, ?, ?, ?, ?)
        ''', [email, created, created, prefs, 0])
    
    # Sample prediction history
    user_id = 1  # demo user
    sample_predictions = [
        ('BTC', 51234.56, 52850.00, '24h', 0.87, 'LSTM+XGBoost'),
        ('ETH', 3234.78, 3450.00, '24h', 0.82, 'LSTM+XGBoost'),
        ('BNB', 310.45, 295.00, '7d', 0.73, 'LSTM+XGBoost'),
        ('ADA', 0.85, 0.92, '24h', 0.79, 'LSTM+XGBoost'),
        ('SOL', 95.67, 102.30, '7d', 0.85, 'LSTM+XGBoost'),
        ('XRP', 0.62, 0.58, '24h', 0.71, 'LSTM+XGBoost'),
        ('LTC', 78.90, 82.15, '24h', 0.88, 'LSTM+XGBoost'),
    ]
    
    for coin, current, predicted, timeframe, confidence, model in sample_predictions:
        change = predicted - current
        change_percent = (change / current) * 100
        timestamp = datetime.now() - timedelta(hours=len(sample_predictions) - sample_predictions.index((coin, current, predicted, timeframe, confidence, model)))
        
        market_data = {
            'volume_24h': current * 1000000 * (0.5 + 0.5 * hash(coin) % 10 / 10),
            'market_cap': current * 19000000,  # Approximate BTC supply
            'volatility': 0.02 + 0.06 * (hash(coin) % 100 / 100)
        }
        
        cursor.execute('''
            INSERT INTO prediction_history 
            (user_id, user_email, coin, current_price, predicted_price, 
             prediction_change, prediction_change_percent, timeframe, 
             confidence_score, model_used, prediction_timestamp, market_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [
            user_id, 'demo@cryptopulse.com', coin, current, predicted,
            change, change_percent, timeframe, confidence, model, timestamp,
            json.dumps(market_data)
        ])
    
    # Sample market data cache
    sample_market_data = [
        ('BTC', 51234.56, 2.45, 28.5e9, 985.4e9, 53890.12, 49123.45),
        ('ETH', 3234.78, 1.87, 15.2e9, 389.2e9, 3456.89, 3098.45),
        ('BNB', 310.45, -0.52, 1.2e9, 47.8e9, 325.67, 298.23),
        ('ADA', 0.85, 3.21, 0.89e9, 28.9e9, 0.89, 0.81),
        ('SOL', 95.67, 5.67, 2.1e9, 42.3e9, 102.34, 89.12),
        ('XRP', 0.62, -1.23, 1.8e9, 34.7e9, 0.65, 0.59),
        ('LTC', 78.90, 2.89, 0.56e9, 5.8e9, 82.15, 75.43),
    ]
    
    for coin, price, change, volume, market_cap, high, low in sample_market_data:
        cursor.execute('''
            INSERT INTO market_data_cache 
            (coin, price, change_24h, volume_24h, market_cap, high_24h, low_24h, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', [coin, price, change, volume, market_cap, high, low, datetime.now()])
    
    # Sample price alerts
    sample_alerts = [
        (1, 'demo@cryptopulse.com', 'BTC', 'above', 55000, None, 51234.56, 1, 0),
        (1, 'demo@cryptopulse.com', 'ETH', 'below', 3000, None, 3234.78, 1, 0),
        (1, 'demo@cryptopulse.com', 'ADA', 'change', None, 10.0, 0.85, 1, 0),
    ]
    
    for user_id, email, coin, alert_type, target_price, target_percentage, current_price, is_active, triggered in sample_alerts:
        cursor.execute('''
            INSERT INTO price_alerts 
            (user_id, user_email, coin, alert_type, target_price, target_percentage, 
             current_price, is_active, triggered, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [user_id, email, coin, alert_type, target_price, target_percentage, 
              current_price, is_active, triggered, datetime.now()])
    
    # Sample system logs
    sample_logs = [
        ('INFO', 'Database initialized successfully', None, None, 'system'),
        ('INFO', 'User demo@cryptopulse.com logged in', 'demo@cryptopulse.com', '127.0.0.1', '/api/login'),
        ('INFO', 'Prediction generated for BTC', 'demo@cryptopulse.com', '127.0.0.1', '/api/predict'),
        ('WARNING', 'High API request rate detected', None, '127.0.0.1', '/api/predict'),
    ]
    
    for level, message, user_email, ip, endpoint in sample_logs:
        cursor.execute('''
            INSERT INTO system_logs (log_level, message, user_email, ip_address, endpoint, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', [level, message, user_email, ip, endpoint, datetime.now()])

def show_database_stats(cursor):
    """Display database statistics"""
    print("\n📊 Database Statistics:")
    print("=" * 50)
    
    # Table counts
    tables = ['users', 'prediction_history', 'user_sessions', 'price_alerts', 'market_data_cache', 'system_logs']
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f"📋 {table.replace('_', ' ').title()}: {count} records")
    
    # Database size
    cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
    size = cursor.fetchone()[0]
    print(f"💾 Database Size: {size / 1024:.1f} KB")
    
    print("=" * 50)
    print("✅ Database setup complete!")
    print(f"📂 Database file: {os.path.abspath(DATABASE)}")
    print("\n🚀 Ready to start CryptoPulse Analytics!")
    print("   Run: python app_complete_database.py")

def main():
    """Main function to setup database"""
    print("🔧 CryptoPulse Database Setup")
    print("=" * 40)
    
    create_database()
    
    print("\n🎯 Next Steps:")
    print("1. Run: python app_complete_database.py")
    print("2. Open: http://localhost:5000/login")
    print("3. Login: demo@cryptopulse.com / demo123")
    print("4. Enjoy your crypto analytics platform!")

if __name__ == '__main__':
    main()