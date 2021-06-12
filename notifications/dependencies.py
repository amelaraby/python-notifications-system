from injector import singleton

from mq.message_queue import MessageQueue
from mq.rabbitmq import RabbitMQ


def configure(binder):
    binder.bind(MessageQueue, to=RabbitMQ, scope=singleton)
