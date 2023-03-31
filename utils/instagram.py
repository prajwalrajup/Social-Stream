import re
import json
from instagrapi import Client
from utils.yaml import getConfig
import utils.directory as directory
from utils.utils import getTime24HoursAgo
from loggingConfig import configure_logging, logging
from instagrapi.exceptions import ClientLoginRequired, PhotoNotUpload

# Configure logging
configure_logging()

# load config
instagramConfig = getConfig("instagram")
maxSearchItems = getConfig("maxSearchItems")


class Instagram():

    # initlilize client for instagram
    def __init__(self):
        # Set up the client with your login credentials
        self.client = Client()
        username = instagramConfig["username"]
        password = instagramConfig["passwd"]
        self.dumpFileLocation = directory.pathJoin(
            directory.getBaseDirectory(),
            "data",
            "instagramDump.json"
        )

        try:
            # load device dump if exists to login to intagram from same device id
            if (directory.dosePathExists(self.dumpFileLocation)):
                self.client.load_settings(self.dumpFileLocation)
            self.client.login(username, password)
        except (ClientLoginRequired, PhotoNotUpload) as e:
            logging.error(
                f"something went wrong while conneting to instagram : '{e}'")
            directory.deleteFile(self.dumpFileLocation)
        # dump device details to be used logging in again
        self.client.dump_settings(self.dumpFileLocation)

    # # This is the destructor method, called to close the client connection
    # def __del__(self):
    #     # pass
    #     self.client.logout()

    # Post the image to instagram
    def uploadImageToInstagram(self, locaion, description):
        logging.info(f"posting image to instagram with locaion {locaion}")
        try:
            self.client.photo_upload(locaion, description)

        # if upload fails due to login issues delete the device dump file
        except (Exception, ClientLoginRequired, PhotoNotUpload) as e:
            logging.error(
                f"something went wrong while uploading to instagram : {e}")

            # check if processing error if it is dont dump the seesion
            errorResponse = json.loads(e.message)
            if ("debug_info" not in errorResponse or "type" not in errorResponse["debug_info"] or errorResponse["debug_info"]["type"] != "ProcessingFailedError"):
                directory.deleteFile(self.dumpFileLocation)
                return
            raise Exception(
                f"something went wrong while uploading to instagram : {e}")

    def getImagesFromHashtags(self, hashtagName):
        medias = self.client.hashtag_medias_top(
            hashtagName, amount=maxSearchItems)
        for media in medias:
            media = media.dict()

            # check if the post is valid
            if (self.checkIfPostIsValidFormat(media)):
                return media

        # if no posts are foud in the last 24 hours
        raise Exception(f"No valid posts found for {hashtagName}")

    def checkIfPostIsValidFormat(self, media):
        # check if posted in last 24 hours
        if (media["taken_at"] >= getTime24HoursAgo() and self.getMediaType(media["thumbnail_url"]) != None):
            return True
        else:
            return False

    def getMediaType(self, url):
        image_type_match = re.search(
            r'(?<=\.)(jpg|jpeg|png|gif|webp)(?=\?)', str(url))

        if image_type_match:
            return image_type_match.group()
        else:
            return None
        

