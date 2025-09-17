from src.shared.api_template import build_service_app
from .service import Operating

app = build_service_app(service_name="geocoder", run_once=run_once)
