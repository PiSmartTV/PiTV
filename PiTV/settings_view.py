"""
SettingsView, SettingsRow template for PiTV, depends on settings_view.glade
TODO: Make this file better coded, add comments, fix issues
This file is the worst
"""
import os
from settings import UserSettings
from pathlib import Path

# Bypass linters
if True:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

HOME_DIR = os.path.dirname(os.path.abspath(__file__))

WIDGET_GETTERS = {
    Gtk.Scale: "get_value",
    # Gtk.ComboBox,
}


Percentage = float


class Setting:
    name = None  # REQUIRED
    name_db = None  # IF NULL, SET TO NAME
    default = None  # IF NULL, SET TO VALUE
    available = None

    def __init__(self, name_db, default, name=None, available=None):
        self.name_db = name_db
        self.available = available
        self.name = name if name else name_db
        self.default = default


@Gtk.Template(filename=os.path.join(HOME_DIR, "settings_view.glade"))
class SettingsView(Gtk.Box):
    __gtype_name__ = 'SettingsView'

    def __init__(self, username, settings,  **kwargs):
        super().__init__(**kwargs)

        # TODO: also find better solution for this
        self.settings_list, self.buttons = self.get_children()
        self.apply_button, self.reset_button = self.buttons.get_children()

        db_location = os.path.join(str(Path.home()), "pitv.db")

        self.settings_db = UserSettings(username, db_location)
        self.settings = settings
        self.count = 0

        self._values = []

        for i in self.settings:
            self.add_setting(i)

        self.apply_button.connect("clicked", self.apply)
        self.reset_button.connect("clicked", self.reset)

    def apply(self, button):
        # Apply code
        # This will save settings to config directory
        pass

    def reset(self, button):
        # Reset everything
        pass

    def add_setting(self, setting):
        setter_widget = Gtk.Label(label=str(setting.default))

        if setting.available:
            available_store = Gtk.ListStore(type(setting.default))
            setter_widget = Gtk.ComboBox.new_with_model(available_store)

            for i, val in enumerate(setting.available):
                available_store.append([val])
                if val == setting.default:
                    setter_widget.set_active(i)

            renderer_text = Gtk.CellRendererText()
            setter_widget.pack_start(renderer_text, True)
            setter_widget.add_attribute(renderer_text, "text", 0)

            print(setter_widget.get_active())

        elif isinstance(setting.default, Percentage):
            setter_widget = Gtk.Scale.new_with_range(
                Gtk.Orientation.HORIZONTAL, 0, 100, 1
            )
            setter_widget.set_size_request(500, -1)

        self._values.append(setter_widget)
        widget = Gtk.Box()
        widget.pack_start(Gtk.Label(label=setting.name), False, False, 0)
        widget.pack_end(setter_widget, False, False, 0)
        self.settings_list.insert(widget, self.count)
        self.count += 1

    def get_value(self, widget):
        pass

    def get_values(self):
        return [self.get_value(i) for i in self._values]
