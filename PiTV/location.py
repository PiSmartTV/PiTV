from requests import get
from json import loads
import socket


# Returns hostname of machine
def getHostname():
    return socket.getfqdn()


# Returns local IP address
def getLocalIP():
    return socket.gethostbyname(socket.gethostname())


class Location:
    def __init__(self):
        self.location_info = loads(get("http://ip-api.com/json/").text)

    @property
    def city(self):
        return self.location_info["city"]

    @property
    def public_ip(self):
        return self.location_info["query"]

    @property
    def timezone(self):
        return self.location_info["timezone"]

    @property
    def country(self):
        return self.location_info["country"]

    @property
    def country_code(self):
        return self.location_info["countryCode"]

    @property
    def region(self):
        return self.location_info["regionName"]
