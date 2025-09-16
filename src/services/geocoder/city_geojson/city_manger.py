from src.services.geocoder.city_geojson.paint_city.city_painting import PaintCity
import json

class CitiesGeojson:
    def __init__(self):
        self.paint_city = PaintCity()

    def manage_all_cities(self,kafka_sub,mongo):
        for city_msg in kafka_sub:
            try:
                print("city",city_msg)
                cities_doc = mongo.get_all_document("collection-to-doc-city", city_msg["city"])
                print(cities_doc)
                geojson_data = self.paint_city.painting(cities_doc)
                print("g             ",geojson_data)
                mongo.insert_document("collection-city-geojson",geojson_data)
                filename = "cities_colored.geojson"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(geojson_data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(e)
                continue



o1 = CitiesGeojson()
bu = [{'city': 'אודים', 'status': 'yes'}, {'city': 'תל אביב', 'status': 'no'}, {'city': 'אוהד', 'status': 'partial'},{'city': 'אודם', 'status': 'no'}]
#[{'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 3},
#       {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 13},
#       {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 15},
#       {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 21},
#       {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 23},
#       {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'yes', 'building': 25},
#       {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no', 'building': 2},
#       {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no', 'building': 4},
#       {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no', 'building': 6},
#       {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no', 'building': 8},
#       {'street': 'דוד אלעזר', 'city': 'אור יהודה', 'status': 'no', 'building': 10}]

