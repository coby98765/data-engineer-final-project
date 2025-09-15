import os

import osmnx as ox
import json

class PaintCity:
    def __init__(self):
        self.COLOR_MAP = os.getenv("COLOR_MAP",{"yes":"green","no":"red","partial":"orange"})
    def painting(self,city_name,city_status):
        gdf = ox.geocode_to_gdf(city_name)
        print(gdf)
        if gdf.empty:
            print(f"No information about {city_name}")
        else:
            geom = gdf.geometry.values[0]

            feature = {
                "type": "Feature",
                "properties": {
                    "name": city_name,
                    "status": city_status,
                    "fill": self.COLOR_MAP[city_status],
                    "fill-opacity": 0.6,
                    "stroke": self.COLOR_MAP[city_status],
                    "stroke-width": 1
                },
                "geometry": gdf.loc[0, "geometry"].__geo_interface__
            }
            return feature