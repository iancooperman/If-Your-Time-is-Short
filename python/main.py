import configparser
import logging

import nltk.data
from GPTSummarizer import GPTSummarizer
from newspaper import Article
from praw import Reddit
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse


def comment_format(raw_summary: str) -> str:
    
    # build the comment piece by piece
    comment = "If your time is short:\n"
    comment += "\n"
    


    # core summary formatting
    raw_summary = raw_summary.strip()
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    summary_sentences = tokenizer.tokenize(raw_summary)

    for i in range(len(summary_sentences)): 
        comment += "* " + summary_sentences[i] + "\n" # add a tab and a markdown bullet point to the front of each sentence
        comment += "\n"

    comment += "----------------------------------------------------------------\n"
    comment += "\n"
    comment += "I am a bot in training. Please feel free to DM me any feedback you have."


    return comment

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


def main() -> None:
    # initialize logger
    logging_config()

    # retrieve config
    config_file_name: str = "config.ini"
    config: configparser.ConfigParser = configparser.ConfigParser(allow_no_value=True)
    config.read(config_file_name)
    logging.info(f"{config_file_name} loaded")

    # initialize Reddit instance
    reddit: Reddit = Reddit(
        client_id=config.get("reddit.credentials", "client_id"),
        client_secret=config.get("reddit.credentials", "client_secret"), 
        user_agent=config.get("reddit.credentials", "user_agent"),
        username=config.get("reddit.credentials", "username"), 
        password=config.get("reddit.credentials", "password"),
    )

    logging.info('Reddit instance initialized')

    subreddit_names: list[str] = config.get("reddit.submissions", "subreddits").split(",")

    urls: list[str] = []
    for subreddit_name in subreddit_names:
        subreddit: praw.models.SubredditHelper = reddit.subreddit(subreddit_name) # type: ignore

        post_sort: str = config.get("reddit.submissions", "post_sort")
        post_limit: int = config.getint("reddit.submissions", "post_limit")

        generated: str = f"subreddit.{post_sort}(limit={post_limit})"
        logging.debug(f"Generated code: `{generated}`")

        # run generated code
        submissions = list(eval(generated)) # get the top n posts at the time according the given sort
    
    summarizer: GPTSummarizer = GPTSummarizer(config.get("openai", "API_Key"))
    for submission in submissions:
        try:
            # parse the submission's url and ensure that the site's robots.txt allows crawling on the url
            url: str = submission.url
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
                article_body: str = article.text
                
                # generate a summary from the extracted article text
                generated_summary: str = summarizer.summarize(article_body)
                
                # format the generated summary into something more visually appealing
                formatted_summary: str = comment_format(generated_summary)
                logging.info(f"Article title: {article.title}")
                logging.info(f"Summary:\n{comment_format(formatted_summary)}")

                # submit the comment!
                submission.reply(formatted_summary)
            else:
                logging.debug(f"{robots_txt_url} prohibits parsing of {url}")

        except NotImplementedError as e:
            logging.warning(f"{submission.url} is not parseable at this time")



if __name__ == "__main__":
    main()