import pika
import os
from .message_queue import MessageQueue


class RabbitMQ(MessageQueue):
    def __init__(self):
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv('MQ_HOST'), retry_delay=5, connection_attempts=5)
        )

    def __del__(self):
        self._connection.close()

    def __declareQueue(self, channel):
        channel.queue_declare(queue=os.getenv('MQ_QUEUE'), durable=True)

    def publish(self, payload: bytes):
        channel = self._connection.channel()
        self.__declareQueue(channel)

        channel.basic_publish(exchange='',
                              routing_key=os.getenv('MQ_QUEUE'),
                              body=payload,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,
                              ))

    def subscribe(self, callback):
        channel = self._connection.channel()
        self.__declareQueue(channel)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=os.getenv('MQ_QUEUE'), on_message_callback=callback)

        channel.start_consuming()
