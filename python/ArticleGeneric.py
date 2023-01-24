from bs4 import BeautifulSoup
import requests


class ArticleGeneric:
    def __init__(self, url):
        self._url = url
        response = requests.get(url)
        if response.status_code == 200:
            self._content = response.text
        else:
            requests.exceptions.HTTPError(response.status_code)

        self._soup = BeautifulSoup(self._content, 'html.parser')


    # five popular domains on /r/news
    #   abcnews.go.com
    #   apnews.com
    #   reuters.com
    #   cnn.com
    #   nbcnews.com
    def get_body(self):
        body = self._soup.select_one('div[class^="article-body__content"]')
        body_text = body.get_text()
        return body_text


    def __repr__(self):
        return str(self._soup)


if __name__ ==  "__main__":
    article = ArticleGeneric("https://www.reuters.com/world/us/seven-dead-shooting-half-moon-bay-calif-cbs-news-2023-01-24/")
    print(article.get_body())
