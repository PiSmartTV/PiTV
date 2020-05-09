"""This will be rewritten."""
import sqlite3

CREATE_TABLE = \
    "CREATE TABLE IF NOT EXISTS users ("\
    "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, "\
    "username TEXT NOT NULL UNIQUE);"


TYPES = {
    "int": "INTEGER",
    "str": "TEXT",
    "bool": "BOOL",
    "datetime": "DATE",
    "float": "REAL",
    "Percentage": "REAL"
}

SET = ""

TABLES = "PRAGMA table_info(users);"


class UserSettings(sqlite3.Connection):
    """Save user settings to database.

    :param username: username
    :param location: full path to save the database

    """

    def __init__(self, username, location, *args):
        super().__init__(location, *args)
        self.username = username
        self.cursor = self.cursor()
        self.cursor.execute(CREATE_TABLE)

        self.cursor.execute(
            "SELECT username FROM users WHERE username=?",
            (username,)
        )

        if not self.cursor.fetchone():
            self.cursor.execute(
                "INSERT INTO users (username) VALUES (?)",
                (username,)
            )

    def _get_type(self, value):
        """

        :param value: value
        :returns: SQLite3 type equivalent

        """
        val_type = type(value).__name__
        return TYPES[val_type] if val_type in TYPES.keys() else "BLOB"

    def set(self, col, value):
        """Set a value for setting.

        :param col: setting
        :param value: value for setting

        """
        columns = [i[1] for i in self.cursor.execute(TABLES)]

        if col not in columns:
            self.cursor.execute(
                f"ALTER TABLE users ADD COLUMN {col} {self._get_type(value)}"
            )

        self.cursor.execute(
            f"UPDATE users SET {col}=? WHERE username=?",
            (value, self.username)
        )

    def setsave(self, col, value):
        """Set a value for setting.

        :param col: setting
        :param value: value for setting

        """
        self.set(col, value)
        self.save()

    def save(self):
        """Save changes to the database."""
        self.commit()
