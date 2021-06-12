from .notification_handler import NotificationHandler


class SMSHandler(NotificationHandler):
    def send(self, data):
        print('Sending via SMS')
