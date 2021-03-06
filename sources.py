#!/usr/bin/env python3
"""
#
# locations, names for image / iso files
# feel free to add some more at etc/sources.toml
#
# also methods for parsing shortcut config files (toml / yaml)
"""


from common import *
import toml
import yaml


class sources(object):

    default_configs = ['sources', 'etc/sources']
    default_settings = ['default', 'etc/default']
    default_types = ['.toml', '.yaml']

    # provides an option to provide etc/sources.toml or add directly to dictionary
    @classmethod
    def get_source(cls):
        for econfig in cls.default_configs:
            for etype in cls.default_types:
                try:
                    if os.path.isfile(econfig + etype):
                        if 'toml' in etype:
                            source = toml.load(econfig + etype)
                        else:
                            source = yaml.load(open(econfig + etype), Loader=yaml.Loader)
                        return source
                except:
                    pass

        else:
            print("couldn't find default source toml or yaml, FYI")
            # catch all if sources.toml doesn't exist:
            source = {
                'stretch_lite': 'http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/2018-11-13'
                                '-raspbian-stretch-lite.zip',
                'stretch_desktop': 'http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-04-09/2019-04-08-raspbian'
                                   '-stretch.zip',
                'octoprint': 'https://octopi.octoprint.org/latest',
            }
            return source

    @staticmethod
    def has_conf():
        # soften argument / no argument
        try:
            if '.toml' in sys.argv[1]:
                return True
            if '.yaml' in sys.argv[1]:
                return True
        except:
            return False

    @classmethod
    def load_args(cls):
        if sources.has_conf():
            source = toml.load(sys.argv[1])
            return source
        else:
            for econfig in cls.default_settings:
                for etype in cls.default_types:
                    try:
                        if os.path.isfile(econfig + etype):
                            if 'toml' in etype:
                                source = toml.load(econfig + etype)
                            else:
                                source = yaml.load(open(econfig + etype), Loader=yaml.Loader)
                            return source
                    except:
                        pass

    @staticmethod
    def do_arg(arg, default):
        xargs = sources.load_args()
        try:
            k = xargs[arg]
            return k
        except:
            return default
