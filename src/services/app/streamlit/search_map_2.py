# pip install streamlit-keyup folium streamlit-folium

import requests
import streamlit as st
from st_keyup import st_keyup
import folium
from streamlit_folium import st_folium
import json
import os

# --- Config ---
API_KEY = "AIzaSyAIwC0O2xEpCFMv5eTc34LBfsjkP3BWFV8"
AUTOCOMPLETE_URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

# --- טעינת קובץ GeoJSON ---
GEOJSON_PATH = "cities_colored.geojson"  # שנה לנתיב של הקובץ שלך


def load_geojson():
    """טוען קובץ GeoJSON אם קיים"""
    if os.path.exists(GEOJSON_PATH):
        with open(GEOJSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


# --- Session state ---
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []
if "selected" not in st.session_state:
    st.session_state.selected = None
if "location" not in st.session_state:
    st.session_state.location = None
if "last_query" not in st.session_state:
    st.session_state.last_query = ""


def fetch_suggestions(query):
    params = {
        "input": query,
        "types": "address",
        "components": "country:il",
        "language": "he",
        "key": API_KEY
    }
    try:
        response = requests.get(AUTOCOMPLETE_URL, params=params, timeout=3)
        data = response.json()
        if data.get("status") == "OK":
            return [p["description"] for p in data["predictions"]]
    except:
        pass
    return []


def get_coordinates(address):
    params = {
        "address": address,
        "components": "country:il",
        "key": API_KEY
    }
    try:
        response = requests.get(GEOCODE_URL, params=params, timeout=3)
        data = response.json()
        if data.get("status") == "OK" and data.get("results"):
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    except:
        pass
    return None, None


# --- UI ---
st.markdown(
    "<h1 style='text-align: center; color: #0b5394;'>בדיקת זכאות להנחת נסיעה ברב־קו</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align: center; color: #333;'>הזינו את כתובת המגורים ובדקו באופן מיידי האם אזורכם מוגדר כזכאי להנחה בתחבורה הציבורית</h3>",
    unsafe_allow_html=True
)

# חיפוש
query = st_keyup("", placeholder="הקלד כתובת...")

# איפוס אוטומטי כשמתחילים חיפוש חדש
if query != st.session_state.last_query:
    st.session_state.last_query = query
    st.session_state.selected = None
    st.session_state.location = None
    st.session_state.suggestions = []

# הצעות
if query and len(query) >= 2 and not st.session_state.selected:
    st.session_state.suggestions = fetch_suggestions(query)

if st.session_state.suggestions and not st.session_state.selected:
    for suggestion in st.session_state.suggestions[:5]:
        if st.button(suggestion, key=suggestion):
            st.session_state.selected = suggestion
            lat, lng = get_coordinates(suggestion)
            if lat and lng:
                st.session_state.location = {"lat": lat, "lng": lng, "address": suggestion}
            st.rerun()

# יצירת מפה
m = folium.Map(
    location=[31.7683, 35.2137],  # מרכז ישראל
    zoom_start=8 if not st.session_state.location else 16,
    tiles="OpenStreetMap"
)

# טעינת GeoJSON לרקע המפה
geojson_data = load_geojson()
if geojson_data:
    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            "fillColor": feature["properties"]["fill"],  # משתמש בערך שהגדרת
            "color": feature["properties"]["stroke"],
            "weight": feature["properties"]["stroke-width"],
            "fillOpacity": feature["properties"]["fill-opacity"]
        }
    ).add_to(m)

# הוספת סמן אם נבחרה כתובת
if st.session_state.location:
    folium.Marker(
        location=[st.session_state.location["lat"], st.session_state.location["lng"]],
        popup=st.session_state.location["address"],
        tooltip=st.session_state.location["address"],
        icon=folium.Icon(color="red", icon="home", prefix="fa")
    ).add_to(m)

    # מרכוז המפה על הנקודה
    m.location = [st.session_state.location["lat"], st.session_state.location["lng"]]

    # הצגת הכתובת שנבחרה
    st.success(f"📍 {st.session_state.selected}")

# הצגת המפה
st_folium(m, height=500, width=None, returned_objects=[])