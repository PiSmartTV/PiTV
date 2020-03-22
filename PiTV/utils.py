"""
Module utils for PiTV
"""
import socket


def check_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Checks if is connected to internet

    :param host: host to ping (Default value = "8.8.8.8")
    :param port: port of the host to ping (Default value = 53)
    :param timeout: maximum tries (Default value = 3)
    :returns: bool
    """

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False
