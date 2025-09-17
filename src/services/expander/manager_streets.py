
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from src.services.expander.streets_parser import CityParser
from src.shared.dal.kafka import Kafka
from src.shared.dal.mongo2 import MongoDAL
from src.services.expander.manager_buildings import Manager_buildings

# Load environment variables
load_dotenv()

class Manager:

    def run(self):
        # Main loop to consume messages from Kafka
        for consumer in self.kafka.sub():
            print(consumer)
            # Get HTML file from MongoDB by ID
            self.get_from_mongo_by_id(consumer)
            html = self.read_files("tmp/data.html")
            # Parse streets and process them
            self.start_city(html)

    def setup(self):
        # Setup Manager for buildings
        self.manager_buildings = Manager_buildings()
        self.manager_buildings.setup()
        # Setup Kafka producer and consumer
        self.kafka = Kafka("parser-service")
        self.kafka.create_producer()
        self.kafka.create_consumer(os.getenv("topic-to-parser-streets", "topic-to-parser-streets"))
        # Setup MongoDB
        self.mongodb = MongoDAL()
        # Setup parser
        self.parser = CityParser()

    def read_files(self, path):
        # Read HTML file from disk
        with open(path, "r",  encoding="utf-8") as file:
            file = file.read()
        return file

    def start_city(self, html):
        # Parse streets and process each
        all_streets = self.parser.parse(html)
        list_of_buildings = []
        for street in all_streets:
            if street["status"] == "partial":
                # Parse buildings for partial streets
                list_of_buildings.append(self.manager_buildings.start_building(street["street_html"], street["city"]))
        # Save streets to MongoDB
        self.saving_in_mongodb(all_streets)

    def saving_in_mongodb(self, doc):
        # Remove HTML content before saving
        for street in doc:
            street.pop("street_html")
        # Insert streets document into MongoDB
        collection = os.getenv("collection-to-doc-streets", "collection-to-doc-streets")
        list_id = self.mongodb.insert_document(collection, doc)
        docs = {"streets" : list_id}
        # Send MongoDB IDs to Kafka
        self.send_id_mongo_to_geo(docs)

    def send_id_mongo_to_geo(self, link):
        # Publish data to Kafka topic for geo service
        self.kafka.pub(link, os.getenv("topic-to-geo-streets", "topic-to-geo-streets"))

    def get_from_mongo_by_id(self, _id):
        # Download HTML file from MongoDB using ID
        folder_path = "tmp"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        city = self.mongodb.get_file(_id, f"{folder_path}/data.html")
        return city
o1 = Manager()
o1.setup()
o1.run()

