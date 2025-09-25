# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-09-24

### Added
- 🧭 **Core Application**: Travel distance & time calculator using Google Maps Platform
- 📍 **Address Input**: Form inputs with validation for origin and destination addresses
- 🔄 **Address Swap**: Button to swap origin and destination addresses with animation
- 🚗 **Travel Modes**: Support for driving, walking, cycling, and transit modes
- 📊 **Calculation Results**: Real-time distance (km) and travel time (HH:MM & decimal)
- 🗺️ **Interactive Google Maps**: Route visualization with markers and polylines
- 💾 **Session Management**: API key storage and result caching
- 📋 **Copy to Clipboard**: Easy copying of coordinate data in CSV format
- 🎨 **Modern UI**: Responsive design with gradients, animations, and glass-morphism effects
- 🔒 **Security**: Secure API key handling with session storage
- ✅ **Error Handling**: Comprehensive validation and user-friendly error messages
- 📱 **Mobile Responsive**: Optimized layout for all screen sizes

### Technical Features
- **Backend**: Flask web application with Google Maps APIs integration
- **Frontend**: Vanilla JavaScript with modern ES6+ features
- **Styling**: Custom CSS with animations and responsive design
- **APIs**: Geocoding, Distance Matrix, Directions, and Maps JavaScript APIs
- **Data Format**: CSV coordinate output for easy export
- **Cross-browser**: Modern Clipboard API with fallback support

### Documentation
- 📚 **README.md**: Comprehensive setup and usage guide
- 🚀 **DEMO.md**: Testing guide with examples
- 🚀 **DEPLOYMENT.md**: Production deployment guide
- 📄 **CHANGELOG.md**: Version history and feature tracking
- 🧪 **test_decimal_conversion.py**: Test suite for decimal hours conversion
- 📝 **Inline Documentation**: Well-documented code with comments
- ⚖️ **LICENSE**: MIT License for open source usage

### Data Output Format
```
lat_origin,lng_origin,lat_destination,lng_destination,distance_km,HH:MM,decimal_hours
```

Example:
```
-0.026700,109.342100,-0.114200,109.406500,12.84,01:30,1.50
```

### Google Maps APIs Required
- Geocoding API
- Distance Matrix API
- Directions API
- Maps JavaScript API

### Browser Compatibility
- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+