import logging

from Article import Article
from praw import Reddit
from Settings import Settings
from GPTSummarizer import GPTSummarizer


def comment_format(raw_summary: str):
    raw_summary = raw_summary.strip()

    summary_sentences = raw_summary.split('. ')
    for i in range(len(summary_sentences)): # add a markdown bullet point to the front of each sentence
        summary_sentences[i] = '* ' + summary_sentences[i]
    
    # glue the sentences back together and return
    return "\n".join(summary_sentences)


def logger_config():

    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s')

    fh = logging.FileHandler('iytis.log', mode='a', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)    
    log.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)


def main():
    # initialize logger
    logger_config()

    # retrieve settings
    settings_file_name = "settings.json"
    settings = Settings()
    settings.load_settings(settings_file_name)
    logging.info(f"{settings_file_name} loaded")

    # initialize Reddit instance
    reddit = Reddit(
        client_id=settings["reddit"]["client_id"], 
        client_secret=settings["reddit"]["secret"], 
        user_agent=settings["reddit"]["user_agent"],
        username=settings["reddit"]["username"], 
        password=settings["reddit"]["password"]
    )

    logging.info('Reddit instance initialized')

    subreddits = settings["reddit"]["subreddits"]

    urls = []
    for subreddit_name in subreddits:
        for submission in reddit.subreddit(subreddit_name).hot(limit=3): # get the top 3 posts at the time 
            urls.append(submission.url)

    
    summarizer = GPTSummarizer(settings["OPENAI_API_KEY"])
    for url in urls:
        try:
            article = Article(url)
            article_body = article.get_body()
            summary = summarizer.summarize(article_body)
            print(article.get_title())
            print(comment_format(summary))
        except NotImplementedError as e:
            logging.warning(f"{url} is not parseable at this time")



if __name__ == "__main__":
    main()