"""Non-gtk functions and classes module for PiTV."""
import socket
import os
import requests
from config import CACHE_DIR, HOST, ROOT_DIR


def check_internet(host="8.8.8.8", port=53, timeout=3):
    """Check if is connected to internet.

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
    """Check if PiTV server is up.

    :param timeout: maximum retries (Default value = 3)
    :returns: bool

    """
    return check_internet(
        host=HOST,
        port=443,
        timeout=timeout
    )


def cache_file(url, filename):
    """Cache file in CACHE_DIR location.

    :param url: URL of file to be downloaded
    :param filename: Name of file, absolute path is CACHE_DIR+filename
    :returns: absolute path to file
    :raises requests.exceptions.MissingSchema: The URL schema (e.g. http or
    https) is missing
    :raises requests.exceptions.ConnectionError: The URL doesn't exist or there
    is no internet connection
    :raises requests.exceptions.InvalidSchema: The URL schema is invalid (e.g.
    ftp)
    :raises Exception: Response code is not 200

    """
    if not os.path.isdir(CACHE_DIR):
        os.mkdir(CACHE_DIR)

    filepath = os.path.join(CACHE_DIR, filename)

    if os.path.exists(filepath):
        return filepath

    with requests.get(url, stream=True) as resp:
        resp.raise_for_status()
        with open(filepath, 'wb') as file:
            for chunk in resp.iter_content(chunk_size=4096):
                file.write(chunk)
    return filepath


def rel_path(filename):
    """Get path of filename.

    :param filename: Name of file relative to ROOT_DIR
    :returns: absolute path to file
    """

    return os.path.join(ROOT_DIR, filename)
