#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unittest script for color.py
"""
__date__ = "Created on Thu Jan 11 17:26:11 2018"
__version__ = "0.1.0"
__author = "Qu Dong"

import unittest

from color import *

class Testcolor(unittest.TestCase):
    def test_ColorByMyOwnEyes(self):
        # based on the wiki/ANSI_escape_code#Colors
        # as this is 8-bit, so 0-7 and 8-15 are the same
        for i in range(16):
            print(i, '\x1b[%sm' % (
            '38;5;{}'.format(i)) + '############' + Color.end)

        def print_format_table():
            """
            prints table of formatted text format options
            """
            for style in range(8):
                for fg in range(30, 38):
                    s1 = ''
                    for bg in range(40, 48):
                        fmt = ';'.join([str(style), str(fg), str(bg)])
                        s1 += '\x1b[%sm %s \x1b[0m' % (fmt, fmt)
                    print(s1)
                print('\n')

        print_format_table()

    def test_ColorClass(self):
        print(Color.red + 'AAAAAAAAA' + Color.end)
        print(Color.green + 'AAAAAAAAA' + Color.end)
        print(Color.blue + 'AAAAAAAAA' + Color.end)
        print()

    def test_ColorDict(self):
        from itertools import product
        for f, b in product(_colorlist, _colorlist):
            colorprint("I'm {} with {} background".format(f, b), color=f,
                       background=b)


if __name__ == "__main__":
    unittest.main()