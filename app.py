"""
orutego - Modern Distance and Travel Time Calculator
A Streamlit web application for calculating distance and travel time between addresses
using Google Maps Platform APIs.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import uuid
from utils import (
    geocode, distance_matrix, directions_polyline,
    seconds_to_hhmm, seconds_to_decimal_hours, make_copy_payload,
    get_places_autocomplete_suggestions, validate_api_key
)


# Page configuration
st.set_page_config(
    page_title="orutego",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load and apply custom CSS
def load_css():
    """Load custom CSS styling"""
    try:
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ CSS file not found. Using default styling.")

load_css()

# Initialize session state
def initialize_session_state():
    """Initialize session state variables"""
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "origin_address" not in st.session_state:
        st.session_state.origin_address = ""
    if "dest_address" not in st.session_state:
        st.session_state.dest_address = ""
    if "travel_mode" not in st.session_state:
        st.session_state.travel_mode = "driving"
    if "calculation_done" not in st.session_state:
        st.session_state.calculation_done = False
    if "results" not in st.session_state:
        st.session_state.results = {}
    if "session_token" not in st.session_state:
        st.session_state.session_token = str(uuid.uuid4())

initialize_session_state()

# Single-screen layout container
with st.container():
    # Compact header
    st.markdown("""
    <div class="app-header">
        <h1>🧭 orutego</h1>
        <p>Modern Distance & Travel Time Calculator</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key and Results section - horizontal layout
    api_results_col1, api_results_col2 = st.columns([3, 2])
    
    # Left column - API Key section
    with api_results_col1:
        st.markdown("**🔑 API Key**")
        api_input_col1, api_input_col2 = st.columns([4, 1])
        
        with api_input_col1:
            api_key_input = st.text_input(
                "API Key",
                type="password",
                value=st.session_state.api_key,
                placeholder="Enter Google Maps API Key...",
                label_visibility="collapsed"
            )
        
        with api_input_col2:
            save_key = st.button("💾 Save Key", use_container_width=True)
    
    # Right column - Results section
    with api_results_col2:
        st.markdown("**📊 Results**")
        
        # Show current API key status
        if st.session_state.api_key:
            st.info("🔑 API Key is saved and ready")
        else:
            st.info("👆 Enter and save your API Key first")
    
    # API Key validation - always available
    if save_key:
        # Mark that save button was clicked
        st.session_state.save_clicked = True
    
    # Process save action if button was clicked
    if st.session_state.get('save_clicked', False):
        if api_key_input and api_key_input.strip():
            with st.spinner("🔍 Validating..."):
                if validate_api_key(api_key_input.strip()):
                    st.session_state.api_key = api_key_input.strip()
                    st.session_state.save_clicked = False  # Reset save state
                    st.rerun()  # Force immediate update
                else:
                    st.error("❌ Invalid API Key or missing permissions")
                    st.session_state.save_clicked = False  # Reset save state
        else:
            st.error("❌ Please enter an API Key")
            st.session_state.save_clicked = False  # Reset save state
    
    # Main content area - Address inputs and calculation
    st.markdown("---")
    main_col1, main_col2 = st.columns([3, 2])
    
    # Left column - Address inputs and travel mode
    with main_col1:
        
        # Address inputs in compact layout
        addr_col1, addr_col2, addr_col3 = st.columns([5, 1, 5])
        
        with addr_col1:
            st.markdown("**📍 Origin**")
            origin_address = st.text_input(
                "Origin Address",
                value=st.session_state.origin_address,
                placeholder="Enter origin address...",
                label_visibility="collapsed",
                key="origin_input"
            )
        
        with addr_col2:
            st.markdown("**🔄**")
            if st.button("🔄", help="Swap Addresses", use_container_width=True, key="swap_btn"):
                temp = st.session_state.origin_address
                st.session_state.origin_address = st.session_state.dest_address
                st.session_state.dest_address = temp
                st.rerun()
        
        with addr_col3:
            st.markdown("**🎯 Destination**")
            dest_address = st.text_input(
                "Destination Address", 
                value=st.session_state.dest_address,
                placeholder="Enter destination address...",
                label_visibility="collapsed",
                key="dest_input"
            )
        
        # Update session state
        if origin_address is not None:
            st.session_state.origin_address = origin_address
        if dest_address is not None:
            st.session_state.dest_address = dest_address
        
        # Travel mode selection
        mode_col1, mode_col2 = st.columns([3, 2])
        with mode_col1:
            st.markdown("**🚗 Travel Mode**")
            travel_mode = st.selectbox(
                "Travel Mode",
                options=["driving", "walking", "bicycling", "transit"],
                format_func=lambda x: {
                    "driving": "🚗 Driving",
                    "walking": "🚶 Walking", 
                    "bicycling": "🚴 Cycling",
                    "transit": "🚌 Transit"
                }[x],
                index=["driving", "walking", "bicycling", "transit"].index(st.session_state.travel_mode),
                label_visibility="collapsed"
            )
            st.session_state.travel_mode = travel_mode
        
        with mode_col2:
            st.markdown("**🧮 Action**")
            calculate = st.button("🧮 Calculate", use_container_width=True, type="primary")
    
    # Right column - Additional results and calculations
    with main_col2:
            
        # Calculation logic
        if calculate:
            if not st.session_state.api_key:
                st.error("❌ Save API Key first")
            elif not origin_address or not origin_address.strip():
                st.error("❌ Enter origin address")
            elif not dest_address or not dest_address.strip():
                st.error("❌ Enter destination address")
            else:
                with st.status("🔍 Processing...", expanded=False) as status:
                    try:
                        # Geocode addresses
                        origin_geo = geocode(origin_address, st.session_state.api_key)
                        if not origin_geo:
                            st.error("❌ Origin not found")
                            st.stop()
                        
                        dest_geo = geocode(dest_address, st.session_state.api_key)
                        if not dest_geo:
                            st.error("❌ Destination not found")
                            st.stop()
                        
                        # Calculate distance and time
                        distance_data = distance_matrix(
                            (origin_geo["lat"], origin_geo["lng"]),
                            (dest_geo["lat"], dest_geo["lng"]),
                            travel_mode,
                            st.session_state.api_key
                        )
                        
                        if not distance_data:
                            st.error("❌ Cannot calculate route")
                            st.stop()
                        
                        # Get directions
                        directions_data = directions_polyline(
                            (origin_geo["lat"], origin_geo["lng"]),
                            (dest_geo["lat"], dest_geo["lng"]),
                            travel_mode,
                            st.session_state.api_key
                        )
                        
                        # Store results
                        st.session_state.results = {
                            "origin_geo": origin_geo,
                            "dest_geo": dest_geo,
                            "distance_data": distance_data,
                            "directions_data": directions_data,
                            "travel_mode": travel_mode
                        }
                        st.session_state.calculation_done = True
                        status.update(label="✅ Complete!", state="complete")
                        
                    except Exception as e:
                        st.error("❌ Processing error. Try again.")
                        st.session_state.calculation_done = False
        
        # Display copy functionality if calculation is done
        if st.session_state.calculation_done and st.session_state.results:
            results = st.session_state.results
            origin_geo = results["origin_geo"]
            dest_geo = results["dest_geo"]
            distance_data = results["distance_data"]
            
            # Calculate values for display and copy payload
            distance_km = distance_data["distance_value"] / 1000
            duration_seconds = distance_data["duration_value"]
            time_hhmm = seconds_to_hhmm(duration_seconds)
            time_decimal = seconds_to_decimal_hours(duration_seconds)
            
            # Display compact horizontal metrics above copy data
            st.markdown("""
            <div style="margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; background: #f8fafc; padding: 0.4rem 0.6rem; border-radius: 4px; border: 1px solid #e2e8f0;">
                    <div style="text-align: center; flex: 1;">
                        <div style="font-size: 0.7rem; color: #64748b; font-weight: 500;">DISTANCE</div>
                        <div style="font-size: 0.85rem; font-weight: 600; color: #0f172a;">{:.2f} km</div>
                    </div>
                    <div style="text-align: center; flex: 1; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0;">
                        <div style="font-size: 0.7rem; color: #64748b; font-weight: 500;">TIME (H:M)</div>
                        <div style="font-size: 0.85rem; font-weight: 600; color: #0f172a;">{}</div>
                    </div>
                    <div style="text-align: center; flex: 1;">
                        <div style="font-size: 0.7rem; color: #64748b; font-weight: 500;">TIME (DECIMAL)</div>
                        <div style="font-size: 0.85rem; font-weight: 600; color: #0f172a;">{:.1f}h</div>
                    </div>
                </div>
            </div>
            """.format(distance_km, time_hhmm, float(time_decimal)), unsafe_allow_html=True)
            
            # Copy data
            copy_payload = make_copy_payload(
                origin_geo["lat"], origin_geo["lng"],
                dest_geo["lat"], dest_geo["lng"],
                distance_km, time_hhmm, time_decimal
            )
            
            st.code(copy_payload, language="text")

