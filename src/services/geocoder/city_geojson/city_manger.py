from src.services.geocoder.city_geojson.paint_city.city_painting import PaintCity

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
        # TODO insert to mongoDB