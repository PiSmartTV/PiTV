"""
Category and ImageTile template for PiTV, depends on sidebar.glade
"""
import os

# Bypass linters
if True:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk


@Gtk.Template(filename="image_tile.glade")
class ImageTile(Gtk.Button):
    __gtype_name__ = "ImageTile"

    def __init__(self, name=None, icon=None, **kwargs):
        super().__init__(**kwargs)


@Gtk.Template(filename="category.glade")
class Category(Gtk.Box):
    __gtype_name__ = 'Category'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # TODO: This is really bad solution fix this as soon as possible
        self.flowbox = self.get_children()[1].get_children()[
            0].get_children()[0]

        for i in range(10):
            it = ImageTile()
            self.flowbox.insert(it, i)

        # self.flowbox = get_children()[0]
