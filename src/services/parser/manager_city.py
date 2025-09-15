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


    def send_link_to_kafka(self, link):
        self.kafka.pub(link, os.getenv("topic-to-scraper", "topic-to-scraper"))

    def saving_in_mongodb(self, doc):
        collection = os.getenv("collection-to-doc-city")
        id = self.mongodb.insert_document(collection, doc)
        self.send_id_mongo_to_geo(id)

    def send_id_mongo_to_geo(self, link):
        self.kafka.producer(link, os.getenv("topic-to-geo", "topic-to-geo"))


    def get_from_mongo_by_id(self, _id):
        city = self.mongodb.get_file(_id, f"tmp/{id}.html")
        return city


a = Manager()
a.setup()
a.run()