from src.services.geocoder.building_geojson.paint_building import PaintStreet


class StreetsGeojson:
    def __init__(self):
        self.paint_city = PaintStreet()

    def manage_all_cities(self,streets):
        features = []
        for street in streets:
            feature = self.paint_city.painting(street["street"], street["street"], street["status"])
            features.append(feature)

        # Geojson creating.
        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }
        # TODO insert to mongoDB