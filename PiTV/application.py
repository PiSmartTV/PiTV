#!/usr/bin/env python3
"""
Main PiTV file, run this
"""
from threading import Thread
import sys
import os
import json
import pickle
import time
import requests
import logging

from imdb import IMDb

from .category import Category
from .sidebar import SideBar, WeatherBox
from .utils import check_internet, rel_path
from .location import Location
from .weather import Weather
from .config import *
from . import ftp_server

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gio  # NOQA


if not os.path.exists(CONFIG_DIR):
    os.mkdir(CONFIG_DIR)

if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)

# Logging settings
logging.basicConfig(level=logging.DEBUG)

# 60*2*1000=120000 Why? 1000 miliseconds is 1 second, we need 2 minutes
REFRESH_MILLS = 120000

# 60seconds
CODE_EXPIRE = 60

SIDEBAR_LABELS = [
    "Home",
    "Movies",
    # "TV Shows",
    # "TV",
    # "Songs"
    "Settings"
]

SIDEBAR_ICONS = [
    "go-home",
    "media-tape",
    # "TV Shows",
    # "TV",
    # "Songs"
    "open-menu"
]

CATEGORIES = [
    "get_popular100_movies",
    "get_popular100_tv",
    "get_top250_movies",
    "get_top250_tv"
]


