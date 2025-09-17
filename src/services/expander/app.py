from src.shared.api_template import build_service_app
from .service import run_once

app = build_service_app(service_name="expander", run_once=run_once)


# if __name__ == "__main__":
#     import uvicorn
#     # Run the FastAPI app
#     uvicorn.run(app, host="0.0.0.0", port=8001)