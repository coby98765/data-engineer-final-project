from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from src.services.parser.city_parser import CityParser
from src.shared.dal.kafka import Kafka
from src.shared.dal.mongo2 import MongoDAL


load_dotenv()

class Manager:

    def run(self):
        for consumer in self.kafka.sub():
            self.get_from_mongo_by_id(consumer)
            html = self.read_files("tmp/data.html")
            self.start_city(html)


    def setup(self):
        self.kafka = Kafka("parser-service")
        self.kafka.create_producer()
        self.kafka.create_consumer(os.getenv("topic-to-parser", "topic-to-parser"))
        self.mongodb = MongoDAL()
        self.parser = CityParser()


    def read_files(self, path):
        with open(path, "r",  encoding="utf-8") as file:
            file = file.read()
        return file

    def start_city(self, html):
        all_city = self.parser.parse(html)
        for row in all_city:
            if row["status"] == "partial":
                self.send_link_to_kafka(row.pop("link"))
            else:
                row.pop("link")
        docs = {"city" : all_city}
        self.saving_in_mongodb(docs)


    def send_link_to_kafka(self, link):
        self.kafka.pub(link, os.getenv("topic-to-streets", "topic-to-streets"))

    def saving_in_mongodb(self, doc):
        collection = os.getenv("collection-to-doc-city", "collection-to-doc-city")
        list_id = self.mongodb.insert_document(collection, doc)
        docs = {"city" : list_id}
        self.send_id_mongo_to_geo(docs)

    def send_id_mongo_to_geo(self, docs):
        self.kafka.pub(docs, os.getenv("topic-to-geo-city", "topic-to-geo-city"))


    def get_from_mongo_by_id(self, _id):
        folder_path = "tmp"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        city = self.mongodb.get_file(_id, f"{folder_path}/data.html")
        return city
