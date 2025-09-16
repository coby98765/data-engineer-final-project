from src.services.geocoder.city_geojson.paint_city.city_painting import PaintCity
import json

from src.services.geocoder.street_geojson.paint_street.street_painting import PaintStreet


class StreetsGeojson:
    def __init__(self):
        self.paint_street = PaintStreet()

    def manage_all_streets(self,kafka_sub,mongo):
        for street_msg in kafka_sub:
            print(street_msg["streets"])
            streets_doc = mongo.get_documents_grouped_by_city("collection-to-doc-streets", street_msg["streets"])
            print(streets_doc)
            all_streets = self.paint_street.painting(dict(streets_doc))

            mongo.insert_document("collection-street-geojson",all_streets)
            filename = "streets_colored.geojson"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(all_streets, f, ensure_ascii=False, indent=2)

o1 = StreetsGeojson()
bu = [{"אור יהודה":[{'street': 'אבי ואביב', 'status': 'yes'}, {'street': 'אבנר', 'city': 'אור יהודה', 'status': 'yes'}, {'street': 'שדרות מנחם בגין', 'city': 'אור יהודה','status':'no'}]}]
