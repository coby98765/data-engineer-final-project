import pandas as pd
import json
from shapely.geometry import Point
import geopandas as gpd
import os
import osmnx as ox
class PaintBuilding:
    def __init__(self):
        self.COLOR_MAP = os.getenv("COLOR_MAP",{"yes":"green","no":"red"})
    def painting(self,buildings):
        all_buildings = gpd.GeoDataFrame()
        nearest_building = None
        for building in buildings:
            # feature = self.paint_city.painting(
            #     building["city"],
            #     building["street"],
            #     building["building"],
            #     building["status"]
            # )

            address_input = f"{building["city"]},{building["building"]} {building["street"]}"
            lat , lon = ox.geocode(address_input)  # מחזיר (lat, lon)
            point = Point(lon, lat)
            # --- 2. חיפוש בניינים קרובים ---
            tags = {"building": True}
            buildings = ox.features.features_from_point((lat,lon), tags=tags, dist=50) # רדיוס 50 מטר
            if buildings.empty:
                print(f"No building found near {address_input}")
                continue  # מחזיר ריק

                # --- 3. מציאת הבניין הקרוב ביותר לנקודה ---
            buildings = buildings.to_crs(epsg=3857)
            point_proj = gpd.GeoSeries([point], crs="EPSG:4326").to_crs(epsg=3857).iloc[0]

            distances = buildings.geometry.distance(point_proj)
            nearest_index = distances.idxmin()
            nearest_building = buildings.loc[[nearest_index]].copy()  # GeoDataFrame של הבניין היחיד

            # --- 4. הוספת צבע / סטטוס ---
            nearest_building["status"] = building["status"]
            nearest_building["color"] = self.COLOR_MAP[building["status"]]
        all_buildings = gpd.GeoDataFrame(
            pd.concat([all_buildings, nearest_building.to_crs(epsg=4326)], ignore_index=True)
        )
        geojson_dict = json.loads(all_buildings.to_json())
        # החזרת GeoDataFrame עם בניין יחיד
        return geojson_dict