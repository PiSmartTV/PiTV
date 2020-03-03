from gi.repository import Gtk, Pango


class ListTile(Gtk.Box):
    def __init__(self, title, icon_name):
        Gtk.Box.__init__(self)
        self.image = Gtk.Image.new_from_icon_name(icon_name, 6)
        self.label = Gtk.Label(label=title)  # TODO: Make it bigger with pango

        # attributes = Pango.AttrList()
        # attrib = Pango.AttrSize
        # attrib.size = 30000
        # attributes.insert()

        self.pack_end(self.image, False, False, 6)
        self.pack_start(self.label, False, True, 6)
