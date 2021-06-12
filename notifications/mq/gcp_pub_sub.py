import pika

from .message_queue import MessageQueue


class GcpPubSub(MessageQueue):
    def publish(self, payload: bytes):
        print('TO BE IMPLEMENTED')

        return True

    def subscribe(self, callback):
        print('TO BE IMPLEMENTED')

