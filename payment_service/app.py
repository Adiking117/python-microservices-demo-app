from fastapi import FastAPI
import asyncio
import threading
import time
import py_eureka_client.eureka_client as eureka_client

from consumer import consume
from db import init_db

app = FastAPI()


# 🔹 Eureka Registration
@app.on_event("startup")
async def register_service():

    def register():
        while True:
            try:
                eureka_client.init(
                    eureka_server="http://eureka:8761/eureka/",
                    app_name="payment-service",
                    instance_port=8001,
                    instance_host="payment_service"
                )
                print("✅ Payment Service registered with Eureka")
                break
            except Exception as e:
                print("❌ Eureka not ready (Payment), retrying...", e)
                time.sleep(5)

    threading.Thread(target=register).start()


# 🔹 Startup tasks
@app.on_event("startup")
async def startup_tasks():
    init_db()
    asyncio.create_task(consume())


# 🔹 Health check
@app.get("/")
async def home():
    return {"service": "payment service running"}

@app.post("/process-payment")
async def process_payment(order: dict):

    print("Processing payment via HTTP:", order)

    return {
        "status": "Payment processed",
        "order_id": order.get("order_id")
    }