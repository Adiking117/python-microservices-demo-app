from fastapi import FastAPI, Request
import asyncio
import threading
import time
import httpx
import py_eureka_client.eureka_client as eureka_client
import socket

from producer import send_order
from breaker import rabbitmq_breaker
from config import load_config, CONFIG  # ✅ NEW

app = FastAPI()


# 🔹 Startup: Load config + Eureka
@app.on_event("startup")
async def startup():

    # ✅ Load config
    await load_config("order_service")

    # 🔹 Eureka registration
    def register():
        while True:
            try:
                eureka_client.init(
                    eureka_server="http://eureka:8761/eureka/",
                    app_name="order-service",
                    instance_port=8000,
                    instance_host=socket.gethostname()
                )
                print(f"✅ Order Service registered with Eureka ({socket.gethostname()})")
                break
            except Exception as e:
                print("❌ Eureka not ready (Order), retrying...", e)
                time.sleep(5)

    threading.Thread(target=register).start()


# 🔹 Get Payment Service URL from Eureka
async def get_payment_service_url():
    try:
        app_obj = await eureka_client.get_application(
            "http://eureka:8761/eureka/",
            CONFIG["PAYMENT_SERVICE_NAME"]   # ✅ from config
        )

        if not app_obj or not app_obj.instances:
            raise Exception("Payment service not found")

        import random
        instance = random.choice(app_obj.instances)
        host = instance.ipAddr or instance.hostName
        port = instance.port.port

        return f"http://{host}:{port}"

    except Exception as e:
        raise Exception("Payment service lookup failed") from e


@app.post("/create-order")
async def create_order(request: Request):

    order = await request.json()

    # 🔹 Send to RabbitMQ (with circuit breaker)
    def sync_send(o):
        asyncio.run(send_order(o))

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            rabbitmq_breaker.call,
            sync_send,
            order
        )
    except Exception as e:
        print("Circuit breaker:", e)
        return {"message": "RabbitMQ unavailable"}

    # 🔥 OPTIONAL: Keep HTTP call (or remove if event-driven only)
    try:
        payment_url = await get_payment_service_url()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{payment_url}/process-payment",
                json=order,
                timeout=CONFIG["REQUEST_TIMEOUT"]   # ✅ from config
            )

        return {
            "message": "Order placed + Payment triggered",
            "order": order,
            "payment_response": response.json()
        }

    except Exception as e:
        print("Payment service call failed:", e)
        return {
            "message": "Order placed, but payment service unavailable",
            "order": order
        }