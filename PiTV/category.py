"""Category and ImageTile template, depends on category.glade, image_tile.glade."""
from utils import cache_file, is_cached
from config import ROOT_DIR
from threading import Thread
import os
import re

import imdb
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf, GLib  # NOQA


@Gtk.Template(filename=os.path.join(ROOT_DIR, "image_tile.glade"))
class ImageTile(Gtk.Button):
    __gtype_name__ = "ImageTile"

    name = ""
    image_location = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # TODO: Fix this line
        self.image, self.label = self.get_children()[0].get_children()

    def draw(self):
        self.label.set_label(self.name)
        self.image.set_from_file(self.image_location)


@Gtk.Template(filename=os.path.join(ROOT_DIR, "category.glade"))
class Category(Gtk.Box):
    __gtype_name__ = 'Category'

    def __init__(self, fetch_type, limit=12, **kwargs):
        super().__init__(**kwargs)

        self.fetch_type = fetch_type
        self.limit = limit

        self.cat_title = ' '.join(re.findall("[^(get)]([a-z]+)", fetch_type))

        # TODO: This is really bad solution fix this as soon as possible
        self.title, self.scroll_view = self.get_children()
        self.box = self.scroll_view.get_children()[0].get_children()[0]

        self.title.set_label(self.cat_title.capitalize())

        self.box.set_focus_hadjustment(self.scroll_view.get_hadjustment())
        self.tiles = []
        self.thread_list = []

        for _ in range(limit):
            temp_it = ImageTile()
            self.tiles.append(temp_it)
            self.box.pack_start(temp_it, False, False, 2)

        self.fetch_data()

    def update_imagetile(self, image_tile, movie):
        self.create_thread(self._update_imagetile, image_tile, movie)

    def _update_imagetile(self, image_tile, movie):
        filename = movie.getID()+".jpg"

        image_sized = ""
        if not is_cached(filename):
            self._imdb.update(movie)

            image_tile.name = movie["title"]
            image_sized = ".".join(movie["full-size cover url"].split(".")[:-1])
            image_sized += "._V1_SY350_.jpg"

        filename = cache_file(image_sized, filename)
        image_tile.image_location = filename
        image_tile.draw()

    def create_thread(self, target, *args):
        thread = Thread(target=target, args=args)
        thread.setName(target.__name__)
        thread.setDaemon(True)
        thread.start()

    def _fetch_data(self):
        self._imdb = imdb.IMDb()
        fetch_func = getattr(self._imdb, self.fetch_type)
        self.fetched_data = fetch_func()

        for i, img_tile in enumerate(self.tiles):
            movie = self.fetched_data[i]
            try:
                self._update_imagetile(img_tile, movie)
            except:
                continue
            #GLib.idle_add(self.update_imagetile, img_tile, movie)

    def fetch_data(self):
        self.create_thread(self._fetch_data)