class PiTV(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="org.grbavacigla.pitv",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        )

        GLib.set_application_name("PiTV")
        GLib.set_prgname("pitv")

        # Initializing builder
        logging.debug("Initiating builder")  # Logger
        self.builder = Gtk.Builder()

        # Adding UI file to builder
        logging.debug("Adding UI file to builder")  # Logger
        self.builder.add_from_file(rel_path("application.glade"))

        # Connecting signals
        logging.debug("Connecting signals")  # Logger
        self.builder.connect_signals(self)

        self.login_window = self.builder.get_object(
            "login_window")
        self.home_window = self.builder.get_object(
            "home_window")

        # Website host URL (As I currenly don't have website,
        # localhost is development sollution)
        # Switched to heroku free plan
        # Switched to Azure donated by Maker NS
        # Again, my website is homeless :(
        self.host = HOST
        self.skip_login = False

        # Session is required to store cookies
        logging.info("Creating browser session")
        self.session = requests.session()
        self.session.headers = {
            "User-Agent": USER_AGENT
        }
        self.load_session()

        if self.skip_login:
            logging.info("Skipping login because cookies exist")
            self.window = self.home_window
            self.home_init()
        else:
            logging.info("Couldn't find cookies, cannot skip login")
            self.window = self.login_window
            self.login_init()

        # self.create_thread(self.recheck_network)

    def home_refresh(self):
        # Fetch weather info
        # TODO:Prompt user for his openweathermap api key
        if not self.weather_info:
            self.weather_info = Weather(
                self.unit_system,
                self.location_info,
                self.openweather_apikey
            )
            self.weather_box.set_weather_object(
                self.weather_info,
                update=True
            )

        else:
            self.weather_box.update_data()
            self.weather_box.refresh()

        GLib.timeout_add(
            REFRESH_MILLS,
            lambda: self.create_thread(self.home_refresh)
        )

    def recheck_network(self):
        self.network_state = check_internet()

    def home_init(self):
        # Setting objects public variables to their object
        self.home_divider = self.builder.get_object("home_divider")
        self.home_stack = self.builder.get_object("home_stack")
        self.category_view = self.builder.get_object("category_view")
        self.home_trending_scroll_view = self.builder.get_object(
            "home_trending_scroll_view")

        # Scrolling adjustment
        self.category_view.set_focus_vadjustment(
            self.home_trending_scroll_view.get_vadjustment()
        )

        # Add Sidebar to window and place it in the beginning
        self.sidebar = SideBar(self.home_stack)
        self.home_divider.pack_start(self.sidebar, False, False, 0)
        self.home_divider.reorder_child(self.sidebar, 0)

        # Fetch some environment variables
        logging.debug("Fetching UNIT_SYSTEM and OPEN_WEATHER_API_KEY")
        self.openweather_apikey = os.environ.get("OPEN_WEATHER_API_KEY")
        self.unit_system = os.environ.get("UNIT_SYSTEM")

        # Check if they are empty
        if not self.unit_system:
            logging.warning("Defaulting unit system to metric")
            self.unit_system = "metric"

        if not self.openweather_apikey:
            logging.warning("No OpenWeather api key found. Using 7Timer!.")

        # Setting weather_info to None
        self.weather_info = None

        # Instantiate and pack WeatherBox widget, later add weather_info to it
        self.weather_box = WeatherBox(SIDEBAR_WIDTH)
        self.sidebar.add_start_widget(self.weather_box)

        # Populate the list with sidebar actions
        logging.info("Populating sidebar")
        sidebar_len = len(SIDEBAR_LABELS)
        for i in range(sidebar_len):
            self.sidebar.add_action(SIDEBAR_LABELS[i], SIDEBAR_ICONS[i])

        logging.info("Creating categories")
        for i in CATEGORIES:
            temp_cat = Category(i)
            self.category_view.pack_start(temp_cat, False, False, 6)

        # Fetch location
        logging.info("Fetching location for weather")
        self.location_info = Location()

        # Fetch all data that needs to be refreshed every 2 minutes
        logging.info("Calling home refresh")
        self.create_thread(self.home_refresh)

        # 60*2*1000=120000 Why? 1000 miliseconds is 1 second, we need 2 minutes
        logging.info("Setting timeout for refresh to %s", REFRESH_MILLS)
        GLib.timeout_add(
            REFRESH_MILLS,
            lambda: self.create_thread(self.home_refresh)
        )

        if USE_FTP_SERVER:
            self.ftp_server = ftp_server.FTPThread()
            self.ftp_server.start()

    def create_thread(self, target, *args):
        thread = Thread(target=target, args=args)
        thread.setName(target.__name__)
        thread.setDaemon(True)
        thread.start()

    def switch_to_code(self, *args):
        stack = self.builder.get_object("login_stack")
        self.stack_state = 1
        stack.set_visible_child(stack.get_children()[2])
        stack.get_children()[2].show()

    def login_init(self):
        # Default to "code view"
        self.switch_to_code()

        # Get error labels and spinners
        self.login_error_label = self.builder.get_object(
            "login_error_label")
        self.signup_error_label = self.builder.get_object(
            "signup_error_label")
        self.login_spinner = self.builder.get_object(
            "login_spinner")
        self.signup_spinner = self.builder.get_object(
            "signup_spinner")

        # Get code label
        self.code_label = self.builder.get_object("code_label")

        # Get code progressbar
        self.login_progress = self.builder.get_object("login_progressbar")

        # Login and Signup state (0 - login, 1 - signup)
        # It also gets inverted when in "code view"
        # Thats why it is set to 1
        self.stack_state = 1

        self.logged = False

        # Default to empty string
        self.password = ""
        self.username = ""
        self.email = ""
        self.name = ""

        self.create_thread(self.update_code)
        self.create_thread(self.update_progressbar)

    def load_session(self):
        cookies_dir = os.path.join(CONFIG_DIR, "cookies.txt")
        if os.path.exists(cookies_dir):
            with open(cookies_dir, 'rb') as file:
                self.session.cookies = pickle.load(file)
                self.skip_login = True

    def save_session(self):
        # Save cookies to CONFIG_DIR/cookies.txt
        with open(os.path.join(CONFIG_DIR, "cookies.txt"), 'wb') as file:
            pickle.dump(self.session.cookies, file)
        # Rest of session settings goes here

    def update_progressbar(self):
        while not self.logged:
            if hasattr(self, "end_time"):
                fraction = (
                    CODE_EXPIRE - self.end_time + time.time()
                ) / CODE_EXPIRE
                self.login_progress.set_fraction(fraction)
                time.sleep(0.05)

    def update_code(self):
        # Fetching login code from website
        raw_code = self.session.get(HOST+"/api/code/")

        # TODO: Add logging here
        if not raw_code.ok:
            sys.exit(1)

        code = json.loads(raw_code.text)["code"]

        # Calculate expire time by adding CODE_EXPIRE seconds to current time
        self.end_time = time.time() + CODE_EXPIRE

        self.code_label.set_label(code)

        while self.end_time >= time.time():
            raw_post = self.session.post(HOST+"/api/code/", data={"code": code})
            if raw_post.ok:
                self.logged = True
                self.save_session()
                GLib.idle_add(self.switch_window, self.home_window)
                GLib.idle_add(self.home_init)
                return
            time.sleep(1)

        # Convert seconds to milliseconds
        GLib.idle_add(lambda: self.create_thread(self.update_code))

    def toggle_login_stack(self, *args):

        # Change state to opposite
        self.stack_state = int(not self.stack_state)

        # Switch to stack of index stack_state
        stack = self.builder.get_object("login_stack")
        stack.set_visible_child(stack.get_children()[self.stack_state])
        stack.get_children()[self.stack_state].show()

    def destroy(self, *args):
        Gtk.main_quit()

    def validate_login(self):
        # TODO: Add more response error for user to know what to do
        # self.network_state = check_server()
        self.network_state = True

        if self.network_state:
            try:
                response = self.session.post(self.host+"/login", data={
                    "username": self.username,
                    "password": self.password
                })

                self.save_session()
                self.logged = True
            except Exception as exception:
                self.login_error_label.set_visible(True)
                self.login_error_label.set_text(
                    "Error code:" + str(exception)
                )
                return

            if response.status_code == 200:
                GLib.idle_add(self.switch_window, self.home_window)
                GLib.idle_add(self.home_init)

            else:
                self.login_error_label.set_visible(True)
                self.login_error_label.set_text(
                    "Error code:" + str(response.status_code)
                )
        else:
            self.login_error_label.set_visible(True)
            self.login_error_label.set_text(
                "No internet connection or server is down!")

        self.login_spinner.set_visible(False)

    def switch_window(self, window):
        window.fullscreen()
        window.show_all()

    def login(self, *args):
        # Get username and password and store it in public variables
        self.username = self.builder.get_object(
            "login_username_field").get_text()
        self.password = self.builder.get_object(
            "login_password_field").get_text()

        # Thread for validating and obtaining the user token
        # TODO: Fetch token
        self.login_spinner.set_visible(True)  # Hide Spinner

        self.create_thread(self.validate_login)

    def signup(self, *args):
        # Get signup info and store it in public variables
        self.username = self.builder.get_object(
            "signup_username_field").get_text()
        self.password = self.builder.get_object(
            "signup_password_field").get_text()
        self.retype_password = self.builder.get_object(
            "signup_retype_password_field").get_text()
        self.email = self.builder.get_object(
            "signup_email_field").get_text()
        self.name = self.builder.get_object(
            "signup_name_field").get_text()

        self.signup_spinner.set_visible(True)

        # Thread for validating and obtaining the user token
        self.create_thread(self.validate_signup)

    def validate_signup(self):
        # TODO: Add more response error for user to know what to do
        # self.network_state = check_server()
        self.network_state = True

        if self.retype_password != self.password:
            return

        if self.network_state:
            response = self.session.post(self.host+"/register", data={
                "username": self.username,
                "password": self.password,
                "name": self.name,
                "email": self.email
            })

            if response.status_code == 200:
                GLib.idle_add(self.toggle_login_stack)

            else:
                self.signup_error_label.set_visible(True)
                self.signup_error_label.set_text(
                    "Error code:" + str(response.status_code))
        else:
            self.signup_error_label.set_visible(True)
            self.signup_error_label.set_text(
                "No internet connection or server is down!")

        self.signup_spinner.set_visible(False)



