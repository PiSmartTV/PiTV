from os import path
from pathlib import Path
from screeninfo import get_monitors

ROOT_DIR = path.dirname(path.abspath(__file__))
HOST = "https://pitv.cf/"
HOME_DIR = str(Path.home())
CONFIG_DIR = path.join(HOME_DIR, ".config", "PiTV")
CACHE_DIR = path.join(HOME_DIR, ".cache", "PiTV")
MONITOR_WIDTH = get_monitors()[0].width
MONITOR_HEIGHT = get_monitors()[0].height
SIDEBAR_WIDTH = MONITOR_WIDTH/8
