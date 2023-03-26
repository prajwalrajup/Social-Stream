import json
import datetime
from utils.yaml import getConfig
import utils.Constants as Constants

from loggingConfig import configure_logging, logging

# Configure logging
configure_logging()

# load config
descConfig = getConfig("desc")


def getTimeStampAndSourceName(sourceName):
    # get the current datetime object
    dateTime = datetime.datetime.now()
    # format the datetime object as a string and return
    return dateTime.strftime('%Y-%m-%d_') + sourceName

def buildDesc(desc, originalSourceName, sourceType):
    sourceRefrence = descConfig["sourceRefrence"][sourceType].replace(
        "<originalSourceName>", originalSourceName)

    desc = desc.lower()
    # remove all the words that should not be there in desc
    for removeElement in descConfig[Constants.DESC_REMOVE_LIST]:
        desc = desc.replace(removeElement, "")

    # add the subreddit source
    desc += descConfig[Constants.DESC_BUILD]
    desc = desc.replace("<sourceRefrence>", sourceRefrence)

    desc.strip()
    return desc


def getTime24HoursAgo():
    # create a datetime object for the current time
    now = datetime.datetime.now(tz=datetime.timezone.utc)

    # create a timedelta object for 24 hours
    delta = datetime.timedelta(hours=24)

    # subtract the timedelta from the current time to get the time 24 hours ago
    return now - delta


def getCurrentHour():
    now = datetime.datetime.now()
    return now.hour
