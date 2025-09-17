# from src.shared.api_template import build_service_app
from src.services.api.app import api
from service import Operating

# app = build_service_app(service_name="geocoder", run_once=run_once)


# Create FastAPI app with Manager class
app = api(Operating, "manager geocoder")

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8006)
