#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import subprocess
import shlex
import re
import json
import urllib2

API_KEY = ''

AIRPORT_TOOL = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport'
GEOLOCATION_URL = 'https://www.googleapis.com/geolocation/v1/geolocate?key=%s' % API_KEY
NOMINATIM_URL =  'http://nominatim.openstreetmap.org'
WTTRIN_URL = 'http://wttr.in/'


def _make_http_request(url, data=None, headers={}):
    req = urllib2.Request(url, data, headers)
    return urllib2.urlopen(req).read()


def _execute(command):
    process = subprocess.Popen(shlex.split(command), stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    stdout, _ = process.communicate()
    return stdout


def get_visible_networks():
    matcher = re.compile('((?:[A-Fa-f0-9]{2}[:-]){5}(?:[A-Fa-f0-9]{2}))\s(-?\d+)')
    for network in _execute('%s scan' % AIRPORT_TOOL).split('\n')[1:]:
        match = matcher.findall(network)
        if match:
            yield match.pop()


def find_current_location(query):
    return json.loads(_make_http_request(GEOLOCATION_URL, query, {'Content-Type': 'application/json'}))


def get_current_city(lat, lon):
    url = '%s/reverse?format=json&lat=%s&lon=%s&zoom=18&addressdetails=1' % (NOMINATIM_URL, lat, lon)
    return json.loads(_make_http_request(url))


def get_weather_in(city):
    return _make_http_request('%s/%s?m' % (WTTRIN_URL, city), None, {'User-Agent': 'curl'})


def main():
    query = {'wifiAccessPoints': list()}
    for network in get_visible_networks():
        query['wifiAccessPoints'].append({'macAddress': network[0],
                                          'signalStrength': network[1]})

    cur_loc = find_current_location(json.dumps(query))['location']
    cur_city = get_current_city(cur_loc['lat'], cur_loc['lng'])
    print 'Current measured location: %s' % cur_city['display_name']
    try:
        print get_weather_in(cur_city['address']['city'])
    except KeyError:
        print get_weather_in(cur_city['address']['village'])


if __name__ == '__main__':
    main()
