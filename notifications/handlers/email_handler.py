from .notification_handler import NotificationHandler

class EmailHandler(NotificationHandler):
    def send(self, data):
        print('Sending via Email')