import os

import osmnx as ox
import json

class PaintCity:
    def __init__(self):
        self.COLOR_MAP = os.getenv("COLOR_MAP",{"yes":"green","no":"red","partial":"orange"})
    def painting(self,cities):
        try:
            features = []
            for city in cities:
                try:
                    city_name = city["city"]
                    city_status = city["status"]
                    gdf = ox.geocode_to_gdf(city_name)
                    print(gdf)
                    if gdf.empty:
                        print(f"No information about {city_name}")
                        continue
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
                        features.append(feature)
                except Exception as e:
                    print(1,e)
                    continue

            # Geojson creating.
            geojson_data = {
                "type": "FeatureCollection",
                "features": features
            }
            return geojson_data
        except Exception as e:
            print(2,e)