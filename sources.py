#!/usr/bin/env python3
"""
#
# locations, names for image / iso files:
#
# feel free to add some more at /sources.toml
#
"""


from common import *


class sources(object):

    # provides an option to provide sources.toml or add directly to dictionary

    @classmethod
    def get_source(cls):
        if os.path.isfile('sources.toml'):
            source = toml.load('sources.toml')
            return source

        if os.path.isfile('etc/sources.toml'):
            source = toml.load('etc/sources.toml')
            return source

        else:
            print("couldn't find sources.toml or etc/sources.toml, FYI")
            # catch all if sources.toml doesn't exist:
            source = {
                'stretch_lite': 'http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/2018-11-13'
                                '-raspbian-stretch-lite.zip',
                'stretch_desktop': 'http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-04-09/2019-04-08-raspbian'
                                   '-stretch.zip',
                'octoprint': 'https://octopi.octoprint.org/latest',
            }
            return source