# Map section - full width below form
if st.session_state.calculation_done and st.session_state.results:
    st.markdown("**🗺️ Interactive Map**")
    
    results = st.session_state.results
    origin_geo = results["origin_geo"]
    dest_geo = results["dest_geo"]
    directions_data = results["directions_data"]
    
    # Create compact map
    center_lat = (origin_geo["lat"] + dest_geo["lat"]) / 2
    center_lng = (origin_geo["lng"] + dest_geo["lng"]) / 2
    
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=10,
        tiles="OpenStreetMap"
    )
    
    # Add markers
    folium.Marker(
        [origin_geo["lat"], origin_geo["lng"]],
        popup=f"🟢 Origin: {origin_geo['formatted_address']}",
        tooltip="Origin",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)
    
    folium.Marker(
        [dest_geo["lat"], dest_geo["lng"]],
        popup=f"🔴 Destination: {dest_geo['formatted_address']}",
        tooltip="Destination", 
        icon=folium.Icon(color="red", icon="stop")
    ).add_to(m)
    
    # Add route if available
    if directions_data and "routes" in directions_data:
        for i, route in enumerate(directions_data["routes"]):
            color = "#06B6D4" if route["is_primary"] else "#64748B"
            weight = 4 if route["is_primary"] else 2
            opacity = 0.8 if route["is_primary"] else 0.6
            
            folium.PolyLine(
                route["polyline_points"],
                color=color,
                weight=weight,
                opacity=opacity,
                popup=f"Route {'Primary' if route['is_primary'] else 'Alternative'}"
            ).add_to(m)
        
        # Fit map to route bounds
        try:
            bounds = directions_data["routes"][0]["bounds"]
            southwest = [bounds["southwest"]["lat"], bounds["southwest"]["lng"]]
            northeast = [bounds["northeast"]["lat"], bounds["northeast"]["lng"]]
            m.fit_bounds([southwest, northeast], padding=[10, 10])
        except:
            # Fallback: fit to markers
            m.fit_bounds([
                [origin_geo["lat"], origin_geo["lng"]],
                [dest_geo["lat"], dest_geo["lng"]]
            ], padding=[20, 20])
    else:
        # No directions, fit to markers
        m.fit_bounds([
            [origin_geo["lat"], origin_geo["lng"]],
            [dest_geo["lat"], dest_geo["lng"]]
        ], padding=[20, 20])
    
    # Display compact map
    st_folium(m, width=None, height=300)

# Footer
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.8rem; margin: 1rem 0; padding-top: 1rem; border-top: 1px solid #E2E8F0;">
    <p>🧭 <strong>orutego</strong> - Modern Distance & Travel Time Calculator | Powered by Google Maps Platform</p>
</div>
""", unsafe_allow_html=True)