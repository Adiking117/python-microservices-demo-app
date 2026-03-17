from fastapi import FastAPI, Request
import asyncio
from producer import send_order
from breaker import rabbitmq_breaker

app = FastAPI()


def sync_send(order):
    """Sync wrapper for circuit breaker"""
    asyncio.run(send_order(order))


@app.post("/create-order")
async def create_order(request: Request):

    order = await request.json()

    try:
        loop = asyncio.get_event_loop()

        await loop.run_in_executor(
            None,
            rabbitmq_breaker.call,
            sync_send,
            order
        )

        return {
            "message": "Order placed successfully",
            "order": order
        }

    except Exception as e:

        print("Circuit breaker triggered:", e)

        return {
            "message": "RabbitMQ unavailable, try later"
        }