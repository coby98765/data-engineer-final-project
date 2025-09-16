import folium
from streamlit_folium import st_folium
import streamlit as st

# מילון של ערים וקואורדינטות שלהן
cities = {
    "תל אביב": [32.0853, 34.7818],
    "ירושלים": [31.7683, 35.2137],
    "חיפה": [32.7940, 34.9896],
    "באר שבע": [31.2518, 34.7913]
}


def show_city_map(city_name):
    # יוצרים מפה מרכזית בישראל
    m = folium.Map(location=[31.5, 34.8], zoom_start=9)

    # מוסיפים Marker לכל הערים, העיר שנבחרה בצבע אדום
    for city, coords in cities.items():
        color = "red" if city == city_name else "blue"
        folium.Marker(coords, tooltip=city, icon=folium.Icon(color=color)).add_to(m)

    return m


# דוגמה להצגה ב-Streamlit
selected_city = st.selectbox("בחר עיר:", list(cities.keys()))
map_to_show = show_city_map(selected_city)
st_data = st_folium(map_to_show, width=800, height=600)