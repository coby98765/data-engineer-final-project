
from bs4 import BeautifulSoup
from src.services.expander.cleaning_html.cleaning_streets import Cleaning_streets

class CityParser:

    @staticmethod
    def parse(html: str):
        # Parse HTML and extract streets
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"class": "table table-bordered table-hover"})
        result = []
        # Get city name
        name_city = Cleaning_streets.get_name_city(soup)

        # Iterate over table rows
        for street in table.find("tbody").find_all("tr"):
            result.append({
                "street": Cleaning_streets.get_name_streets(street),
                "status": Cleaning_streets.get_status_streets(street),
                "city" : name_city,
                "street_html" : street  # Keep raw HTML for later parsing buildings
            })
        return result