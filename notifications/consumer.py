#!/usr/bin/env python
import os
import sys
import json
from injector import inject, Injector
from dependencies import configure
from mq.message_queue import MessageQueue
from service import NotificationService


class NotificationConsumer:
    @inject
    def __init__(self, mq: MessageQueue):
        self._mq = mq

    def handle(self):
        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            NotificationService().send(json.loads(body))
            ch.basic_ack(delivery_tag=method.delivery_tag)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self._mq.subscribe(callback)


if __name__ == '__main__':
    try:
        injector = Injector(configure)
        consumer = injector.get(NotificationConsumer)
        consumer.handle()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
