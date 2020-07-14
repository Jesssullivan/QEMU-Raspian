#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

import toml
import sys
import platform
import subprocess
from time import sleep
from names import names
from qemu import qemu
from sources import sources
from kernel import kernel
from common import common
from dd import dd
from alias import alias
from menus import menus
from nmap import nmap


class clipi(object):

    def __init__(self):

        try:
            if sources.has_conf():
                self.config = toml.load(sys.argv[1])
            else:
                self.config = None
        except:
            self.config = None

    def arg_true(self, text='', menu=''):

        if self.config is not None:
            try:
                if self.config[text]:
                    return True
                else:
                    return False
            except KeyError:
                return False
        else:
            if menu == text:
                return True
            else:
                return False

    def main(self):
        
        if self.config is None:
            graphics = menus.main_menu()
            graphical = True
        else:
            graphics = ''
            graphical = False

        if self.arg_true('Launch a Pi emulation', graphics):
            if graphical:
                image = menus.launch_img()
            else:
                image = sources.get_source()[self.config['image']]
            qemu.launch(image)

        if self.arg_true('__Launch a Pi emulation w/ 64 bits', graphics):
            if graphical:
                image = menus.launch_img()
            else:
                image = sources.get_source()[self.config['image']]
            qemu.launch(image, use64=True)

        if self.arg_true('Burn a bootable disk image', graphics):
            if graphical:
                print('Follow the prompts: select and image')
                response_image = menus.launch_img()
                target_disk = menus.what_disk()
                print("checking types....")
                dd.dd_write(sd_disk=target_disk, image=response_image)
            else:
                image = sources.get_source()[self.config['image']]
                print(sources.get_source())
                target_disk = self.config['target_disk']
                print(target_disk)
                print("checking types....")
                dd.dd_write(sd_disk=target_disk, image=image)
                quit()

        if self.arg_true('__Burn a bootable disk image w/ verbatim raw', graphics):
            if graphical:
                print('Follow the prompts: select and image')
                response_image = menus.launch_img()
                target_disk = menus.what_disk()
                print("checking types....")
                dd.dd_write_verbatim(sd_disk=target_disk, image=response_image)
            else:
                image = sources.get_source()[self.config['image']]
                print(sources.get_source())
                target_disk = self.config['target_disk']
                print(target_disk)
                print("checking types....")
                dd.dd_write_verbatim(sd_disk=target_disk, image=image)
                quit()

        if self.arg_true('Find Pi devices on this network', graphics):
            nmap.nmap_search()

        if self.arg_true('Cleanup...', graphics):
            common.cleanup()

        if self.arg_true('Install clipi as alias', graphics):
            alias.do_alias()

        if self.arg_true('Check / install dependencies', graphics):
            print(str('checking all clipi.py depends for your ' +
                      platform.platform.__str__() + ' - based machine....'))
            common.main_install()

        if self.arg_true('Check / build kernel & gcc tools', graphics):
            kernel.depends()
            kernel.build_binutils()
            kernel.build_gcc()


if __name__ == '__main__':

    run = clipi()

    try:
        run.main()

    except KeyboardInterrupt:
        print('keyboard interrupt, exiting...')
        sys.exit(1)

    except:
        print('exiting clipi...')
        quit()
