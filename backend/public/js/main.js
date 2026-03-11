// Enhanced CryptoPulse Main JavaScript with Professional Features
const USD_TO_INR = 83;
let coinData = {};
let selectedCoins = ['BTC', 'ETH', 'ADA', 'SOL'];
let currentTimeframe = '24h';
let chartInstance = null;
let refreshInterval = null;
let currentSelectedCoin = 'BTC';

// Enhanced coin configurations with professional logos and fallbacks
const COIN_CONFIG = {
    BTC: { 
        name: 'Bitcoin', 
        color: '#F7931A', 
        logo: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png',
        fallbackLogo: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjQiIGN5PSIyNCIgcj0iMjQiIGZpbGw9IiNGNzkzMUEiLz4KPHRleHQgeD0iMjQiIHk9IjMwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSJ3aGl0ZSIgZm9udC1zaXplPSIxNiIgZm9udC13ZWlnaHQ9ImJvbGQiPkI8L3RleHQ+Cjwvc3ZnPg=='
    },
    ETH: { 
        name: 'Ethereum', 
        color: '#627EEA', 
        logo: 'https://cryptologos.cc/logos/ethereum-eth-logo.png',
        fallbackLogo: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjQiIGN5PSIyNCIgcj0iMjQiIGZpbGw9IiM2MjdFRUEiLz4KPHRleHQgeD0iMjQiIHk9IjMwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSJ3aGl0ZSIgZm9udC1zaXplPSIxNiIgZm9udC13ZWlnaHQ9ImJvbGQiPkU8L3RleHQ+Cjwvc3ZnPg=='
    },
    LTC: { 
        name: 'Litecoin', 
        color: '#BFBBBB', 
        logo: 'https://cryptologos.cc/logos/litecoin-ltc-logo.png',
        fallbackLogo: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjQiIGN5PSIyNCIgcj0iMjQiIGZpbGw9IiNCRkJCQkIiLz4KPHRleHQgeD0iMjQiIHk9IjMwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSJibGFjayIgZm9udC1zaXplPSIxNiIgZm9udC13ZWlnaHQ9ImJvbGQiPkw8L3RleHQ+Cjwvc3ZnPg=='
    },
    ADA: { 
        name: 'Cardano', 
        color: '#3CC8C8', 
        logo: 'https://cryptologos.cc/logos/cardano-ada-logo.png',
        fallbackLogo: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjQiIGN5PSIyNCIgcj0iMjQiIGZpbGw9IiMzQ0M4QzgiLz4KPHRleHQgeD0iMjQiIHk9IjMwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSJ3aGl0ZSIgZm9udC1zaXplPSIxNiIgZm9udC13ZWlnaHQ9ImJvbGQiPkE8L3RleHQ+Cjwvc3ZnPg=='
    },
    BNB: { 
        name: 'BNB', 
        color: '#F3BA2F', 
        logo: 'https://cryptologos.cc/logos/bnb-bnb-logo.png',
        fallbackLogo: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjQiIGN5PSIyNCIgcj0iMjQiIGZpbGw9IiNGM0JBMkYiLz4KPHRleHQgeD0iMjQiIHk9IjMwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSJibGFjayIgZm9udC1zaXplPSIxNCIgZm9udC13ZWlnaHQ9ImJvbGQiPkJOQjwvdGV4dD4KPC9zdmc+'
    },
    XRP: { 
        name: 'XRP', 
        color: '#25A768', 
        logo: 'https://cryptologos.cc/logos/xrp-xrp-logo.png',
        fallbackLogo: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjQiIGN5PSIyNCIgcj0iMjQiIGZpbGw9IiMyNUE3NjgiLz4KPHRleHQgeD0iMjQiIHk9IjMwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSJ3aGl0ZSIgZm9udC1zaXplPSIxNCIgZm9udC13ZWlnaHQ9ImJvbGQiPlhSUDwvdGV4dD4KPC9zdmc+'
    },
    SOL: { 
        name: 'Solana', 
        color: '#C08AFF', 
        logo: 'https://cryptologos.cc/logos/solana-sol-logo.png',
        fallbackLogo: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjQiIGN5PSIyNCIgcj0iMjQiIGZpbGw9IiNDMDhBRkYiLz4KPHRleHQgeD0iMjQiIHk9IjMwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSJibGFjayIgZm9udC1zaXplPSIxNCIgZm9udC13ZWlnaHQ9ImJvbGQiPlNPTDwvdGV4dD4KPC9zdmc+'
    }
};

