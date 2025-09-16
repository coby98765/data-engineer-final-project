import os
from fastapi import FastAPI
from threading import Thread



def api(Manager, name):
    manager = Manager()
    print("1")
    app = FastAPI()
    print("2")
    status = {"value": "stopped"}
    print("3")

    @app.get("/")
    def get_status():
        print("4")
        return {"service": name, "status": status["value"]}

    @app.post("/setup")
    def setup():
        print("1")
        manager.setup()
        print("1")
        status["value"] = "initialized"
        return {"service": name, "status": status["value"]}

    @app.post("/run")
    def run():
        thread = Thread(target=manager.run)
        thread.start()
        status["value"] = "running"
        return {"service": name, "status": status["value"]}

    @app.get("/status")
    def get_status():
        return {"service": name, "status": status["value"]}

    @app.post("/stop")
    def stop():
        os._exit(1)

    return app
