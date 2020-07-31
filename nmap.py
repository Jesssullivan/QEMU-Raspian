#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""
import subprocess
import socket
from common import common

"""
nmap.py:
control nmap functions to search the local network by MAC address-
Pi devices are matched by OUI bits
"""


class nmap(object):

    oui_dict = {'B8:27:EB': 'Pi Device <= 3', 'DC:A6:32': 'Pi Device >= 4'}

    @staticmethod
    def _search(oui=''):

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
              " | awk '/^Nmap/{ip=$NF}/" + oui + "/{print ip}'"

        search = subprocess.Popen(cmd, shell=True).wait()
        # todo- parse & sort by wifi module version (3|4);
        # - search.stdout.read() ...

    @classmethod
    def nmap_search(cls):

        # just to make sure nmap is available
        common.main_install()

        print('Uses nmap to find local Pi devices by OUI --> MAC address....')

        for oui in nmap.oui_dict.keys():
            nmap._search(oui=oui)

        print('\n ...search complete. \n')
