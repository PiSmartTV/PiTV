"""
Class for weather data.
"""
from json import loads

from requests import get
from location import Location


class Weather:
    """Class for weather data."""
    def __init__(self, measure, location: Location, apikey=None):
        self.apikey = apikey
        self.measure = measure
        self.location = location

        self.refresh()

    def refresh(self):
        """Refetch data from API."""
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
        """Get temperature."""
        if self.apikey:
            return self.parsed["main"]["temp"]
        return self.parsed["dataseries"][0]["temp2m"]

    @property
    def icon_code(self):
        """Get icon code (can be None)"""
        if self.apikey:
            return self.parsed["weather"][0]["icon"]
        return None
