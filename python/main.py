import logging

from Article import Article
from praw import Reddit
from Settings import Settings
from GPTSummarizer import GPTSummarizer


def comment_format(raw_summary: str) -> str:
    raw_summary = raw_summary.strip()

    summary_sentences = raw_summary.split('. ')
    for i in range(len(summary_sentences)): # add a markdown bullet point to the front of each sentence
        summary_sentences[i] = '* ' + summary_sentences[i]
    
    # glue the sentences back together and return
    return "\n".join(summary_sentences)


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

    urls: list[str] = []
    for subreddit_name in subreddit_names:
        for submission in reddit.subreddit(subreddit_name).hot(limit=3): # get the top 3 posts at the time 
            urls.append(submission.url)
        for post in posts: # get the top 3 posts at the time 
            urls.append(post.url)

    
    summarizer: GPTSummarizer = GPTSummarizer(settings["OPENAI_API_KEY"])
    for url in urls:
        try:
            article: Article = Article(url)
            article_body: str = article.get_body()
            summary: str = summarizer.summarize(article_body)
            logging.info(article.get_title())
            logging.info(comment_format(summary))
        except NotImplementedError as e:
            logging.warning(f"{url} is not parseable at this time")



if __name__ == "__main__":
    main()