// Timeframe configurations with prediction models
const TIMEFRAME_CONFIG = {
    '24h': { label: '24 Hours', days: 1, predictionType: 'short-term', model: 'hourly' },
    '7d': { label: '7 Days', days: 7, predictionType: 'medium-term', model: 'daily' },
    '15d': { label: '15 Days', days: 15, predictionType: 'medium-term', model: 'daily' },
    '30d': { label: '30 Days', days: 30, predictionType: 'long-term', model: 'daily' }
};

// Enhanced API functions
async function fetchCoinPrediction(coin, timeframe) {
    try {
        const timeframeConfig = TIMEFRAME_CONFIG[timeframe];
        const freq = timeframeConfig ? timeframeConfig.model : 'daily';

        showLoadingToast('Generating AI prediction...');

        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                coin: coin.toLowerCase(), 
                freq: freq, 
                timeframe: timeframe 
            })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        hideLoadingToast();
        showSuccessToast('Prediction generated successfully!');

        return data;
    } catch (error) {
        console.error(`Error fetching prediction for ${coin}:`, error);
        hideLoadingToast();
        showErrorToast(`Failed to get prediction: ${error.message}`);
        return null;
    }
}

async function fetchAllPrices() {
    try {
        const response = await fetch('/api/prices/all');
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching all prices:', error);
        return null;
    }
}

// Enhanced UI functions
function createCompactCoinCard(coin, data) {
    const isPositive = data.percentChange >= 0;
    const priceINR = Math.round(data.currentPrice * USD_TO_INR);

    return `
        <div class="compact-coin-card p-4 rounded-xl hover:scale-105 transition-all cursor-pointer" 
             onclick="selectCoin('${coin}')" 
             data-coin="${coin}">
            <div class="flex items-center justify-between mb-3">
                <div class="flex items-center space-x-2">
                    <img src="${data.logo}" 
                         alt="${data.name}" 
                         class="crypto-logo"
                         onerror="this.src='${data.fallbackLogo}'"
                         loading="lazy">
                    <div>
                        <div class="font-semibold text-sm">${coin}</div>
                        <div class="text-xs text-gray-400">${data.name}</div>
                    </div>
                </div>
                ${data.apiSource ? '<div class="w-2 h-2 bg-green-400 rounded-full"></div>' : ''}
            </div>

            <div class="space-y-1">
                <div class="price-display">₹${priceINR.toLocaleString()}</div>
                <div class="text-sm text-gray-400">$${data.currentPrice.toFixed(2)}</div>
                <div class="flex items-center justify-between">
                    <span class="text-xs ${isPositive ? 'change-positive' : 'change-negative'} font-medium">
                        ${isPositive ? '+' : ''}${data.percentChange.toFixed(2)}%
                    </span>
                    <span class="text-xs text-gray-500">${data.volatility || 'Low'}</span>
                </div>
            </div>
        </div>
    `;
}

function createAIPredictionCard(coin, data) {
    if (!data.predictions) return '';

    const prediction = data.predictions.shortTerm;
    if (!prediction) return '';

    const isPositive = prediction.price > data.currentPrice;
    const changePercent = ((prediction.price - data.currentPrice) / data.currentPrice * 100).toFixed(2);

    return `
        <div class="prediction-card p-4 rounded-lg">
            <div class="flex items-center justify-between mb-3">
                <div class="flex items-center space-x-2">
                    <img src="${data.logo}" 
                         alt="${data.name}" 
                         class="w-6 h-6 rounded-full"
                         onerror="this.src='${data.fallbackLogo}'">
                    <span class="font-semibold text-sm">${coin}</span>
                </div>
                <span class="text-xs px-2 py-1 bg-purple-600 rounded-full">${currentTimeframe}</span>
            </div>

            <div class="space-y-2">
                <div class="flex justify-between items-center">
                    <span class="text-xs text-gray-400">Predicted Price</span>
                    <span class="font-semibold">₹${Math.round(prediction.price * USD_TO_INR).toLocaleString()}</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-xs text-gray-400">Expected Change</span>
                    <span class="text-sm font-medium ${isPositive ? 'text-green-400' : 'text-red-400'}">
                        ${isPositive ? '+' : ''}${changePercent}%
                    </span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-xs text-gray-400">Confidence</span>
                    <span class="text-sm font-semibold text-blue-400">${(prediction.confidence * 100).toFixed(0)}%</span>
                </div>
                <div class="w-full bg-gray-700 rounded-full h-2 mt-2">
                    <div class="bg-blue-400 h-2 rounded-full transition-all" 
                         style="width: ${prediction.confidence * 100}%"></div>
                </div>
            </div>
        </div>
    `;
}

