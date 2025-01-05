import configparser
import logging
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import openai
from newspaper import Article
from newspaper import Config
from newspaper.article import ArticleException
from util import *


logger: logging.Logger = logging.getLogger("iytis_log")

class GPTSummarizer:
    def __init__(self, openai_api_key: str, model: str="gpt-3.5-turbo", **kwargs: dict[str, str]):
        openai.api_key = openai_api_key
        self.model = model
        self.params = kwargs

        self.prompt = 'You will be given the complete text of an online news article. Please summarize the article in exactly 3 bullet points, one single, complete, non-run-on sentence per bullet. Output in markdown.'
        # example text sourced from https://www.politifact.com/factchecks/2023/jul/24/kamala-harris/do-Florida-school-standards-say-enslaved-people/
        self.example = '- The Florida Board of Education set new social studies standards for middle schoolers July 19.\n- In a section about the duties and trades performed by enslaved people, the state adopted a clarification that said "instruction includes how slaves developed skills which, in some instances, could be applied for their personal benefit.\n- Experts on Black history said that such language is factually misleading and offensive."'

        self._newspaper_config = Config()
        self._newspaper_config.browser_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        
    def summarize(self, text: str) -> (str | None):
        if len(text) <= 600: # if the given text is already short enough to be considered a summary, then there is no point in summarizing it.
            return None

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "assistant", "content": self.example},
                {"role": "user", "content": text}
            ]
        )
        logger.debug(response)
        return response["choices"][0]["message"]["content"] # type: ignore
    
    # Given a url, provide a 3-bulleted summary of the news article the url directs to
    def url_to_summary(self, url: str) -> str | None:
        # parse the url and ensure that the site's robots.txt allows crawling on the url
        try:
            domain: str = urlparse(url).netloc
            scheme: str = urlparse(url).scheme
            robots_txt_url: str = f"{scheme}://{domain}/robots.txt"
            robot_file_parser: RobotFileParser = RobotFileParser()
            robot_file_parser.set_url(robots_txt_url)
            robot_file_parser.read()

            if robot_file_parser.can_fetch(self._newspaper_config.browser_user_agent, url): # if crawling is allowed...
                logger.debug(f"{robots_txt_url} allows parsing of {url} by user agent {self._newspaper_config.browser_user_agent}")
                
                # retrieve the text content of the article
                article: Article = Article(url, config=self._newspaper_config)
                article.download()
                article.parse()
                logger.info(f"Article title: {article.title}")
                article_body: str = article.text
                
                # generate a summary from the extracted article text
                generated_summary: str | None = self.summarize(article_body)
                return generated_summary
            else:
                logger.debug(f"{robots_txt_url} prohibits parsing of {url} by user agent {self._newspaper_config.browser_user_agent}")

        except Exception as e:
            logger.warning(f"{url} is not parseable at this time")
            logger.warning(e)

        return None # mypy was yelling at me for not putting this
 

if __name__ == "__main__":
    config: configparser.ConfigParser = configparser.ConfigParser(allow_no_value=True)
    config.read("./" + "config.ini")

    logger_init()

    summarizer = GPTSummarizer(config.get("openai", "api_key"))
    summary = summarizer.url_to_summary("https://www.washingtonpost.com/national-security/2023/07/22/air-force-general-ai-judeochristian/")
    print(summary)

