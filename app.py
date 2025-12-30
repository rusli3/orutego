from flask import Flask, render_template, request, jsonify, session
import requests
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'orutego_secret_key_2024'  # Change this in production

# Google Maps API endpoints
GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
DISTANCE_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'
DIRECTIONS_URL = 'https://maps.googleapis.com/maps/api/directions/json'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/save-key', methods=['POST'])
def save_api_key():
    """Save Google Maps API key to session"""
    try:
        data = request.get_json()
        api_key = data.get('apiKey', '').strip()
        
        if not api_key:
            return jsonify({'success': False, 'error': 'API key is required'})
        
        # Store in session
        session['google_maps_api_key'] = api_key
        session.permanent = True
        
        return jsonify({'success': True, 'message': 'API key saved successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/geocode', methods=['POST'])
def geocode_address():
    """Geocode an address to get coordinates"""
    try:
        data = request.get_json()
        address = data.get('address', '').strip()
        
        if not address:
            return jsonify({'success': False, 'error': 'Address is required'})
        
        api_key = session.get('google_maps_api_key')
        if not api_key:
            return jsonify({'success': False, 'error': 'API key not found. Please save your API key first.'})
        
        # Make request to Google Geocoding API
        params = {
            'address': address,
            'key': api_key
        }
        
        response = requests.get(GEOCODE_URL, params=params)
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            return jsonify({
                'success': True,
                'coordinates': [location['lat'], location['lng']],
                'formatted_address': data['results'][0]['formatted_address']
            })
        else:
            return jsonify({'success': False, 'error': f'Geocoding failed: {data.get("status", "Unknown error")}'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/mass-geocode', methods=['POST'])
def mass_geocode():
    """Geocode multiple addresses"""
    try:
        data = request.get_json()
        addresses = data.get('addresses', [])
        
        if not addresses:
            return jsonify({'success': False, 'error': 'No addresses provided'})
        
        api_key = session.get('google_maps_api_key')
        if not api_key:
            return jsonify({'success': False, 'error': 'API key not found. Please save your API key first.'})
            
        results = []
        
        for addr in addresses:
            if not addr or not addr.strip():
                continue
                
            clean_addr = addr.strip()
            
            # Make request to Google Geocoding API
            params = {
                'address': clean_addr,
                'key': api_key
            }
            
            try:
                response = requests.get(GEOCODE_URL, params=params)
                data = response.json()
                
                if data['status'] == 'OK' and data['results']:
                    location = data['results'][0]['geometry']['location']
                    results.append({
                        'input_address': clean_addr,
                        'success': True,
                        'lat': location['lat'],
                        'lng': location['lng'],
                        'formatted_address': data['results'][0]['formatted_address']
                    })
                else:
                    results.append({
                        'input_address': clean_addr,
                        'success': False,
                        'error': data.get("status", "Unknown error")
                    })
            except Exception as req_err:
                results.append({
                    'input_address': clean_addr,
                    'success': False,
                    'error': str(req_err)
                })
        
        return jsonify({'success': True, 'results': results})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/calculate', methods=['POST'])
def calculate_route():
    """Calculate distance and time between two addresses"""
    try:
        data = request.get_json()
        origin = data.get('origin', '').strip()
        destination = data.get('destination', '').strip()
        travel_mode = data.get('travelMode', 'driving').lower()
        
        if not origin or not destination:
            return jsonify({'success': False, 'error': 'Both origin and destination are required'})
        
        api_key = session.get('google_maps_api_key')
        if not api_key:
            return jsonify({'success': False, 'error': 'API key not found. Please save your API key first.'})
        
        # First geocode both addresses
        origin_coords = None
        dest_coords = None
        
        # Geocode origin
        geocode_params = {'address': origin, 'key': api_key}
        geocode_response = requests.get(GEOCODE_URL, params=geocode_params)
        geocode_data = geocode_response.json()
        
        if geocode_data['status'] == 'OK' and geocode_data['results']:
            origin_location = geocode_data['results'][0]['geometry']['location']
            origin_coords = [origin_location['lat'], origin_location['lng']]
        else:
            return jsonify({'success': False, 'error': 'Could not geocode origin address'})
        
        # Geocode destination
        geocode_params = {'address': destination, 'key': api_key}
        geocode_response = requests.get(GEOCODE_URL, params=geocode_params)
        geocode_data = geocode_response.json()
        
        if geocode_data['status'] == 'OK' and geocode_data['results']:
            dest_location = geocode_data['results'][0]['geometry']['location']
            dest_coords = [dest_location['lat'], dest_location['lng']]
        else:
            return jsonify({'success': False, 'error': 'Could not geocode destination address'})
        
        # Calculate distance and time using Distance Matrix API
        matrix_params = {
            'origins': origin,
            'destinations': destination,
            'mode': travel_mode,
            'units': 'metric',
            'key': api_key
        }
        
        matrix_response = requests.get(DISTANCE_MATRIX_URL, params=matrix_params)
        matrix_data = matrix_response.json()
        
        if matrix_data['status'] == 'OK' and matrix_data['rows']:
            element = matrix_data['rows'][0]['elements'][0]
            
            if element['status'] == 'OK':
                distance_km = element['distance']['value'] / 1000  # Convert meters to km
                duration_seconds = element['duration']['value']
                
                # Convert duration to HH:MM and decimal hours with better precision
                duration_minutes = duration_seconds / 60  # Use float division for precision
                hours = int(duration_minutes // 60)
                minutes = int(duration_minutes % 60)
                duration_formatted = f"{hours:02d}:{minutes:02d}"
                
                # Calculate decimal hours more precisely: hours + (minutes/60)
                decimal_hours = round(hours + (minutes / 60), 2)
                
                # Get route polyline for map display
                directions_params = {
                    'origin': origin,
                    'destination': destination,
                    'mode': travel_mode,
                    'key': api_key
                }
                
                directions_response = requests.get(DIRECTIONS_URL, params=directions_params)
                directions_data = directions_response.json()
                
                route_polyline = None
                if directions_data['status'] == 'OK' and directions_data['routes']:
                    route_polyline = directions_data['routes'][0]['overview_polyline']['points']
                
                result = {
                    'success': True,
                    'originCoords': origin_coords,
                    'destinationCoords': dest_coords,
                    'distance': round(distance_km, 2),
                    'duration': duration_formatted,
                    'decimalHours': decimal_hours,
                    'routePolyline': route_polyline,
                    'travelMode': travel_mode
                }
                
                # Cache result in session
                session['last_calculation'] = result
                
                return jsonify(result)
            else:
                return jsonify({'success': False, 'error': f'Route calculation failed: {element["status"]}'})
        else:
            return jsonify({'success': False, 'error': 'Distance Matrix API request failed'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get-cached-result')
def get_cached_result():
    """Get the last cached calculation result"""
    cached_result = session.get('last_calculation')
    if cached_result:
        return jsonify(cached_result)
    else:
        return jsonify({'success': False, 'error': 'No cached result found'})

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)