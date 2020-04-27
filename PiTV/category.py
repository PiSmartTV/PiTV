"""
Category and ImageTile template for PiTV, depends on sidebar.glade
"""
import os

# Bypass linters
if True:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@Gtk.Template(filename=os.path.join(ROOT_DIR, "image_tile.glade"))
class ImageTile(Gtk.Button):
    __gtype_name__ = "ImageTile"

    def __init__(self, name=None, icon=None, **kwargs):
        super().__init__(**kwargs)

        if name:
            pass


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
            it = ImageTile()
            self.box.pack_start(it, False, False, 2)
