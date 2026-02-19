import configparser
import os

CONFIG_FILE_LOCATION = os.path.expanduser(
    "~") + "/.config/KRunner-Spotify/KRunner-Spotify.config"
REQUIRED_SECTIONS = ("Settings", "CommandNames")


def loadConfig():
    read_files = config.read(CONFIG_FILE_LOCATION)
    if not read_files:
        raise RuntimeError(
            f"Configuration file not found: {CONFIG_FILE_LOCATION}")

    for section_name in REQUIRED_SECTIONS:
        if section_name not in config:
            raise RuntimeError(
                f"Missing config section '{section_name}' in: {CONFIG_FILE_LOCATION}")

    if "CACHE_PATH" not in config["Settings"]:
        raise RuntimeError(
            f"Missing setting 'CACHE_PATH' in: {CONFIG_FILE_LOCATION}")

    config["Settings"]["CACHE_PATH"] = os.path.expanduser(
        config["Settings"]["CACHE_PATH"])


def getCommandName(commandName):
    if commandName not in config["CommandNames"]:
        raise KeyError(f"Command '{commandName}' not found in config")

    if(config["Settings"]["CASE_SENSITIVE"] == "False"):
        return config["CommandNames"][commandName].upper()
    return config["CommandNames"][commandName]


def getSetting(settingName):
    if settingName not in config["Settings"]:
        raise KeyError(f"Setting '{settingName}' not found in config")
    return config["Settings"][settingName]


config = configparser.ConfigParser()
loadConfig()
