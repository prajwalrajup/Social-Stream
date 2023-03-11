from instagrapi import Client
from instagrapi.exceptions import ClientLoginRequired
from dotenv import load_dotenv
import os
load_dotenv()


class Instagram():

    # initlilize client for instagram
    def __init__(self):
        # Set up the client with your login credentials
        self.client = Client()
        username = os.getenv('instagramUsername')
        password = os.getenv('instagramPasswd')
        try:
            self.client.login(username, password)
        except ClientLoginRequired as e:
            print(f"something went wrong while conneting to instagram : '{e}'")

    # This is the destructor method, called to close the client connection
    def __del__(self):

        self.client.close()

    # Post the image to instagram
    def uploadImageToInstagram(self, locaion, description):
        print(f"posting image to instagram with description {description}")
        self.client.photo_upload(locaion, description)
