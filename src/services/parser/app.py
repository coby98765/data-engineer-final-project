from src.shared.api_template import build_service_app
from .service import run_once

app = build_service_app(service_name="parser", run_once=run_once)
