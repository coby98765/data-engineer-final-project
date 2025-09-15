from osmnx import geocode_to_gdf, features
import json
from shapely.geometry import Point
import os

class PaintBuilding:
    def __init__(self):
        self.COLOR_MAP = os.getenv("COLOR_MAP",{"yes":"green","no":"red"})
    def painting(self,city_name,street_name,building_num,building_status):
        address_input = f"{city_name},{building_num} {street_name}"


        # אם לא נמצא, נשתמש בקואורדינטות מהגיאוקוד
        point_gdf = geocode_to_gdf(address_input, which_result=1)
        lat, lon = point_gdf.geometry.centroid.y.values[0], point_gdf.geometry.centroid.x.values[0]

        # bounding box קטן סביב הנקודה (50 מטר בערך)
        delta = 0.00045
        north, south = lat + delta, lat - delta
        east, west = lon + delta, lon - delta

        gdf_buildings = features.features_from_address(north, south, east, west, tags={"building": True})

        if gdf_buildings.empty:
            print(f"No information about {city_name}")
        else:
            point = Point(lon, lat)
            gdf_buildings["distance"] = gdf_buildings.geometry.centroid.distance(point)
            closest_building = gdf_buildings.sort_values("distance").iloc[0]
            geom = closest_building.geometry
            feature = {
                "type": "Feature",
                "properties": {
                    "name": address_input,
                    "fill": self.COLOR_MAP[building_status],
                    "fill-opacity": 0.6,
                    "stroke": self.COLOR_MAP[building_status],
                    "stroke-width": 1
                },
                "geometry": gdf_buildings.loc[0, "geometry"].__geo_interface__
            }
            return feature