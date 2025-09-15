from fastapi import FastAPI
from threading import Thread
import subprocess


from src.services.parser.manager_city import Manager

app = FastAPI()

manager = None
thread = None
status = "stopped"


@app.post("/setup")
def setup():
    global manager, status
    manager = Manager()
    manager.setup()
    status = "initialized"
    return {"status": status}


@app.post("/run")
def run():
    global thread, status
    #
    def run_manager():
        global status
        status = "running"
        manager.run()
        status = "stopped"
    #
    thread = Thread(target=run_manager, daemon=True)
    thread.start()
    return {"status": "running"}


@app.get("/status")
def get_status():
    return {"status": status}


@app.post("/stop")
def stop():
    global status, manager
    manager.kafka.sub().close()
    status = "stopped"
    return {"status": status}