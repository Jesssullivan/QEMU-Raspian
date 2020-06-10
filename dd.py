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
        xargs = common.all_args()
        common.main_install()
        common.ensure_dir()
        common.ensure_bins()
        qemu.ensure_img(image)
        print('preparing to write out image, unmount target....')
        umount_cmd = str('umount /dev/' + sd_disk + ' 2>/dev/null || true')
        subprocess.Popen(umount_cmd, shell=True).wait()
        sleep(.2)
        print('writing ' + names.any_img(image) + ' to target....')
        dd_cmd = str('sudo dd if=' + names.any_img(image) + ' of=/dev/' + sd_disk + ' bs=1048576')
        print('writing to target....')
        subprocess.Popen(dd_cmd, shell=True).wait()
        sleep(.1)
        print('completed write, syncing....')
        subprocess.Popen('sync ', shell=True).wait()
        print('finished xD \n ' +
              'to pre-enable wifi and ssh, reinsert sd_disk, then ' +
              'copy file `ssh` and a configured `wpa_supplicant.conf` to /boot :)')
