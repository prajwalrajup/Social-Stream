import os
import dynamic_yaml

fileLocaion = "config.yaml"
config = {}


def init(baseDir):
    global config
    with open(os.path.join(baseDir, fileLocaion)) as fileobj:
        config = dynamic_yaml.load(fileobj)


def getConfig(key=""):
    if (key == ""):
        return config
    else:
        return config[key]
