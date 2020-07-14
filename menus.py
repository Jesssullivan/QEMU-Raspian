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
from PyInquirer import prompt, Separator

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
                '__Launch a Pi emulation w/ 64 bits',
                'Burn a bootable disk image',
                '__Burn a bootable disk image w/ verbatim raw',
                'Find Pi devices on this network',
                Separator('-----Utilities:-----'),
                'Cleanup...',
                'Install clipi as alias',
                'Check / install dependencies',
                'Check / build kernel & gcc tools'
            ]
        }
        answers = prompt(menu_1)
        return answers['menu_1']

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
        print('IMAGE = ' + source[answers['launches']])
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
