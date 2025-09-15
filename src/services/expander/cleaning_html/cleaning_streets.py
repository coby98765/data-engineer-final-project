
class Cleaning_streets:


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

#



