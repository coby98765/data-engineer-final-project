from src.services.scraper.html_fetcher.html_fetcher import HtmlFetcher
from src.shared.dal.mongo2 import MongoDAL
from  src.shared.dal.kafka import Kafka
from src.shared.dal.kafka import Kafka
from src.shared.logging.logger import Logger

class Manager:
    def __init__(self,url = "https://ravkavonline.co.il/he/ravkav-geographic/eligible-localities"):
        self.fetcher = HtmlFetcher()
        self.url = url
        self.html =None
        self.mongo = None
        self.kafka = None
        self.id = None
        self.logger = Logger.get_logger()


    """
    This function searches the internet for information.
    """
    def get_html(self):
        self.html = self.fetcher.fetch_html(self.url)
        self.logger.info("html fetched successfully")
    """
    This function saves the information to a local file.
    """
    def save_html_to_file(self):
        self.fetcher.save_html_to_file(self.html)
        self.logger.info("html saved in file successfully")

    """
    This function creates an initial connection to Kafka.
    """
    def get_kafka_connection(self):
        try:
            self.kafka = Kafka("scraper_servic")
            self.kafka.create_producer()
            self.logger.info("kafka connection successfully")
        except Exception as e:
            self.logger.error(f"kafka connection failed {e}")

    """
    This function creates an initial connection to MongoDB.
    """
    def get_mongo_connection(self):
        try:
            self.mongo = MongoDAL()
            self.logger.info("mongo connection successfully")
        except Exception as e:
            self.logger.error(f"mongo connection failed {e}")


    """
    This function saves the monodiv by gridfs and gets the unique identifier
    """
    def save_in_mongo_and_get_id(self):
        self.id = self.mongo.insert_file("tmp/data.html")
        self.logger.info("id inserted successfully")
    """
    This function sends to Kafka
    """
    def send_to_kafka(self):
        self.kafka.pub(self.id,"topic-to-parser")
        self.logger.info("topic-to-parser sent successfully")


    """
    This function initializes the service by making an initial connection to MongoDB and Kafka.
    """
    def setup(self):
        self.get_kafka_connection()
        self.get_mongo_connection()
        self.logger.info("manager scraper setup successfully")


    """
    This function manages the entire service by receiving the html from the url and saving the information to a file,
     then saving it to MongoDB and sending the unique identifier to Kafka.
    """

    def run(self):
        self.get_html()
        self.save_html_to_file()
        self.save_in_mongo_and_get_id()
        self.send_to_kafka()