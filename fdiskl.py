#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

from common import *
import subprocess
import re
from sys import platform
from names import names
from sources import sources
import os


"""

fdiskl.py:
controls fdisk -l utility to inspect partitions & sectors from image.
"""


class fdiskl(object):

    @classmethod
    def setup(cls):
        if sys.platform == 'darwin':
            print('detected osx, checking fdisk in gptfdisk via brew...')
        if sys.platform == "linux" or sys.platform == "linux2":
            print('checking fdisk...')
        common.dep_install(dep='fdisk', brew_dep='gptfdisk')
        sleep(.1)

    @classmethod
    def read(cls, image):
        # ensure we've got fdisk- not sure yet if this works from osx via gptfdisk
        # fdiskl.setup()
        cmd = str('fdisk -l ' + image)

        # read fdisk -l output:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        result = proc.stdout.read().__str__()

        # figure out what type we should iterate with when looking via file / part contained within image-
        # (plz only use .img for now)
        if '.iso' in result:
            iter = '.iso'
        # not sure it this one will work......
        if '.qcow2' in result:
            iter = '.qcow2'
        else:
            iter = '.img'

        # chop up fdisk results by file / partition:
        parts = re.findall(r'' + iter + '\d', result)
        #
        disk = {}
        for p in parts:
            # sub dict 'part' will contain fdisk -l output values:
            part = {}
            # get just the number words:
            line = result.split(p)[1]
            words = re.split(r'\s+', line)
            # place each word into 'part':
            part['Start'] = words[1]
            part['End'] = words[2]
            part['Sectors'] = words[3]
            part['Size'] = words[4]
            part['Id'] = words[5]
            part['Format'] = words[6].split('\\n')[0]
            # stick this part into 'disk', move onto next disk part:
            disk[p] = part
        return disk
