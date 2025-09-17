
class Cleaning_city:

    @staticmethod
    def get_status_city(city):
        # Extract city status from HTML
        status_city = city.find("div", {"class": "flex flex--wrap"}).text[80:110].strip()
        if status_city == "זכאי":
            return "yes"
        elif status_city == "לא זכאי":
            return "no"
        else:
            return "partial"

    @staticmethod
    def get_name_city(city):
        # Extract city name from HTML
        name_city = city.find("td", {"class": "w--0 t--no-wrap"}).text
        return name_city

    @staticmethod
    def get_link(city):
        # Extract link from city row, return empty string if not found
        try:
            link_city = city.find("a").get("href")
            return link_city
        except:
            return ""