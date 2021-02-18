import html

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

class ImageTile(Gtk.Button):
    __gtype_name__ = "ImageTile"

    name = ""
    image_location = ""

    _label_markup = "<b>{}</b>"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Title of the image tile
        self._label = Gtk.Label()
        self._label.set_ellipsize(Pango.EllipsizeMode.END)

        # Image of the image tile
        self._image = Gtk.Image.new_from_icon_name("image-loading", 6)
        self._image.set_pixel_size(200)
        self._image.set_size_request(236, 350)

        # Vertical box to hold image and title
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(self._image, True, True, 2)
        box.pack_start(self._label, False, True, 2)

        # Add box to button
        self.add(box)

    def draw(self):
        self.name = html.escape(self.name)

        self._label.set_markup(self._label_markup.format(self.name))
        self._image.set_from_file(self.image_location)

        print(self.image_location)
