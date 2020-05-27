#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""
from dd import *
from qemu import *
from nmap import *
from alias import *
from common import *


# Menus

def main_menu():
    menu_1 = {
        'type': 'list',
        'name': 'menu_1',
        'message': 'Options:',
        'choices': [
            'Launch a Pi emulation',
            'Burn a bootable disk image',
            'Find Pi devices on this network',
            'Utilities...'
        ]
    }
    answers = prompt(menu_1)
    return answers['menu_1']


def utils_menu():
    utils_1 = {
        'type': 'list',
        'name': 'utils_1',
        'message': 'Options:',
        'choices': [
            'Cleanup...',
            'Install clipi as alias',
            'Check / install dependencies',
            'TODO: Launch some emulations w/ virtual network bridge'
        ]
    }
    answers = prompt(utils_1)
    return answers['utils_1']


def launch_img():
    launches = {
        'type': 'list',
        'name': 'launches',
        'message': 'Select an image....',
        'choices': source
    }
    answers = prompt(launches)
    return source[answers['launches']]


def cleanup():
    rm = {
        'type': 'confirm',
        'message': 'Are you sure? (This completely removes the /image directory!)',
        'name': 'continue',
        'default': True,
    }
    checked = prompt(rm)
    if checked:
        # removes as admin from shell to avoid a wonky super python user xD
        subprocess.Popen('sudo rm -rf image', shell=True).wait()
        restart()


def do_alias():
    print('Adds `clipi` alias to your shell \n' +
          '( Also copies clipi.py & sources.py to ~/.clipi)')
    # double checks w/ a confirm:
    alias = {
        'type': 'confirm',
        'message': "Are you sure? \n "
                   "(You'll need to restart or source this shell for this change to take effect)",
        'name': 'continue',
        'default': True,
    }
    checked = prompt(alias)
    if checked:
        bash_alias_update()
        add_to_bash()
        print('please source or restart your shell for changes to take effect')


# this is the main, initial menu:
def menu():
    op1 = main_menu()

    if op1 == 'Launch a Pi emulation':
        # check if we are able to run:
        print('dfsdf')
        main_install()
        # check for emulation dir
        ensure_dir()
        response = launch_img()
        qemu.launch(response)

    if op1 == 'Burn a bootable disk image':
        print('Follow the prompts: select and image')
        main_install()
        ensure_dir()
        response_image = launch_img()
        target_disk = dd.what_disk()
        qemu.ensure_img(response_image)
        result = os.path.join(names.src_dir(response_image),
                              names.src_img(response_image))
        to_write = dd.dd_output_convert(qcow=result)
        dd.dd_write(sd_disk=target_disk, image=to_write)
        restart()

    if op1 == 'Find Pi devices on this network':
        nmap_search()
        restart()

    if op1 == 'Utilities...':
        print('Additional settings:')
        response = utils_menu()  # shows utils_menu() menu

        if response == 'Cleanup...':
            # double checks w/ a confirm:
            cleanup()

        if response == 'Install clipi as alias':
            do_alias()

        if response == 'Check / install dependencies':
            print(str('checking all clipi.py depends for your ' +
                      platform + ' - based machine....'))
            main_install()
            restart()


if __name__ == '__main__':

    try:
        menu()

    except KeyboardInterrupt:
        print('keyboard interrupt, exiting...')
        sys.exit(1)

    except:
        print('....exiting....')
        sys.exit(1)
