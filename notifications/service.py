from handlers.sms_handler import SMSHandler
from handlers.email_handler import EmailHandler
from handlers.push_handler import PushHandler


class NotificationService:
    def __init__(self) -> None:
        self._handlers = {
            'sms': SMSHandler,
            'email': EmailHandler,
            'push': PushHandler,
        }

    def send(self, data) -> None:
        handler = self._handlers[data['type']]()
        handler.send(data)

