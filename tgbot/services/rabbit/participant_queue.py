import json

import pika


class ParticipantSender:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # self.channel.exchange_declare(exchange='logs', exchange_type='fanout')

        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(exchange='logs', queue=queue_name)

        print(' [*] Waiting for message. To exit press CTRL+C')

    def on_response(self, ch, method, properties, body):
        print(" [x] %r" % body)
        obj = json.loads(body.decode('utf8'))
        print(f'obj={obj}')
        print(f'key1={obj["key1"]}')

    def send(self):
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.on_response, auto_ack=True)

        self.channel.start_consuming()