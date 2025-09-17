# from src.shared.api_template import build_service_app
# from src.services.scraper_2.service import run_once
from src.services.scraper_2.manager_utils import Manager

from src.services.api.app import api


app = api(Manager, "manager scraper2")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)