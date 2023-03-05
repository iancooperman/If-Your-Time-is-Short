import logging

from praw import Reddit
from Settings import Settings


def main():
    # retrieve settings
    settings = Settings()
    settings.load_settings("settings.json")

    # initialize Reddit instance
    reddit = Reddit(
        client_id="my client id", 
        client_secret=settings["reddit"]["secret"], 
        user_agent="IfYourTimeIsShort v0.1 by /u/BananaZen314159"
        username=settings["reddit"]["username"], 
        password=settings["reddit"]["password"]
    )

    subreddits = settings["reddit"]["subreddits"]

    urls = []
    for sub_name in subreddits:
        subreddit = reddit.subreddit(sub_name)
        print(subreddit)
        for post in subreddit.rising(limit=3): # get the top 3 posts at the time 
            print(post.title)

            # urls.append(post.url)
    
    print(urls)


if __name__ == "__main__":
    main()