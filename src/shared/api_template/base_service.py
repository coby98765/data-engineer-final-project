from fastapi import FastAPI
from pydantic import BaseModel
from typing import Callable, Optional
from ..logging import get_logger

class StartRequest(BaseModel):
    params: dict | None = None

def build_service_app(service_name: str, run_once: Callable[[], None]):
    app = FastAPI(title=f"{service_name} service")
    log = get_logger(service_name)
    state = {"status":"idle","last_error":None}

    @app.get("/status")
    def status():
        return state

    @app.post("/start")
    def start(req: StartRequest):
        if state["status"] == "running":
            return {"ok": False, "msg": "already running"}
        state["status"] = "running"
        state["last_error"] = None
        try:
            run_once()
            state["status"] = "idle"
            return {"ok": True}
        except Exception as e:
            log.error("run_once_failed", error=str(e))
            state["status"] = "error"
            state["last_error"] = str(e)
            return {"ok": False, "error": str(e)}

    return app
