from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from city_parser import CityParser
from src.shared.dal.kafka import Kafka
from src.shared.dal.mongo2 import MongoDAL


load_dotenv()

class Manager:

    def run(self):
        for consumer in self.kafka.sub():
            html = self.get_from_mongo_by_id(consumer["_id"])
            self.start_city(html)


    def setup(self):
        self.kafka = Kafka("parser-service")
        self.kafka.create_producer()
        self.kafka.create_consumer(os.getenv("topic-to-parser", "topic-to-parser"))
        self.mongodb = MongoDAL()
        self.parser = CityParser()


    def start_city(self, html):
        all_city = self.parser.parse(html)
        for row in all_city:
            if row["status"] == "partial":
                self.send_link_to_kafka(row.pop("link"))
        self.saving_in_mongodb(all_city)


    def send_link_to_kafka(self, link):
        self.kafka.pub(link, os.getenv("topic-to-streets", "topic-to-streets"))

    def saving_in_mongodb(self, doc):
        collection = os.getenv("collection-to-doc-city")
        id = self.mongodb.insert_document(collection, doc)
        self.send_id_mongo_to_geo(id)

    def send_id_mongo_to_geo(self, link):
        self.kafka.producer(link, os.getenv("topic-to-geo-city", "topic-to-geo-city"))


    def get_from_mongo_by_id(self, _id):
        folder_path = "tmp"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        city = self.mongodb.get_file(_id, f"{folder_path}/data.html")
        return city


a = Manager()
a.setup()
a.run()