from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from streets_parser import CityParser
from src.shared.dal.kafka import Kafka
from src.shared.dal.mongo2 import MongoDAL
from manager_buildings import Manager_buildings


load_dotenv()

class Manager:

    def __init__(self):
        self.manager_buildings = Manager_buildings()

    def run(self):
        for consumer in self.kafka.sub():
            html = self.get_from_mongo_by_id(consumer["_id"])
            self.start_city(html)


    def setup(self):
        self.kafka = Kafka("parser-service")
        self.kafka.create_producer()
        self.kafka.create_consumer(os.getenv("topic-to-parser-streets", "topic-to-parser-streets"))
        self.mongodb = MongoDAL()
        self.parser = CityParser()


    def start_city(self, html):
        all_streets = self.parser.parse(html)
        list_of_buildings = []
        for street in all_streets:
            if street["status"] == "partial":
                list_of_buildings.append(self.manager_buildings.start_city(street, street["city"]))
        self.saving_in_mongodb(all_streets)


    def saving_in_mongodb(self, doc):
        collection = os.getenv("collection-to-doc-streets")
        id = self.mongodb.insert_document(collection, doc)
        self.send_id_mongo_to_geo(id)

    def send_id_mongo_to_geo(self, link):
        self.kafka.producer(link, os.getenv("topic-to-geo-streets", "topic-to-geo-streets"))


    def get_from_mongo_by_id(self, _id):
        folder_path = "tmp"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        city = self.mongodb.get_file(_id, f"{folder_path}/data.html")
        return city


a = Manager()
a.setup()
a.run()