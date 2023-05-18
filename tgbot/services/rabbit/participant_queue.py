import json

from aio_pika import DeliveryMode, Message, connect


class ParticipantSender:
    # def __init__(self):
    #     self.connection = pika.BlockingConnection(
    #         pika.ConnectionParameters(host='localhost'))
    #     self.channel = self.connection.channel()
    #     self.channel.queue_declare(queue='participant', exclusive=True)
    #     print(' [*] Waiting for message. To exit press CTRL+C')
    #
    # def send(self, message):
    #     print(f'message={message}')
    #     self.channel.basic_publish(
    #         exchange='',
    #         routing_key='participant',
    #         body=message,
    #         properties=pika.BasicProperties(
    #             delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    #         )
    #     )
    #     self.connection.close()
    def __init__(self):
        pass

    async def send(self, message):
        self.connection = await connect("amqp://guest:guest@localhost/")
        async with self.connection:
            # Creating a channel
            channel = await self.connection.channel()
            await channel.set_qos(prefetch_count=1)

            # Declaring queue
            queue = await channel.declare_queue("participant", durable=True)

            # Sending the message
            await channel.default_exchange.publish(
                Message(message.encode(), delivery_mode=DeliveryMode.PERSISTENT),
                routing_key=queue.name,
            )

            print(f" [x] Sent -> {message}")
