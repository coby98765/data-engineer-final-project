import os.path

from src.services.geocoder.city_geojson.paint_city.city_painting import PaintCity
import json
import geopandas as gpd
from src.services.geocoder.street_geojson.paint_street.street_painting import PaintStreet
import pandas as pd


class StreetsGeojson:
    def __init__(self):
        self.paint_street = PaintStreet()

    def manage_all_streets(self,kafka,mongo):
        all_streets = gpd.GeoDataFrame()
        for street_msg in kafka.sub():
            #print(street_msg)
            try:
                print(len(street_msg["streets"]))
                streets_doc = mongo.get_documents_grouped_by_city("collection-to-doc-streets", street_msg["streets"])
                #print(streets_doc)
                city_streets = self.paint_street.painting(streets_doc)
                all_streets = gpd.GeoDataFrame(
                    pd.concat([all_streets, city_streets], ignore_index=True)
                )
                new_data = all_streets.to_json()

                self.update_geojson(r"C:\Users\HOME\PycharmProjects\data-engineer-final-project\geojsons\streets_colored.geojson",new_data)
            except Exception as e:
                print("Error:",e)
                continue

    @staticmethod
    def update_geojson(file_path: str, new_data: dict):
        """
        טוען קובץ GeoJSON, מוסיף נתונים חדשים לכל Feature, ושומר חזרה באותו קובץ.

        :param file_path: קובץ GeoJSON קיים
        :param new_data: מילון של נתונים להוספה ב-properties של כל Feature
        """
        try:
            print(new_data)
            if os.path.exists(file_path):

                # טוען את הקובץ
                with open(file_path, "r", encoding="utf-8") as f:
                    geojson_data = json.load(f)

                # מוסיף את הנתונים החדשים לכל Feature
                for feature in geojson_data.get("features", []):
                    feature.setdefault("properties", {})
                    feature["properties"].update(new_data)

            # שומר חזרה על אותו קובץ
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(geojson_data, f, ensure_ascii=False, indent=2)
            print("new_data:\n\n", new_data)
        except Exception as e:
            print("create geojson error:\n\n",e)
    # דוגמה לשימוש:
    # update_geojson("streets.geojson", {"city": "Bnei Brak", "source": "my_script"})


o1 = StreetsGeojson()
bu = [{"אור יהודה":[{'street': 'אבי ואביב', 'status': 'yes'}, {'street': 'אבנר', 'city': 'אור יהודה', 'status': 'yes'}, {'street': 'שדרות מנחם בגין', 'city': 'אור יהודה','status':'no'}]}]
