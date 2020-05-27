#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

from common import *
import toml
import clipi
import inspect

"""
toml.py:
manage, parse toml config files for clipi.py.
This stuff is completely unimplemented and totally doesn't work yet
xD
"""


def load_toml():
    try:
        if len(sys.argv[1]) > 1:
            arg = sys.argv[1]
            if 'toml' in sys.argv[1]:
                conf = toml.load(arg, _dict=dict)
                return conf
            else:
                print(sys.argv[1] + ' is not .toml, continuing...')
                return False
    except:
        print('')
        return False


def use_toml():

    conf = load_toml()
    opts = inspect.getmembers(clipi.menus, predicate=inspect.ismethod)

    for item in opts:
        if item[0] in conf['flow'][0]:
            print(item)

