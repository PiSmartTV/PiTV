import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, WebKit2
# from ..config import MONITOR_HEIGHT
MONITOR_HEIGHT = 1080

from imdb import IMDb

class MoviePreview(Gtk.Window):
    __gtype_name__ = "MoviePreview"

    def __init__(self, movie):
        super().__init__(title=movie["title"])
        self.movie = movie

        ratings = round(movie['rating']/2, 1)

        divider = Gtk.Box(spacing=18)

        self._title = Gtk.Label()
        self._title.set_markup(
            f"<span font_desc='20' weight='bold'>{movie['title']}</span>"
        )
        self._title.set_hexpand(True)
        self._title.set_halign(Gtk.Align.START)

        self.desc = Gtk.Label()
        self.desc.set_markup(
            f"<span font_desc='16' weight='semibold'>{movie['title']}</span>"
        )
        self.desc.set_line_wrap(True)
        self.desc.set_halign(Gtk.Align.START)

        self.add(self._title)


if __name__ == "__main__":
    # ia = IMDb()
    # the_matrix = ia.get_movie('0133093')
    the_matrix = {'title': "MATRIX 1003", 'rating' : 7.8}

    Gtk.init()
    window = MoviePreview(the_matrix)
    window.fullscreen()
    window.show_all()
    Gtk.main()