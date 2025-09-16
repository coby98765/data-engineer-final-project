from src.services.expander.manager_streets import Manager
from src.services.api.app import api

app = api(Manager, "manager scraper")