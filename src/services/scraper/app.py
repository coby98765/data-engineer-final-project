from src.services.scraper.manager import Manager
from src.services.api.app import api

app = api(Manager, "manager scraper")