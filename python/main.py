import logging

from praw import Reddit
from Settings import Settings


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
            print(submission.title)

            # urls.append(post.url)
    
    print(urls)


if __name__ == "__main__":
    main()