import os
import geopandas as gpd
import osmnx as ox
import json
import pandas as pd

class PaintStreet:
    def __init__(self):
        self.COLOR_MAP = os.getenv("COLOR_MAP",{"yes":"green","no":"red","partial":"orange"})


    def painting(self,streets_in_cities:dict):
        city_streets = gpd.GeoDataFrame()
        keys = list(streets_in_cities.keys())
        print(streets_in_cities[keys[0]])

        G = ox.graph_from_place(f"{keys[0]}", network_type='drive')
        edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
        print("g:",G)
        print("edges:",edges)

        for s in streets_in_cities[keys[0]]:
            street = edges[edges["name"] == s["street"]]
            print(street,type(street))
            if street.empty:
                print(f"Street: {s["street"]}, not found.")
            else:
                street['color'] = self.COLOR_MAP[s["status"]]
                street['city'] = keys[0]

                city_streets = gpd.GeoDataFrame(
                    pd.concat([city_streets, street], ignore_index=True)
                )
        city_streets = city_streets.dropna(axis=1, how="all")

        return city_streets