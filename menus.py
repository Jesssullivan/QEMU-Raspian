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

    @staticmethod
    def main_menu():
        menu_1 = {
            'type': 'list',
            'name': 'menu_1',
            'message': 'Options:',
            'choices': [
                'Launch a Pi emulation',
                'Burn a bootable disk image',
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

    @staticmethod
    def launch_img():
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

    @staticmethod
    def image_settings():
        img_config = [
            {
                'type': 'list',
                'message': 'Bit Depth:',
                'name': 'bits',
                'choices': ['32 Bit', '64 Bit']
            },
            {
                'type': 'list',
                'message': 'Networking:',
                'name': 'network',
                'choices': ['SLiRP']
             },
        ]
        answers = prompt(img_config)
        return answers

    @staticmethod
    def cleanup():
        # removes as admin from shell to avoid a wonky super python user xD
        subprocess.Popen('sudo rm -rf image', shell=True).wait()
        print()
        for x in range(3):
            print('...\n')
            sleep(.1)
        print('complete. \n\n')

    @staticmethod
    def do_alias():
        print('Adds `clipi` alias to your shell \n' +
              '( Also copies clipi.py & sources.py to ~/.clipi)')
        alias.bash_alias_update()
        print('please source or restart your shell for changes to take effect')

    @staticmethod
    def what_disk():
        # prompt following image selection for target disk
        target = {
            'type': 'input',
            'name': 'target',
            'message': "please type the target disk's system name, such as `sdb` or sdc`",
            'default': "sdc"
        }
        response = prompt(target)
        return response['target']