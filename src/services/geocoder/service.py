import os
from lib2to3.fixer_util import consuming_calls

from src.shared.dal.mongo import MongoDAL
from src.shared.dal.kafka import Kafka

class Operating:
    def __init__(self):
        self.kafka_city = None
        self.kafka_street = None
        self.kafka_building = None
        self.mongo = None

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
        for city in self.kafka_city.sub():
            self.mongo.load_report()
        for street in self.kafka_street.sub():

        for building in self.kafka_building.sub():


