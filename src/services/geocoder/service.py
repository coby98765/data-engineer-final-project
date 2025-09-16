from city_geojson.city_manger import CitiesGeojson
from street_geojson.street_manger import StreetsGeojson
from building_geojson.building_manger import BuildingsGeojson
from src.shared.dal.mongo2 import MongoDAL
from src.shared.dal.kafka import Kafka
import json

class Operating:
    def __init__(self):
        self.kafka_city = None
        self.kafka_street = None
        self.kafka_building = None
        self.mongo = None
        self.city_to_geo = CitiesGeojson()
        self.street_to_geo = StreetsGeojson()
        self.building_to_geo = BuildingsGeojson()

    def setup(self):
        self.kafka_city = Kafka("geocoder")
        self.kafka_street = Kafka("geocoder")
        self.kafka_building = Kafka("geocoder")
        self.kafka_city.create_consumer("topic-to-geo-city")
        self.kafka_street.create_consumer("topic-to-geo-streets")
        self.kafka_building.create_consumer("topic-to-geo-building")
        self.mongo = MongoDAL()

    def run(self):
        print("running geocoder...")
        print(self.kafka_city.sub())
        self.city_to_geo.manage_all_cities(self.kafka_city.sub(),self.mongo)
        print("city geomap complete.")
        self.street_to_geo.manage_all_streets(self.kafka_street.sub(), self.mongo)
        print("street geomap complete.")

        self.building_to_geo.manage_all_buildings(self.kafka_building.sub(), self.mongo)
        print("building geomap complete.")



o1 = Operating()
o1.setup()
o1.run()