#!/usr/bin/env python3
from threading import Thread
from gi.repository import Gtk, GLib, Gio
from entertainment import Weather, Location
import requests
import os
import sys


HOME_DIR = os.path.dirname(os.path.abspath(__file__))
SIDEBAR_WIDTH = 250

sys.path.append(HOME_DIR)

CONDITIONS = {
    "01d": "weather-clear",
    "02d": "weather-few-clouds",
    "03d": "weather-overcast",
    "04d": "weather-overcast",
    "09d": "weather-showers",
    "10d": "weather-showers-scattered",
    "11d": "weather-storm",
    "13d": "weather-snow",
    "50d": "weather-fog",
    "01n": "weather-clear-night",
    "02n": "weather-few-clouds-night",
    "03n": "weather-overcast",
    "04n": "weather-overcast",
    "09n": "weather-showers",
    "10n": "weather-showers-scattered",
    "11n": "weather-storm",
    "13n": "weather-snow",
    "50n": "weather-fog"
}

SIDEBAR_ITEMS = {

}


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
            os.path.join(HOME_DIR, "main.glade"))
        self.builder.connect_signals(self)

        self.login_window = self.builder.get_object(
            "login_window")
        self.login_window.fullscreen()

        self.home_window = self.builder.get_object(
            "home_window")

        # Website host URL (As I currenly don't have website,
        # localhost is development sollution)
        self.host = "http://127.0.0.1:8000"

        self.login_init()

    def home_refresh(self):
        # Fetch weather info
        # TODO:Prompt user for his openweathermap api key
        self.weather_info = Weather(
            self.openweather_apikey,
            self.unit_system,
            self.city_and_country
        )

        self.weather_image.set_from_icon_name(
            CONDITIONS[self.weather_info.icon_code], SIDEBAR_WIDTH
        )

        if self.unit_system == "metric":
            postfix = "C"
        elif self.unit_system == "imperial":
            postfix = "F"

        self.weather_label.set_label(
            str(self.weather_info.temperature) + chr(176) + postfix)

    def home_init(self):
        # Fetch some environment variables
        self.openweather_apikey = os.environ.get("OPEN_WEATHER_API_KEY")
        self.unit_system = os.environ.get("UNIT_SYSTEM")

        # Setting objects public variables to their object
        self.weather_image = self.builder.get_object("weather_image")
        self.weather_label = self.builder.get_object("weather_label")

        # Fetch location
        self.location_info = Location()

        # Make formatted location for open weather map
        self.city_and_country = "{},{}".format(
            self.location_info.city,
            self.location_info.countryCode
        )

        # Fetch all data that needs to be refreshed every 2 minutes
        self.home_refresh()

        # 60*2*1000=120000 Why? 1000 miliseconds is 1 second, we need 2 minutes
        GLib.timeout_add(120000, self.home_refresh)

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
        except Exception as e:
            self.login_error_label.set_visible(True)
            self.login_error_label.set_text(
                "Error code:" + str(e)
            )
            return

        self.login_spinner.set_visible(False)

        if response.status_code == 200:
            GLib.idle_add(self.switch_window, self.home_window)
            GLib.idle_add(self.home_init)
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

        self.login_thread = Thread(target=self.validate_login)
        self.login_thread.start()

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
        thread = Thread(target=self.validate_signup)
        thread.start()

    def validate_signup(self):
        # TODO: Add more response error for user to know what to do

        if self.retype_password != self.password:
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
        else:
            self.signup_error_label.set_visible(True)
            self.signup_error_label.set_text(
                "Error code:" + str(response.status_code))


if __name__ == "__main__":
    app = PiTV()
    app.login_window.show()
    Gtk.main()
