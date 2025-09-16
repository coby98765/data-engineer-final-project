from src.services.expander.manager_streets import Manager
from src.services.api.app import api

app = api(Manager, "manager expander")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)