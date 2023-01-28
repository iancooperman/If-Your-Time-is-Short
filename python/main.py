import logging
import sys
import time

from Settings import Settings


def wait_one_hour():
    time.sleep(3600)

def main():
    logging.basicConfig(filename='iytis.log', encoding='utf-8', level=logging.DEBUG, format='%(levelname)s [%(asctime)s]: %(message)s (%(filename)s:%(lineno)s)')

    logger = logging.getLogger()


    try:
        while True:
            logger.info("get top 3 posts from Rising in /r/news")
            logger.info("summarize each of them")
            logger.info("return each summary as a comment on their respective post")
            
            logger.info("wait for one hour")
            wait_one_hour()
            
    except Exception as e:
        logging.error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()