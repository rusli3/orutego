# 📖 orutego — Full Documentation

> **Version**: 1.1.0 | **Updated**: 2026-02-10 | **Author**: rusli3

orutego is a modern web application for calculating travel distance (km) and travel time (Hours-Minutes & Decimal Hours) between addresses using Google Maps Platform. It supports both single route calculation with interactive map visualization and bulk route calculation from multiple origins to a single destination.

---

## Table of Contents

1. [Architecture Overview](#-architecture-overview)
2. [Technology Stack](#-technology-stack)
3. [Installation & Setup](#-installation--setup)
4. [Google Maps API Configuration](#-google-maps-api-configuration)
5. [Application Features](#-application-features)
6. [API Reference](#-api-reference)
7. [Frontend Architecture](#-frontend-architecture)
8. [Utility Functions](#-utility-functions)
9. [Data Formats](#-data-formats)
10. [File Structure](#-file-structure)
11. [Security Considerations](#-security-considerations)
12. [Troubleshooting](#-troubleshooting)

---

## 🏗 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Browser (Client)                     │
│  ┌─────────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   index.html    │  │  script.js   │  │ styles.css │ │
│  │   (Template)    │  │ (OrutegoApp) │  │  (Styling) │ │
│  └────────┬────────┘  └──────┬───────┘  └────────────┘ │
│           │                  │                           │
│           │    fetch() API calls                         │
└───────────┼──────────────────┼───────────────────────────┘
            │                  │
            ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│                   Flask Server (app.py)                   │
│                                                          │
│  Routes:                                                 │
│  ├── GET  /                    → Render index.html       │
│  ├── POST /api/save-key        → Store API key           │
│  ├── POST /api/geocode         → Geocode address         │
│  ├── POST /api/calculate       → Single route calc       │
│  ├── POST /api/mass-route      → Bulk route calc         │
│  └── GET  /api/get-cached-result → Cached result         │
│                                                          │
│  Session: API key, cached results                        │
└──────────────────────────┬──────────────────────────────┘
                           │
                           │  HTTP requests
                           ▼
┌─────────────────────────────────────────────────────────┐
│              Google Maps Platform APIs                   │
│  ├── Geocoding API                                       │
│  ├── Distance Matrix API                                 │
│  ├── Directions API                                      │
│  └── Maps JavaScript API (client-side)                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠 Technology Stack

### Backend
| Component | Technology | Version |
|-----------|-----------|---------|
| Web Framework | Flask | 2.3.3 |
| HTTP Client | requests | 2.31.0 |
| Env Management | python-dotenv | 1.0.0 |
| Language | Python | 3.7+ |

### Frontend
| Component | Technology |
|-----------|-----------|
| Structure | HTML5 |
| Logic | Vanilla JavaScript (ES6+) |
| Styling | Custom CSS3 |
| Maps | Google Maps JavaScript API |
| Icons | Font Awesome 6 |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- A Google Maps Platform API key

### Step-by-Step

```bash
# 1. Clone the repository
git clone https://github.com/rusli3/orutego.git
cd orutego

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py
```

The application will start on `http://localhost:5000`.

### Dependencies (`requirements.txt`)
```
Flask==2.3.3
requests==2.31.0
python-dotenv==1.0.0
```

---

## 🔑 Google Maps API Configuration

### Required APIs
You must enable **all 4 APIs** in Google Cloud Console:

| API | Purpose |
|-----|---------|
| **Geocoding API** | Convert address text → latitude/longitude coordinates |
| **Distance Matrix API** | Calculate distance (km) and travel time between coordinates |
| **Directions API** | Get route polyline for map visualization |
| **Maps JavaScript API** | Render interactive map with markers and routes (client-side) |

### How to Get Your API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Navigate to **APIs & Services** → **Library**
4. Enable the 4 APIs listed above
5. Go to **APIs & Services** → **Credentials**
6. Click **Create Credentials** → **API Key**
7. (Recommended) Restrict the key:
   - **Application restrictions**: HTTP referrers → `localhost:5000/*` (dev) or your domain (prod)
   - **API restrictions**: Select the 4 APIs above

### Using the API Key
Enter your API key directly in the application's UI (sidebar → "API Key" section → paste → click "Save API Key"). The key is stored in the Flask server session (not persisted to disk).

---

## ✨ Application Features

### Feature 1: Single Route Calculation

Calculate distance and travel time between one origin and one destination.

**How to use:**
1. Save your API key
2. Enter **Origin** address
3. Enter **Destination** address
4. Select **Travel Mode** (Driving / Walking / Cycling / Transit)
5. Click **Calculate Route**

**Results displayed:**
- Origin coordinates (lat, lng)
- Destination coordinates (lat, lng)
- Distance in kilometers
- Travel time in HH:MM format
- Travel time in decimal hours
- Interactive Google Map with route polyline and markers

**Additional features:**
- 🔄 **Swap addresses** button to reverse origin/destination
- 🗺️ **Expand view** to enlarge the map
- 📋 **Copy to clipboard** in CSV format
- 💾 **Result caching** in session and localStorage

---

### Feature 2: Mass Route Calculation

Calculate distance and travel time from **multiple origin addresses** to a **single destination**.

**How to use:**
1. Click the **"Mass Route"** tab
2. Enter the **Destination** address
3. Enter **Origin addresses** (one per line) in the textarea
4. Select **Travel Mode**
5. Click **"Calculate Routes"**

**Results displayed (per origin):**

| Column | Description |
|--------|-------------|
| Lat Origin | Latitude of origin |
| Lng Origin | Longitude of origin |
| Lat Dest | Latitude of destination |
| Lng Dest | Longitude of destination |
| Distance | Distance in km |
| Duration | Travel time (HH:MM) |
| Decimal | Decimal hours |
| Status | OK or error message |

**Export:** Click **"Copy All (CSV)"** to copy results to clipboard.

---

## 📡 API Reference

### `GET /`
Renders the main application page.

---

### `POST /api/save-key`
Saves the Google Maps API key to the server session.

**Request:**
```json
{
  "apiKey": "AIzaSy..."
}
```

**Response (success):**
```json
{
  "success": true,
  "message": "API key saved successfully"
}
```

---

### `POST /api/geocode`
Geocodes a single address to coordinates.

**Request:**
```json
{
  "address": "Jalan Ahmad Yani, Pontianak"
}
```

**Response:**
```json
{
  "success": true,
  "lat": -0.0267,
  "lng": 109.3421,
  "formatted_address": "Jl. Jenderal Ahmad Yani, Pontianak"
}
```

---

### `POST /api/calculate`
Calculates the route between two addresses (geocoding + distance matrix + directions).

**Request:**
```json
{
  "origin": "Jalan Ahmad Yani, Pontianak",
  "destination": "Bandara Supadio, Pontianak",
  "travelMode": "driving"
}
```

**Response:**
```json
{
  "success": true,
  "origin": {
    "lat": -0.0267,
    "lng": 109.3421,
    "formatted_address": "Jl. Jenderal Ahmad Yani, Pontianak"
  },
  "destination": {
    "lat": -0.1142,
    "lng": 109.4065,
    "formatted_address": "Bandara Internasional Supadio"
  },
  "distance": "12.84 km",
  "distance_value": 12840,
  "duration": "01:30",
  "duration_value": 5400,
  "decimal_hours": "1.50",
  "polyline": "encoded_polyline_string",
  "travel_mode": "driving"
}
```

---

### `POST /api/mass-route`
Calculates routes from multiple origins to a single destination.

**Request:**
```json
{
  "origins": [
    "Jalan Ahmad Yani, Pontianak",
    "Jalan Gajah Mada, Pontianak",
    "Siantan, Pontianak"
  ],
  "destination": "Bandara Supadio, Pontianak",
  "travelMode": "driving"
}
```

**Response:**
```json
{
  "success": true,
  "destinationCoords": [-0.1142, 109.4065],
  "results": [
    {
      "input_address": "Jalan Ahmad Yani, Pontianak",
      "success": true,
      "originCoords": [-0.0267, 109.3421],
      "destinationCoords": [-0.1142, 109.4065],
      "distance": 12.84,
      "duration": "01:30",
      "decimalHours": 1.50
    },
    {
      "input_address": "Invalid Address",
      "success": false,
      "error": "ZERO_RESULTS"
    }
  ]
}
```

**Travel Modes:** `driving`, `walking`, `bicycling`, `transit`

---

### `GET /api/get-cached-result`
Returns the last cached calculation result from the session.

**Response:**
```json
{
  "success": true,
  "result": { ... }
}
```

---

## 🖥 Frontend Architecture

### OrutegoApp Class (`script.js`)

The entire frontend is managed by a single `OrutegoApp` class, initialized on `DOMContentLoaded`.

#### State Properties
```javascript
this.selectedMode     // Travel mode for single route ('driving')
this.massTravelMode   // Travel mode for mass route ('driving')
this.isApiKeySaved    // Whether API key has been saved
this.lastResult       // Last calculation result (for copy/cache)
this.googleMap        // Google Maps instance
this.directionsService   // Google Directions service
this.directionsRenderer  // Google Directions renderer
this.pendingMapData      // Queued map data while Maps is loading
this.apiKey              // Current API key
```

#### Core Methods

| Method | Description |
|--------|-------------|
| `init()` | Initialize app, bind events, check API key |
| `bindEvents()` | Attach all DOM event listeners |
| `saveApiKey()` | Save API key to server and load Maps JS API |
| `loadGoogleMapsAPI()` | Dynamically load Google Maps JavaScript API |
| `initializeGoogleMaps()` | Initialize map, directions service/renderer |

#### Single Route Methods

| Method | Description |
|--------|-------------|
| `calculateRoute()` | POST to `/api/calculate`, display results |
| `displayResults(data)` | Render coordinates, distance, time in UI |
| `drawGoogleMap(data)` | Render route on Google Map with polyline |
| `addCustomMarkers(origin, dest, data)` | Add origin/destination markers |
| `expandView()` | Expand map to full width |
| `closeExpandedView()` | Restore normal layout |
| `copyToClipboard()` | Copy single result as CSV string |
| `swapAddresses()` | Swap origin ↔ destination inputs |
| `selectTravelMode(btn)` | Set travel mode for single route |
| `validateDecimalHours(duration, backend)` | Cross-check decimal hours |

#### Mass Route Methods

| Method | Description |
|--------|-------------|
| `selectMassTravelMode(btn)` | Set travel mode for mass route |
| `processMassRoute()` | POST to `/api/mass-route`, display results |
| `displayMassResults(results)` | Render results table rows |
| `copyMassResults()` | Copy all results as CSV with headers |
| `updateAddressCount()` | Update "X addresses" counter |

#### UI Utility Methods

| Method | Description |
|--------|-------------|
| `switchTab(tab)` | Switch between Route / Mass Route tabs |
| `showLoading(show)` | Show/hide loading overlay |
| `showError(message)` | Display error message |
| `clearError()` | Hide error message |
| `showStatus(element, message, type)` | Show status badge |
| `showCopyStatus(message, type)` | Show copy confirmation |

#### Standalone Function

| Function | Description |
|----------|-------------|
| `decodePolyline(str, precision)` | Decode Google polyline to lat/lng array |

---

## 🔧 Utility Functions (`utils.py`)

A library of helper functions for Google Maps API interactions. These are standalone utility functions that can be imported separately.

| Function | Description |
|----------|-------------|
| `geocode(address, api_key)` | Geocode address → `{lat, lng, formatted_address}` |
| `distance_matrix(origin, dest, mode, api_key)` | Calculate distance & duration |
| `directions_polyline(origin, dest, mode, api_key)` | Get route polyline data |
| `seconds_to_hhmm(seconds)` | Convert seconds → `"HH:MM"` string |
| `seconds_to_decimal_hours(seconds)` | Convert seconds → `"1.50"` decimal string |
| `make_copy_payload(...)` | Create CSV copy string from results |
| `get_places_autocomplete_suggestions(text, api_key)` | Places API autocomplete |
| `validate_api_key(api_key)` | Validate API key with test geocode call |

---

## 📊 Data Formats

### Single Route — Copy Format
Raw CSV **without headers**, comma-separated:
```
lat_origin,lng_origin,lat_destination,lng_destination,distance_km,HH:MM,decimal_hours
```

**Example:**
```
-0.026700,109.342100,-0.114200,109.406500,12.84,01:30,1.50
```

### Mass Route — CSV Export Format
CSV **with headers**:
```csv
Lat_Origin,Lng_Origin,Lat_Destination,Lng_Destination,Distance_km,Duration_HHMM,Decimal_Hours,Status
-0.032100,109.345600,-0.114200,109.406500,12.84,01:30,1.50,OK
```

### Decimal Hours Conversion
Travel time is provided in two formats:

| Format | Example | Description |
|--------|---------|-------------|
| HH:MM | `01:30` | Standard hours:minutes |
| Decimal | `1.50` | Hours as decimal (1h 30m = 1 + 30/60 = 1.50) |

**Formula:** `decimal_hours = hours + (minutes / 60)`

---

## 📁 File Structure

```
orutego/
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
├── LICENSE                    # MIT License
├── README.md                  # Quick-start guide
├── DOCUMENTATION.md           # This file — full documentation
├── CHANGELOG.md               # Version history
├── DEPLOYMENT.md              # Production deployment guide
├── app.py                     # Flask backend (routes + API handlers)
├── utils.py                   # Utility functions for Google Maps API
├── requirements.txt           # Python dependencies
├── style.css                  # Legacy CSS file
├── test_decimal_conversion.py # Test suite for decimal hours
├── templates/
│   └── index.html             # Main HTML template (Jinja2)
└── static/
    ├── styles.css             # CSS styling and animations
    └── script.js              # JavaScript application logic (OrutegoApp)
```

### File Descriptions

| File | Lines | Purpose |
|------|-------|---------|
| `app.py` | ~314 | Flask server with 6 routes, session management, Google API calls |
| `utils.py` | ~312 | Standalone utility functions (geocoding, distance, polyline, etc.) |
| `script.js` | ~854 | Frontend logic — OrutegoApp class with 30+ methods |
| `styles.css` | ~984 | Full CSS with responsive design, animations, glassmorphism |
| `index.html` | ~280 | HTML template with both Single Route and Mass Route UI |

---

## 🔒 Security Considerations

| Concern | Implementation |
|---------|----------------|
| API Key Storage | Stored in Flask session (server-side memory), not on disk |
| API Key Input | Uses `type="password"` input with toggle visibility |
| API Key Transmission | Sent via POST body, never in URL query params |
| Session Secret | `app.secret_key` — **must be changed for production** |
| Error Messages | Sanitized — no stack traces exposed to client |
| CORS | Not configured — single-origin by default |

### Production Recommendations
- Set `debug=False`
- Use environment variable for `SECRET_KEY`
- Enable HTTPS/SSL
- Restrict API key to specific HTTP referrers
- Set API quotas in Google Cloud Console

---

## 🔍 Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "API key not found" | Key not saved in session | Click "Save API Key" again |
| "ZERO_RESULTS" | Address not recognized by Google | Try a more specific address |
| "REQUEST_DENIED" | API key invalid or API not enabled | Check Google Cloud Console |
| "OVER_QUERY_LIMIT" | Too many API requests | Wait or check billing |
| Map not showing | Maps JavaScript API not enabled | Enable it in Cloud Console |
| "Network error" | Server not running or connection issue | Run `python app.py` and check `localhost:5000` |

### Testing Decimal Conversion
Run the built-in test suite:
```bash
python test_decimal_conversion.py
```

This verifies that HH:MM → Decimal Hours conversion works correctly (e.g., `01:30` → `1.50`).

---

## 📝 Version History

See [CHANGELOG.md](CHANGELOG.md) for full version history.

| Version | Date | Highlights |
|---------|------|------------|
| 1.1.0 | 2026-02-10 | Mass Route feature (multi-origin → single destination) |
| 1.0.0 | 2025-09-24 | Initial release with single route + mass geocode |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

Made with ❤️ by rusli3
