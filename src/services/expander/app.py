from src.services.expander.manager_streets import Manager
from src.services.api.app import api

# Create FastAPI app with Manager class
app = api(Manager, "manager expander")

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8001)