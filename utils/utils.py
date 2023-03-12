import json
import datetime
from utils.constants import *

def getTimeStampAndReditName(reditName):
    # get the current datetime object
    dateTime = datetime.datetime.now()
    # format the datetime object as a string and return
    return dateTime.strftime('%Y-%m-%d_') + reditName

def readJson(location):
    # Read data from a JSON file
    with open(location, 'r') as f:
        data = json.load(f)
    return data

def writeJson(locaion, data):
    # Write data to a JSON file
    with open(locaion, 'w') as f:
        json.dump(data, f)

def updateCurrentSubredditIndex(data):
    # get the current subreddit index and increament it with loop around
    currentSubredditIndex = data[CURRENT_SUBREDIT_INDEX]
    currentSubredditIndex +=1
    if(len(data[SUB_REDITS]) <= currentSubredditIndex):
        print("resetting currentSubredditIndex to 0")
        currentSubredditIndex = 0
    else :
        print(f"updating currentSubredditIndex to {currentSubredditIndex}")
    data[CURRENT_SUBREDIT_INDEX] = currentSubredditIndex
    return data

def buildDesc(data, desc, subredditName):
    desc = desc.lower()

    # remove all the words that should not be there in desc
    for removeElement in data[DESC_REMOVE_LIST]:
        desc = desc.replace(removeElement, "")
    
    # if desc is empty give a default desc
    if(len(desc) == 0):
        desc = data[DESC_DEFAULT]
    
    # add the subreddit source
    desc += f"\n\nCredit goes to respective owner \n\n ----DECLARATION: This video/audio/photo is not own by ourselves. \n Credit subreddit source : https://www.reddit.com/r/{subredditName}"
    
    # add the elemts to be added into the desc
    for addElement in data[DESC_ADD_LIST]:
        desc += addElement

    desc.strip()
    return desc