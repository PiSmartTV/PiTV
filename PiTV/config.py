"""Common global variables"""
from os import path
from pathlib import Path
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk  # NOQA

# I know this is deprecated, but i don't have better solution
# TODO: Fix deprecation warning
screen = Gdk.Screen.get_default()

ROOT_DIR = path.dirname(path.abspath(__file__))
HOST = "http://127.0.0.1:8000" # Again, we are looking for hosting
STREAM_PORT = "23000"
VIDEO_PLAYER = "/usr/bin/celluloid"
HOME_DIR = str(Path.home())
CONFIG_DIR = path.join(HOME_DIR, ".config", "PiTV")
CACHE_DIR = path.join(HOME_DIR, ".cache", "PiTV")
MONITOR_WIDTH = screen.get_width()
MONITOR_HEIGHT = screen.get_height()
SIDEBAR_WIDTH = MONITOR_WIDTH/8
USE_FTP_SERVER = False
USER_AGENT = "PiTV/0.0.1 (Linux)"
