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
            G = ox.graph_from_place(f"{city_name},Israel", network_type='drive')
            edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

            for s in streets_list:
                street = edges[edges["name"] == s["street"]]
                street['color'] = self.COLOR_MAP[s["status"]]
                street['city'] = city_name

                all_streets = gpd.GeoDataFrame(
                    pd.concat([all_streets, street], ignore_index=True)
                )

        # המרה ל־dict שמוכן לשמירה במונגו
        geojson_dict = json.loads(all_streets.to_json())
        return geojson_dict
        # print(streets_in_city)
        # features = []
        # G = ox.graph_from_place(next(iter(streets_in_city)), network_type="drive")
        # edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
        # for s in streets_in_city:
        #     s = edges[edges["name"] == s]
        #     print(G)
        #     if s.empty:
        #         print(f"No information about {s}")
        #     else:
        #
        #
        #         # סינון לפי שם הרחוב
        #
        #         # geom = G.geometry.values[0]
        #
        #         for _, row in s.iterrows():
        #             feature = {
        #                 "type": "Feature",
        #                 "properties": {
        #                     "name": s,
        #                     "status": s['status'],
        #                     "stroke": self.COLOR_MAP[s['status']],
        #                     "stroke-width": 1
        #                 },
        #                 "geometry": row["geometry"].__geo_interface__
        #             }
        #             features.append(feature)
        #
        # return features