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


class Category(Gtk.Box):
    def __init__(self, category_name, items):
        Gtk.Box.__init__(
            self, orientation=Gtk.Orientation.VERTICAL, spacing=2)

        # Title
        self.title = Gtk.Label(label=category_name)
        self.title.set_halign(Gtk.Align.START)
        self.pack_start(self.title, False, False, 4)

        # Scrollable
        self.scroll_view = Gtk.ScrolledWindow()
        self.scroll_view.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.NEVER
        )
        self.pack_end(self.scroll_view, True, True, 0)

        # Grid that hold cards
        self.grid = Gtk.Grid()
        # self.grid.set_size_request(1000, 500)

        for i, j in enumerate(items):
            name, image = j
            temp_button = Gtk.Button()
            # temp_button.set_valign(Gtk.Align.FILL)
            # temp_button.set_halign(Gtk.Align.FILL)
            # temp_button.set_hexpand(True)
            # temp_button.set_vexpand(True)
            temp_button.set_relief(Gtk.ReliefStyle.NONE)
            temp_box = Gtk.Box()
            temp_box.set_orientation(Gtk.Orientation.VERTICAL)
            temp_image = Gtk.Image.new_from_file(image)

            temp_box.pack_start(temp_image, False, False, 2)
            temp_box.pack_start(Gtk.Label(label=name), False, False, 2)
            temp_button.add(temp_box)
            self.grid.attach(temp_button, i, 0, 1, 1)

        self.scroll_view.add(self.grid)


# For testing purposes
if __name__ == "__main__":
    win = Gtk.Window()
    listbox = Gtk.ListBox()
    listbox.insert(ListTile("Blah", "go-home"), 0)
    win.add(listbox)
    win.show_all()
    Gtk.main()
