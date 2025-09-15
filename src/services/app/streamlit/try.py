import folium
from streamlit_folium import st_folium
import streamlit as st
import json

# טוענים את קובץ ה-GeoJSON
with open("municipalities.geojson", "r", encoding="utf-8") as f:
    geo_data = json.load(f)

all_cities = [feature['properties']['MUN_HEB'] for feature in geo_data['features']]

def show_city_map(city_name):
    # יצירת מפה עם מרכז בישראל
    m = folium.Map(location=[31.5, 34.8], zoom_start=8)

    # פונקציה לצביעת העיר שבחרת בצבע אדום
    def style_function(feature):
        city_name = feature['properties']['MUN_HEB']
        if city_name == selected_city:
            return {'fillColor': 'green', 'color': 'green', 'weight': 2, 'fillOpacity': 0.5}
        else:
            return {'fillColor': 'red', 'color': 'red', 'weight': 1, 'fillOpacity': 0.3}

    folium.GeoJson(geo_data, style_function=style_function).add_to(m)
    return m


# Streamlit: מאפשר למשתמש לבחור עיר
selected_city = st.selectbox("בחר עיר:", all_cities)
map_to_show = show_city_map(selected_city)
st_data = st_folium(map_to_show, width=800, height=600)


