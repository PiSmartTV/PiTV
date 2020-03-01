from gi.repository import Gtk


class ListTile(Gtk.Box):
    def __init__(self, title, icon_name):
        Gtk.Box.__init__(self)
        image = Gtk.Image.new_from_icon_name(icon_name, 6)
        label = Gtk.Label(label=title)  # TODO: Make it bigger with pango
        self.pack_end(image, False, False, 6)
        self.pack_start(label, False, True, 6)
