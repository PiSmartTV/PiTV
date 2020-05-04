"""
Category and ImageTile template for PiTV, depends on sidebar.glade
"""
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@Gtk.Template(filename=os.path.join(ROOT_DIR, "image_tile.glade"))
class ImageTile(Gtk.Button):
    __gtype_name__ = "ImageTile"

    def __init__(self, data=None, **kwargs):
        super().__init__(**kwargs)

        if data:
            try:
                self.set_data(data[0], data[1], data[2])
            except:
                raise Exception("You have to either pass (name, image, function) or nothing")

        # TODO: Fix this line
        self.image, self.label = self.get_children()[0].get_children()

    def set_data(name, image, function):
        self.name = name
        self.image = image
        self.function = function

        self.label.set_label(name)
        self.connect("clicked", function)

    @classmethod
    def from_movie(cls, movie):

        self.set_data(movie["title"])



@Gtk.Template(filename=os.path.join(ROOT_DIR, "category.glade"))
class Category(Gtk.Box):
    __gtype_name__ = 'Category'
    # TODO: Arrow navigation

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # TODO: This is really bad solution fix this as soon as possible
        self.scroll_view = self.get_children()[1]
        self.box = self.scroll_view.get_children()[0].get_children()[0]

        self.box.set_focus_hadjustment(self.scroll_view.get_hadjustment())

        for i in range(10):
            it = ImageTile(name="bla", icon="bla",
                           function=print, func_args=("bla",))
            self.box.pack_start(it, False, False, 2)
