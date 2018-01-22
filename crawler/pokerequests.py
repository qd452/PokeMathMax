#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
__date__ = "Created on Mon Jan 22 08:51:42 2018"
__version__ = "0.1.0"
__author = "Qu Dong"

import requests

import json
import os
import sys
import time
from datetime import timedelta
from geopy.distance import vincenty

try:
    from ..wheel.color import * 
except ValueError:
    from wheel.color import *
except SystemError:
    import sys
    from pathlib import Path # new in 3.4
    _pp_dir = str(Path(__file__).parents[1])
    sys.path.insert(0, _pp_dir)
    from wheel.color import *

DEBUG = False


FILE = os.path.dirname(__file__)

def PokeCrawlerError(Exception):
    pass


def is_nearby(poke_lat_lng, current_lat_lng=(1.457501, 133.812063), radius=500):
    return vincenty(current_lat_lng, poke_lat_lng).meters <= radius


def get_favor_poke_ids(pokejson= "favourite_poke.json"):
    """https://github.com/rkern/line_profiler/issues/37
    """
    with open(os.path.join(FILE, 'favourite_poke.json'), encoding='utf-8') as data_file:
        pokelist = json.load(data_file)
    poke_ids = [x["i"] for x in pokelist]
    return poke_ids, pokelist
    
_, _fv_pklist = get_favor_poke_ids()

_myfavourite_pokes_dict = {}
for fv_pk in _fv_pklist:
    if fv_pk in list(_myfavourite_pokes_dict.keys()):
        raise PokeCrawlerError("My Json is wrong!")
    _myfavourite_pokes_dict[int(fv_pk['i'])] = fv_pk['n']
    
def getDataFromSGPokeMap():
    """
    todo-qd: fixed the InsecureRequestWarning issue
    
    return: list of my favourite Pokemons across the whole SG
    """
    list_of_pokemon_ids = ','.join(get_favor_poke_ids()[0])
    current_epoch_time = 0
    with requests.Session() as s:
        s.headers = { # request headers setting
            "authority": "sgpokemap.com",
            "method": "GET",
            "path": "/query2.php?since=" + str(current_epoch_time) + "&mons=" + list_of_pokemon_ids,
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, sdch, br",
            "accept-language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ms;q=0.2",
            "cache-control": "no-cache",
#            "cookie": "__cfduid=d4d51b55890b0ecaed8a096ca9e8bd8b01511605718; _ga=GA1.2.2119617142.1511605711; _gat=GA1.2.65321968.1515334414",
            "pragma": "no-cache",
            "referer": "https://sgpokemap.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
    
        r = s.get("https://sgpokemap.com/query2.php?since=" + str(current_epoch_time) + "&mons=" + list_of_pokemon_ids,
                  verify=False)

        if r.status_code != 200:
            PokeCrawlerError("Crawling Failed with status code: {}".format(r.status_code)) 
    response = r.json() # decoding json to dict
    if DEBUG:
        colorprint(response.keys(), color="blue")
        colorprint("In Total, {} Pokemons were found".format(len(response['pokemons'])), color="blue")
#        colorprint(response['pokemons'][0], color="magenta")
    poke_all_sg = response['pokemons']
    return poke_all_sg
    
def get_favor_poke_nearby(pokescanned, **kwargs):
    nearby_pm = []
    for pm in pokescanned:
        poke_lat_lng = (pm["lat"], pm["lng"])
        if is_nearby(poke_lat_lng, **kwargs):
            nearby_pm.append(pm)
    return nearby_pm

class Dict2Cls:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        
        
def poke_detail_deserialization(**poke_info_dict):
    """
    JSON is a format that encodes objects in a string. Serialization means 
    to convert an object into that string, and deserialization is its 
    inverse operation.
    
    https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    
    {'level': '29', 'gender': '2', 'disguise': '0', 'costume': '0', 
    'pokemon_id': '242', 'move1': '222', 'defence': '14', 
    'lng': '103.90356926', 'cp': '2628', 'form': '0', 'stamina': '2', 
    'attack': '15', 'move2': '14', 'shiny': '0', 'lat': '1.41604088', 
    'despawn': '1516605285', 'weather': '0'}
    """
    for k,v in poke_info_dict.items():
        if k =="despawn":
            poke_info_dict[k] = time.strftime("%I:%M:%S%p", time.localtime(float(v)))
            t = time.time()
            seconds_left = int(float(v) - t)
            time_left = "{}:{}".format(seconds_left//60, seconds_left%60)
        elif k in ('lat', 'lng'):
            pass
        else:
            if int(v) != -1:
                poke_info_dict[k] = int(v)
            else:
                poke_info_dict[k] = None
    poke_info_dict['time_left'] = time_left
    
    poke_info_dict['stats'] = [None, None, None]
    poke_info_dict['location'] = [None, None] # [lat, lng]
    for k,v in poke_info_dict.items():
        if k == "pokemon_id":
            try:
                pk_name = _myfavourite_pokes_dict[v]
            except KeyError:
                raise PokeCrawlerError("Scanned Pokemon ID: {}is NOT in my favrouite list".format(v))
        elif k == "attack":
            poke_info_dict['stats'][0] = v
        elif k == "defence":
            poke_info_dict['stats'][1] = v
        elif k == "stamina":
            poke_info_dict['stats'][2] = v
        elif k == "lat":
            poke_info_dict['location'][0] = v
        elif k == "lng":
            poke_info_dict['location'][1] = v
    poke_info_dict["name"] = pk_name
    if poke_info_dict['stats'] == [None, None, None]:
        poke_info_dict["iv"] = None
        poke_info_dict["stats"] = None
    else:
        poke_info_dict["iv"] = round(sum(poke_info_dict['stats']) / 45.0, 2)

    poke_obj = Dict2Cls(**poke_info_dict)
    
    return poke_obj
    
def get_nearby_pkm_obj_list(**kwargs):
    poke_all_sg = getDataFromSGPokeMap()
    nearby_pm = get_favor_poke_nearby(poke_all_sg, **kwargs)
    nby_pm_obj_lst = [poke_detail_deserialization(**x) for x in nearby_pm]
    return nby_pm_obj_lst
        
def main(**kwargs):
    for i in kwargs:
        if i=="radius":
            radius = kwargs[i]
        if i=="loc":
            loc = kwargs[i]
    pkms = get_nearby_pkm_obj_list(current_lat_lng=loc, radius = radius)
    colorprint("\nBased on the current location {}, within radius of {}m, {} Pokemons are found".format(loc, radius, len(pkms)), color="blue")
    for pkm in pkms:
        if pkm.cp:
            colorprint("===================================================", color="red")
            colorprint("{} - (IV:{}) - (CP: {}) - (Level: {})".format(pkm.name, pkm.iv, pkm.cp, pkm.level), color="red")
            colorprint("Until: {} ({} left)".format(pkm.despawn, pkm.time_left), color="red")
            colorprint("Weather Boost: {}".format(True if pkm.weather>0 else False), color="red")
            colorprint("L30+ Stats: ({}) {}".format(pkm.stats, pkm.iv), color="red")
            colorprint("L20+ CP: {} (Level: {})".format(pkm.cp, pkm.level), color="red")
            colorprint("Location: {}".format(pkm.location), color="red")
        else:
            colorprint("===================================================", color="magenta")
            colorprint("{}".format(pkm.name, pkm.iv, pkm.cp, pkm.level), color="magenta")
            colorprint("Until: {} ({} left)".format(pkm.despawn, pkm.time_left), color="magenta")
            colorprint("Location: {}".format(pkm.location), color="magenta")
    
if __name__ == "__main__":
    pass
    