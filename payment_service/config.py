import httpx

async def load_config(service_name):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://config_service:8003/config/{service_name}"
        )
        config = response.json()

    print(f"✅ Loaded config for {service_name}:", config)
    return config   # return the dict instead of relying on a global