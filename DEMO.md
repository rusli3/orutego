# 🧭 orutego - Demo & Testing Guide

## 🚀 Quick Demo

After the application is running at `http://localhost:5000`, follow these steps:

### 1. Setup API Key
1. Enter your Google Maps API Key in the "Google Maps API Key" field
2. Click the "Save" button - it will turn green and display "Saved"
3. Google Maps will automatically load in the background

### 2. Test Route Calculations
Try these sample addresses for testing:

#### Example 1: Local Route (Indonesia)
- **Origin**: `Jl. Gajah Mada No.1, Pontianak, West Kalimantan`
- **Destination**: `Jl. Ahmad Yani, Pontianak, West Kalimantan`
- **Travel Mode**: Driving
- **Expected**: Distance ~2-3 km, time ~5-10 minutes

#### Example 2: Intercity Route
- **Origin**: `Central Jakarta, DKI Jakarta`
- **Destination**: `Bandung, West Java`
- **Travel Mode**: Driving
- **Expected**: Distance ~150 km, time ~3-4 hours

#### Example 3: International Route
- **Origin**: `Kuala Lumpur, Malaysia`
- **Destination**: `Singapore`
- **Travel Mode**: Driving
- **Expected**: Distance ~350 km, time ~4-5 hours

### 3. Features to Test

#### ✅ Address Input & Validation
- Try leaving one field empty → error message will appear
- Enter invalid addresses → proper error handling is displayed

#### ✅ Address Swap
- Fill in origin and destination
- Click the arrow button ↕️ in the center
- Addresses will swap positions with animation

#### ✅ Travel Mode Selection
- Try all modes: Driving, Walking, Cycling, Transit
- Notice the changes in calculation results

#### ✅ Interactive Google Maps
- **Zoom & Pan**: Use mouse wheel and drag
- **Markers**: Click marker A (origin) and B (destination) for info
- **Route**: Displays actual route from Google Maps
- **Auto-fit**: Map automatically adjusts to show entire route

#### ✅ Results Display
- **Distance**: In kilometers
- **Time**: Format HH:MM and decimal hours
- **Coordinates**: CSV format data with 6 decimal precision
- **Copy to Clipboard**: Click copy button (📋) to copy coordinate data

#### ✅ Copy to Clipboard Feature
- Click the green button with copy icon next to coordinate data
- Data will be copied to clipboard in CSV format
- Visual feedback: icon changes to ✓ with confirmation message
- Compatible with all modern browsers

## 🔧 Troubleshooting

### Google Maps not showing?
1. Ensure API key is saved properly
2. Check browser console (F12) for errors
3. Verify Maps JavaScript API is enabled
4. Check quota and billing in Google Cloud Console

### Calculation failed?
1. Ensure all 4 APIs are enabled:
   - Geocoding API
   - Distance Matrix API
   - Directions API
   - Maps JavaScript API
2. Check if API key has overly restrictive limitations

### Network Error?
1. Ensure stable internet connection
2. Check if firewall is blocking Google APIs
3. Restart the Flask application

## 🌟 Advanced Testing

### Test Multiple Calculations
1. Perform several calculations in succession
2. Notice caching - results are stored in session
3. Refresh browser - last data persists (localStorage)

### Test Responsive Design
1. Resize browser window
2. Test in mobile view (F12 → Device simulation)
3. All elements should remain accessible

### Test Error Handling
1. Disable internet connection → should show error message
2. Use incorrect API key → proper error handling
3. Input non-existent addresses → graceful failure

## 📱 Production Checklist

Before deploying to production:

- [ ] Change `app.secret_key` to a secure key
- [ ] Set `debug=False` in `app.run()`
- [ ] Restrict API key with proper domain
- [ ] Setup proper web server (nginx + gunicorn)
- [ ] Enable HTTPS
- [ ] Monitor API usage & costs
- [ ] Setup error logging
- [ ] Test with load testing tools

## 🎯 Expected Results Format

Output coordinate data should be in this format:
```
lat_origin,lng_origin,lat_destination,lng_destination,distance_km,HH:MM,decimal_hours
```

Example:
```
-0.026700,109.342100,-0.114200,109.406500,12.84,01:30,1.50
```

The application now uses **Google Maps JavaScript API** which provides:
- ✅ Real interactive maps
- ✅ Accurate routes based on actual road conditions
- ✅ Zoom, pan, and map navigation
- ✅ Info windows with coordinate details
- ✅ Custom markers with labels A and B
- ✅ Automatic bounds fitting to display entire route