// Main data loading function
async function loadAllCoinsData() {
    try {
        showLoadingOverlay(true);
        console.log('🚀 Loading CryptoPulse with enhanced features...');

        // Load real-time price data
        const pricesResponse = await fetchAllPrices();
        if (pricesResponse && pricesResponse.success) {
            const coins = Object.keys(pricesResponse.prices);

            for (const coin of coins) {
                const priceData = pricesResponse.prices[coin];

                // Generate prediction
                const predictionData = await fetchCoinPrediction(coin, currentTimeframe);

                // Process and store data
                coinData[coin] = {
                    ...COIN_CONFIG[coin],
                    currentPrice: priceData.price_usd || 0,
                    percentChange: priceData.change_24h || 0,
                    volume: formatNumber(priceData.volume_24h) || 'N/A',
                    marketCap: formatNumber(priceData.market_cap) || 'N/A',
                    volatility: calculateVolatility(priceData.change_24h || 0),
                    predictions: predictionData ? {
                        shortTerm: {
                            price: predictionData.predicted_price || priceData.price_usd,
                            confidence: predictionData.confidence || 0.75,
                            signal: predictionData.percent_change > 2 ? 'bullish' : 
                                   predictionData.percent_change < -2 ? 'bearish' : 'neutral'
                        }
                    } : null,
                    lastUpdated: new Date().toISOString(),
                    apiSource: true
                };
            }
        } else {
            // Fallback to demo data
            console.warn('Using fallback data');
            generateFallbackData();
        }

        // Update all UI components
        updateAllUI();
        setupInteractivity();

        showLoadingOverlay(false);
        showSuccessToast('Data loaded successfully!');

    } catch (error) {
        console.error('Failed to load data:', error);
        showErrorToast('Failed to load data: ' + error.message);
        generateFallbackData();
        updateAllUI();
        showLoadingOverlay(false);
    }
}

function generateFallbackData() {
    const coins = ['BTC', 'ETH', 'ADA', 'SOL', 'BNB', 'XRP', 'LTC'];
    const basePrices = { BTC: 65000, ETH: 3500, BNB: 600, ADA: 0.65, SOL: 180, XRP: 0.60, LTC: 110 };

    coins.forEach(coin => {
        const price = (basePrices[coin] || 100) * (0.85 + Math.random() * 0.3);
        const change = (Math.random() - 0.5) * 8;

        coinData[coin] = {
            ...COIN_CONFIG[coin],
            currentPrice: price,
            percentChange: change,
            volume: formatNumber(price * 1000000 * Math.random()),
            marketCap: formatNumber(price * 19000000),
            volatility: calculateVolatility(change),
            predictions: {
                shortTerm: {
                    price: price * (1 + change / 100 * 1.2),
                    confidence: 0.7 + Math.random() * 0.2,
                    signal: change > 2 ? 'bullish' : change < -2 ? 'bearish' : 'neutral'
                }
            },
            lastUpdated: new Date().toISOString(),
            apiSource: false
        };
    });
}

// UI update functions
function updateAllUI() {
    console.log('🎨 Updating all UI components...');

    // Update compact coin cards
    updateCompactCoinCards();

    // Update AI predictions section
    updateAIPredictions();

    // Update market overview table
    updateMarketOverviewTable();

    // Update chart if available
    if (typeof updateChart === 'function') {
        updateChart();
    }

    // Update timestamps
    updateTimestamps();
}

