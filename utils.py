"""
Utility functions for Google Maps Platform API interactions
Used by the orutego application for geocoding, distance calculation, and routing
"""

import requests
import streamlit as st
import polyline
from typing import Dict, List, Tuple, Optional, Any


@st.cache_data(ttl=3600)  # Cache for 1 hour
def geocode(address: str, api_key: str) -> Optional[Dict]:
    """
    Geocode an address to get coordinates using Google Geocoding API
    
    Args:
        address: The address to geocode
        api_key: Google Maps API key
        
    Returns:
        Dictionary with lat, lng, and formatted_address or None if failed
    """
    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data["status"] == "OK" and data["results"]:
            result = data["results"][0]
            location = result["geometry"]["location"]
            return {
                "lat": location["lat"],
                "lng": location["lng"],
                "formatted_address": result["formatted_address"]
            }
        elif data["status"] == "ZERO_RESULTS":
            return None
        elif data["status"] == "REQUEST_DENIED":
            st.error("🔑 Invalid API Key or no permission for Geocoding API")
            return None
        else:
            st.error(f"❌ Geocoding error: {data.get('status', 'Unknown error')}")
            return None
            
    except requests.RequestException as e:
        st.error("🌐 Connection error occurred. Please try again.")
        return None
    except Exception as e:
        st.error("❌ Server error occurred. Please try again.")
        return None


@st.cache_data(ttl=3600)  # Cache for 1 hour
def distance_matrix(origin_coords: Tuple[float, float], 
                   dest_coords: Tuple[float, float], 
                   mode: str, 
                   api_key: str) -> Optional[Dict]:
    """
    Calculate distance and duration using Google Distance Matrix API
    
    Args:
        origin_coords: (lat, lng) tuple for origin
        dest_coords: (lat, lng) tuple for destination
        mode: Travel mode (driving, walking, bicycling, transit)
        api_key: Google Maps API key
        
    Returns:
        Dictionary with distance and duration info or None if failed
    """
    try:
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": f"{origin_coords[0]},{origin_coords[1]}",
            "destinations": f"{dest_coords[0]},{dest_coords[1]}",
            "mode": mode,
            "units": "metric",
            "key": api_key
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        if data["status"] == "OK":
            element = data["rows"][0]["elements"][0]
            
            if element["status"] == "OK":
                return {
                    "distance_text": element["distance"]["text"],
                    "distance_value": element["distance"]["value"],  # in meters
                    "duration_text": element["duration"]["text"],
                    "duration_value": element["duration"]["value"]  # in seconds
                }
            elif element["status"] == "ZERO_RESULTS":
                st.warning("⚠️ Sorry, no route found between these two locations.")
                return None
            else:
                st.error(f"❌ Error calculating route: {element['status']}")
                return None
        elif data["status"] == "REQUEST_DENIED":
            st.error("🔑 Invalid API Key or no permission for Distance Matrix API")
            return None
        else:
            st.error(f"❌ Error: {data.get('status', 'Unknown error')}")
            return None
            
    except requests.RequestException as e:
        st.error("🌐 Connection error occurred. Please try again.")
        return None
    except Exception as e:
        st.error("❌ Server error occurred. Please try again.")
        return None


@st.cache_data(ttl=3600)  # Cache for 1 hour
def directions_polyline(origin_coords: Tuple[float, float], 
                       dest_coords: Tuple[float, float], 
                       mode: str, 
                       api_key: str) -> Optional[Dict]:
    """
    Get directions polyline and route information using Google Directions API
    
    Args:
        origin_coords: (lat, lng) tuple for origin
        dest_coords: (lat, lng) tuple for destination
        mode: Travel mode (driving, walking, bicycling, transit)
        api_key: Google Maps API key
        
    Returns:
        Dictionary with polyline points and route info or None if failed
    """
    try:
        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": f"{origin_coords[0]},{origin_coords[1]}",
            "destination": f"{dest_coords[0]},{dest_coords[1]}",
            "mode": mode,
            "alternatives": "true",  # Get alternative routes
            "key": api_key
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        if data["status"] == "OK" and data["routes"]:
            routes = []
            for i, route in enumerate(data["routes"]):
                # Decode the polyline
                encoded_polyline = route["overview_polyline"]["points"]
                decoded_points = polyline.decode(encoded_polyline)
                
                route_info = {
                    "polyline_points": decoded_points,
                    "bounds": route["bounds"],
                    "is_primary": i == 0  # First route is primary
                }
                routes.append(route_info)
            
            return {"routes": routes}
        elif data["status"] == "ZERO_RESULTS":
            st.warning("⚠️ Sorry, no route found between these two locations.")
            return None
        elif data["status"] == "REQUEST_DENIED":
            st.error("🔑 Invalid API Key or no permission for Directions API")
            return None
        else:
            st.error(f"❌ Error getting directions: {data.get('status', 'Unknown error')}")
            return None
            
    except requests.RequestException as e:
        st.error("🌐 Connection error occurred. Please try again.")
        return None
    except Exception as e:
        st.error("❌ Server error occurred. Please try again.")
        return None


def seconds_to_hhmm(seconds: int) -> str:
    """
    Convert seconds to HH:MM format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Time string in HH:MM format
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"


def seconds_to_decimal_hours(seconds: int) -> str:
    """
    Convert seconds to decimal hours format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Decimal hours string with 2 decimal places using dot separator
    """
    decimal_hours = seconds / 3600
    return f"{decimal_hours:.2f}"


def make_copy_payload(lat_origin: float, lng_origin: float,
                     lat_dest: float, lng_dest: float,
                     distance_km: float, time_hhmm: str, 
                     time_decimal: str) -> str:
    """
    Create the copy payload string in the specified format
    
    Args:
        lat_origin: Origin latitude
        lng_origin: Origin longitude
        lat_dest: Destination latitude
        lng_dest: Destination longitude
        distance_km: Distance in kilometers
        time_hhmm: Time in HH:MM format
        time_decimal: Time in decimal hours format
        
    Returns:
        Comma-separated string ready for copying
    """
    return f"{lat_origin},{lng_origin},{lat_dest},{lng_dest},{distance_km:.2f},{time_hhmm},{time_decimal}"


def get_places_autocomplete_suggestions(input_text: str, api_key: str, 
                                      session_token: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Get autocomplete suggestions from Google Places API
    
    Args:
        input_text: The input text to get suggestions for
        api_key: Google Maps API key
        session_token: Optional session token for billing optimization
        
    Returns:
        List of dictionaries with place_id, description, and main_text
    """
    if not input_text or len(input_text) < 3:
        return []
    
    try:
        url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        params = {
            "input": input_text,
            "key": api_key,
            "types": "address"
        }
        
        if session_token:
            params["sessiontoken"] = session_token
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data["status"] == "OK":
            suggestions = []
            for prediction in data.get("predictions", []):
                suggestions.append({
                    "place_id": prediction["place_id"],
                    "description": prediction["description"],
                    "main_text": prediction["structured_formatting"]["main_text"]
                })
            return suggestions
        else:
            return []
            
    except Exception as e:
        return []


def validate_api_key(api_key: str) -> bool:
    """
    Validate the Google Maps API key by making a simple geocoding request
    
    Args:
        api_key: The API key to validate
        
    Returns:
        True if API key is valid, False otherwise
    """
    try:
        # Test with a simple geocoding request
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": "Google",
            "key": api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        return data["status"] != "REQUEST_DENIED"
        
    except Exception:
        return False