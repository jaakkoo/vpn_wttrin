# vpn_wttrin
I'm almost always behind VPN so the excellent wttr.in service cannot know my current location based on IP. And because i'm lazy I don't want to type my current location there manually every time (also i should know where I am?!).

There is no error handling, so if it works it works. If not, submit a pull request ;)

Note! Works only on OSX.

## Usage
1. Get your api key for google location services: https://developers.google.com/maps/documentation/geolocation/get-api-key
2. Save your key to API_KEY in weather.py
3. `./weather.py`


## What?
Small python script that:

1. Gets's nearby wifi hotspots
2. Finds your current location using google geolocation services
3. Finds your current city using openstreetmap nominatim
4. Prints the weather in the city you currently are in.


## Why?
Lazy.
