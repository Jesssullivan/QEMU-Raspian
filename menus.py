#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

from common import *

"""
menus.py:
PyInquirer prompts, for clipi to be used as an interactive CLI
"""


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
    # removes as admin from shell to avoid a wonky super python user xD
    subprocess.Popen('sudo rm -rf image', shell=True).wait()
    print()
    for x in range(3):
        print('...\n')
        sleep(.1)
    print('complete. \n\n')


def do_alias():
    print('Adds `clipi` alias to your shell \n' +
          '( Also copies clipi.py & sources.py to ~/.clipi)')
    bash_alias_update()
    add_to_bash()
    print('please source or restart your shell for changes to take effect')
