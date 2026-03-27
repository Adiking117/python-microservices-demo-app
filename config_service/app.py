from fastapi import FastAPI
import json

app = FastAPI()

with open("config.json") as f:
    CONFIG = json.load(f)


@app.get("/config/{service_name}")
async def get_config(service_name: str):
    service_config = CONFIG.get(service_name)

    if not service_config:
        return {"error": "Service config not found"}

    return service_config