import dynamic_yaml

fileLocaion = "config.yaml"
config = {}


def init():
    global config
    with open(fileLocaion) as fileobj:
        config = dynamic_yaml.load(fileobj)


def getConfig(key=""):
    if (key == ""):
        return config
    else:
        return config[key]
