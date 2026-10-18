import configparser
import os

CONFIG_FILE_LOCATION = (
    os.path.expanduser("~") + "/.config/KRunner-Spotify/KRunner-Spotify.config"
)


def loadConfig():
    if not os.path.isfile(CONFIG_FILE_LOCATION):
        raise SystemExit(
            f"Config not found: {CONFIG_FILE_LOCATION}\nRun install.sh first."
        )
    config.read(CONFIG_FILE_LOCATION)
    config["Settings"]["CACHE_PATH"] = os.path.expanduser(
        config["Settings"]["CACHE_PATH"]
    )


def getCommandName(commandName):
    try:
        if config["Settings"]["CASE_SENSITIVE"] == "False":
            return config["CommandNames"][commandName].upper()
        return config["CommandNames"][commandName]
    except KeyError as e:
        print("Command: " + str(e) + "not found!")


def getSetting(settingName):
    try:
        return config["Settings"][settingName]
    except KeyError as e:
        print("Setting: " + str(e) + "not found!")


config = configparser.ConfigParser()
loadConfig()
