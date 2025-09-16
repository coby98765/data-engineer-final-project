from bs4 import BeautifulSoup
from src.services.parser.cleaning_html.cleaning_city import Cleaning_city

class CityParser:

    @staticmethod
    def parse(html: str):
        # Parse HTML string using BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        # Find the table containing city data
        table = soup.find("table", {"class": "table table-bordered table-hover"})
        result = []

        # Iterate over each row in table body
        for row in table.find("tbody").find_all("tr"):
            result.append({
                # Extract city name
                "city": Cleaning_city.get_name_city(row),
                # Extract city status
                "status": Cleaning_city.get_status_city(row),
                # Extract link to city page
                "link": Cleaning_city.get_link(row)
            })
        return result

