import logging

from Article import Article
from praw import Reddit
from Settings import Settings
from GPTSummarizer import GPTSummarizer




def main():
    # retrieve settings
    settings = Settings()
    settings.load_settings("settings.json")

    # initialize Reddit instance
    reddit = Reddit(
        client_id=settings["reddit"]["client_id"], 
        client_secret=settings["reddit"]["secret"], 
        user_agent=settings["reddit"]["user_agent"],
        username=settings["reddit"]["username"], 
        password=settings["reddit"]["password"]
    )

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
            print(summary)
        except NotImplementedError as e:
            continue



if __name__ == "__main__":
    main()