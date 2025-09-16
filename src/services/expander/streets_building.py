
from bs4 import BeautifulSoup
from src.services.expander.cleaning_html.cleaning_buildings import Cleaning_buildings

class building_Parser:

    @staticmethod
    def parse(street, name_city):
        # Parse buildings from street HTML
        list_status_streets = []
        street_str_yes = Cleaning_buildings.get_str_buildings_yes(street)
        street_str_no = Cleaning_buildings.get_str_buildings_no(street)
        street_yes_list = Cleaning_buildings.convert_str_to_list(street_str_yes)
        street_no_list = Cleaning_buildings.convert_str_to_list(street_str_no)

        if not street_yes_list:
            print(street)
            print(name_city)
            return None

        # Add "yes" buildings
        for building in street_yes_list:
            building_dict = building_Parser.create_dict_of_streets(street, name_city)
            building_dict['building'] = building
            building_dict["status"] = "yes"
            list_status_streets.append(building_dict)

        if not street_no_list:
            print(street)
            print(name_city)
            return None

        # Add "no" buildings
        for building in street_no_list:
            building_dict = building_Parser.create_dict_of_streets(street, name_city)
            building_dict['building'] = building
            building_dict["status"] = "no"
            list_status_streets.append(building_dict)

        return list_status_streets

    @staticmethod
    def create_dict_of_streets(street, name_city):
        # Create basic building dictionary
        name_street = Cleaning_buildings.get_name_streets(street)
        building_dict = {
            "street": name_street,
            "city": name_city
        }
        return building_dict