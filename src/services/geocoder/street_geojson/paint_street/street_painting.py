import os
import geopandas as gpd
import osmnx as ox
import json
import pandas as pd

class PaintStreet:
    def __init__(self):
        self.COLOR_MAP = os.getenv("COLOR_MAP",{"yes":"green","no":"red","partial":"orange"})
    def painting(self,streets_in_cities):
        all_streets = gpd.GeoDataFrame()

        for city in streets_in_cities:
            city_name = list(city.keys())[0]
            streets_list = city[city_name]
            print(streets_list)
            print(city_name)
            G = ox.graph_from_place(f"{city_name}", network_type='drive')
            edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

            for s in streets_list:
                street = edges[edges["name"] == s["street"]]
                print(street,type(street))
                if street.empty:
                    print("Street not found.")
                else:
                    street['color'] = self.COLOR_MAP[s["status"]]
                    street['city'] = city_name

                    all_streets = gpd.GeoDataFrame(
                        pd.concat([all_streets, street], ignore_index=True)
                    )

        # המרה ל־dict שמוכן לשמירה במונגו
        geojson_dict = json.loads(all_streets.to_json())
        return geojson_dict