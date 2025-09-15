from html_fetcher.html_fetcher import HtmlFetcher
from src.shared.dal.mongo import MongoDAL
from  src.shared.dal.kafka import Kafka
from src.shared.dal.kafka import Kafka
from src.shared.logging.logger import Logger

class Manager:
    def __init__(self):
        self.fetcher = HtmlFetcher()
        self.url ="https://ravkavonline.co.il/he/ravkav-geographic/eligible-localities"
        self.html =None
        self.mongo = None
        self.pub = None
        self.id = None
        self.logger = Logger.get_logger()
        self.path=None


    def get_html(self):
        self.html = self.fetcher.fetch_html(self.url)
        self.logger.info("html fetched successfully")

    def save_html_to_file(self):
        self.fetcher.save_html_to_file(self.html)
        self.path = "tmp\data_html"
        self.logger.info("html saved in file successfully")


    def get_kafka_connection(self):
        try:
            self.pub = Kafka("scraper_servic")
            self.logger.info("kafka connection successfully")
        except Exception as e:
            self.logger.error(f"kafka connection failed {e}")

    def get_mongo_connection(self):
        try:
            self.mongo = MongoDAL()
            self.logger.info("mongo connection successfully")
        except Exception as e:
            self.logger.error(f"mongo connection failed {e}")

    def save_in_mongo_and_get_id(self):
        self.id = self.mongo.insert_file(self.path)
        self.logger.info("id inserted successfully")

    def send_to_kafka(self):
        self.pub.pub(self.id,"topic-to-parser")
        self.logger.info("topic-to-parser sent successfully")



    def setup(self):
        self.get_kafka_connection()
        self.get_mongo_connection()


    def run(self):
        self.get_html()
        self.save_html_to_file()
        self.save_in_mongo_and_get_id()
        self.send_to_kafka()

