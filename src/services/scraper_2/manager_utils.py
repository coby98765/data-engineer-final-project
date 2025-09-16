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

    """
    This function defines the URL we will work on.
    """
    def set_url(self,url):
        self.url = url
    """
    This function receives all the information in the html of the url we received.
    """
    def get_html(self):
        self.html = self.fetcher.fetch_html(self.url)
        self.logger.info("html fetched successfully")
    """
    This function sends to a function found in the HtmlFetcher file that saves the information in a local folder.
    """
    def save_html_to_file(self):
        self.fetcher.save_html_to_file(self.html)
        self.logger.info("html saved in file successfully")

    """
    This function creates an initial connection to Kafka located in the Kafka folder.
    """
    def get_kafka_connection(self):
        try:
            self.kafka = Kafka("scraper_servic")
            self.kafka.create_producer()
            self.logger.info("kafka connection successfully")
        except Exception as e:
            self.logger.error(f"kafka connection failed {e}")
    """
    This function creates an initial connection to the MongoDB found in the Mongo DAL file.
    """
    def get_mongo_connection(self):
        try:
            self.mongo = MongoDAL()
            self.logger.info("mongo connection successfully")
        except Exception as e:
            self.logger.error(f"mongo connection failed {e}")
    """
    This function saves the data in MongoDB using GridFS and returns a unique identifier.
    """
    def save_in_mongo_and_get_id(self):
        self.id = self.mongo.insert_file("tmp/data.html")
        self.logger.info("id inserted successfully")
    """
    This function sends the unique identifier to Kafka.
    """
    def send_to_kafka(self):
        self.kafka.pub(self.id,"topic-to-parser-streets")
        self.logger.info("topic-to-parser sent successfully")


    """
    This function initializes scraper_2 by initially connecting to MongoDB
     and Kafka and also creates a listener in Kafka and gives it the name of the topic.
    """
    def setup(self):
        self.get_kafka_connection()
        self.get_mongo_connection()
        self.kafka.create_consumer("topic-to-streets")
        self.logger.info("Manager scraper was setup successfully")


    """
    This function receives a message from the function that listens to the topic
    and handles it by extracting what needs to be saved in MongoDB and sending the unique identifier to the next stage.
    """
    def run_from_sub(self,url):
        self.set_url(url)
        self.get_html()
        self.save_html_to_file()
        self.save_in_mongo_and_get_id()
        self.send_to_kafka()

    """
    This function runs the program by starting to listen to the topic it is initializing
    and sending any acknowledgement it receives to the data processing.
    """
    def run(self):
        for msg in self.kafka.sub():
            msg = f"https://ravkavonline.co.il{msg}"
            self.logger.debug(f"got message from kafka: {msg} ")
            self.run_from_sub(msg)


# a=Manager()
# a.setup()
# a.run()