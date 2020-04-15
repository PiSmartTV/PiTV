"""
Non-gtk functions and classes module for PiTV
"""
import socket
import sqlite3
import os
import requests

# TODO: This is temporary change this to system cache folder
# like ~/.cache
# This will also remove on reboot
CACHE_DIR = "/tmp/pitv"
HOST = "https://pitv.herokuapp.com/"


def check_internet(host="8.8.8.8", port=53, timeout=3):
    """Checks if is connected to internet

    :param host: host to ping (Default value = "8.8.8.8")
    :param port: port of the host to ping (Default value = 53)
    :param timeout: maximum retries (Default value = 3)
    :returns: bool

    """

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


def check_server(timeout=3):
    """Checks if PiTV server is up

    :param timeout: maximum retries (Defaukt value = 3) (Default value = 3)
    :returns: bool

    """
    return check_internet(
        host=HOST,
        port=443,
        timeout=timeout
    )


def cache_file(url, filename):
    """Caches file in CACHE_DIR location

    :param url: URL of file to be downloaded\n
    :param filename: Name of file, absolute path is CACHE_DIR+filename\n
    :returns: absolute path to file\n
    :raises requests.exceptions.MissingSchema: The URL schema (e.g. http or https) is missing\n
    :raises requests.exceptions.ConnectionError: The URL doesn't exist or there is no internet connection\n
    :raises requests.exceptions.InvalidSchema: The URL schema is invalid (e.g. ftp)\n
    :raises Exception: Response code is not 200\n

    """

    if not os.path.isdir(CACHE_DIR):
        os.mkdir(CACHE_DIR)

    filepath = os.path.join(CACHE_DIR, filename)
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, "w+") as file:
            file.write(response.text)
        return filepath
    else:
        raise Exception(f"Response code: {response.status_code}")
