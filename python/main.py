import logging

import nltk.data
from Article import Article
from GPTSummarizer import GPTSummarizer
from praw import Reddit
from Settings import Settings


def comment_format(raw_summary: str) -> str:
    
    # build the comment piece by piece
    comment = "If your time is short:\n"
    comment += "\n"
    


    # core summary formatting
    raw_summary = raw_summary.strip()
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    summary_sentences = tokenizer.tokenize(raw_summary)

    for i in range(len(summary_sentences)): 
        comment += "\t * " + summary_sentences[i] + "\n" # add a tab and a markdown bullet point to the front of each sentence
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

    # retrieve settings
    settings_file_name: str = "settings.json"
    settings: Settings = Settings()
    settings.load_settings(settings_file_name)
    logging.info(f"{settings_file_name} loaded")

    # initialize Reddit instance
    reddit: Reddit = Reddit(
        client_id=settings["reddit"]["client_id"], 
        client_secret=settings["reddit"]["secret"], 
        user_agent=settings["reddit"]["user_agent"],
        username=settings["reddit"]["username"], 
        password=settings["reddit"]["password"]
    )

    logging.info('Reddit instance initialized')

    subreddit_names: list[str] = settings["reddit"]["subreddits"]

    urls = []
    for subreddit_name in subreddit_names:
        subreddit: praw.models.SubredditHelper = reddit.subreddit(subreddit_name) # type: ignore

        post_sort: str = settings["reddit"]["post_sort"]
        post_limit: int = settings["reddit"]["post_limit"]

        generated: str = f"subreddit.{post_sort}(limit={post_limit})"
        logging.debug(f"Generated code: `{generated}`")

        # run generated code
        submissions = list(eval(generated)) # get the top n posts at the time according the given sort
    
    summarizer: GPTSummarizer = GPTSummarizer(settings["OPENAI_API_KEY"])
    for submission in submissions:
        try:
            article: Article = Article(submission.url)
            article_body: str = article.get_body()
            generated_summary: str = summarizer.summarize(article_body)
            formatted_summary: str = comment_format(generated_summary)
            logging.info(f"Article title: {article.get_title()}")
            logging.info(f"Summary:\n{comment_format(formatted_summary)}")

            # submit the comment!
            submission.reply(formatted_summary)

        except NotImplementedError as e:
            logging.warning(f"{submission.url} is not parseable at this time")



if __name__ == "__main__":
    main()