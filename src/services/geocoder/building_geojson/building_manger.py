from paint_building.building_painting import PaintBuilding
import json
import geopandas as gpd
import pandas as pd

class BuildingsGeojson:
    def __init__(self):
        self.paint_city = PaintBuilding()

    def manage_all_buildings(self,buildings):
        all_buildings = gpd.GeoDataFrame()
        for building in buildings:
            feature = self.paint_city.painting(
                building["city"],
                building["street"],
                building["building"],
                building["status"]
            )
            all_buildings = gpd.GeoDataFrame(
                pd.concat([all_buildings, feature], ignore_index=True)
            )
        geojson_dict = json.loads(all_buildings.to_json())
        return geojson_dict
o1 = BuildingsGeojson()
bu = [{'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 3}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 13}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 15}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 21}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 23}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 25}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no', 'building': 2}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no', 'building': 4}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no', 'building': 6}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no', 'building': 8}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no','building':10}]
o1.manage_all_buildings(bu)