
class Cleaning_streets:

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