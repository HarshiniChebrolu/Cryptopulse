 <script>
        // Enhanced coin data with comprehensive information
        const coinData = {
            BTC: {
                name: 'Bitcoin',
                symbol: 'BTC',
                image: 'https://images.unsplash.com/photo-1621761191319-c6fb62004040?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                fallbackImage: 'https://images.unsplash.com/photo-1584824486509-112e4181ff6b?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                basePrice: 4285340,
                priceUSD: 51234.56,
                marketCap: '84.2T',
                supply: '19.6M BTC',
                volume24h: '2.4B',
                ath: '58,67,890',
                volatility: 'Medium',
                color: '#00d4ff'
            },
            LTC: {
                name: 'Litecoin',
                symbol: 'LTC',
                image: 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                fallbackImage: 'https://images.unsplash.com/photo-1621761191319-c6fb62004040?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                basePrice: 7845,
                priceUSD: 94.12,
                marketCap: '5.8B',
                supply: '74.2M LTC',
                volume24h: '125M',
                ath: '31,450',
                volatility: 'Medium-High',
                color: '#00ff88'
            },
            ADA: {
                name: 'Cardano',
                symbol: 'ADA',
                image: 'https://images.unsplash.com/photo-1644088379091-d574269d422f?q=80&w=2595&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                fallbackImage: 'https://images.unsplash.com/photo-1621761191319-c6fb62004040?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                basePrice: 37.84,
                priceUSD: 0.453,
                marketCap: '1.3T',
                supply: '35.0B ADA',
                volume24h: '45M',
                ath: '246.78',
                volatility: 'High',
                color: '#ffb800'
            },
            BNB: {
                name: 'Binance Coin',
                symbol: 'BNB',
                image: 'https://images.unsplash.com/photo-1640340434855-6084b1f4901c?q=80&w=2926&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                fallbackImage: 'https://images.unsplash.com/photo-1621761191319-c6fb62004040?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                basePrice: 55234,
                priceUSD: 662.45,
                marketCap: '8.2B',
                supply: '147.6M BNB',
                volume24h: '890M',
                ath: '56,789',
                volatility: 'Medium',
                color: '#ff4757'
            },
            XRP: {
                name: 'Ripple',
                symbol: 'XRP',
                image: 'https://images.unsplash.com/photo-1640926994546-2c000e5ba4c6?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                fallbackImage: 'https://images.unsplash.com/photo-1621761191319-c6fb62004040?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                basePrice: 189.34,
                priceUSD: 2.27,
                marketCap: '1.1T',
                supply: '99.9B XRP',
                volume24h: '2.1B',
                ath: '276.89',
                volatility: 'High',
                color: '#8e44ad'
            },
            SOL: {
                name: 'Solana',
                symbol: 'SOL',
                image: 'https://images.unsplash.com/photo-1640340434976-9da6bafa3849?q=80&w=2926&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                fallbackImage: 'https://images.unsplash.com/photo-1621761191319-c6fb62004040?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                basePrice: 11234,
                priceUSD: 134.67,
                marketCap: '6.1B',
                supply: '416.4M SOL',
                volume24h: '1.2B',
                ath: '21,456',
                volatility: 'Very High',
                color: '#e84393'
            }
        };

        let currentCoin = 'BTC';
        let mainPriceChart, volumeChart;
        let currentStartDate = '2025-01-01';
        let currentEndDate = '2025-01-30';
        let currentChartType = 'candlestick';
        let activeIndicators = ['MA'];

        // Initialize the dashboard
        function initializeDashboard() {
            checkAuthStatus();
            
            // Check if a specific coin was selected from overview
            const selectedCoin = localStorage.getItem('selectedCoin');
            if (selectedCoin && coinData[selectedCoin]) {
                currentCoin = selectedCoin;
                document.getElementById('coinSelector').value = selectedCoin;
                localStorage.removeItem('selectedCoin'); // Clear after use
            }
            
            initializeCharts();
            updateCoinDisplay(currentCoin);
            setupEventListeners();
            startRealTimeUpdates();
        }

        // Check authentication status
        function checkAuthStatus() {
            const session = localStorage.getItem('cryptopulse_session');
            if (!session) {
                window.location.href = '../index.html';
                return;
            }

            try {
                const sessionData = JSON.parse(session);
                const userEmail = document.getElementById('userEmail');
                const userInitial = document.getElementById('userInitial');
                
                if (userEmail && userInitial) {
                    userEmail.textContent = sessionData.user;
                    userInitial.textContent = sessionData.user.charAt(0).toUpperCase();
                }
            } catch (e) {
                window.location.href = '../index.html';
            }
        }

        // Initialize Charts
        function initializeCharts() {
            const mainCtx = document.getElementById('mainPriceChart').getContext('2d');
            const chartData = generateChartData();
            
            mainPriceChart = new Chart(mainCtx, {
                type: currentChartType === 'candlestick' ? 'line' : currentChartType,
                data: chartData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            backgroundColor: 'rgba(42, 42, 42, 0.9)',
                            titleColor: '#ffffff',
                            bodyColor: '#a0a0a0',
                            borderColor: '#00d4ff',
                            borderWidth: 1
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            },
                            ticks: {
                                color: '#a0a0a0'
                            }
                        },
                        y: {
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            },
                            ticks: {
                                color: '#a0a0a0',
                                callback: function(value) {
                                    return '₹' + value.toLocaleString();
                                }
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    }
                }
            });

            const volumeCtx = document.getElementById('volumeChart').getContext('2d');
            volumeChart = new Chart(volumeCtx, {
                type: 'bar',
                data: generateVolumeData(),
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            },
                            ticks: {
                                color: '#a0a0a0'
                            }
                        },
                        y: {
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            },
                            ticks: {
                                color: '#a0a0a0',
                                callback: function(value) {
                                    return '₹' + value + 'M';
                                }
                            }
                        }
                    }
                }
            });
        }

        // Generate chart data based on current settings
        function generateChartData() {
            const labels = generateDateLabels();
            const data = coinData[currentCoin];
            const priceData = generatePriceDataForTimeframe(data.basePrice, labels.length);
            const maData = generateMovingAverage(priceData, 7);

            const datasets = [
                {
                    label: `${currentCoin} Price`,
                    data: priceData,
                    borderColor: data.color,
                    backgroundColor: currentChartType === 'area' ? data.color + '20' : 'transparent',
                    tension: 0.4,
                    fill: currentChartType === 'area',
                    pointRadius: currentChartType === 'line' ? 3 : 0,
                    pointHoverRadius: 6
                }
            ];

            // Add moving average if active
            if (activeIndicators.includes('MA')) {
                datasets.push({
                    label: 'Moving Average',
                    data: maData,
                    borderColor: '#00ff88',
                    backgroundColor: 'transparent',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 0,
                    borderDash: [5, 5]
                });
            }

            return { labels, datasets };
        }

        // Generate volume chart data
        function generateVolumeData() {
            const labels = generateDateLabels();
            const volumeData = generateVolumeDataForTimeframe(labels.length);

            return {
                labels,
                datasets: [{
                    label: 'Volume',
                    data: volumeData,
                    backgroundColor: 'rgba(255, 184, 0, 0.6)',
                    borderColor: '#ffb800',
                    borderWidth: 1
                }]
            };
        }

        // Generate date labels based on date range
        function generateDateLabels() {
            const labels = [];
            const start = new Date(currentStartDate);
            const end = new Date(currentEndDate);
            const diffTime = Math.abs(end - start);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            const step = Math.max(1, Math.floor(diffDays / 10));
            for (let i = 0; i <= diffDays; i += step) {
                const date = new Date(start);
                date.setDate(start.getDate() + i);
                labels.push(date.toLocaleDateString('en-GB', { month: 'short', day: 'numeric' }));
            }

            return labels;
        }

        // Generate price data for specific timeframe
        function generatePriceDataForTimeframe(basePrice, dataPoints) {
            const data = [];
            let currentPrice = basePrice;

            for (let i = 0; i < dataPoints; i++) {
                const volatility = 0.05; // 5% volatility
                const change = (Math.random() - 0.5) * volatility;
                currentPrice = currentPrice * (1 + change);
                data.push(Math.round(currentPrice));
            }

            return data;
        }

        // Generate volume data for specific timeframe
        function generateVolumeDataForTimeframe(dataPoints) {
            const data = [];
            const baseVolume = parseFloat(coinData[currentCoin].volume24h.replace(/[^\d.]/g, ''));

            for (let i = 0; i < dataPoints; i++) {
                const variation = (Math.random() - 0.5) * 0.8;
                const volume = baseVolume * (1 + variation);
                data.push(Math.round(volume));
            }

            return data;
        }

        // Generate moving average
        function generateMovingAverage(data, period) {
            const ma = [];
            for (let i = 0; i < data.length; i++) {
                if (i < period - 1) {
                    ma.push(null);
                } else {
                    const sum = data.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
                    ma.push(sum / period);
                }
            }
            return ma;
        }

        // Update UI for selected coin
        function updateCoinDisplay(coin) {
            const data = coinData[coin];
            const currentPrice = generateCurrentPrice(data.basePrice);
            const change = generatePriceChange();
            
            // Update main coin header
            document.getElementById('coinImage').src = data.image;
            document.getElementById('coinImage').alt = data.name;
            document.getElementById('coinTitle').textContent = `${data.name} (${data.symbol})`;

            // Update live price section
            document.getElementById('priceINR').textContent = `₹${currentPrice.toLocaleString()}`;
            document.getElementById('priceUSD').textContent = `$${data.priceUSD.toLocaleString()}`;
            
            const changeElement = document.getElementById('priceChangePercent');
            const changeClass = change >= 0 ? 'bg-accent/20 text-accent' : 'bg-error/20 text-error';
            changeElement.className = `text-xs px-2 py-1 rounded ${changeClass}`;
            changeElement.textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)}%`;

            // Update 24h high/low
            document.getElementById('high24h').textContent = `₹${(currentPrice * 1.08).toLocaleString()}`;
            document.getElementById('low24h').textContent = `₹${(currentPrice * 0.92).toLocaleString()}`;

            // Update key statistics
            updateKeyStatistics(data);
            
            // Update recent alerts
            updateRecentAlerts(data);
            
            // Update volume analysis
            updateVolumeAnalysis(data);
            
            // Update volatility metrics
            updateVolatilityMetrics(data);
            
            // Update AI predictions
            updateAIPredictions(data);

            // Update chart data
            updateCharts();
        }

        // Update key statistics
        function updateKeyStatistics(data) {
            const container = document.getElementById('keyStatistics');
            container.innerHTML = `
                <div class="flex justify-between items-center">
                    <span class="text-text-secondary">Market Cap</span>
                    <span class="font-mono text-text-primary">₹${data.marketCap}</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-text-secondary">Circulating Supply</span>
                    <span class="font-mono text-text-primary">${data.supply}</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-text-secondary">24h Volume</span>
                    <span class="font-mono text-text-primary">₹${data.volume24h}</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-text-secondary">All-Time High</span>
                    <span class="font-mono text-text-primary">₹${data.ath}</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-text-secondary">Volatility (30d)</span>
                    <span class="px-2 py-1 rounded text-xs ${getVolatilityClass(data.volatility)}">${data.volatility}</span>
                </div>
            `;
        }

        // Get volatility class for styling
        function getVolatilityClass(volatility) {
            if (volatility.includes('Low')) return 'bg-accent/20 text-accent';
            if (volatility.includes('Medium')) return 'bg-warning/20 text-warning';
            return 'bg-error/20 text-error';
        }

        // Update recent alerts
        function updateRecentAlerts(data) {
            const alerts = generateAlertsForCoin(data);
            const container = document.getElementById('recentAlerts');
            
            container.innerHTML = alerts.map(alert => `
                <div class="p-3 rounded-lg bg-${alert.color}/10 border border-${alert.color}/20">
                    <div class="flex items-center space-x-2 mb-1">
                        <div class="w-2 h-2 bg-${alert.color} rounded-full"></div>
                        <span class="text-xs text-${alert.color} font-medium">${alert.type}</span>
                    </div>
                    <p class="text-sm text-text-primary">${alert.message}</p>
                    <p class="text-xs text-text-tertiary">${alert.time}</p>
                </div>
            `).join('');
        }

        // Generate alerts for specific coin
        function generateAlertsForCoin(data) {
            const alerts = [
                {
                    type: 'BREAKOUT',
                    color: 'accent',
                    message: `${data.symbol} broke resistance at ₹${(data.basePrice * 0.95).toLocaleString()}`,
                    time: `${Math.floor(Math.random() * 10) + 1} minutes ago`
                },
                {
                    type: 'VOLUME SPIKE',
                    color: 'warning',
                    message: `Unusual volume detected (+${Math.floor(Math.random() * 200) + 50}%)`,
                    time: `${Math.floor(Math.random() * 20) + 5} minutes ago`
                },
                {
                    type: 'SUPPORT',
                    color: 'primary',
                    message: `Strong support at ₹${(data.basePrice * 0.88).toLocaleString()}`,
                    time: `${Math.floor(Math.random() * 30) + 10} minutes ago`
                }
            ];

            return alerts.slice(0, 3);
        }

        // Update volume analysis
        function updateVolumeAnalysis(data) {
            const baseVolume = parseFloat(data.volume24h.replace(/[^\d.]/g, ''));
            document.getElementById('avgVolume').textContent = `₹${(baseVolume * 0.8).toFixed(1)}B`;
            document.getElementById('peakVolume').textContent = `₹${(baseVolume * 1.3).toFixed(1)}B`;
            
            const trendChange = Math.floor(Math.random() * 40) - 20;
            const trendElement = document.getElementById('volumeTrend');
            const trendClass = trendChange >= 0 ? 'bg-accent/20 text-accent' : 'bg-error/20 text-error';
            trendElement.className = `text-xs px-2 py-1 rounded ${trendClass}`;
            trendElement.textContent = `${trendChange >= 0 ? '+' : ''}${trendChange}%`;
        }

        // Update volatility metrics
        function updateVolatilityMetrics(data) {
            const container = document.getElementById('volatilityMetrics');
            const volatilityData = [
                { period: '1-Day', value: (Math.random() * 5 + 1).toFixed(2), width: Math.random() * 50 + 10 },
                { period: '7-Day', value: (Math.random() * 8 + 2).toFixed(2), width: Math.random() * 70 + 20 },
                { period: '30-Day', value: (Math.random() * 12 + 3).toFixed(2), width: Math.random() * 90 + 30 }
            ];

            const volatilityHTML = volatilityData.map(item => `
                <div class="p-4 rounded-lg bg-surface/30">
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-text-secondary">${item.period} Volatility</span>
                        <span class="font-mono text-text-primary">${item.value}%</span>
                    </div>
                    <div class="w-full bg-surface rounded-full h-2">
                        <div class="bg-accent h-2 rounded-full" style="width: ${item.width}%"></div>
                    </div>
                </div>
            `).join('');

            const riskLevel = data.volatility.includes('High') ? 'High' : data.volatility.includes('Low') ? 'Low' : 'Medium';
            const riskClass = riskLevel === 'Low' ? 'bg-accent/20 text-accent' : riskLevel === 'Medium' ? 'bg-warning/20 text-warning' : 'bg-error/20 text-error';

            container.innerHTML = volatilityHTML + `
                <div class="grid grid-cols-2 gap-4 mt-4">
                    <div class="text-center p-3 rounded-lg bg-surface/50">
                        <p class="text-xs text-text-tertiary">Risk Level</p>
                        <span class="text-sm px-2 py-1 rounded ${riskClass}">${riskLevel}</span>
                    </div>
                    <div class="text-center p-3 rounded-lg bg-surface/50">
                        <p class="text-xs text-text-tertiary">Trend Strength</p>
                        <span class="text-sm px-2 py-1 rounded bg-accent/20 text-accent">Strong</span>
                    </div>
                </div>
            `;
        }

        // Update AI predictions
        function updateAIPredictions(data) {
            updatePriceForecasts(data);
            updatePriceMilestones(data);
            updateModelPerformance();
        }

        // Update price forecasts
        function updatePriceForecasts(data) {
            const forecasts = [
                { period: '1 Hour', price: data.basePrice * (1 + (Math.random() - 0.5) * 0.02), confidence: Math.floor(Math.random() * 15) + 85 },
                { period: '4 Hours', price: data.basePrice * (1 + (Math.random() - 0.5) * 0.05), confidence: Math.floor(Math.random() * 20) + 70 },
                { period: '24 Hours', price: data.basePrice * (1 + (Math.random() - 0.5) * 0.1), confidence: Math.floor(Math.random() * 25) + 60 }
            ];

            const container = document.getElementById('priceForecasts');
            container.innerHTML = forecasts.map(forecast => {
                const change = ((forecast.price - data.basePrice) / data.basePrice) * 100;
                const changeClass = change >= 0 ? 'text-accent' : 'text-error';
                const confidenceClass = forecast.confidence >= 85 ? 'accent' : forecast.confidence >= 70 ? 'warning' : 'primary';
                
                return `
                    <div class="p-4 rounded-lg bg-surface/30 border border-border">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm text-text-secondary">${forecast.period}</span>
                            <span class="text-xs px-2 py-1 rounded bg-${confidenceClass}/20 text-${confidenceClass}">${forecast.confidence}% Confidence</span>
                        </div>
                        <p class="text-xl font-mono text-text-primary">₹${Math.round(forecast.price).toLocaleString()}</p>
                        <p class="text-sm ${changeClass}">${change >= 0 ? '+' : ''}${change.toFixed(2)}% ↗</p>
                        <div class="w-full bg-surface rounded-full h-2 mt-2">
                            <div class="bg-${confidenceClass} h-2 rounded-full" style="width: ${forecast.confidence}%"></div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        // Update price milestones
        function updatePriceMilestones(data) {
            const milestones = [
                { price: data.basePrice * 1.05, type: 'Resistance Level', eta: '2-4 hours', color: 'accent' },
                { price: data.basePrice * 1.15, type: 'Next Target', eta: '6-12 hours', color: 'warning' },
                { price: data.basePrice * 1.25, type: 'Major Milestone', eta: '1-2 days', color: 'primary' },
                { price: data.basePrice * 0.9, type: 'Support Level', eta: 'If bearish', color: 'error' }
            ];

            const container = document.getElementById('priceMilestones');
            container.innerHTML = milestones.map(milestone => `
                <div class="p-3 rounded-lg bg-surface/30 border border-border">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="font-mono text-text-primary">₹${Math.round(milestone.price).toLocaleString()}</p>
                            <p class="text-xs text-text-tertiary">${milestone.type}</p>
                        </div>
                        <div class="text-right">
                            <p class="text-sm text-${milestone.color}">${milestone.eta}</p>
                            <p class="text-xs text-text-tertiary">ETA</p>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        // Update model performance
        function updateModelPerformance() {
            const overallAccuracy = Math.floor(Math.random() * 15) + 80;
            const oneHourAccuracy = Math.floor(Math.random() * 10) + 90;
            const twentyFourHourAccuracy = Math.floor(Math.random() * 20) + 70;

            const container = document.getElementById('modelPerformance');
            container.innerHTML = `
                <div class="p-4 rounded-lg bg-surface/30 border border-border">
                    <div class="text-center mb-3">
                        <p class="text-3xl font-bold text-accent">${overallAccuracy}.3%</p>
                        <p class="text-sm text-text-secondary">Overall Accuracy</p>
                    </div>
                    <div class="w-full bg-surface rounded-full h-3">
                        <div class="bg-accent h-3 rounded-full" style="width: ${overallAccuracy}%"></div>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-3">
                    <div class="p-3 rounded-lg bg-surface/50 text-center">
                        <p class="text-lg font-bold text-text-primary">${oneHourAccuracy}%</p>
                        <p class="text-xs text-text-tertiary">1H Accuracy</p>
                    </div>
                    <div class="p-3 rounded-lg bg-surface/50 text-center">
                        <p class="text-lg font-bold text-text-primary">${twentyFourHourAccuracy}%</p>
                        <p class="text-xs text-text-tertiary">24H Accuracy</p>
                    </div>
                </div>

                <div class="p-4 rounded-lg bg-surface/30 border border-border">
                    <h4 class="text-sm font-medium text-text-primary mb-2">Recent Predictions</h4>
                    <div class="space-y-2">
                        <div class="flex items-center justify-between text-sm">
                            <span class="text-text-secondary">Jan 14, 15:00</span>
                            <span class="px-2 py-1 rounded text-xs bg-accent/20 text-accent">✓ Correct</span>
                        </div>
                        <div class="flex items-center justify-between text-sm">
                            <span class="text-text-secondary">Jan 14, 11:00</span>
                            <span class="px-2 py-1 rounded text-xs bg-accent/20 text-accent">✓ Correct</span>
                        </div>
                        <div class="flex items-center justify-between text-sm">
                            <span class="text-text-secondary">Jan 13, 20:00</span>
                            <span class="px-2 py-1 rounded text-xs bg-error/20 text-error">✗ Missed</span>
                        </div>
                    </div>
                </div>
            `;
        }

        // Generate current price with variation
        function generateCurrentPrice(basePrice) {
            const variation = (Math.random() - 0.5) * 0.1;
            return Math.round(basePrice * (1 + variation));
        }

        // Generate price change percentage
        function generatePriceChange() {
            return (Math.random() - 0.5) * 20;
        }

        // Update charts with new data
        function updateCharts() {
            if (mainPriceChart) {
                const newData = generateChartData();
                mainPriceChart.data = newData;
                mainPriceChart.update();
            }

            if (volumeChart) {
                const newVolumeData = generateVolumeData();
                volumeChart.data = newVolumeData;
                volumeChart.update();
            }
        }

        // Setup event listeners
        function setupEventListeners() {
            // Coin selector
            document.getElementById('coinSelector').addEventListener('change', function() {
                const selectedCoin = this.value;
                currentCoin = selectedCoin;
                updateCoinDisplay(selectedCoin);
            });

            // Date range inputs
            document.getElementById('startDate').addEventListener('change', function() {
                currentStartDate = this.value;
                updateCharts();
            });

            document.getElementById('endDate').addEventListener('change', function() {
                currentEndDate = this.value;
                updateCharts();
            });

            // Chart type selector
            document.getElementById('chartTypeSelector').addEventListener('change', function() {
                currentChartType = this.value;
                updateChartType();
            });

            // Technical indicators
            document.querySelectorAll('.indicator-toggle').forEach(button => {
                button.addEventListener('click', function() {
                    const indicator = this.getAttribute('data-indicator');
                    toggleIndicator(indicator, this);
                });
            });

            // User menu
            document.getElementById('userMenuButton').addEventListener('click', function() {
                const dropdown = document.getElementById('userDropdown');
                dropdown.classList.toggle('hidden');
            });

            // Logout button
            document.getElementById('logoutButton').addEventListener('click', function() {
                logout();
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', function(e) {
                const userMenu = document.getElementById('userMenuButton');
                const dropdown = document.getElementById('userDropdown');
                if (!userMenu.contains(e.target) && !dropdown.contains(e.target)) {
                    dropdown.classList.add('hidden');
                }
            });
        }

        // Toggle technical indicator
        function toggleIndicator(indicator, button) {
            if (activeIndicators.includes(indicator)) {
                activeIndicators = activeIndicators.filter(i => i !== indicator);
                button.classList.remove('active', 'bg-primary', 'text-white');
                button.classList.add('bg-surface', 'text-text-secondary');
            } else {
                activeIndicators.push(indicator);
                button.classList.add('active', 'bg-primary', 'text-white');
                button.classList.remove('bg-surface', 'text-text-secondary');
            }
            updateCharts();
        }

        // Update chart type
        function updateChartType() {
            if (mainPriceChart) {
                mainPriceChart.config.type = currentChartType === 'candlestick' ? 'line' : currentChartType;
                const newData = generateChartData();
                mainPriceChart.data = newData;
                mainPriceChart.update();
            }
        }

        // Start real-time updates
        function startRealTimeUpdates() {
            setInterval(() => {
                updateLastUpdateTime();
                updateCoinDisplay(currentCoin);
            }, 30000); // Update every 30 seconds
        }

        // Update last update time
        function updateLastUpdateTime() {
            const now = new Date();
            const timeString = now.toLocaleString('en-GB', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
            });
            document.getElementById('lastUpdateTime').textContent = timeString;
        }

        // Logout function
        function logout() {
            localStorage.removeItem('cryptopulse_session');
            localStorage.removeItem('selectedCoin');
            window.location.href = '../index.html';
        }

        // Initialize dashboard when page loads
        document.addEventListener('DOMContentLoaded', initializeDashboard);
    </script>
</body>
</html>