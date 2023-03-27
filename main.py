from utils.yaml import init, getConfig

# load yaml file
init()
accountName = getConfig("instagram")["username"]
sourceConfig = getConfig("source")

from utils.redit import RedditBot
from utils.media import Media
from utils.instagram import Instagram
import utils.utils as utils
import utils.directory as directory
from utils.constants import *
from loggingConfig import configure_logging, logging
import utils.Bot as DiscordBot

# Configure logging
configure_logging()


def instagramSourceUpload(hashtagName):
    
    instagram = Instagram()                                                    # initilize instagram
    instagramMedia = instagram.getImagesFromHashtags(hashtagName)              # get post from instagram
    media = Media(utils.getTimeStampAndSourceName(hashtagName))                # initilize folder structure
    mediaType = instagram.getMediaType(instagramMedia["thumbnail_url"])        
    fileName = f"Post-instagram-{instagramMedia['code']}.{mediaType}"
    fileLocaion = media.getMedia(instagramMedia["thumbnail_url"], fileName)

    desc = utils.buildDesc("", instagramMedia["user"]["username"], SOURCE_INSTAGRAM)
    instagram.uploadImageToInstagram(fileLocaion, desc)
    return instagramMedia["thumbnail_url"]

def redditSourceUpload(subReditName):
    # initilize redit and median
    redditbot = RedditBot()
    media = Media(utils.getTimeStampAndSourceName(subReditName))
    submission = redditbot.getPosts(subReditName)
    fileName = f"Post-reddit-{submission.id}{submission.url.lower()[-4:]}"
    fileLocaion = media.getMedia(submission.url.lower(), fileName)
    media.resize(fileLocaion)
    desc = utils.buildDesc(submission.title, subReditName, SOURCE_REDDIT)

    # initilize instagram
    instagram = Instagram()
    instagram.uploadImageToInstagram(fileLocaion, desc)
    return submission.url.lower()

# MAIN script

# Define a dictionary mapping case values to corresponding functions
case_handlers = {
    SOURCE_REDDIT: redditSourceUpload,
    SOURCE_INSTAGRAM: instagramSourceUpload
}

try :
    for key, value in sourceConfig["sequence"][utils.getCurrentHour()].items():
        logging.info(f"Processing to upload image from {key} - {value}")
        # Get the function object corresponding to the case value
        handler_func = case_handlers.get(key)

        # Call the function with the arguments
        if handler_func:
            fileUrl = handler_func(value)
            DiscordBot.botRun(f'Uploaded {fileUrl} from {key} - {value} ')
        else:
            raise Exception(f"Invalid source found {key}")

except Exception as e: 
    logging.error(e)
    import traceback
    DiscordBot.botRun(f"An error occurred in {accountName} with exception {e}  with trace \n {traceback.format_exc()}", DISCORD_INCEDENT_CHANNEL)

finally:
    logging.info("------------------------------------------------->")

# cron string
# */1 * * * * python3 /home/prajwal/instagramBot/Reddit-instagram-bot/main.py >> /home/prajwal/instagramBot/Reddit-instagram-bot/cronOutput.txt