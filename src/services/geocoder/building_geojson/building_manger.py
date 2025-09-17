from .paint_building.building_painting import PaintBuilding
import json
import geopandas as gpd
import pandas as pd

class BuildingsGeojson:
    def __init__(self):
        self.paint_city = PaintBuilding()

    def manage_all_buildings(self,kafka_buildings,mongo):
        for building_nsg in kafka_buildings:
            buildings_doc = mongo.get_all_document("collection-to-doc-building", building_nsg["buildings"])
            buildings_geojson = self.paint_city.painting(buildings_doc)
            mongo.insert_document("collection-building-geojson", buildings_geojson)
            filename = "buildings_colored.geojson"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(buildings_geojson, f, ensure_ascii=False, indent=2)

o1 = BuildingsGeojson()
bu = [{'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 3}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 13}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 15}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 21}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 23}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 25}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no', 'building': 2}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no', 'building': 4}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no', 'building': 6}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no', 'building': 8}, {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no','building':10}]
