
class Cleaning_buildings:

    @staticmethod
    def get_name_city(soup):
        # Extract city name from HTML head
        head = soup.find("head")
        name_city = head.title.text[51:].strip()
        return name_city

    @staticmethod
    def get_name_streets(street):
        # Extract street name from street row
        status_city = street.find("td").text[100:130].strip()
        return status_city

    @staticmethod
    def get_str_buildings_yes(street):
        # Get string of "yes" buildings from street
        index_yes = street.text.index("מספרי בתים זכאים:")
        index_no = street.text.index("מספרי בתים שאינם זכאים:")
        str_building_yes = street.text[index_yes + len("מספרי בתים זכאים:"): index_no].strip()
        return str_building_yes

    @staticmethod
    def get_str_buildings_no(street):
        # Get string of "no" buildings from street
        index_no = street.text.index("מספרי בתים שאינם זכאים:")
        str_building_no = street.text[index_no + len("מספרי בתים שאינם זכאים:"):].strip()
        return str_building_no

    @staticmethod
    def convert_str_to_list(street):
        # Convert string of numbers to list of integers
        try:
            building_list = [int(x.strip().replace('.', '')) for x in street.split(",")]
            return building_list
        except:
            return None

    @staticmethod
    def get_status_streets(street):
        # Get street status from first 100 characters
        status_streets = street.find("td").text[:100].strip()
        if status_streets == "🟢":
            return "yes"
        elif status_streets == "🔴":
            return "no"
        else:
            return "partial"

    @staticmethod
    def get_link(city):
        # Extract link from HTML
        link_city = city.find("a").get("href")
        return link_city