from praw import Reddit
import logging
from Settings import Settings

settings = Settings()
settings.load_settings("settings.json")



class RedditBot:
    def __init__(self) -> None:
        self._reddit = Reddit(
            client_id=settings["reddit"]["client_id"], 
            client_secret=settings["reddit"]["secret"], 
            user_agent="my user agent", 
            username=settings["reddit"]["username"], 
            password=settings["reddit"]["password"]
        )

        assert not self._reddit.read_only

        self._subreddits = [self._reddit.subreddit(sub) for sub in settings["reddit"]["subreddits"]]


    def get_articles(self) -> list[str]:
        urls = []
        for sub in self._subreddits:
            for post in sub.rising(limit=3): # get the top 3 posts at the time 
                urls.append(post.url)

        return urls


if __name__ == "__main__":
    reddit_bot = RedditBot()
    urls = reddit_bot.get_articles()
    print(urls)


