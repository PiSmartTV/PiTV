"""
SettingsView, SettingsRow template for PiTV, depends on settings_view.glade
TODO: Make this file better coded, add comments, fix issues
This file is the worst
"""
import os
import json

from ..config import ROOT_DIR

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # NOQA


def load_settings(filepath):
    with open(filepath, "r") as file:
        raw_json = file.read()
    return json.loads(raw_json)["settings"]


@Gtk.Template(filename=os.path.join(ROOT_DIR, "ui",  "settings_view.glade"))
class SettingsView(Gtk.Box):
    __gtype_name__ = 'SettingsView'

    def __init__(self, username, settings,  **kwargs):
        super().__init__(**kwargs)

        # TODO: also find better solution for this
        self.settings_list, self.buttons = self.get_children()
        self.apply_button, self.reset_button = self.buttons.get_children()
