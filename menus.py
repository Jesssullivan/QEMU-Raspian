#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

from common import *
from alias import alias
from sources import sources

"""
menus.py:
PyInquirer prompts, for clipi to be used as an interactive CLI
"""


class menus(object):

    @classmethod
    def main_menu(cls):
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

    @classmethod
    def utils_menu(cls):
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

    @classmethod
    def launch_img(cls):
        launches = {
            'type': 'list',
            'name': 'launches',
            'message': 'Select an image....',
            'choices': sources.get_source()
        }
        answers = prompt(launches)
        source = sources.get_source()
        return source[answers['launches']]

    @classmethod
    def cleanup(cls):
        # removes as admin from shell to avoid a wonky super python user xD
        subprocess.Popen('sudo rm -rf image', shell=True).wait()
        print()
        for x in range(3):
            print('...\n')
            sleep(.1)
        print('complete. \n\n')

    @classmethod
    def do_alias(cls):
        print('Adds `clipi` alias to your shell \n' +
              '( Also copies clipi.py & sources.py to ~/.clipi)')
        alias.bash_alias_update()
        print('please source or restart your shell for changes to take effect')

    @classmethod
    def ask_brew(cls):
        # on osx, use brew a the package manager of choice
        brew_yn = {
            'type': 'list',
            'name': 'brew',
            'message': 'install Brew?',
            'choices': ['Yes',
                        'No'],
        }
        result = prompt(brew_yn)
        if result == 'Yes':
            return True
        else:
            return False
