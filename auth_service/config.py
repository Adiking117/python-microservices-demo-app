import httpx
import asyncio

CONFIG = {}

async def load_config(service_name):
    global CONFIG

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://config_service:8003/config/{service_name}"
        )
        CONFIG = response.json()

    print(f"✅ Loaded config for {service_name}:", CONFIG)