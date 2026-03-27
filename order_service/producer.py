import json
import aio_pika
from config import CONFIG  # ✅ NEW


async def send_order(order):

    connection = await aio_pika.connect_robust(
                CONFIG["RABBITMQ_URL"]   # ✅ from config
            )

    async with connection:

        channel = await connection.channel()

        queue = await channel.declare_queue(
            "order_queue",
            durable=True
        )

        message = aio_pika.Message(
            body=json.dumps(order).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await channel.default_exchange.publish(
            message,
            routing_key=queue.name
        )