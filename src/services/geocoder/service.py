from city_geojson.city_manger import CitiesGeojson
from street_geojson.street_manger import StreetsGeojson
from building_geojson.building_manger import BuildingsGeojson
from src.shared.dal.mongo2 import MongoDAL
from src.shared.dal.kafka import Kafka

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
        self.mongo = MongoDAL()
        print("running job once...")
        for city_msg in self.kafka_city.sub():
            cities_doc = self.mongo.get_all_document("collection-to-doc-city", city_msg["city"])
            city_geojson = self.city_to_geo.manage_all_cities(cities_doc)
            self.mongo.insert_document("collection-city-geojson",city_geojson)
        for street_msg in self.kafka_street.sub():
            streets_doc = self.mongo.get_all_document("collection-to-doc-street", street_msg["streets"])
            streets_geojson = self.street_to_geo.manage_all_streets(streets_doc)
            self.mongo.insert_document("collection-street-geojson",streets_geojson)
        for building_nsg in self.kafka_building.sub():
            buildings_doc = self.mongo.get_all_document("collection-to-doc-building", building_nsg["buildings"])
            buildings_geojson = self.building_to_geo.manage_all_buildings(buildings_doc)
            self.mongo.insert_document("collection-building-geojson", buildings_geojson)


