from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from src.services.parser.city_parser import CityParser
from src.shared.dal.kafka import Kafka
from src.shared.dal.mongo2 import MongoDAL

# Load environment variables from .env file
load_dotenv()

class Manager:

    def run(self):
        # Main loop to consume messages from Kafka
        print("parser running...")
        for consumer in self.kafka.sub():
            # Get HTML file from MongoDB by ID
            self.get_from_mongo_by_id(consumer)
            html = self.read_files("tmp/data.html")
            # Parse cities and process them
            self.start_city(html)


    def setup(self):
        # Setup Kafka producer and consumer
        self.kafka = Kafka("parser-service")
        self.kafka.create_producer()
        self.kafka.create_consumer(os.getenv("topic-to-parser", "topic-to-parser"))
        # Setup MongoDB access
        self.mongodb = MongoDAL()
        # Setup parser
        self.parser = CityParser()


    def read_files(self, path):
        # Read HTML file from disk
        with open(path, "r",  encoding="utf-8") as file:
            file = file.read()
        return file

    def start_city(self, html):
        # Parse HTML and process city data
        all_city = self.parser.parse(html)
        for row in all_city:
            if row["status"] == "partial":
                # Send link to Kafka if city status is partial
                self.send_link_to_kafka(row.pop("link"))
            else:
                # Remove link if not needed
                row.pop("link")
        # Save processed city data to MongoDB
        self.saving_in_mongodb(all_city)


    def send_link_to_kafka(self, link):
        # Publish link to Kafka topic for streets
        self.kafka.pub(link, os.getenv("topic-to-streets", "topic-to-streets"))

    def saving_in_mongodb(self, doc):
        # Insert city document into MongoDB
        collection = os.getenv("collection-to-doc-city", "collection-to-doc-city")
        list_id = self.mongodb.insert_document(collection, doc)
        docs = {"city" : list_id}
        # Send MongoDB ID to Kafka
        self.send_id_mongo_to_geo(docs)

    def send_id_mongo_to_geo(self, docs):
        # Publish MongoDB IDs to Kafka topic for geo service
        self.kafka.pub(docs, os.getenv("topic-to-geo-city", "topic-to-geo-city"))


    def get_from_mongo_by_id(self, _id):
        # Download HTML file from MongoDB using ID
        folder_path = "tmp"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        city = self.mongodb.get_file(_id, f"{folder_path}/data.html")
        return city
