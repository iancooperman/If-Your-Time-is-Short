import configparser
from pathlib import Path
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from newspaper import Article
from newspaper.article import ArticleException
import logging
import configparser

import openai


class GPTSummarizer:
    def __init__(self, openai_api_key: str, model: str="gpt-3.5-turbo", **kwargs: dict[str, str]):
        openai.api_key = openai_api_key
        self.model = model
        self.params = kwargs

        self.prompt = 'You will be given the complete text of an online news article. Please summarize the article in exactly 3 bullet points, one single, complete, non-run-on sentence per bullet. Output in markdown.'
        # example text sourced from https://www.politifact.com/factchecks/2023/jul/24/kamala-harris/do-Florida-school-standards-say-enslaved-people/
        self.example = '- The Florida Board of Education set new social studies standards for middle schoolers July 19.\n- In a section about the duties and trades performed by enslaved people, the state adopted a clarification that said "instruction includes how slaves developed skills which, in some instances, could be applied for their personal benefit.\n- Experts on Black history said that such language is factually misleading and offensive."'
        
    def summarize(self, text: str) -> str:
        prompt = self.prompt + text
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "assistant", "content": self.example},
                {"role": "user", "content": text}
            ]
        )
        logging.debug(response)
        return response["choices"][0]["message"]["content"] # type: ignore
    
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

        except (NotImplementedError,  ArticleException) as e:
            logging.warning(f"{url} is not parseable at this time")
            logging.warning(e)

        return None # mypy was yelling at me for not putting this
 

if __name__ == "__main__":
    config: configparser.ConfigParser = configparser.ConfigParser(allow_no_value=True)
    config.read("./" + "config.ini")

    summarizer = GPTSummarizer(config.get("openai", "api_key"))
    summary = summarizer.url_to_summary("https://www.iflscience.com/the-worlds-largest-wind-turbine-has-been-switched-on-70047")
    print(summary)

