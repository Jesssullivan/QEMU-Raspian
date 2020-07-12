#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

from alias import alias
from common import *
from common import common
from dd import dd
from kernel import kernel
from menus import menus
from nmap import nmap
from qemu import qemu
from sources import sources
import toml


def main():

    try:
        if sources.has_conf():
            config = toml.load(sys.argv[1])
            conf = True
        else:
            config = None
            conf = False
    except:
        config = None
        conf = False

    def arg_true(text):
        try:
            if config[text]:
                return True
        except KeyError:
            pass

    if conf:

        if arg_true('Launch a Pi emulation'):
            image = sources.get_source()[config['image']]
            qemu.launch(image)

        if arg_true('Burn a bootable disk image'):
            image = sources.get_source()[config['image']]
            print(sources.get_source())
            target_disk = config['target_disk']
            print(target_disk)
            print("checking types....")
            if arg_true('verbatim'):
                dd.dd_write_verbatim(sd_disk=target_disk, image=image)
                quit()

            dd.dd_write(sd_disk=target_disk, image=image)
            quit()

        if arg_true('Find Pi devices on this network'):
            nmap.nmap_search()
            quit()

        if arg_true('Cleanup...'):
            common.cleanup()
            quit()

        if arg_true('Install clipi as alias'):
            alias.do_alias()
            quit()

        if arg_true('Check / install dependencies'):
            print(str('checking all clipi.py depends for your ' +
                      platform + ' - based machine....'))
            common.main_install()

        if arg_true('Check / build kernel & gcc tools'):
            common.main_install()
            print('checking all depends in /kernel_sh.....')
            kernel.depends()
            print('configuring & building binutils...')
            kernel.build_binutils()
            print('configuring & building gcc...')
            kernel.build_gcc()

    else:  # if there isn't a provided shortcut file, use the interactive menus

        op1 = menus.main_menu()

        if op1 == 'Launch a Pi emulation':
            image = menus.launch_img()
            qemu.launch(image)

        if op1 == '__Launch a Pi emulation w/ 64 bits':
            print('\n!!this is an experimental feature, YMMV!!\n')
            image = menus.launch_img()
            qemu.launch(image, use64=True)

        if op1 == 'Burn a bootable disk image':
            print('Follow the prompts: select and image')
            response_image = menus.launch_img()
            target_disk = menus.what_disk()
            print("checking types....")
            dd.dd_write(sd_disk=target_disk, image=response_image)

        if op1 == '__Burn a bootable disk image w/ verbatim raw':
            print('Follow the prompts: select and image')
            response_image = menus.launch_img()
            target_disk = menus.what_disk()
            print("checking types....")
            dd.dd_write_verbatim(sd_disk=target_disk, image=response_image)

        if op1 == 'Find Pi devices on this network':
            nmap.nmap_search()

        if op1 == 'Utilities...':
            print('Additional settings:')
            response = menus.utils_menu()  # shows utils_menu() menu

            if response == 'Cleanup...':
                # double checks w/ a confirm:
                common.cleanup()

            if response == 'Install clipi as alias':
                alias.do_alias()

            if response == 'Check / install dependencies':
                print(str('checking all clipi.py depends for your ' +
                          platform + ' - based machine....'))
                common.main_install()


if __name__ == '__main__':

    try:

        main()

    except KeyboardInterrupt:
        print('keyboard interrupt, exiting...')
        sys.exit(1)
