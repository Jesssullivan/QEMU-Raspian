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
from menus import menus


"""
dd.py:
control dd utility to write raw out to disk / sd card.
"""


class dd(object):

    @classmethod
    def dd_write(cls, sd_disk, image):
        common.main_install()
        common.ensure_dir()
        common.ensure_bins()
        img = qemu.ensure_img(image)

        umount_cmd = str('umount /dev/' + str(sd_disk) + ' 2>/dev/null || true')
        subprocess.Popen(umount_cmd, shell=True).wait()

        print('writing to target....')
        dd_cmd = str('sudo qemu-img dd -f qcow2 -O raw bs=1M ' +
                     ' if=' + str(img) +
                     ' of=/dev/' + str(sd_disk))
        print('working....')
        subprocess.Popen(dd_cmd, shell=True).wait()
        sleep(.1)
        print('finished xD \n ' +
              'to pre-enable or double check wifi and ssh, reinsert sd_disk, then ' +
              'copy file `ssh` and a configured `wpa_supplicant.conf` to /boot :)')

    @classmethod
    def dd_write_verbatim(cls, sd_disk, image):
        common.main_install()
        common.ensure_dir()
        common.ensure_bins()

        qemu.ensure_img(image)
        print('preparing to write out image using verbatim dd utility...')
        print('unmounting target....')
        umount_cmd = str('umount /dev/' + str(sd_disk) + ' 2>/dev/null || true')
        subprocess.Popen(umount_cmd, shell=True).wait()

        print('writing to target....')
        dd_cmd = str('sudo dd if=' + names.any_img(image) + ' of=/dev/' + sd_disk + ' bs=1048576')
        subprocess.Popen(dd_cmd, shell=True).wait()
        sleep(.1)

        print('completed write, syncing....')
        subprocess.Popen('sync ', shell=True).wait()

        print('finished xD \n ' +
              'to pre-enable wifi and ssh, reinsert sd_disk, then ' +
              'copy file `ssh` and a configured `wpa_supplicant.conf` to /boot :)')
