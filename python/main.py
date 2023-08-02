import configparser
import logging

import nltk.data
from GPTSummarizer import GPTSummarizer
from praw import Reddit
from util import *

# globals
config_file_name: str = "config.ini"
config: configparser.ConfigParser = configparser.ConfigParser(allow_no_value=True)
config.read("../" + config_file_name)
logging.info(f"{config_file_name} loaded")
summarizer = GPTSummarizer(config.get("openai", "API_Key"))

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


def reddit_init() -> Reddit:
    # initialize Reddit instance
    reddit: Reddit = Reddit(
        client_id=config.get("reddit.credentials", "client_id"),
        client_secret=config.get("reddit.credentials", "client_secret"), 
        user_agent=config.get("reddit.credentials", "user_agent"),
        username=config.get("reddit.credentials", "username"), 
        password=config.get("reddit.credentials", "password"),
    )

    return reddit


def main() -> None:
    # initialize logger
    logging_config()

    

    reddit: Reddit = reddit_init()
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
        # parse the submission's url and ensure that the site's robots.txt allows crawling on the url
            url: str = submission.url
            generated_summary: str = url_to_summary(url)
            
            # format the generated summary into something more visually appealing
            formatted_summary: str = comment_format(generated_summary)
            
            logging.info(f"Summary:\n{comment_format(formatted_summary)}")

            # submit the comment!
            submission.reply(formatted_summary)
            



if __name__ == "__main__":
    main()