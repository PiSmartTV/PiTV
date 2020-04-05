from requests import get
from json import loads


class Weather:
    def __init__(self, apikey, measure, location):
        self.apikey = apikey
        self.measure = measure
        self.location = location

        self.url = "https://api.openweathermap.org/data/2.5/weather?"\
            "q={}&units={}&appid={}"
        self.response = get(self.url.format(location, measure, apikey)).text

        self.parsed = loads(self.response)

    def refresh(self):
        self.response = get(self.url.format(
            self.location,
            self.measure,
            self.apikey
        )).text
        self.parsed = loads(self.response)

    @property
    def temperature(self):
        return self.parsed["main"]["temp"]

    @property
    def icon_code(self):
        return self.parsed["weather"][0]["icon"]
