import logging
import sys
import unittest

sys.path.append(__file__ + "/../..")
from Article import Article


def logging_config() -> None:
    log: logging.Logger = logging.getLogger()
    log.setLevel(logging.DEBUG)

    formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s')

    fh: logging.FileHandler = logging.FileHandler('iytis.log', mode='w', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)    
    log.addHandler(fh)

    ch: logging.StreamHandler = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)


# Test by observation for initial development
def test_qualitative():
    article: Article = Article(r"https://ktla.com/news/local-news/1-dead-2-hospitalized-after-alleged-dui-driver-sends-cars-flying-off-pch-and-onto-rocks-surf-in-pacific-palisades/")

    logging.debug(article.get_title())
    logging.debug(article.get_body())


if __name__ == "__main__":
    logging_config()
    test_qualitative()