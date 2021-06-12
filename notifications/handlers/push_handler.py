from .notification_handler import NotificationHandler

class PushHandler(NotificationHandler):
    def send(self, data):
        print('Sending via Push Notification')