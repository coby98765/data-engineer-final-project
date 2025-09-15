from bs4 import BeautifulSoup
from cleaning_html.cleaning_city import Cleaning_city

class CityParser:

    @staticmethod
    def parse(html: str):
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"class": "table table-bordered table-hover"})
        result = []

        for row in table.find("tbody").find_all("tr"):
            result.append({
                "city": Cleaning_city.get_name_city(row),
                "status": Cleaning_city.get_status_city(row),
                "link": Cleaning_city.get_link(row)
            })
        return result

