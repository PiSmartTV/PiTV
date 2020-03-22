"""
Non-gtk functions and classes module for PiTV
"""
import socket
import sqlite3


def check_internet(host="8.8.8.8", port=53, timeout=3):
    """Checks if is connected to internet

    :param host: host to ping (Default value = "8.8.8.8")
    :param port: port of the host to ping (Default value = 53)
    :param timeout: maximum retries (Default value = 3)
    :returns: bool

    """

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


def check_server(timeout):
    """Checks if PiTV server is up

    :param timeout: maximum retries (Defaukt value = 3)
    :returns bool
    """
    return check_internet(
        host="pitv.herokuapp.com",
        port=443,
        timeout=timeout
    )


# TODO: Test and fix this class, don't use it now
class Settings(dict):
    """SQLite3 Wrapper to store config file

    :param username: unique username string

    """

    def __init__(self, username):
        super().__init__()

        self.username = username

        # Set it to tmp so it gets deleted on reboot
        # This is for testing
        # TODO: Change this to something like ~/.config/pitv
        self.connection = sqlite3.connect("/tmp/settings.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS settings"
            "("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "username varchar(64) UNIQUE"
            ");")

    def flush(self):
        """Adds all keys to database as columns"""
        for key, value in self.items():
            # TODO: Add edge cases, this function is very bad

            # Checking the variable type
            if isinstance(value, str):
                value = "text"
            else:
                column_type = type(value).__name__

            # Adding column to settings
            self.cursor.execute(
                "ALTER TABLE settings ADD COLUMN {} {};".format(key, column_type))

    def save(self):
        """Commits changes to database
        alias to connection.commit()


        """
        self.connection.commit()