function updateCompactCoinCards() {
    const container = document.getElementById('priceCards');
    if (!container) return;

    const coins = Object.keys(coinData).sort();
    container.innerHTML = coins.map(coin => createCompactCoinCard(coin, coinData[coin])).join('');
}

function updateAIPredictions() {
    const container = document.getElementById('aiPredictions');
    if (!container) return;

    const coins = Object.keys(coinData).slice(0, 4); // Show top 4
    container.innerHTML = coins.map(coin => createAIPredictionCard(coin, coinData[coin])).join('');
}

function updateMarketOverviewTable() {
    const tbody = document.getElementById('marketOverviewTable');
    if (!tbody) return;

    const coins = Object.keys(coinData);
    tbody.innerHTML = coins.map(coin => {
        const data = coinData[coin];
        const isPositive = data.percentChange >= 0;

        return `
            <tr class="hover:bg-gray-800/50 transition-colors">
                <td class="p-4">
                    <div class="flex items-center space-x-3">
                        <img src="${data.logo}" alt="${data.name}" class="w-8 h-8 rounded-full"
                             onerror="this.src='${data.fallbackLogo}'">
                        <div>
                            <div class="font-semibold">${coin}</div>
                            <div class="text-sm text-gray-400">${data.name}</div>
                        </div>
                    </div>
                </td>
                <td class="p-4 font-semibold">$${data.currentPrice.toFixed(2)}</td>
                <td class="p-4">
                    <span class="${isPositive ? 'text-green-400' : 'text-red-400'} font-medium">
                        ${isPositive ? '+' : ''}${data.percentChange.toFixed(2)}%
                    </span>
                </td>
                <td class="p-4">${data.marketCap}</td>
                <td class="p-4">${data.volume}</td>
                <td class="p-4">
                    <span class="px-2 py-1 text-xs rounded-full ${getVolatilityColor(data.volatility)}">
                        ${data.volatility}
                    </span>
                </td>
                <td class="p-4">
                    <button class="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm transition-colors"
                            onclick="selectCoin('${coin}')">
                        Analyze
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Utility functions
function formatNumber(num) {
    if (!num) return '0';
    const value = parseFloat(num);
    if (value >= 1e12) return `$${(value / 1e12).toFixed(1)}T`;
    if (value >= 1e9) return `$${(value / 1e9).toFixed(1)}B`;
    if (value >= 1e6) return `$${(value / 1e6).toFixed(1)}M`;
    return `$${value.toFixed(0)}`;
}

function calculateVolatility(change) {
    const abs = Math.abs(change);
    if (abs < 2) return 'Low';
    if (abs < 5) return 'Medium';
    if (abs < 8) return 'High';
    return 'Very High';
}

function getVolatilityColor(volatility) {
    switch (volatility) {
        case 'Low': return 'bg-green-600 text-white';
        case 'Medium': return 'bg-yellow-600 text-white';
        case 'High': return 'bg-orange-600 text-white';
        case 'Very High': return 'bg-red-600 text-white';
        default: return 'bg-gray-600 text-white';
    }
}

function selectCoin(coin) {
    currentSelectedCoin = coin;

    // Update active states in coin pills
    document.querySelectorAll('.coin-pill').forEach(pill => {
        pill.classList.remove('active');
        if (pill.dataset.coin === coin) {
            pill.classList.add('active');
        }
    });

    // Update deep analysis if on that page
    if (window.location.pathname.includes('dashboard') || window.location.pathname.includes('deep-analysis')) {
        updateDeepAnalysisForCoin(coin);
    }

    console.log(`Selected coin: ${coin}`);
}

function updateDeepAnalysisForCoin(coin) {
    const data = coinData[coin];
    if (!data) return;

    // Update live price display
    const livePriceElement = document.getElementById('livePrice');
    if (livePriceElement) {
        livePriceElement.textContent = `₹${Math.round(data.currentPrice * USD_TO_INR).toLocaleString()}`;
    }

    const livePriceUSDElement = document.getElementById('livePriceUSD');
    if (livePriceUSDElement) {
        livePriceUSDElement.textContent = `$${data.currentPrice.toFixed(2)}`;
    }

    const priceChangeElement = document.getElementById('priceChange');
    if (priceChangeElement) {
        const isPositive = data.percentChange >= 0;
        priceChangeElement.className = `px-3 py-1 rounded-full text-sm font-medium inline-flex items-center ${
            isPositive ? 'price-change-positive' : 'price-change-negative'
        }`;
        priceChangeElement.innerHTML = `
            <i data-lucide="${isPositive ? 'trending-up' : 'trending-down'}" class="w-4 h-4 mr-1"></i>
            ${isPositive ? '+' : ''}${data.percentChange.toFixed(2)}%
        `;

        // Reinitialize Lucide icons
        if (typeof lucide !== 'undefined' && lucide.createIcons) {
            lucide.createIcons();
        }
    }

    // Update other statistics
    updateStatistics(data);
}

function updateStatistics(data) {
    const elements = {
        'dayHigh': `₹${Math.round(data.currentPrice * 1.05 * USD_TO_INR).toLocaleString()}`,
        'dayLow': `₹${Math.round(data.currentPrice * 0.95 * USD_TO_INR).toLocaleString()}`,
        'marketCap': data.marketCap,
        'volume': data.volume
    };

    Object.entries(elements).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) element.textContent = value;
    });
}

function updateTimestamps() {
    const now = new Date();
    const timestamp = now.toLocaleString();

    ['lastUpdated', 'chartLastUpdated'].forEach(id => {
        const element = document.getElementById(id);
        if (element) element.textContent = timestamp;
    });
}

// Toast notification functions
function showSuccessToast(message) {
    const toast = document.getElementById('successToast');
    if (toast) {
        toast.querySelector('span').textContent = message;
        toast.classList.remove('translate-x-full');
        setTimeout(() => toast.classList.add('translate-x-full'), 3000);
    }
}

function showErrorToast(message) {
    console.error(message);
    // Create error toast if it doesn't exist
    const toast = document.createElement('div');
    toast.className = 'fixed top-4 right-4 bg-red-600 text-white p-4 rounded-lg shadow-lg z-50';
    toast.innerHTML = `
        <div class="flex items-center space-x-2">
            <i data-lucide="alert-circle" class="w-5 h-5"></i>
            <span>${message}</span>
        </div>
    `;
    document.body.appendChild(toast);

    if (typeof lucide !== 'undefined' && lucide.createIcons) {
        lucide.createIcons();
    }

    setTimeout(() => {
        document.body.removeChild(toast);
    }, 5000);
}

function showLoadingToast(message) {
    const toast = document.createElement('div');
    toast.id = 'loadingToast';
    toast.className = 'fixed top-4 right-4 bg-blue-600 text-white p-4 rounded-lg shadow-lg z-50';
    toast.innerHTML = `
        <div class="flex items-center space-x-2">
            <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <span>${message}</span>
        </div>
    `;
    document.body.appendChild(toast);
}

function hideLoadingToast() {
    const toast = document.getElementById('loadingToast');
    if (toast) {
        document.body.removeChild(toast);
    }
}

function showLoadingOverlay(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        if (show) {
            overlay.classList.remove('hidden');
        } else {
            overlay.classList.add('hidden');
        }
    }
}

// Setup interactivity
function setupInteractivity() {
    // Auto-refresh every 30 seconds
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }

    refreshInterval = setInterval(() => {
        loadAllCoinsData();
    }, 30000);

    console.log('✅ Interactivity setup complete');
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 CryptoPulse Enhanced JavaScript Loaded');

    // Initialize data loading
    setTimeout(() => {
        loadAllCoinsData();
    }, 500);

    // Setup global error handling
    window.addEventListener('error', function(e) {
        console.error('Global error:', e.error);
        showErrorToast('An unexpected error occurred');
    });
});

// Export functions for global access
window.CryptoPulse = {
    loadAllCoinsData,
    selectCoin,
    updateDeepAnalysisForCoin,
    coinData,
    COIN_CONFIG,
    currentTimeframe,
    currentSelectedCoin
};

// Legacy support
window.loadAllCoinsData = loadAllCoinsData;
window.selectCoin = selectCoin;
