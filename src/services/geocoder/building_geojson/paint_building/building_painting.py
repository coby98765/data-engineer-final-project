import os

import osmnx as ox
import json

class PaintBuilding:
    def __init__(self):
        self.COLOR_MAP = os.getenv("COLOR_MAP",{"yes":"green","no":"red"})
    def painting(self,city_name,street_name,building_num,building_status):
        gdf = ox.features.g(f"{city_name},{street_name},{building_num}",tags=)
        if gdf.empty:
            print(f"No information about {city_name}")
        else:
            geom = gdf.geometry.values[0]

            feature = {
                "type": "Feature",
                "properties": {
                    "name": city_name,
                    "status": street_status,
                    "stroke": self.COLOR_MAP[street_status],
                    "stroke-width": 1
                },
                "geometry": gdf.loc[0, "geometry"].__geo_interface__
            }
            return feature