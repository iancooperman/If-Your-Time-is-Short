import configparser
from pathlib import Path
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from newspaper import Article
import logging
import configparser

import openai


class GPTSummarizer:
    def __init__(self, openai_api_key: str, engine: str="text-davinci-003", **kwargs: dict[str, str]):
        openai.api_key = openai_api_key
        self.engine = engine
        self.params = kwargs

        self.command = "Please summarize the following text in exactly 3 sentences, leaving no whitespace above or below the paragraph created: \n"
        
    def summarize(self, text: str) -> str:
        prompt = self.command + text
        completion = openai.Completion.create(engine=self.engine, prompt=prompt, max_tokens=128)
        return completion.choices[0].text # type: ignore
    
    def url_to_summary(self, url: str) -> str | None:
        # parse the url and ensure that the site's robots.txt allows crawling on the url
        try:
            domain: str = urlparse(url).netloc
            scheme: str = urlparse(url).scheme
            robots_txt_url: str = f"{scheme}://{domain}/robots.txt"
            robot_file_parser: RobotFileParser = RobotFileParser(robots_txt_url)
            robot_file_parser.read()

            if robot_file_parser.can_fetch("/u/IfYourTimeIsShort", url): # if crawling is allowed...
                logging.debug(f"{robots_txt_url} allows parsing of {url}")
                
                # retrieve the text content of the article
                article: Article = Article(url)
                article.download()
                article.parse()
                logging.info(f"Article title: {article.title}")
                article_body: str = article.text
                
                # generate a summary from the extracted article text
                generated_summary: str = summarizer.summarize(article_body)
                return generated_summary
            else:
                logging.debug(f"{robots_txt_url} prohibits parsing of {url}")

        except NotImplementedError as e:
            logging.warning(f"{url} is not parseable at this time")

        return None # mypy was yelling at me for not putting this
 

if __name__ == "__main__":
    config: configparser.ConfigParser = configparser.ConfigParser(allow_no_value=True)
    config.read("./" + "config.ini")

    summarizer = GPTSummarizer(config.get("openai", "api_key"))
    summary = summarizer.url_to_summary("https://www.npr.org/2023/07/29/1190701793/economy-fed-earnings-barbie-taylor-swift")
    print(summary)

