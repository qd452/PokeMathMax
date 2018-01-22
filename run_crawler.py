#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
__date__ = "Created on Mon Jan 22 16:32:01 2018"
__version__ = "0.1.0"
__author = "Qu Dong"

import crawler.pokerequests as pokemaxcrawler
from wheel.color import *

# SG length and width measure from goolge map
Sg_length_ns = 23000
Sg_width_ew = 42000

loco = pokemaxcrawler.get_current_loc()
loco = (1.447501, 103.812063)
colorprint("Current location is ({}, {})".format(*loco), color="cyan")

radius_all = 500

pokemaxcrawler.main(loc=loco, radius=radius_all)



# filtered based on IV and Level
IV_min = 80
Level_min = 20
flt_r1 = 2000
pkms = pokemaxcrawler.get_nearby_pkm_obj_list(current_lat_lng=loco,
                                              radius=flt_r1)
colorprint(
    "Within {}m of location {}, Pokemons with IV>={} and Level>={} are:".format(
    flt_r1, loco, IV_min, Level_min), color="blue")
for pkm in pkms:
    if pkm.level and pkm.iv >= IV_min and pkm.level >= Level_min:
        colorprint(
            "===================================================", color="red")
        colorprint(pkm, color="red")
        
# filtered based on favourite of favourite
flt_r1 = 5000
my_uber_catch_list = ["Blissey", "Dragonite", "Snorlax", "Lapras", "Gyarados",
                      "Chansey", "Steelix"]
pkms = pokemaxcrawler.get_nearby_pkm_obj_list(current_lat_lng=loco,
                                              radius=flt_r1)
colorprint(
    "Within {}m of location {}, Pokemons Favourite of Favourite of are:".format(
    flt_r1, loco, IV_min, Level_min), color="blue")
for pkm in pkms:
    if pkm.name in my_uber_catch_list:
        colorprint(
            "===================================================", color="red")
        colorprint(pkm, color="red")
