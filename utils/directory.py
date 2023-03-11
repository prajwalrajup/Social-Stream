import os

# method to create director if it dose not exists


def makeDirIfNotExists(baseDir, dirName):
    if (baseDir == None or dirName == None):
        print("Base dir or dir name is none")
        return

    targetDir = os.path.join(baseDir, dirName)

    # checking if the target dir dose not exists
    if (not os.path.isdir(targetDir)):
        try:
            # making a dir
            os.makedirs(targetDir, exist_ok=True)
            return targetDir
        except OSError as error:
            print(f"someting went wrong while creating dir : {error}")
            return None

    # return the director location if it exists
    else:
        return targetDir


def pathJoin(*paths):
    basePath = ""
    for path in paths:
        basePath = os.path.join(basePath, path)
    return basePath
