from html_fetcher.html_fetcher import HtmlFetcher
from src.shared.dal.mongo2 import MongoDAL
from src.shared.dal.kafka import Kafka
from src.shared.logging.logger import Logger




class Manager:
    def __init__(self):
        self.fetcher = HtmlFetcher()
        self.url = None
        self.html =None
        self.mongo = None
        self.kafka = Kafka("consumer_2")
        self.id = None
        self.logger = Logger.get_logger()


    def set_url(self,url):
        self.url = url

    def get_html(self):
        self.html = self.fetcher.fetch_html(self.url)
        self.logger.info("html fetched successfully")

    def save_html_to_file(self):
        self.fetcher.save_html_to_file(self.html)
        self.logger.info("html saved in file successfully")


    def get_kafka_connection(self):
        try:
            self.kafka = Kafka("scraper_servic")
            self.kafka.create_producer()
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
        self.id = self.mongo.insert_file("tmp/data.html")
        self.logger.info("id inserted successfully")

    def send_to_kafka(self):
        self.kafka.pub(self.id,"topic-to-parser-streets")
        self.logger.info("topic-to-parser sent successfully")



    def setup(self):
        self.get_kafka_connection()
        self.get_mongo_connection()
        self.kafka.create_consumer("topic-to-streets")



    def run_from_sub(self,url):
        self.set_url(url)
        self.get_html()
        self.save_html_to_file()
        self.save_in_mongo_and_get_id()
        self.send_to_kafka()


    def run(self):
        for msg in self.kafka.sub():
            msg = f"https://ravkavonline.co.il{msg}"
            print(msg)
            self.run_from_sub(msg)


# a=Manager()
# a.setup()
# a.run()