import praw
from utils.yaml import getConfig
from loggingConfig import configure_logging, logging

# load config
redditConfig = getConfig("reddit")
maxSearchItems = getConfig("maxSearchItems")

# Configure logging
configure_logging()


class RedditBot():
    # initilize the reddit wrapper praw lib
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=redditConfig['clientId'],
            client_secret=redditConfig['clientSecret'],
            user_agent=redditConfig['agentId'],
        )

    # methond to get all the top posts with a set limit
    def getPosts(self, subredditName):
        subreddit = self.reddit.subreddit(subredditName)
        logging.info(f"fetching data from {subreddit.display_name}")

        for submission in subreddit.top("day", limit=maxSearchItems):
            if submission.stickied:
                logging.info("Skiping Mod Post")

            else:

                # validate the submission is valid to be posted
                if (self.checkIfPostIsValidFormat(submission)):
                    return submission

        # No valid post was found
        raise Exception("No valid post found")

    # methond to validate if the post is usable or not
    def checkIfPostIsValidFormat(self, submission):
        url = submission.url.lower()
        if "jpg" in url and not submission.over_18:
            return True
        else:
            return False
