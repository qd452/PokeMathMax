#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
__date__ = "Created on Mon Jan 22 16:32:01 2018"
__version__ = "0.1.0"
__author = "Qu Dong"

import crawler.pokerequests as pokemaxcrawler

loch = (1.439399, 103.801980)
loco = (1.447501, 103.812063)

pokemaxcrawler.main(loc=loco, radius=500)

pkms = pokemaxcrawler.get_nearby_pkm_obj_list(current_lat_lng=loco,
                                              radius=5000)

for pkm in pkms:
    if pkm.level and pkm.iv > 80 and pkm.level >= 25:
        pokemaxcrawler.colorprint(
            "===================================================", color="red")
        pokemaxcrawler.colorprint(pkm, color="red")
