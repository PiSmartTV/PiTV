# PiTV
New version of SmartTV. Better code, faster, optimized.

## Installation
It is advised to use numix circle icon theme and [official theme](https://github.com/PiSmartTV/Canta-theme).

If you want OpenWeatherMap weather info, you have to get [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) account.
```sh
git clone https://www.github.com/PiSmartTV/PiTV.git
cd PiTV
```

### Installing dependencies
Recommended way:
```
pipenv install
pipenv shell
```
Old way:

```
pip install -r requirements.txt
```


## Running

```sh
export OPEN_WEATHER_API_KEY="YOUR_OPEN_WEATHER_MAP_KEY_HERE"
export UNIT_SYSTEM="metric"
python3 -m PiTV
```
Or run it with defaults (7timer weather info)
```sh
python3 -m PiTV
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
