import configparser
import logging
import sqlite3
import time

import praw
from GPTSummarizer import GPTSummarizer
from praw import Reddit
from util import *

# globals
config_file_name: str = "config.ini"
config: configparser.ConfigParser = configparser.ConfigParser(allow_no_value=True)
config.read(config_file_name)
logging.info(f"{config_file_name} loaded")
summarizer = GPTSummarizer(config.get("openai", "API_Key"))


def comment_format(raw_summary: str) -> str:
    # build the comment piece by piece
    comment = "If your time is short:\n"
    comment += "\n"
    comment += raw_summary
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

def db_init() -> sqlite3.Cursor:
    connection: sqlite3.Connection = sqlite3.connect("iytis.db")
    cursor: sqlite3.Cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS submissions (id TEXT PRIMARY KEY)")

    return cursor

def main() -> None:
    # initialize logger
    logging_config()

    reddit: Reddit = reddit_init()
    logging.info('Reddit instance initialized')

    db = db_init()

    subreddit_names: list[str] = config.get("reddit.submissions", "subreddits").split(",")

    # time in seconds before refreshing the posts
    refresh_delay: float = float(config.get("reddit.submissions", "refresh_delay"))

    # mainloop
    while True:
        urls: list[str] = []
        for subreddit_name in subreddit_names:
            subreddit: praw.models.SubredditHelper = reddit.subreddit(subreddit_name) # type: ignore

            post_sort: str = config.get("reddit.submissions", "post_sort")
            post_limit: int = config.getint("reddit.submissions", "post_limit")

            generated: str = f"subreddit.{post_sort}(limit={post_limit})"
            logging.debug(f"Generated code: `{generated}`")

            # run generated code
            # TODO: using eval is a terrible idea
            submissions: list[praw.models.Submission] = list(eval(generated)) # get the top n posts at the time according the given sort
        
        for submission in submissions:
            db.execute(f"SELECT * FROM submissions WHERE id = '{submission.id}'")
            if db.fetchone():
                continue
            else:
                db.execute(f"INSERT INTO submissions VALUES ('{submission.id}')")
            
            
            # parse the submission's url and ensure that the site's robots.txt allows crawling on the url
                url: str = submission.url
                generated_summary: str = summarizer.url_to_summary(url) #type: ignore

                # format the generated summary into something more visually appealing
                if generated_summary:
                    formatted_summary: str = comment_format(generated_summary)
                
                    logging.info(f"Summary:\n{formatted_summary}")

                    # submit the comment!
                    submission.reply(formatted_summary)

        time.sleep(refresh_delay)
        logging.info(f"Halting for {refresh_delay} {'seconds' if refresh_delay != 1 else 'second'}.")

if __name__ == "__main__":
    main()