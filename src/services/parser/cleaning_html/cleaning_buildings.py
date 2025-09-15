
class Cleaning_buildings:

    @staticmethod
    def get_name_city(soup):
        head = soup.find("head")
        name_city = head.title.text[51:].strip()
        return name_city

    @staticmethod
    def get_name_streets(street):
        status_city = street.find("td").text[100:130].strip()
        return status_city

    @staticmethod
    def get_str_buildings_yes(street):
        index_yes = street.text.index("מספרי בתים זכאים:")
        index_no = street.text.index("מספרי בתים שאינם זכאים:")
        str_building_yes = street.text[index_yes + len("מספרי בתים זכאים:"): index_no].strip()
        return str_building_yes

    @staticmethod
    def get_str_buildings_no(street):
        index_yes = street.text.index("מספרי בתים זכאים:")
        index_no = street.text.index("מספרי בתים שאינם זכאים:")
        str_building_no = street.text[index_no + len("מספרי בתים שאינם זכאים:"):].strip()
        return str_building_no

    @staticmethod
    def convert_str_to_list(street):
        building_list = [int(x.strip().replace('.', '')) for x in street.split(",")]
        return building_list

    @staticmethod
    def get_status_streets(street):
        status_streets = street.find("td").text[:100].strip()
        if status_streets == "🟢":
            return "yes"
        elif status_streets == "🔴":
            return "no"
        else:
            return "partial"

    @staticmethod
    def get_link(city):
        link_city = city.find("a").get("href")
        return link_city
