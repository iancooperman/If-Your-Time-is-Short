import abc
import re
import urllib.parse

import requests
from bs4 import BeautifulSoup


# ALL HANDLERS MUST BE PLACED IN THIS FILE OR THEY WILL BE IGNORED BY Aritcle.py ( specifically Article._choose_handler() )!!!


# Abstract Base Class
class ArticleHandler(metaclass=abc.ABCMeta):
    def __init__(self, url) -> None:
        self._url = url
        self._build_soup(self._url)
        

    def _build_soup(self, url) -> BeautifulSoup:
        response = requests.get(url)
        if response.status_code == 200:
            self._content = response.text
        else:
            requests.exceptions.HTTPError(response.status_code)

        self._soup = BeautifulSoup(self._content, 'html.parser')

    @classmethod
    @abc.abstractmethod
    def _valid_url(self, url) -> bool:
        pass

    @abc.abstractmethod
    def get_title(self) -> str:
        pass
    
    @abc.abstractmethod
    def get_body(self) -> str:
        pass

    def __repr__(self):
        return str(self._soup)

class ReutersArticleHandler(ArticleHandler):

    # five popular domains on /r/news
    #   abcnews.go.com
    #   apnews.com
    #   reuters.com
    #   cnn.com
    #   nbcnews.com

    @classmethod
    def _valid_url(cls, url) -> bool:

        parsed = urllib.parse.urlparse(url)

        # not great, but a lot more readable than trying to do everything with a single regular expression
        return parsed.scheme in ['https', 'http'] and parsed.netloc == "www.reuters.com" and any([
            re.match(r"/world/[a-z]+/.+", parsed.path),
            re.match(r"/legal/.+", parsed.path),
            re.match(r"/business/[a-z]+/.+", parsed.path),
            re.match(r"/technology/.+", parsed.path),
            re.match(r"/lifestyle/.+", parsed.path),
        ]) 

    def get_title(self):
        h1 = self._soup.select_one('h1[data-testid="Heading"]')
        title = h1.get_text()
        return title

    def get_body(self):
        paragraphs = []
        for p in self._soup.select('p[data-testid^="paragraph-"]'):
            paragraphs.append(p.get_text())
        return " ".join(paragraphs)
    
    def __repr__(self):
        return str(self._soup)


class APNewsArticleHandler(ArticleHandler):

    @classmethod
    def _valid_url(cls, url) -> bool:
        pass


    def get_title(self):
        # # normal article
        # h1 = self._soup.select_one('h1[class^="Component-heading-"]')
        # if h1:
        #     title = h1.get_text()
        #     return title

        # backup plan
        title_tag = self._soup.find('title')
        title = title_tag.get_text()[:-10]

        return title

    def get_body(self):
        p_tags = self._soup.select('p[class^="Component-root-"]')

        paragraphs = []

        for p in p_tags:
            paragraph = p.get_text()
            if paragraph != "___":
                paragraphs.append(paragraph)
            else:
                break

        return " ".join(paragraphs)
        

