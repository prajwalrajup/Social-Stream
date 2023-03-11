from utils.redit import RedditBot
from utils.media import Media
from PIL import Image
from utils.instagram import Instagram

redditbot = RedditBot()
media = Media("now")
instagram = Instagram()

submissions = redditbot.getPosts("GetMotivated", 1)
for submission in submissions:
    if (redditbot.checkIfPostIsValidFormat(submission)):
        fileLocaion = media.getMedia(submission)
        media.resize(fileLocaion)
        instagram.uploadImageToInstagram(
            fileLocaion, "This is a test #motivationalquotes #inspirationalquotes")

# Delete the instances of objects
del redditbot
del media
del instagram
