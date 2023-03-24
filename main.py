import os
from utils.redit import RedditBot
from utils.media import Media
from PIL import Image
from utils.instagram import Instagram
import utils.utils as utils
import utils.directory as directory
from utils.constants import *
from loggingConfig import configure_logging, logging
import utils.Bot as DiscordBot

# Configure logging
configure_logging()


#     # get the data from the config file
jsonFileLocation = directory.pathJoin(
    directory.getBaseDirectory(), "config.json")
data = utils.readJson(jsonFileLocation)

try:
    currentPostIndex = str(data['currentPostIndex'])
    descDefault = str(data['descDefault'])
    
    instagram = Instagram()
    instagram.uploadImageToInstagram(f"videos/{currentPostIndex}.mp4", descDefault.replace("{index}", currentPostIndex ), True)

except Exception as e:
    import traceback
    DiscordBot.botRun(
        f"An error occurred in {os.getenv('accountName') } with exception {e}  with trace \n {traceback.format_exc()}", DISCORD_INCEDENT_CHANNEL)
    logging.exception(f"An error occurred: {e}")

finally :
    # write the data file to config json
    utils.writeJson(jsonFileLocation, data)
    logging.info("------------------------------------------------->")

# cron string
# */1 * * * * python3 /home/prajwal/instagramBot/Reddit-instagram-bot/main.py >> /home/prajwal/instagramBot/Reddit-instagram-bot/cronOutput.txt
