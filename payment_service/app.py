from fastapi import FastAPI
import asyncio
import threading
import time
import py_eureka_client.eureka_client as eureka_client
import socket

from consumer import consume
from db import init_db, get_all_orders
from config import load_config

app = FastAPI()
CONFIG = {}   # keep a module-level reference


@app.on_event("startup")
async def startup():
    global CONFIG
    CONFIG = await load_config("payment_service")   # ✅ load config first

    init_db(CONFIG)   # ✅ pass config explicitly
    asyncio.create_task(consume(CONFIG))

    def register():
        while True:
            try:
                eureka_client.init(
                    eureka_server="http://eureka:8761/eureka/",
                    app_name="payment-service",
                    instance_port=8001,
                    instance_host=socket.gethostname()
                )
                print(f"✅ Payment Service registered with Eureka ({socket.gethostname()})")
                break
            except Exception as e:
                print("❌ Eureka not ready (Payment), retrying...", e)
                time.sleep(5)

    threading.Thread(target=register).start()


@app.get("/")
async def home():
    return {
        "service": "payment service running",
        "instance": socket.gethostname()
    }


@app.post("/process-payment")
async def process_payment(order: dict):
    print(f"Processing payment via HTTP ({socket.gethostname()}):", order)
    return {
        "status": "Payment processed",
        "order_id": order.get("order_id"),
        "instance": socket.gethostname()
    }


@app.get("/orders")
async def get_orders():
    try:
        print(f"Fetching orders from DB ({socket.gethostname()})")
        orders = get_all_orders(CONFIG)   # ✅ pass config explicitly
        return {
            "count": len(orders),
            "orders": orders
        }
    except Exception as e:
        return {
            "error": "Failed to fetch orders",
            "details": str(e)
        }