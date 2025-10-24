from abc import ABC, abstractmethod


class RequestAbstract(ABC):

    @abstractmethod
    def _get(self, **kwargs):
        ...

    @abstractmethod
    def _post(self, **kwargs):
        ...
