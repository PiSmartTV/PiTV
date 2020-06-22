# PiTV
New version of SmartTV. Better code, faster, optimized.

## Installation
It is advised to use numix icon theme, because that will be default.<br />
Here I am using canta theme, but it works on any theme

If you want weather, you have to have [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) account
```sh
git clone https://www.github.com/PiSmartTV/PiTV.git
cd PiTV
pip install -r requirements.txt
```


## Running

```sh
export OPEN_WEATHER_API_KEY="YOUR_OPEN_WEATHER_MAP_KEY_HERE"
export UNIT_SYSTEM="metric"
python3 PiTV/application.py
```
Or run it with defaults (no weather info)
```sh
python3 PiTV/application.py
```

## Screenshots
Default theme is Canta by vinceliuice: https://github.com/vinceliuice/Canta-theme
![](screenshots/Code.png?raw=true)
![](screenshots/Trending.png?raw=true)

## Contributing

```sh
git clone https://www.github.com/PiSmartTV/PiTV.git
cd PiTV
grep "TODO" -rnw .
```

And fix what is wrong!
