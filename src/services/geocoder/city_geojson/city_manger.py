from src.services.geocoder.city_geojson.paint_city.city_painting import PaintCity
import json

class CitiesGeojson:
    def __init__(self):
        self.paint_city = PaintCity()

    def manage_all_cities(self,cities):
        features = []
        for city in cities:
            feature = self.paint_city.painting(city["city"],city["status"])
            features.append(feature)

        # Geojson creating.
        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }
        filename = "cities_colored.geojson"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(geojson_data, f, ensure_ascii=False, indent=2)
        # TODO insert to mongoDB

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

o1.manage_all_cities(bu)