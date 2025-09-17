from src.services.scraper.manager import Manager
from src.services.api.app import api

app = api(Manager, "manager scraper")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)