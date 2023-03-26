import os
import json
from instagrapi import Client
from dotenv import load_dotenv
import utils.directory as directory
from instagrapi.exceptions import ClientLoginRequired, PhotoNotUpload

from loggingConfig import configure_logging, logging

# Configure logging
configure_logging()

# loading .env
load_dotenv()


class Instagram():

    # initlilize client for instagram
    def __init__(self):
        # Set up the client with your login credentials
        self.client = Client()
        username = os.getenv('instagramUsername')
        password = os.getenv('instagramPasswd')
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
        except (ClientLoginRequired, PhotoNotUpload) as e:
            logging.error(
                f"something went wrong while uploading to instagram : '{e}'")
            
            # check if processing error if it is dont dump the seesion
            errorResponse = json.loads(e.message)
            if ("debug_info" not in errorResponse or "type" not in errorResponse["debug_info"] or errorResponse["debug_info"]["type"] != "ProcessingFailedError"):
                directory.deleteFile(self.dumpFileLocation)
