
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from src.services.expander.streets_building import building_Parser
from src.shared.dal.kafka import Kafka
from src.shared.dal.mongo2 import MongoDAL

# Load environment variables
load_dotenv()

class Manager_buildings:

    def setup(self):
        # Setup Kafka producer and consumer
        self.kafka = Kafka("parser-service")
        self.kafka.create_producer()
        self.kafka.create_consumer(os.getenv("topic-to-parser-streets", "topic-to-parser-streets"))
        # Setup MongoDB
        self.mongodb = MongoDAL()

    def start_building(self, street, name_city):
        # Parse buildings for a given street
        all_building = building_Parser.parse(street, name_city)
        if all_building:
            # Save parsed buildings to MongoDB
            self.saving_in_mongodb(all_building)

    def saving_in_mongodb(self, doc):
        # Insert building document into MongoDB
        collection = os.getenv("collection-to-doc-building", "collection-to-doc-building")
        list_id = self.mongodb.insert_document(collection, doc)
        docs = {"buildings" : list_id}
        # Send MongoDB IDs to Kafka
        self.send_id_mongo_to_geo(docs)

    def send_id_mongo_to_geo(self, link):
        # Publish data to Kafka topic for geo service
        self.kafka.pub(link, os.getenv("topic-to-geo-building", "topic-to-geo-building"))

    def get_from_mongo_by_id(self, _id):
        # Download HTML file from MongoDB using ID
        folder_path = "tmp"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        city = self.mongodb.get_file(_id, f"{folder_path}/data.html")
        return city