from .registry import TOP_LEVEL_KEYS, resolve


def executeCommand(command, spotify):
    return resolve(command, spotify, TOP_LEVEL_KEYS)
