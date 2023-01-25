import abc

import requests
from bs4 import BeautifulSoup


# Abstract Base Class
class Article(metaclass=abc.ABCMeta):
    def __init__(self, url) -> None:
        self._url = url
        response = requests.get(url)
        if response.status_code == 200:
            self._content = response.text
        else:
            requests.exceptions.HTTPError(response.status_code)

        self._soup = BeautifulSoup(self._content, 'html.parser')

    @abc.abstractmethod
    def get_title(self) -> str:
        pass
    
    @abc.abstractmethod
    def get_body(self) -> str:
        pass

    def __repr__(self):
        return str(self._soup)
