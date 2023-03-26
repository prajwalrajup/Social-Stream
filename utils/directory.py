import os
from loggingConfig import configure_logging, logging

# Configure logging
configure_logging()

# method to create director if it dose not exists


def makeDirIfNotExists(baseDir, dirName):
    if (baseDir == None or dirName == None):
        logging.error("Base dir or dir name is none")
        return

    targetDir = os.path.join(baseDir, dirName)

    # checking if the target dir dose not exists
    if (not os.path.isdir(targetDir)):
        try:
            # making a dir
            os.makedirs(targetDir, exist_ok=True)
            return targetDir
        except OSError as error:
            raise Exception(
                f"someting went wrong while creating dir : {error}")

    # return the director location if it exists
    else:
        return targetDir


# return true if path exists

def dosePathExists(locaion):
    return os.path.exists(locaion)


# if the path exists delete the location

def deleteFile(location):
    if (dosePathExists(location)):
        logging.info(f"deleting file {location}")
        os.remove(location)
    else:
        logging.error(f"file dose not exists to delete")

# join multiple directritoires to build a paths

def pathJoin(*paths):
    basePath = ""
    for path in paths:
        basePath = os.path.join(basePath, path)
    return basePath


# returns the base dir

def getBaseDirectory():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
