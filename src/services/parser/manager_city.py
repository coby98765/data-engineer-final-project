from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from src.services.parser.cleaning_html.cleaning_city import Cleaning_city
from dal.kafka import Kafka

load_dotenv()

class Manager:

    def run(self):
        for i in self.kafka.sub():
            html = i
            self.start_city(html)


    def setup(self):
        self.kafka = Kafka("parser-service")
        self.kafka.create_producer()
        self.kafka.create_consumer(os.getenv("topic-to-parser", "topic-to-parser"))

    @staticmethod
    def create_dict_of_city(city):
        name_city = Cleaning_city.get_name_city(city)
        status_city = Cleaning_city.get_status_city(city)
        city_dict = {
            "city": name_city,
            "status": status_city,
        }
        return city_dict


    @staticmethod
    def check_if_partial(city_dict):
        return "זכאי באופן חלקי" in city_dict['status']


    def send_link_to_kafka(self, link):
        self.kafka.pub(link, os.getenv("topic-to-scraper", "topic-to-scraper"))


    @staticmethod
    def get_link_for_city(city):
        link = Cleaning_city.get_link(city)
        return link


    def start_city(self, html):
        #get data from kafka
        soup = BeautifulSoup(html, "html.parser")
        #get table from html
        table = soup.find("table", {"class": "table table-bordered table-hover"})

        all_city = []

        for city in table.find("tbody").find_all("tr"):
            city_dict = self.create_dict_of_city(city)
            if self.check_if_partial(city_dict):
                link = self.get_link_for_city(city)
                self.send_link_to_kafka(link)
            all_city.append(city_dict)

        print(all_city)



a = Manager()
a.setup()
a.run()