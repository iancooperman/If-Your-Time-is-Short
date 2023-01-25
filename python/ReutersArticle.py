import abc

import requests
from Article import Article
from bs4 import BeautifulSoup


class ReutersArticle(Article):
    # def __init__(self, url):
    #     self._url = url
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         self._content = response.text
    #     else:
    #         requests.exceptions.HTTPError(response.status_code)

    #     self._soup = BeautifulSoup(self._content, 'html.parser')


    # five popular domains on /r/news
    #   abcnews.go.com
    #   apnews.com
    #   reuters.com
    #   cnn.com
    #   nbcnews.com

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


if __name__ ==  "__main__":
    article = ReutersArticle("https://www.reuters.com/world/us/seven-dead-shooting-half-moon-bay-calif-cbs-news-2023-01-24/")
    print(article.get_body())
    print(article.get_title())
