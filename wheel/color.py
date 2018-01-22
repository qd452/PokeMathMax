#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
https://en.wikipedia.org/wiki/ANSI_escape_code

    ESC[ … 38:5:<n> … m Select foreground color
    ESC[ … 48:5:<n> … m Select background color
    

The following color code works on Python 3.x and IPython Console
"""
__date__ = "Created on Wed Jan 10 16:22:48 2018"
__version__ = "0.1.0"
__author = "Qu Dong"

import sys


__all__ = ['Color', 'ColorBackground', 'colorprint', '_colorlist']

_colorlist = ['black', 'red', 'green', 'candy', 'blue', 'magenta', 'cyan']
# fg_bg = ['38;5', '48;5']
END = '\x1b[0m'
_color = {'end': END}  # foreground
_colorbackground = {'end': END}  # background
for i, clr in enumerate(_colorlist):
    _color[clr] = '\x1b[%sm' % ('38;5;{}'.format(i))
    _colorbackground[clr] = '\x1b[%sm' % ('48;5;{}'.format(i))


class DictToClass:
    def __init__(self, **entries):
        """
        https://stackoverflow.com/questions/1305532/convert-python-dict-to-object

        :param entries: dict object
        """
        self.__dict__.update(entries)


Color = DictToClass(**_color)
ColorBackground = DictToClass(**_colorbackground)


def colorprint(*args, **kwargs):
    """
    wrapper function on top of the default print function in Python 3
        
    :param color: prints values in specified color: (red green brightred blue magenta cyan)
    :param background: prints values on specified color (same as color)
    """
    color = kwargs.pop('color', None)
    background = kwargs.pop('background', None)

    file = kwargs.get('file', sys.stdout)

    if color or background:
        end = kwargs.pop('end', "\n")
        kwargs['end'] = ""

        if color:
            print(_color[color], file=file, end='')
        if background:
            print(_colorbackground[background], file=file, end='')

        print(*args, **kwargs)
        print(END, file=file, end=end)
    else:
        print(*args, **kwargs)

