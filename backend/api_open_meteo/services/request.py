import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from .request_abstract import RequestAbstract


class RequestService(RequestAbstract):

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10))
    def _get(self, url: str, params: dict = None, **kwargs):
        response = requests.get(
            url=url,
            params=params,
        )
        response.raise_for_status()
        return response.json()

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10))
    def _post(self, url: str, params: dict = None, **kwargs):
        response = requests.get(
            url=url,
            params=params,
        )
        response.raise_for_status()
        return response.json()


