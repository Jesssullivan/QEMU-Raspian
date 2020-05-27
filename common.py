#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

import sys
import os
import socket
import subprocess
from PyInquirer import prompt
from time import sleep
from sys import platform
from zipfile import ZipFile
from sources import source


def is_installed(cmd):
    print('checking if ' + cmd + ' is present...')
    from shutil import which
    if not which(cmd):
        print("didn't find " + cmd)
        return False
    else:
        return True


# on osx, use brew a the package manager of choice
def ask_brew():
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


def dep_install(dep):
    if platform == "linux" or platform == "linux2":
        print("environment: detected Linux, continuing...")
        subprocess.Popen('sudo apt-get install ' + dep + ' -y', shell=True).wait()
        # todo: maybe prompt for other package manager options

    elif platform == 'darwin':
        print("environment: detected osx, not completely tested yet, YMMV")
        if is_installed('brew'):
            print('attempting brew install of ' + dep + '...... \n')
            subprocess.Popen('brew install' + dep, shell=True).wait()
        else:
            print("brew package manager not detected, would you like to install brew now?")
            if ask_brew():
                brew_string = str(
                    '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)')
                subprocess.Popen(brew_string,
                                 shell=True).wait()


def ensure_dir(dirname='image'):
        if not os.path.isdir(dirname):
            os.mkdir(dirname)


def ensure_bins():
    if not os.path.isdir('bin'):
        os.mkdir('bin')
        print('TODO: go fetch binaries from github plz')


def main_install():
    if not is_installed(cmd='wget'):
        dep_install(dep='wget')

    if not is_installed(cmd='qemu-system-arm'):
        dep_install(dep='qemu-system-arm')

    if not is_installed(cmd='dd'):
        dep_install(dep='dd')

    if not is_installed(cmd='nmap'):
        dep_install(dep='nmap')

    if not is_installed(cmd='p7zip'):
        dep_install(dep='p7zip')


def unzip(input, output):
    if input.split('.')[-1] == 'zip':
        with ZipFile(input, 'r') as zip_ref:
            zip_ref.extractall(output)
        sleep(.1)  #
    elif input.split('.')[-1] == '7z':
        if not is_installed(cmd='p7zip'):
            print('installing p7zip to extract this image...')
            dep_install(dep='p7zip')
            dep_install(dep='p7zip-full')
            sleep(.1)
        print('attempting to extract image from 7z...')
        cmd = str('7z e ' + input + ' -o' + output + '  -aoa')
        subprocess.Popen(cmd, shell=True).wait()
        sleep(.1)


def restart():
    # behavior to cleanup & restart at main menu:
    for x in range(3):
        print('...\n')
        sleep(.1)
    print('complete. \n\n')
    clipi_path = os.path.abspath(__file__)
    sys.stdout.flush()
    os.execl(sys.executable, clipi_path, *sys.argv)


class names(object):

    @classmethod
    def src_name(cls, img_text):
        return img_text.split('/')[-1]

    @classmethod
    def src_dir(cls, img_text):
        return str('image/' + cls.src_name(img_text)).split('.')[0]

    @classmethod
    def src_img(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.')[0] + '.img')

    @classmethod
    def src_zip(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.')[0] + '.zip')

    @classmethod
    def src_7z(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.')[0] + '.7z')

    @classmethod
    def src_qcow(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.')[0] + '.qcow')

    @classmethod
    def src_local(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text))

    @classmethod
    def src_output(cls, img_text):
        return str(cls.src_dir(img_text) +
                   '/output_' + names.src_dir(img_text) + '.img')

