from utils.redit import RedditBot
from utils.media import Media
from PIL import Image
from utils.instagram import Instagram
import utils.utils as utils
import utils.directory as directory
from utils.constants import *

# get the data from the config file
jsonFileLocation = directory.pathJoin(
    directory.getBaseDirectory(), "config.json")
data = utils.readJson(jsonFileLocation)


def collectData():
    # run if the to upload object is None
    if (len(data[TO_UPLOAD]) == 0):

        # update the subredt index
        utils.updateCurrentSubredditIndex(data)
        subReditName = data[SUB_REDITS][data[CURRENT_SUBREDIT_INDEX]]

        # initilize redit and median
        redditbot = RedditBot()
        media = Media(utils.getTimeStampAndReditName(subReditName))

        # get n number of posts depending on number of subredits
        submissions = redditbot.getPosts(
            subReditName, (24 // len(data[SUB_REDITS])))

        # save and resize all the images of submissions
        for submission in submissions:
            # validate the submission is valid to be posted
            if (redditbot.checkIfPostIsValidFormat(submission)):
                fileName = f"Post-{submission.id}{submission.url.lower()[-4:]}"
                fileLocaion = media.getMedia(submission, fileName)
                media.resize(fileLocaion)

                # build an object to be saved in json
                toUploadObject = {
                    "image": fileLocaion,
                    "desc": utils.buildDesc(data, submission.title, subReditName)
                }

                toUpload = data[TO_UPLOAD]
                toUpload[fileName] = toUploadObject
                data[TO_UPLOAD] = toUpload
    
    if (len(data[TO_UPLOAD]) == 0):
        print("No valid posts to be saved")
        return False
    else:
        return True


def uploadMedia():
    # pick the first object from the toUploadList
    toUploadList = data[TO_UPLOAD]
    toUploadObject = next(iter(toUploadList.items()))

    # upload the image with desc to instagram
    instagram = Instagram()
    instagram.uploadImageToInstagram(
        toUploadObject[1]["image"], toUploadObject[1]["desc"])

    # remove the object from the toUploadList
    del toUploadList[toUploadObject[0]]
    data[TO_UPLOAD] = toUploadList


isSuccess = collectData()
if (isSuccess):
    uploadMedia()

# write the data file to config json
utils.writeJson(jsonFileLocation, data)


# cron string
# */1 * * * * python3 /home/prajwal/instagramBot/Reddit-instagram-bot/main.py >> /home/prajwal/instagramBot/Reddit-instagram-bot/cronOutput.txt