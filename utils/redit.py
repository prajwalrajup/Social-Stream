import os
import praw
import requests
from dotenv import load_dotenv
from loggingConfig import configure_logging, logging

# loading .env
load_dotenv()


# Configure logging
configure_logging()


class RedditBot():
    # initilize the reddit wrapper praw lib
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv('clientId'),
            client_secret=os.getenv('clientSecret'),
            user_agent=os.getenv('agentId'),
        )

    # methond to get all the top posts with a set limit
    def getPosts(self, subredditName, limit):
        subreddit = self.reddit.subreddit(subredditName)
        logging.info(
            f"fetching data from {subreddit.display_name} with limit {limit}")
        posts = []
        for submission in subreddit.top("day", limit=limit):
            if submission.stickied:
                logging.info("Skiping Mod Post")
            else:
                posts.append(submission)
        return posts

    # methond to validate if the post is usable or not
    def checkIfPostIsValidFormat(self, submission):
        url = submission.url.lower()
        if "jpg" in url and not submission.over_18:
            return True
        else:
            return False
