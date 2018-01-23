#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
__date__ = "Created on Tue Jan 23 20:45:47 2018"
__version__ = "0.1.0"
__author = "Qu Dong"

try:
    from ..wheel.color import *
except SystemError:
    import sys
    from pathlib import Path  # new in 3.4

    _pp_dir = str(Path(__file__).parents[1])
    sys.path.insert(0, _pp_dir)
    from wheel.color import *
import json
import sys
import requests

DEBUG = False

class GoogleMapError(Exception):
    pass

with open("googlemap_api.json") as f:
    API_KEY = json.load(f)['api_key']

def access_googlemap_geocoding_api():
    """
    """
    with requests.Session() as s:
        if DEBUG:
            s.headers = {  # request headers setting
                           "authority": "sgpokemap.com",
                           "method": "GET",
                           "scheme": "https",
                           "accept": "*/*",
                           "accept-encoding": "gzip, deflate, sdch, br",
                           "accept-language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ms;q=0.2",
                           "cache-control": "no-cache",
                           "pragma": "no-cache",
                           "referer": "https://maps.googleapis.com/maps/api/geocode/",
                           "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
                           "x-requested-with": "XMLHttpRequest"
                           }
        else:
            assert isinstance(s.headers, requests.structures.CaseInsensitiveDict)
            s.headers = dict(s.headers)
        colorprint(json.dumps(s.headers, indent=4), color="blue")

        r = s.get("https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key={}".format(API_KEY),

                  verify=False)
        

        if r.status_code != 200:
            GoogleMapError(
                "Crawling Failed with status code: {}".format(r.status_code))
    response = r.json()  # decoding json to dict
    return response
    
r= access_googlemap_geocoding_api()

colorprint("Result is \n", json.dumps(r, indent=4), color="magenta")