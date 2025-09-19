# 🧭 orutego

**orutego** is a modern web application for calculating travel distance (km) and travel time (Hours-Minutes & Decimal Hours) between origin and destination addresses using Google Maps Platform.

## ✨ Key Features

- **📍 Address Input**: Form inputs with auto-complete for origin and destination addresses
- **🔄 Address Swap**: Button to swap origin and destination addresses
- **🚗 Travel Modes**: Options for driving, walking, cycling, and transit
- **📊 Calculation Results**: Coordinates, distance (km), and travel time (HH:MM & decimal)
- **🗺️ Interactive Map**: Route visualization with markers and polylines
- **💾 Session Management**: API key storage and result caching

## 🚀 Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd orutego
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Google Maps API Key
1. Open [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing project
3. Enable the following APIs:
   - Geocoding API
   - Distance Matrix API
   - Directions API
   - Places API
4. Create an API key in the Credentials section
5. (Optional) Copy `.env.example` to `.env` and add your API key

### 4. Run Application
```bash
streamlit run app.py
```

The application will run at `http://localhost:8501`

## 📱 How to Use

1. **Input API Key**: Enter your Google Maps API Key and click "Save API Key"
2. **Enter Addresses**: Input origin and destination addresses (with autocomplete feature)
3. **Select Mode**: Choose travel mode (driving/walking/cycling/transit)
4. **Calculate**: Click "Calculate" button
5. **View Results**: Coordinates, distance, and time will be displayed
6. **View Map**: Interactive map with route will appear below

## 📊 Data Output Format

The coordinate data is displayed in comma-separated format:
```
lat_origin,lng_origin,lat_destination,lng_destination,distance_km,HH:MM,decimal_hours
```

Example:
```
-0.026700,109.342100,-0.114200,109.406500,12.84,01:30,1.50
```

## 🎨 Single-Screen Design

The application features a **no-scroll, single-screen experience** with:
- **Compact Layout**: All controls fit within viewport height
- **Responsive Design**: Adapts to different screen sizes
- **Efficient Space Usage**: Form and results displayed side-by-side
- **Interactive Map**: Compact map below the main interface
- **Modern UI**: Clean, professional appearance with turquoise/teal theme

## 🔧 Project Structure

```
orutego/
├── app.py              # Main Streamlit application
├── utils.py            # Google Maps API utilities
├── style.css           # Custom CSS styling
├── requirements.txt    # Python dependencies
├── .env.example        # Environment setup guide
└── README.md          # Documentation
```

## 🛠️ Dependencies

- `streamlit` - Web framework
- `requests` - HTTP requests for API calls
- `python-dotenv` - Environment variable management
- `folium` - Interactive maps
- `streamlit-folium` - Folium integration for Streamlit
- `polyline` - Polyline decoding for routes

## 🎨 Styling & Theme

The application uses a modern theme with primary colors:
- **Primary**: Turquoise/Teal (#06B6D4)
- **Secondary**: Slate (#0F172A)  
- **Light**: Light gray for backgrounds

Custom CSS is stored in `style.css` and injected into the application.

## ⚠️ Important Notes

- **API Quota**: Use API key wisely to avoid excessive charges
- **Caching**: Application uses `st.cache_data` to save API quota
- **Validation**: All inputs are validated before API calls
- **Error Handling**: Informative error messages for all possible issues

## 🔒 Security

- API key stored temporarily in `st.session_state`
- API key never written to logs or output
- Password input type for API key entry

## 📞 Support

If you encounter issues:
1. Ensure API key is valid and all APIs are enabled
2. Check internet connection
3. Verify entered addresses are valid
4. Check browser console for error messages

---

**Powered by Google Maps Platform APIs**
Made with ❤️ by rusli3
