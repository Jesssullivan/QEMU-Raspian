#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

import glob
import os


"""
mini.py: 
the idea here is to automatically condense classes into a distributable script for alias.py and whatnot
"""

# todo: maybe finish writing this stuff lol
modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules
           if os.path.isfile(f) and not f.endswith('__init__.py')]

