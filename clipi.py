#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

# local modules:
from common import *
from common import common
from sources import sources
from dd import dd
from menus import menus
from names import names
from nmap import nmap
from qemu import qemu
from alias import alias


def main():
    try:
        if common.has_toml():
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
            response_image = config['image']
            target_disk = config['target_disk']
            result = os.path.join(names.src_dir(response_image),
                                  names.src_img(response_image))
            print("checking types....")
            to_write = dd.dd_output_convert(qcow=result)
            dd.dd_write(sd_disk=target_disk, image=to_write)

        if arg_true('Find Pi devices on this network'):
            nmap.nmap_search()

        if arg_true('Cleanup...'):
            common.cleanup()

        if arg_true('Install clipi as alias'):
            alias.do_alias()

        if arg_true('Check / install dependencies'):
            print(str('checking all clipi.py depends for your ' +
                      platform + ' - based machine....'))
            common.main_install()

    else:

        op1 = menus.main_menu()

        if op1 == 'Launch a Pi emulation':
            image = menus.launch_img()
            qemu.launch(image)

        if op1 == 'Burn a bootable disk image':
            print('Follow the prompts: select and image')
            response_image = menus.launch_img()
            target_disk = dd.what_disk()
            result = os.path.join(names.src_dir(response_image),
                                  names.src_img(response_image))
            print("checking types....")
            to_write = dd.dd_output_convert(qcow=result)
            dd.dd_write(sd_disk=target_disk, image=to_write)

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
