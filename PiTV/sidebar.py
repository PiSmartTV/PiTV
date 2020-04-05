"""
Sidebar, ListTile and WeatherBox template for PiTV, depends on sidebar.glade, weather_box.glade, list_tile.glade
"""
import os

# Bypass linters
if True:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

HOME_DIR = os.path.dirname(os.path.abspath(__file__))

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

UNITS = {
    "metric": {"temperature": "C"},
    "imperial": {"temperature": "F"}
}


@Gtk.Template(filename=os.path.join(HOME_DIR, "sidebar.glade"))
class SideBar(Gtk.Box):
    __gtype_name__ = 'SideBar'

    def __init__(self, stack, **kwargs):
        super().__init__(**kwargs)
        self.stack = stack
        self.index = 0

        # TODO:Better solution for this (critical)
        self.actions = self.get_children()[0].get_children()[
            0].get_children()[0]

        # Signal when row is selected
        self.actions.connect("row-selected", self.on_sidebar_row_selected)

    def add_start_widget(self, widget):
        # Pack widget on the start in box ordered first
        self.pack_start(widget, False, False, 2)
        self.reorder_child(widget, 0)

    def add_action_widget(self, widget):
        # Add widget to list of actions
        self.actions.insert(widget, self.index)

        if self.index == 0:
            self.actions.select_row(self.actions.get_row_at_index(0))

        # Increment index by one, so next widget will be packed next
        self.index += 1

    def add_action(self, text, icon_name):
        # Standard ListTile
        tile = ListTile(text, icon_name)

        # Add tile to action widgets
        self.add_action_widget(tile)

    def on_sidebar_row_selected(self, listbox, listbox_row):
        # Connected to row_select of self.actions
        # Switch to stack to index of selected self.actions row
        index = listbox_row.get_index()
        children = self.stack.get_children()
        self.stack.set_visible_child(children[index])


@Gtk.Template(filename=os.path.join(HOME_DIR, "weather_box.glade"))
class WeatherBox(Gtk.Box):
    __gtype_name__ = "WeatherBox"

    def __init__(self, width, weather_object=None, **kwargs):
        super().__init__(**kwargs)

        # Making method arguments public
        self.weather_object = weather_object
        if weather_object:
            self.temperature = self.weather_object.temperature
            self.icon_name = CONDITIONS[self.weather_object.icon_code]

        self.width = width

        # Gettings only 2 children in this order
        self.image, self.label = self.get_children()

        self.refresh()

    def set_weather_object(self, weather_object, update=False):
        self.weather_object = weather_object
        if update:
            self.update_data()
            self.refresh()

    def update_data(self):
        # Checking if weather_object exists
        if self.weather_object:
            # Updating new data from weather object
            # Getting the data
            self.weather_object.refresh()

            # Setting the data
            self.temperature = self.weather_object.temperature
            self.icon_name = CONDITIONS[self.weather_object.icon_code]

    def refresh(self):
        # Checking if weather_object exists
        if self.weather_object:
            # Changing the label to data in public variable temperature
            self.label.set_label(
                str(self.temperature) +
                chr(176) +  # Degree sign
                UNITS[self.weather_object.measure]["temperature"]
            )

            # Changing the label to data in public variables icon_name and width
            self.image.set_from_icon_name(self.icon_name, self.width)
        else:
            self.label.set_label("?"+chr(176)+"?")
            self.image.set_from_icon_name("image-loading", self.width)

    def show(self):
        super().__init__()
        self.image.show()
        self.label.show()


@Gtk.Template(filename=os.path.join(HOME_DIR, "list_tile.glade"))
class ListTile(Gtk.Box):
    __gtype_name__ = 'ListTile'

    def __init__(self, text, icon_name, **kwargs):
        super().__init__(**kwargs)
        label, image = self.get_children()
        label.set_label(text)

        # Icon size doesn't work, don't know why
        image.set_from_icon_name(icon_name, 48)
