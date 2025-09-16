from src.services.geocoder.city_geojson.paint_city.city_painting import PaintCity
import json

from src.services.geocoder.street_geojson.paint_street.street_painting import PaintStreet


class StreetsGeojson:
    def __init__(self):
        self.paint_street = PaintStreet()

    def manage_all_streets(self,cities_streets):
        all_streets = self.paint_street.painting(cities_streets)
        return all_streets

o1 = StreetsGeojson()
bu = [{"אור יהודה":[{'street': 'אבי ואביב', 'status': 'yes'}, {'street': 'אבנר', 'city': 'אור יהודה', 'status': 'yes'}, {'street': 'שדרות מנחם בגין', 'city': 'אור יהודה','status':'no'}]}]
o1.manage_all_streets(bu)