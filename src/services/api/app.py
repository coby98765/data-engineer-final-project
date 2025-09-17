import os
from fastapi import FastAPI
from threading import Thread



def api(Manager, name):
    manager = Manager()
    app = FastAPI()
    status = {"value": "stopped"}

    @app.get("/")
    def get_status():
        return {"service": name, "status": status["value"]}

    @app.post("/setup")
    def setup():
        manager.setup()
        status["value"] = "initialized"
        return {"service": name, "status": status["value"]}

    @app.post("/run")
    def run():
        thread = Thread(target=manager.run)
        thread.start()
        status["value"] = "running"
        return {"service": name, "status": status["value"]}

    @app.post("/stop")
    def stop():
        os._exit(1)

    return app
