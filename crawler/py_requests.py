#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
rebrushing requests, http


http://docs.python-requests.org/en/master/user/advanced/
http://www.pythonforbeginners.com/requests/using-requests-in-python
"""
__date__ = "Created on Mon Jan 22 10:24:01 2018"
__version__ = "0.1.0"
__author = "Qu Dong"

import requests

"""
In particular, relative import do not work inside simple modules located at 
the top level of scripts. They also won’t work if parts of a package are 
executed directly as a script.
"""
try:
    from ..wheel.color import * # therefore relative import wouldn't work
    # i'm directly running it but not use it as a whole package
except SystemError:
    import sys
    from pathlib import Path # new in 3.4
    _pp_dir = str(Path(__file__).parents[1])
    sys.path.insert(0, _pp_dir)
    from wheel.color import *

# ================================================================
# http://docs.python-requests.org/en/master/user/advanced/
# ================================================================

# my debug
Part = {1:True,
        2:False,
        3:True}

###############################
# PART 1: Session Objects
###############################
if Part[1]:
    """
    The Session object allows you to persist certain parameters across requests. 
    It also persists cookies across all requests made from the Session instance, 
    and will use urllib3's connection pooling. So if you're making several requests 
    to the same host, the underlying TCP connection will be reused, which can 
    result in a significant performance increase (see HTTP persistent connection).
    """
    
    # Let's persist some cookies across requests:
    with requests.Session() as s:
        s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
        r = s.get('http://httpbin.org/cookies')
        
        colorprint(r,color="green") # 200 OK: The request has succeeded.
        print(r.text)
        
        s.get('http://httpbin.org/cookies/set/maxcookie/123')
        r = s.get('http://httpbin.org/cookies')
        
        colorprint(r,color="green") # 200 OK: The request has succeeded.
        print(r.text) # isinstance(r.text, str)
        
    assert isinstance(r.text, str)
    # The Requests library also comes with a built-in JSON decoder
    # r.json is <bound method Response.json of <Response [200]>>
    assert isinstance(r.json(), dict)
    assert r.json()['cookies']['maxcookie'] == '123'
    
    # the new session, the cookies is not persisted
    with requests.Session() as s:
        s.get('http://httpbin.org/cookies/set/sessioncookie/111111')
        r = s.get('http://httpbin.org/cookies')
        
        assert r.json()['cookies']['sessioncookie'] == "111111"
        
    assert isinstance(r.text, str)
    
    #NOTE: session.headers is the request header!!!!!
    assert s.headers['Accept'] == '*/*'


#########################################
# PART 2: Request and Response Objects
#########################################
if Part[2]:
    r = requests.get('http://en.wikipedia.org/wiki/Monty_Python')
    assert isinstance(r, requests.models.Response) # Response obj
    
    colorprint(r.headers, color="blue")
    colorprint(r.request.headers, color="magenta")
