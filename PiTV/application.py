#!/usr/bin/env python3
import sys
import os
from threading import Thread
from screeninfo import get_monitors
import requests
from entertainment import Weather, Location
from utils import check_internet
from sidebar import SideBar, ListTile, WeatherBox
from category import Category


# Bypass linters
if True:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, GLib, Gio


HOME_DIR = os.path.dirname(os.path.abspath(__file__))

MONITOR_WIDTH = get_monitors()[0].width
MONITOR_HEIGHT = get_monitors()[0].height
SIDEBAR_WIDTH = MONITOR_WIDTH/8


SIDEBAR_LABELS = [
    "Home",
    "Movies",
    # "TV Shows",
    # "TV",
    # "Songs"
    # "Settings"
]

SIDEBAR_ICONS = [
    "go-home",
    "media-tape",
    # "TV Shows",
    # "TV",
    # "Songs"
    # "Settings"
]


class PiTV(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id="org.grbavacigla.pitv",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
        )

        GLib.set_application_name("PiTV")
        GLib.set_prgname("pitv")

        # Initializing builder and connecting signal
        self.builder = Gtk.Builder()
        self.builder.add_from_file(
            os.path.join(HOME_DIR, "application.glade"))
        self.builder.connect_signals(self)

        self.login_window = self.builder.get_object(
            "login_window")
        self.home_window = self.builder.get_object(
            "home_window")

        # Website host URL (As I currenly don't have website,
        # localhost is development sollution)
        # Switched to heroku basic plan (free)
        self.host = "https://pitv.herokuapp.com"

        self.login_init()  # Switch this back after debugging

    def home_refresh(self):
        # Fetch weather info
        # TODO:Prompt user for his openweathermap api key
        if not self.weather_info:
            self.weather_info = Weather(
                self.openweather_apikey,
                self.unit_system,
                self.city_and_country
            )
            self.weather_box.set_weather_object(self.weather_info, update=True)

        else:
            self.weather_box.update_data()
            self.weather_box.refresh()

        GLib.idle_add(self.current_thread.join)

    def home_init(self):
        # Setting objects public variables to their object
        self.main_divider = self.builder.get_object("main_divider")
        self.main_stack = self.builder.get_object("main_stack")
        self.category_view = self.builder.get_object("category_view")

        # Add Sidebar to window and place it in the beginning
        self.sidebar = SideBar(self.main_stack)
        self.main_divider.pack_start(self.sidebar, False, False, 0)
        self.main_divider.reorder_child(self.sidebar, 0)

        # Fetch some environment variables
        self.openweather_apikey = os.environ.get("OPEN_WEATHER_API_KEY")
        self.unit_system = os.environ.get("UNIT_SYSTEM")

        # Setting weather_info to None
        self.weather_info = None

        # Instantiate and pack WeatherBox widget, later add weather_info to it
        self.weather_box = WeatherBox(SIDEBAR_WIDTH)
        self.sidebar.add_start_widget(self.weather_box)

        # Populate the list with sidebar actions
        sidebar_len = len(SIDEBAR_LABELS)
        for i in range(sidebar_len):
            self.sidebar.add_action(SIDEBAR_LABELS[i], SIDEBAR_ICONS[i])

        for i in range(10):
            cat = Category()
            self.category_view.pack_start(cat, True, True, 2)
            self.category_view.reorder_child(cat, i)

        # Fetch location
        self.location_info = Location()

        # Make formatted location for open weather map
        self.city_and_country = "{},{}".format(
            self.location_info.city,
            self.location_info.countryCode
        )

        # Fetch all data that needs to be refreshed every 2 minutes
        self.create_thread(self.home_refresh)

        # 60*2*1000=120000 Why? 1000 miliseconds is 1 second, we need 2 minutes
        GLib.timeout_add(120000, lambda: self.create_thread(self.home_refresh))

    def create_thread(self, function, *args):
        self.current_thread = Thread(target=function)
        self.current_thread.start()

    def login_init(self):
        self.login_error_label = self.builder.get_object(
            "login_error_label")
        self.signup_error_label = self.builder.get_object(
            "signup_error_label")
        self.login_spinner = self.builder.get_object(
            "login_spinner")
        self.signup_spinner = self.builder.get_object(
            "signup_spinner")

        # Login and Signup state (0 - login, 1 - signup)
        self.stack_state = 0

        # Default to empty string
        self.password = ""
        self.username = ""
        self.email = ""
        self.name = ""

        # Session is required to store cookies
        self.session = requests.session()

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
        try:
            response = self.session.post(self.host+"/login", data={
                "username": self.username,
                "password": self.password
            })
        except Exception as exception:
            self.login_error_label.set_visible(True)
            self.login_error_label.set_text(
                "Error code:" + str(exception)
            )
            return

        self.login_spinner.set_visible(False)

        if response.status_code == 200:
            GLib.idle_add(self.switch_window, self.home_window)
            GLib.idle_add(self.home_init)
            GLib.idle_add(self.current_thread.join)
        else:
            self.login_error_label.set_visible(True)
            self.login_error_label.set_text(
                "Error code:" + str(response.status_code)
            )

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

        self.network_state = check_internet()
        if self.network_state:
            self.create_thread(self.validate_login)
        else:
            self.login_error_label.set_text("No internet connection")

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

        if self.retype_password != self.password:
            GLib.idle_add(self.current_thread.join)
            return

        response = self.session.post(self.host+"/register", data={
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "email": self.email
        })

        self.signup_spinner.set_visible(False)

        if response.status_code == 200:
            GLib.idle_add(self.toggle_login_stack)
            GLib.idle_add(self.current_thread.join)
        else:
            self.signup_error_label.set_visible(True)
            self.signup_error_label.set_text(
                "Error code:" + str(response.status_code))

    # def on_sidebar_row_selected(self, listbox, listbox_row):
    #     index = listbox_row.get_index()
    #     item = SIDEBAR_LABELS[index]
    #     getattr(self, item.lower()+"_stack")()

    # def home_stack(self):
    #     print("Home")

    # def movies_stack(self):
    #     print("Movies")


if __name__ == "__main__":
    app = PiTV()
    app.login_window.fullscreen()
    app.login_window.show_all()
    Gtk.main()
