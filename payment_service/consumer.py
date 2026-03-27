import json
import aio_pika
import asyncio
from db import save_payment

async def consume(config):
    while True:
        try:
            # ✅ Use config passed in, not global
            connection = await aio_pika.connect_robust(
                config["RABBITMQ_URL"]
            )

            channel = await connection.channel()

            queue = await channel.declare_queue(
                "order_queue",
                durable=True
            )

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        order = json.loads(message.body.decode())
                        print("Received order:", order)

                        try:
                            save_payment(order, config)   # ✅ pass config
                        except Exception as e:
                            print("DB insert failed:", e)

        except Exception as e:
            print("RabbitMQ not ready, retrying in 5s:", e)
            await asyncio.sleep(5)