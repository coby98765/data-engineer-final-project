from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from streets_building import building_Parser
from src.shared.dal.kafka import Kafka
from src.shared.dal.mongo2 import MongoDAL


load_dotenv()

class Manager_buildings:


    def setup(self):
        self.kafka = Kafka("parser-service")
        self.kafka.create_producer()
        self.kafka.create_consumer(os.getenv("topic-to-parser-streets", "topic-to-parser-streets"))
        self.mongodb = MongoDAL()


    def start_building(self, street, name_city):
        all_building = building_Parser.parse(street, name_city)
        self.saving_in_mongodb(all_building)


    def saving_in_mongodb(self, doc):
        collection = os.getenv("collection-to-doc-building")
        id = self.mongodb.insert_document(collection, doc)
        self.send_id_mongo_to_geo(id)

    def send_id_mongo_to_geo(self, link):
        self.kafka.producer(link, os.getenv("topic-to-geo-building", "topic-to-geo-building"))


    def get_from_mongo_by_id(self, _id):
        folder_path = "tmp"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        city = self.mongodb.get_file(_id, f"{folder_path}/data.html")
        return city
