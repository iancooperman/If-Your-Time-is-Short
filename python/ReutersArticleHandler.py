import abc

import requests
from ArticleHandler import ArticleHandler
from bs4 import BeautifulSoup
import re
import urllib.parse


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


if __name__ ==  "__main__":
    assert ReutersArticleHandler._valid_url("https://www.reuters.com/legal/ftx-founder-bankman-fried-objects-tighter-bail-says-prosecutors-sandbagged-him-2023-01-28/")
    assert ReutersArticleHandler._valid_url("https://www.reuters.com/technology/twitter-research-group-stall-complicates-compliance-with-new-eu-law-2023-01-27/")
