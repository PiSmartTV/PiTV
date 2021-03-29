from requests import get
from json import loads
import socket


# Returns hostname of machine
def getHostname():
    return socket.getfqdn()


# Returns local IP address
def getLocalIP(lookup="8.8.8.8", port=80) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((lookup, port))
    ip = s.getsockname()[0]
    s.close()

    return ip


class Location:
    def __init__(self):
        self.location_info = loads(get("https://freegeoip.app/json/").text)

    @property
    def city(self):
        return self.location_info["city"]

    @property
    def public_ip(self):
        return self.location_info["ip"]

    @property
    def timezone(self):
        return self.location_info["time_zone"]

    @property
    def country(self):
        return self.location_info["country_name"]

    @property
    def country_code(self):
        return self.location_info["country_code"]

    @property
    def region(self):
        return self.location_info["region_name"]

    @property
    def longitude(self):
        return self.location_info["longitude"]
    
    @property
    def latitude(self):
        return self.location_info["latitude"]
