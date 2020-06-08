#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

from common import *
from common import common as com

"""
nmap.py:
control nmap functions to search the local network by MAC address-
Pi devices are matched by OUI bits
"""


class nmap(object):

    @classmethod
    def nmap_search(cls):
        print('Uses nmap to find local Pi devices by MAC address....')
        # just to make sure nmap is available
        com.main_install()

        # find the first two ip quadrants from which to increment:
        get_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        get_socket.connect(("8.8.8.8", 80))
        ip_quad = str(get_socket.getsockname()[0]).split('.')
        get_socket.close()

        # execute nmap:
        print('\n ...starting search for Pi devices, this may take a while... \n')
        cmd = "sudo nmap -sP " \
              + ip_quad[0] + \
              "." + ip_quad[1] + ".1.1/24" + \
              " | awk '/^Nmap/{ip=$NF}/B8:27:EB/{print ip}'"
        subprocess.Popen(cmd, shell=True).wait()
        print('\n ...search complete. \n')
