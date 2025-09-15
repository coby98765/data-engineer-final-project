from bs4 import BeautifulSoup
from src.services.expander.cleaning_html.cleaning_streets import Cleaning_streets

class CityParser:

    @staticmethod
    def parse(html: str):
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"class": "table table-bordered table-hover"})
        result = []
        city = None
        for street in table.find("tbody").find_all("tr"):
            result.append({
                "street": Cleaning_streets.get_name_streets(street),
                "status": Cleaning_streets.get_status_streets(street)
            })
            city = Cleaning_streets.get_name_city(street)
        result = {
            city : result
        }
        return result

