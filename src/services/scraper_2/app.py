from src.shared.api_template import build_service_app
from src.services.scraper_2.service import run_once

app = build_service_app(service_name="scraper", run_once=run_once)
