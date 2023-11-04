import asyncio
import json
import logging

from aio_pika import connect, connect_robust
from aio_pika.abc import AbstractIncomingMessage

from tgbot import config
from tgbot.controllers.user_controller import send_message, send_message_to_customer

logger = logging.getLogger(__name__)

class NotificationReceiverQueue:
    def __init__(self, bot, loop):
        self.bot = bot
        self.loop = loop #asyncio.get_running_loop()
        self.connection = None

    # async def __aenter__(self):
    #     self.connection = await connect_robust(config.load_config('.env').rabbit.dsn(), loop=self.loop, timeout=60)
    #
    # async def __aexit__(self, exc_type, exc_val, exc_tb):
    #     self.connection.close()
    #     self.loop.close()

    async def connect(self):
        # try:
            # Perform connection
        self.connection = await connect_robust(config.load_config('.env').rabbit.dsn(), loop=self.loop, timeout=60)
        # except:
        #     self.connection = None

    async def on_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            # logger.info(f" [x] Received message {message!r}")
            # await asyncio.sleep(message.body.count(b'.'))
            # logger.info(f"     Message body is: {message.body!r}")
            text_decoded = message.body.decode()
            record = json.loads(text_decoded)
            logger.info(f'record={record}')
            # send message to bot
            await send_message(self.bot, record)

    async def on_message_customer(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            # logger.info(f" [x] Received message {message!r}")
            # await asyncio.sleep(message.body.count(b'.'))
            # logger.info(f"     Message body is: {message.body!r}")
            text_decoded = message.body.decode()
            record = json.loads(text_decoded)
            logger.info(f'record={record}')
            # send message to bot
            await send_message_to_customer(self.bot, record)

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

            # queue for customer regular notifications
            queue_customer = await channel.declare_queue(
                "customer_notif_queue",
                durable=True,
            )

            # Start listening the queue with name 'reminder_queue'
            await queue.consume(self.on_message)

            # Start listening the queue with name 'customer_notif_queue'
            await queue_customer.consume(self.on_message_customer)

            logging.getLogger(__name__).info(" [*] Waiting for messages. To exit press CTRL+C")
            await asyncio.Future(loop=self.loop)