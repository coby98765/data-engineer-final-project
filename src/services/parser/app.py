from src.services.parser.manager_city import Manager
from src.services.api.app import api

app = api(Manager, "manager scraper")