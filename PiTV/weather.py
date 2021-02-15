from requests import get
from json import loads

from location import Location


class Weather:
    def __init__(self, measure, location: Location, apikey=None):
        self.apikey = apikey
        self.measure = measure
        self.location = location

        self.refresh()

    def refresh(self):
        if self.apikey:
            self.url = "https://api.openweathermap.org/data/2.5/weather?" \
                "q={}&units={}&appid={}"

            self.response = get(self.url.format(
                self.location.city,
                self.measure,
                self.apikey
            )).text
        else:
            self.url = "http://www.7timer.info/bin/astro.php?lon={}&lat={}" \
                "&unit={}&output=json&tzshift=0"

            self.response = get(self.url.format(
                self.location.longitude,
                self.location.latitude,
                self.measure
            )).text

        self.parsed = loads(self.response)

    @property
    def temperature(self):
        if self.apikey:
            return self.parsed["main"]["temp"]
        else:
            return self.parsed["dataseries"][0]["temp2m"]

    @property
    def icon_code(self):
        if self.apikey:
            return self.parsed["weather"][0]["icon"]
        else:
            return None
