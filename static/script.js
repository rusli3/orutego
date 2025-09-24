// Orutego JavaScript Application
class OrutegoApp {
    constructor() {
        this.selectedMode = 'driving';
        this.isApiKeySaved = false;
        this.lastResult = null;
        this.googleMap = null;
        this.directionsService = null;
        this.directionsRenderer = null;
        this.pendingMapData = null;
        this.apiKey = null;
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.checkApiKeyStatus();
    }
    
    bindEvents() {
        // API Key functionality
        document.getElementById('toggleApiKey').addEventListener('click', this.toggleApiKeyVisibility.bind(this));
        document.getElementById('saveApiKey').addEventListener('click', this.saveApiKey.bind(this));
        
        // Address functionality
        document.getElementById('swapAddresses').addEventListener('click', this.swapAddresses.bind(this));
        
        // Travel mode selection
        document.querySelectorAll('.travel-mode').forEach(btn => {
            btn.addEventListener('click', (e) => this.selectTravelMode(e.target.closest('.travel-mode')));
        });
        
        // Calculate button
        document.getElementById('calculateBtn').addEventListener('click', this.calculateRoute.bind(this));
        
        // Copy button
        document.getElementById('copyBtn').addEventListener('click', this.copyToClipboard.bind(this));
        
        // Enter key support for inputs
        document.getElementById('apiKey').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.saveApiKey();
        });
        
        document.getElementById('origin').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.calculateRoute();
        });
        
        document.getElementById('destination').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.calculateRoute();
        });
    }
    
    toggleApiKeyVisibility() {
        const apiKeyInput = document.getElementById('apiKey');
        const eyeIcon = document.getElementById('eyeIcon');
        
        if (apiKeyInput.type === 'password') {
            apiKeyInput.type = 'text';
            eyeIcon.className = 'fas fa-eye-slash';
        } else {
            apiKeyInput.type = 'password';
            eyeIcon.className = 'fas fa-eye';
        }
    }
    
    async saveApiKey() {
        const apiKey = document.getElementById('apiKey').value.trim();
        const statusElement = document.getElementById('apiKeyStatus');
        const saveBtn = document.getElementById('saveApiKey');
        
        if (!apiKey) {
            this.showStatus(statusElement, 'Please enter a valid API key', 'error');
            return;
        }
        
        try {
            const response = await fetch('/api/save-key', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ apiKey: apiKey })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.isApiKeySaved = true;
                this.apiKey = apiKey;
                saveBtn.textContent = 'Saved';
                saveBtn.classList.remove('btn-outline');
                saveBtn.classList.add('btn-primary');
                this.showStatus(statusElement, 'API key saved successfully!', 'success');
                this.clearError();
                
                // Load Google Maps API
                this.loadGoogleMapsAPI();
            } else {
                this.showStatus(statusElement, data.error || 'Failed to save API key', 'error');
            }
        } catch (error) {
            this.showStatus(statusElement, 'Network error. Please try again.', 'error');
        }
    }
    
    loadGoogleMapsAPI() {
        if (window.google && window.google.maps) {
            this.initializeGoogleMaps();
            return;
        }
        
        // Check if script is already loading
        if (document.getElementById('google-maps-script')) {
            return;
        }
        
        const script = document.createElement('script');
        script.id = 'google-maps-script';
        script.src = `https://maps.googleapis.com/maps/api/js?key=${this.apiKey}&callback=initMap&libraries=geometry`;
        script.async = true;
        script.defer = true;
        
        script.onerror = () => {
            this.showError('Failed to load Google Maps. Please check your API key and internet connection.');
        };
        
        document.head.appendChild(script);
        window.orutegoApp = this; // Make instance available globally for callback
    }
    
    initializeGoogleMaps() {
        const mapElement = document.getElementById('googleMap');
        
        this.googleMap = new google.maps.Map(mapElement, {
            zoom: 13,
            center: { lat: -0.0267, lng: 109.3421 }, // Default center (Pontianak, Indonesia)
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            styles: [
                {
                    featureType: 'poi',
                    stylers: [{ visibility: 'off' }]
                },
                {
                    featureType: 'transit.station',
                    stylers: [{ visibility: 'off' }]
                }
            ]
        });
        
        this.directionsService = new google.maps.DirectionsService();
        this.directionsRenderer = new google.maps.DirectionsRenderer({
            suppressMarkers: false,
            polylineOptions: {
                strokeColor: '#0ea5e9',
                strokeWeight: 4,
                strokeOpacity: 0.8
            }
        });
        
        this.directionsRenderer.setMap(this.googleMap);
        
        // Show the map and hide placeholder
        document.getElementById('googleMap').classList.add('show');
        document.getElementById('mapPlaceholder').classList.add('hidden');
        
        // If there's pending map data, draw it
        if (this.pendingMapData) {
            this.drawGoogleMap(this.pendingMapData);
            this.pendingMapData = null;
        }
    }
    
    checkApiKeyStatus() {
        // Check if there's a saved API key by attempting a simple request
        const apiKeyInput = document.getElementById('apiKey');
        const saveBtn = document.getElementById('saveApiKey');
        
        if (localStorage.getItem('orutego_api_key_saved')) {
            this.isApiKeySaved = true;
            saveBtn.textContent = 'Saved';
            saveBtn.classList.remove('btn-outline');
            saveBtn.classList.add('btn-primary');
            apiKeyInput.value = '*********************'; // Placeholder
        }
    }
    
    swapAddresses() {
        const originInput = document.getElementById('origin');
        const destinationInput = document.getElementById('destination');
        
        const temp = originInput.value;
        originInput.value = destinationInput.value;
        destinationInput.value = temp;
        
        // Add animation effect
        const swapBtn = document.getElementById('swapAddresses');
        swapBtn.style.transform = 'rotate(180deg)';
        setTimeout(() => {
            swapBtn.style.transform = 'rotate(0deg)';
        }, 300);
    }
    
    selectTravelMode(selectedBtn) {
        // Remove active class from all buttons
        document.querySelectorAll('.travel-mode').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Add active class to selected button
        selectedBtn.classList.add('active');
        this.selectedMode = selectedBtn.dataset.mode;
    }
    
    async calculateRoute() {
        const origin = document.getElementById('origin').value.trim();
        const destination = document.getElementById('destination').value.trim();
        
        // Validation
        if (!this.isApiKeySaved) {
            this.showError('Please save your API key first');
            return;
        }
        
        if (!origin || !destination) {
            this.showError('Please enter both origin and destination addresses');
            return;
        }
        
        // Show loading state
        this.showLoading(true);
        
        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    origin: origin,
                    destination: destination,
                    travelMode: this.selectedMode
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.lastResult = data;
                this.displayResults(data);
                this.drawGoogleMap(data);
                this.clearError();
                
                // Save to localStorage for persistence
                localStorage.setItem('orutego_last_result', JSON.stringify(data));
            } else {
                this.showError(data.error || 'Calculation failed');
            }
        } catch (error) {
            this.showError('Network error. Please check your connection and try again.');
        } finally {
            this.showLoading(false);
        }
    }
    
    displayResults(data) {
        // Hide no results and show results content
        document.getElementById('noResults').style.display = 'none';
        document.getElementById('resultsContent').classList.remove('hidden');
        
        // Validate and format decimal hours (double-check the backend calculation)
        const validatedDecimalHours = this.validateDecimalHours(data.duration, data.decimalHours);
        
        // Update result values
        document.getElementById('distanceValue').textContent = `${data.distance} km`;
        document.getElementById('durationValue').textContent = data.duration;
        document.getElementById('decimalHoursValue').textContent = `${validatedDecimalHours}h decimal`;
        
        // Format coordinates to 6 decimal places for consistency
        const formattedOriginLat = parseFloat(data.originCoords[0]).toFixed(6);
        const formattedOriginLng = parseFloat(data.originCoords[1]).toFixed(6);
        const formattedDestLat = parseFloat(data.destinationCoords[0]).toFixed(6);
        const formattedDestLng = parseFloat(data.destinationCoords[1]).toFixed(6);
        
        // Update coordinate output with validated data
        const coordinateOutput = `${formattedOriginLat},${formattedOriginLng},${formattedDestLat},${formattedDestLng},${data.distance},${data.duration},${validatedDecimalHours}`;
        document.getElementById('coordinateOutput').textContent = coordinateOutput;
        
        // Animate results
        const resultsContent = document.getElementById('resultsContent');
        resultsContent.style.animation = 'slideInUp 0.5s ease-out';
        
        // Log for debugging if needed
        console.log('Results:', {
            distance: data.distance,
            duration: data.duration,
            decimalHours: validatedDecimalHours,
            coordinates: coordinateOutput
        });
    }
    
    validateDecimalHours(duration, backendDecimal) {
        // Parse HH:MM format to validate decimal conversion
        const [hours, minutes] = duration.split(':').map(Number);
        
        // Convert to decimal hours: hours + (minutes/60)
        const calculatedDecimal = parseFloat((hours + minutes / 60).toFixed(2));
        
        // Use our calculation if there's a discrepancy (shouldn't happen, but safety check)
        if (Math.abs(calculatedDecimal - backendDecimal) > 0.01) {
            console.warn(`Decimal hours mismatch detected. Backend: ${backendDecimal}, Calculated: ${calculatedDecimal}. Using calculated value.`);
            return calculatedDecimal;
        }
        
        return backendDecimal;
    }
    
    drawGoogleMap(data) {
        // If Google Maps is not yet initialized, store the data for later
        if (!this.googleMap) {
            this.pendingMapData = data;
            return;
        }
        
        const origin = new google.maps.LatLng(data.originCoords[0], data.originCoords[1]);
        const destination = new google.maps.LatLng(data.destinationCoords[0], data.destinationCoords[1]);
        
        // Convert travel mode to Google Maps format
        let googleTravelMode;
        switch (this.selectedMode.toLowerCase()) {
            case 'driving':
                googleTravelMode = google.maps.TravelMode.DRIVING;
                break;
            case 'walking':
                googleTravelMode = google.maps.TravelMode.WALKING;
                break;
            case 'bicycling':
                googleTravelMode = google.maps.TravelMode.BICYCLING;
                break;
            case 'transit':
                googleTravelMode = google.maps.TravelMode.TRANSIT;
                break;
            default:
                googleTravelMode = google.maps.TravelMode.DRIVING;
        }
        
        // Request directions
        const request = {
            origin: origin,
            destination: destination,
            travelMode: googleTravelMode,
            unitSystem: google.maps.UnitSystem.METRIC
        };
        
        this.directionsService.route(request, (result, status) => {
            if (status === google.maps.DirectionsStatus.OK) {
                this.directionsRenderer.setDirections(result);
                
                // Fit map to show the entire route
                const bounds = new google.maps.LatLngBounds();
                bounds.extend(origin);
                bounds.extend(destination);
                this.googleMap.fitBounds(bounds);
                
                // Add custom markers
                this.addCustomMarkers(origin, destination, data);
                
            } else {
                console.error('Directions request failed due to ' + status);
                // Fallback: just show markers without route
                this.showFallbackMarkers(origin, destination, data);
            }
        });
    }
    
    addCustomMarkers(origin, destination, data) {
        // Create custom origin marker (green)
        const originMarker = new google.maps.Marker({
            position: origin,
            map: this.googleMap,
            title: 'Origin',
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                fillColor: '#10b981',
                fillOpacity: 1,
                strokeColor: '#ffffff',
                strokeWeight: 3,
                scale: 12
            },
            label: {
                text: 'A',
                color: '#ffffff',
                fontWeight: 'bold',
                fontSize: '14px'
            }
        });
        
        // Create custom destination marker (red)
        const destinationMarker = new google.maps.Marker({
            position: destination,
            map: this.googleMap,
            title: 'Destination',
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                fillColor: '#ef4444',
                fillOpacity: 1,
                strokeColor: '#ffffff',
                strokeWeight: 3,
                scale: 12
            },
            label: {
                text: 'B',
                color: '#ffffff',
                fontWeight: 'bold',
                fontSize: '14px'
            }
        });
        
        // Add info windows
        const originInfo = new google.maps.InfoWindow({
            content: `<div style="padding: 5px;"><strong>Origin</strong><br/>${data.originCoords[0].toFixed(6)}, ${data.originCoords[1].toFixed(6)}</div>`
        });
        
        const destinationInfo = new google.maps.InfoWindow({
            content: `<div style="padding: 5px;"><strong>Destination</strong><br/>${data.destinationCoords[0].toFixed(6)}, ${data.destinationCoords[1].toFixed(6)}<br/><strong>Distance:</strong> ${data.distance} km<br/><strong>Duration:</strong> ${data.duration} (${data.decimalHours}h)</div>`
        });
        
        originMarker.addListener('click', () => {
            destinationInfo.close();
            originInfo.open(this.googleMap, originMarker);
        });
        
        destinationMarker.addListener('click', () => {
            originInfo.close();
            destinationInfo.open(this.googleMap, destinationMarker);
        });
    }
    
    showFallbackMarkers(origin, destination, data) {
        // Clear any existing directions
        this.directionsRenderer.setDirections({routes: []});
        
        // Show just the markers and fit bounds
        const bounds = new google.maps.LatLngBounds();
        bounds.extend(origin);
        bounds.extend(destination);
        this.googleMap.fitBounds(bounds);
        
        this.addCustomMarkers(origin, destination, data);
    }
    
    async copyToClipboard() {
        const coordinateOutput = document.getElementById('coordinateOutput');
        const copyBtn = document.getElementById('copyBtn');
        const copyStatus = document.getElementById('copyStatus');
        const copyIcon = copyBtn.querySelector('i');
        
        if (!coordinateOutput.textContent.trim()) {
            this.showCopyStatus('No data to copy!', 'error');
            return;
        }
        
        try {
            // Try using the modern Clipboard API first
            if (navigator.clipboard && window.isSecureContext) {
                await navigator.clipboard.writeText(coordinateOutput.textContent);
            } else {
                // Fallback for older browsers or non-HTTPS
                const textArea = document.createElement('textarea');
                textArea.value = coordinateOutput.textContent;
                textArea.style.position = 'fixed';
                textArea.style.left = '-999999px';
                textArea.style.top = '-999999px';
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                
                const successful = document.execCommand('copy');
                document.body.removeChild(textArea);
                
                if (!successful) {
                    throw new Error('Copy command failed');
                }
            }
            
            // Success feedback
            copyBtn.classList.add('copied');
            copyIcon.className = 'fas fa-check';
            this.showCopyStatus('Copied to clipboard! 📋', 'success');
            
            // Reset button after animation
            setTimeout(() => {
                copyBtn.classList.remove('copied');
                copyIcon.className = 'fas fa-copy';
            }, 1000);
            
        } catch (error) {
            console.error('Copy failed:', error);
            this.showCopyStatus('Failed to copy. Try selecting and copying manually.', 'error');
        }
    }
    
    showCopyStatus(message, type) {
        const copyStatus = document.getElementById('copyStatus');
        copyStatus.textContent = message;
        copyStatus.className = `copy-status ${type}`;
        
        // Auto hide after animation
        setTimeout(() => {
            copyStatus.classList.remove('success', 'error');
        }, type === 'success' ? 2000 : 3000);
    }
    
    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        const calculateBtn = document.getElementById('calculateBtn');
        const calculateText = document.getElementById('calculateText');
        const icon = calculateBtn.querySelector('i');
        
        if (show) {
            overlay.classList.remove('hidden');
            calculateBtn.disabled = true;
            calculateText.textContent = 'Calculating...';
            icon.classList.add('spinning');
        } else {
            overlay.classList.add('hidden');
            calculateBtn.disabled = false;
            calculateText.textContent = 'Calculate Route';
            icon.classList.remove('spinning');
        }
    }
    
    showError(message) {
        const errorElement = document.getElementById('errorMessage');
        errorElement.textContent = message;
        errorElement.classList.add('show');
        
        // Auto hide after 5 seconds
        setTimeout(() => {
            this.clearError();
        }, 5000);
    }
    
    clearError() {
        const errorElement = document.getElementById('errorMessage');
        errorElement.classList.remove('show');
    }
    
    showStatus(element, message, type) {
        element.textContent = message;
        element.className = `status-message ${type}`;
        
        if (type === 'success') {
            setTimeout(() => {
                element.style.display = 'none';
            }, 3000);
        }
    }
}

// Utility functions
function decodePolyline(str, precision = 5) {
    // Simple polyline decoder (basic implementation)
    let index = 0;
    let lat = 0;
    let lng = 0;
    const coordinates = [];
    const factor = Math.pow(10, precision);
    
    while (index < str.length) {
        let result = 1;
        let shift = 0;
        let b;
        
        do {
            b = str.charCodeAt(index++) - 63;
            result += (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);
        
        lat += (result & 1) ? ~(result >> 1) : (result >> 1);
        
        result = 1;
        shift = 0;
        
        do {
            b = str.charCodeAt(index++) - 63;
            result += (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);
        
        lng += (result & 1) ? ~(result >> 1) : (result >> 1);
        
        coordinates.push([lat / factor, lng / factor]);
    }
    
    return coordinates;
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new OrutegoApp();
});