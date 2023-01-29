import ArticleHandler


# Wrapper around all domain handlers. Given url, correct handler (if it exists) is chosen automatically so long as it is defined in ArticleHandler.py.
class Article:
    def __init__(self, url):
        self._url = url
        self._choose_handler()

    def _choose_handler(self):
        handlers = ArticleHandler.ArticleHandler.__subclasses__()
        for handler in handlers:
            if handler._valid_url(self._url):
                self._handler = handler(self._url)
                return

        raise NotImplementedError("Appropriate domain handler is either not defined or not detected.")

    def get_title(self):
        return self._handler.get_title()
    
    def get_body(self):
        return self._handler.get_body()


if __name__ == '__main__':
    article = Article('https://www.reuters.com/world/india/bankers-adani-25-bln-share-sale-consider-delay-price-cut-after-rout-2023-01-28/')
    print(article.get_title())
    print()
    print(article.get_body())
