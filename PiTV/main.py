from threading import Thread
from gi.repository import Gtk, GObject
from requests import post


class LoginWindow:
    def __init__(self):
        self.builder = Gtk.Builder()                # Initialize builder
        self.builder.add_from_file("./main.glade")  # Glade file
        self.builder.connect_signals(self)          # Connect Signals

        self.window = self.builder.get_object(      # Get window object
            "login_window")
        self.window.fullscreen()

        self.stack_state = 0                      # Stack index
        self.host = "https://pitv.herokuapp.com"  # Website host URL

        # Default to empty string
        self.password = ""
        self.username = ""
        self.email = ""
        self.name = ""

        # Threading signals
        self.create_signal("validate_login", self._validate_login)
        self.create_signal("validate_signup", self._validate_signup)

    def create_signal(self, name, function):
        GObject.signal_new(name,
                           self.window,
                           GObject.SignalFlags.RUN_LAST,
                           GObject.TYPE_PYOBJECT,
                           (GObject.TYPE_PYOBJECT,)
                           )
        self.window.connect(name, function)

    def toggle_stack(self, *args):

        # Change state to opposite
        self.stack_state = int(not self.stack_state)

        # Switch to stack of index stack_state
        stack = self.builder.get_object("login_stack")
        stack.set_visible_child(stack.get_children()[self.stack_state])
        stack.get_children()[self.stack_state].show()

    def destroy(self, *args):
        Gtk.main_quit()

    def show(self):
        self.window.show_all()

    def hide(self):
        self.window.hide()

    def validate_login(self):
        # TODO: Add more response error for user to know what to do

        response = post(self.host+"/login", data={
            "username": self.username,
            "password": self.password
        })
        self.builder.get_object("spinner_revealer").set_reveal_child(False)
        if response.status_code == 200:
            self.window.emit("validate_login", None)

        else:
            self.builder.get_object("error_revealer").set_reveal_child(True)
            self.builder.get_object("error_label").set_text(
                "Error code:" + str(response.status_code)
            )

    def _validate_login(self, *args):
        bla = SomeWindow()
        bla.fullscreen()
        bla.show_all()

    def login(self, *args):
        # Get username and password and store it in public variables
        self.username = self.builder.get_object(
            "login_username_field").get_text()
        self.password = self.builder.get_object(
            "login_password_field").get_text()

        # Thread for validating and obtaining the user token
        # TODO: Fetch token
        self.builder.get_object("spinner_revealer").set_reveal_child(True)
        self.login_thread = Thread(target=self.validate_login)
        self.login_thread.start()

    def signup(self, *args):
        # Get signup info and store it in public variables
        self.username = self.builder.get_object(
            "signup_username_field").get_text()
        self.password = self.builder.get_object(
            "signup_password_field").get_text()
        self.email = self.builder.get_object(
            "signup_email_field").get_text()
        self.name = self.builder.get_object(
            "signup_name_field").get_text()

        # Thread for validating and obtaining the user token
        thread = Thread(target=self.validate_signup)
        thread.start()

    def validate_signup(self):
        # TODO: Add more response error for user to know what to do

        response = post(self.host+"/register", data={
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "email": self.email
        })
        if response.status_code == 200:
            self.window.emit("validate_signup", None)

    def _validate_signup(self, *args):
        # Add label that tells the user success message
        self.toggle_stack()


class SomeWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)


LoginWindow().show()
Gtk.main()
