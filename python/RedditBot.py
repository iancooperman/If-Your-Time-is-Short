from praw import Reddit
import logging
from Settings import Settings

settings = Settings()
settings.load_settings("settings.json")



class RedditBot:
    def __init__(self) -> None:
        self._reddit = Reddit(
            client_id="my client id", 
            client_secret=settings["reddit"]["secret"], 
            user_agent="my user agent", 
            username=settings["reddit"]["username"], 
            password=settings["reddit"]["password"])

        assert not self._reddit.read_only


if __name__ == "__main__":
    reddit_bot = RedditBot()


