from abc import ABC, abstractmethod

class MessageQueue(ABC):
    @abstractmethod
    def publish(self, data):
        pass

    @abstractmethod
    def subscribe(self, callback):
        pass