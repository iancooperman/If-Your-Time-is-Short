import configparser
import logging
import sqlite3
import time
import sys

import praw
from GPTSummarizer import GPTSummarizer
from praw import Reddit
from util import *
from SubmissionDB import SubmissionDB

# globals
config: configparser.ConfigParser = None
summarizer: GPTSummarizer = None

# utility function for loading the settings from a config file
def load_config(config_file_name: str = "config.ini"): # default file name is 'config.ini'
    global config
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(config_file_name)
    logging.info(f"{config_file_name} loaded")


def comment_format(raw_summary: str) -> str:
    # build the comment piece by piece
    comment = "If your time is short:\n"
    comment += "\n"
    comment += raw_summary
    comment += "\n"
    comment += "----------------------------------------------------------------\n"
    comment += "\n"
    comment += "I am a bot in training. Please feel free to DM any feedback you have to my creator, /u/BananaZen314159."

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

# def db_init() -> sqlite3.Connection:
#     connection: sqlite3.Connection = sqlite3.connect("iytis.db")
#     cursor: sqlite3.Cursor = connection.cursor()
#     cursor.execute("CREATE TABLE IF NOT EXISTS submissions (id TEXT PRIMARY KEY)")
#     connection.commit()

#     return connection

def main() -> None:
    # parse command line arguments
    argv: list[str] = sys.argv

    # load desired config file
    try:
        config_file_name: str = argv[1]
    except IndexError:
        config_file_name = "config.ini" # default filename of 'config.ini'

    load_config(config_file_name)


    # initialize logger
    logging_config()

    global summarizer
    summarizer = GPTSummarizer(config.get("openai", "API_Key"))

    reddit: Reddit = reddit_init()
    logging.info('Reddit instance initialized')

    # db_conn = db_init()
    iytis_db: SubmissionDB = SubmissionDB('iytis.db')
    

    subreddit_names: list[str] = config.get("reddit.submissions", "subreddits").split(",")
    logging.info(f"Subreddits to monitor: {', '.join(subreddit_names)}")

    # time in seconds before refreshing the posts
    subreddit_refresh_delay: float = float(config.get("reddit.submissions", "refresh_delay"))

    # mainloop
    done: bool = False
    while not done:
        submission_urls: list[str] = []
        for subreddit_name in subreddit_names:
            logging.info(f"Scanning /r/{subreddit_name}")
            subreddit: praw.models.SubredditHelper = reddit.subreddit(subreddit_name) # type: ignore

            submission_sort: str = config.get("reddit.submissions", "post_sort").lower()
            submission_limit: int = config.getint("reddit.submissions", "post_limit")

            # generated_code_for_submission_generator_creation: str = f"subreddit.{submission_sort}(limit={submission_limit})"
            # logging.debug(f"Generated code: `{generated_code_for_submission_generator_creation}`")

            # # run generated code
            # # TODO: using eval is a terrible idea
            # submissions: list[praw.models.Submission] = list(eval(generated_code_for_submission_generator_creation)) # get the top n posts at the time according the given sort

            submissions: list[praw.models.Submission] = None
            match submission_sort:
                case "hot":
                    submissions = list(subreddit.hot(limit=submission_limit))
                case "new":
                    submissions = list(subreddit.new(limit=submission_limit))
                case "rising":
                    submissions = list(subreddit.rising(limit=submission_limit))
                case "top":
                    submissions = list(subreddit.top(limit=submission_limit))
                case _:
                    logging.error(f"Invalid submission sort option: {submission_sort}. Terminating.")
                    quit(1)
            logging.info(f"Sorting by {submission_sort}")
        
            for submission in submissions:
                # db_cursor = db_conn.cursor()
                # db_cursor.execute(f"SELECT * FROM submissions WHERE id = '{submission.id}'")
                # submission_already_seen: bool = db_cursor.fetchone()
                submission_already_seen: bool = iytis_db.submission_present(submission.id)
                if submission_already_seen:
                    continue
                else:
                    # db_cursor.execute(f"INSERT INTO submissions VALUES ('{submission.id}')")
                    # db_conn.commit()
                    iytis_db.insert_submission(submission.id)
                
                # parse the submission's url and ensure that the site's robots.txt allows crawling on the url
                submission_url: str = submission.url
                generated_submission_summary: str = summarizer.url_to_summary(submission_url) #type: ignore

                # format the generated summary into something more visually appealing
                if generated_submission_summary:
                    formatted_submission_summary: str = comment_format(generated_submission_summary)
                
                    logging.info(f"Summary:\n{formatted_submission_summary}")

                    # submit the comment!
                    submission.reply(formatted_submission_summary)

        logging.info(f"Halting for {subreddit_refresh_delay} {'seconds' if subreddit_refresh_delay != 1 else 'second'}.")
        time.sleep(subreddit_refresh_delay)

if __name__ == "__main__":
    main()