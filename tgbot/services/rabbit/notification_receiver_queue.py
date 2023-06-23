import asyncio
import json

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage

from tgbot import config
from tgbot.controllers.user_controller import send_message


class NotificationReceiverQueue:
    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_running_loop()
        self.connection = None

    async def connect(self):
        # Perform connection
        self.connection = await connect(config.load_config('.env').rabbit.dsn())

    async def on_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            print(f" [x] Received message {message!r}")
            await asyncio.sleep(message.body.count(b'.'))
            print(f"     Message body is: {message.body!r}")
            text_decoded = message.body.decode()
            records = json.loads(text_decoded)
            print(f'records={records}')
            await send_message(self.bot, records)

    async def main(self) -> None:
        async with self.connection:
            # Creating a channel
            channel = await self.connection.channel()
            await channel.set_qos(prefetch_count=1)

            # Declaring queue
            queue = await channel.declare_queue(
                "reminder_queue",
                durable=True,
            )

            # Start listening the queue with name 'task_queue'
            await queue.consume(self.on_message)

            print(" [*] Waiting for messages. To exit press CTRL+C")
            await asyncio.Future()