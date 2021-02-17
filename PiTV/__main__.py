from .application import *
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # NOQA

Gtk.init()
app = PiTV()
app.window.fullscreen()
app.window.show_all()
Gtk.main()