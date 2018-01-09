#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lots of stuff are still hard coded, need to change

"""
__date__ = "Created on Tue Jan  9 08:48:15 2018"
__version__ = "0.1.0"
__author = "Qu Dong"

"""
the following rate is assuming that have gold badge for the Pokemon and 
the through is curved and with the Golden Berry

todo: need to generate the following dict programmally and dump it into json
"""
RAIDBOSS = {'Mewtwo': {'Normal': 0.2479,
                        'Nice': 0.279,
                        'Great': 0.3476,
                        'Excellent': 0.4051},
            'Groudon': {'Normal': 0.0891,
                        'Nice': 0.1016,
                        'Great': 0.1306,
                        'Excellent': 0.1565},
            'Tyranitar': {'Normal': 0.2105, 
                          'Nice': 0.2377,
                          'Great': 0.2984,
                          'Excellent': 0.3501},}
                        
class color:
   RED = '\x1b[1;31m'
   END = '\x1b[0m'
                        
class DictToClass:
    def __init__(self, **entries):
        """
        https://stackoverflow.com/questions/1305532/convert-python-dict-to-object

        :param entries: dict object
        """
        self.__dict__.update(entries)


legendary = DictToClass(**RAIDBOSS)  # if you want to use the class style

def total_catch_rate(raidboss, totalsamethrough, through):
    """
    :param totalsamethrough: all the throughs are the same    
    """
    return 1 - (1-RAIDBOSS[raidboss][through]) ** totalsamethrough


for i in range(7, 14):
    catch = ('Mewtwo', i, 'Great')
    catchrate = total_catch_rate(*catch)
    print('The Final catch rate for {} with {} {} throughs are: '.format(*catch), end='')
    print(color.RED + '{:.2f}%'.format(catchrate*100) + color.END)
print()

for i in range(7, 14):
    catch = ('Groudon', i, 'Great')
    catchrate = total_catch_rate(*catch)
    print('The Final catch rate for {} with {} {} throughs are: '.format(*catch), end='')
    print(color.RED + '{:.2f}%'.format(catchrate*100) + color.END)
print()

for i in range(2, 14):
    catch = ('Tyranitar', i, 'Nice')
    catchrate = total_catch_rate(*catch)
    print('The Final catch rate for {} with {} {} throughs are: '.format(*catch), end='')
    print(color.RED + '{:.2f}%'.format(catchrate*100) + color.END)