# 🧭 orutego

orutego is a modern web application for calculating travel distance (km) and travel time (Hours-Minutes & Decimal Hours) between origin and destination addresses using Google Maps Platform.

## ✨ Key Features

- 📍 **Address Input**: Form inputs with auto-complete for origin and destination addresses
- 🔄 **Address Swap**: Button to swap origin and destination addresses  
- 🚗 **Travel Modes**: Options for driving, walking, cycling, and transit
- 📊 **Calculation Results**: Coordinates, distance (km), and travel time (HH:MM & decimal)
- 🗺️ **Interactive Map**: Route visualization with markers and polylines
- 💾 **Session Management**: API key storage and result caching
- 📋 **Copy to Clipboard**: Easy copying of coordinate data in CSV format

## 🚀 Getting Started

### Prerequisites

- Python 3.7+ installed
- Google Maps API Key with the following APIs enabled:
  - Geocoding API
  - Distance Matrix API
  - Directions API
  - **Maps JavaScript API** (newly required for interactive maps)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOURUSERNAME/orutego.git
   cd orutego
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## 📱 How to Use

1. **Input API Key**: Enter your Google Maps API Key and click "Save API Key"
2. **Enter Addresses**: Input origin and destination addresses (with autocomplete feature)
3. **Select Mode**: Choose travel mode (driving/walking/cycling/transit)
4. **Calculate**: Click "Calculate Route" button
5. **View Results**: Coordinates, distance, and time will be displayed
6. **View Map**: Interactive map with route will appear below

## 📊 Data Output Format

The coordinate data is displayed in comma-separated format:

```
lat_origin,lng_origin,lat_destination,lng_destination,distance_km,HH:MM,decimal_hours
```

**Example**:
```
-0.026700,109.342100,-0.114200,109.406500,12.84,01:30,1.50
```

## 🔧 Technical Details

### Backend (Python/Flask)
- **Flask**: Web framework for Python
- **Google Maps APIs**: Geocoding, Distance Matrix, and Directions
- **Session Management**: API key and result caching
- **Error Handling**: Comprehensive validation and error messages

### Frontend
- **Modern CSS**: Responsive design with animations and gradients
- **Vanilla JavaScript**: Clean, modern ES6+ code
- **Google Maps Integration**: Interactive maps with real route rendering
- **Local Storage**: Client-side result persistence

### API Endpoints

- `GET /` - Main application page
- `POST /api/save-key` - Save Google Maps API key
- `POST /api/calculate` - Calculate route distance and time
- `GET /api/get-cached-result` - Retrieve cached calculation

## 🎨 UI Features

- **Compact Layout**: Responsive design that adapts to different screen sizes
- **Modern Design**: Glass-morphism effects with gradient backgrounds
- **Smooth Animations**: CSS transitions and keyframe animations
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages

## ⚠️ Important Notes

### Security
- API key stored temporarily in server session
- API key never written to logs or output
- Password input type for API key entry

### Caching
- Results cached in server session
- Client-side persistence with localStorage
- Input validation before API calls

### Error Handling
- Comprehensive validation for all inputs
- Informative error messages for API failures
- Network error handling with retry suggestions

## 🗪️ Project Structure

```
orutego/
├── .gitignore             # Git ignore file
├── LICENSE                # MIT License
├── README.md              # This file
├── CHANGELOG.md           # Version history and changes
├── DEMO.md                # Testing guide with examples
├── DEPLOYMENT.md          # Production deployment guide
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── test_decimal_conversion.py  # Test suite for decimal hours
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── styles.css        # CSS styling and animations
    └── script.js         # JavaScript application logic
```

## 🚦 Getting Your Google Maps API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable these APIs:
   - Geocoding API
   - Distance Matrix API  
   - Directions API
   - **Maps JavaScript API**
4. Create credentials (API Key)
5. Restrict your API key (recommended for production)
   - For HTTP referrers: Add your domain (e.g., `localhost:5000/*` for development)
   - For API restrictions: Select the 4 APIs listed above

## 🌐 Browser Compatibility

- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+

## 📝 License

This project is open source. Feel free to use and modify as needed.

## 🤝 Contributing

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Made with ❤️ by rusli3
