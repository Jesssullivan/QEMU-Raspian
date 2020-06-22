#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

from PyInquirer import prompt
from common import *
from names import names
from qemu import qemu

"""
dd.py:
control dd utility to write raw out to disk / sd card.
"""


class dd(object):

    @classmethod
    def what_disk(cls):
        # prompt following image selection for target disk
        target = {
            'type': 'input',
            'name': 'target',
            'message': "please type the target disk's system name, such as `sdb` or sdc`",
            'default': "sdc"
        }
        response = prompt(target)
        return response['target']

    @classmethod
    def dd_write(cls, sd_disk, image):
        common.main_install()
        common.ensure_dir()
        common.ensure_bins()
        qemu.ensure_img(image)
        print('preparing to write out image, unmount target....')
        sleep(.1)
        img = names.any_qcow(image)
        print('writing ' + img + ' to target....')
        dd_cmd = str('sudo qemu-img dd -f qcow2 -O raw bs=1M ' +
                     ' if=' + img +
                     ' of=/dev/' + str(sd_disk))
        print('working....')
        subprocess.Popen(dd_cmd, shell=True).wait()
        sleep(.1)
        print('finished xD \n ' +
              'to pre-enable or double check wifi and ssh, reinsert sd_disk, then ' +
              'copy file `ssh` and a configured `wpa_supplicant.conf` to /boot :)')
