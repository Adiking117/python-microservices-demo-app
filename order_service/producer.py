import json
import aio_pika


async def send_order(order):

    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq/"
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