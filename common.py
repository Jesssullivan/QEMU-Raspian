#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

import os
import subprocess
# standard library:
import sys
from sys import platform
from time import sleep
from zipfile import ZipFile

# pip install:
import toml


class common(object):

    @classmethod
    def is_installed(cls, cmd):
        print('checking if ' + cmd + ' is present...')
        from shutil import which
        if not which(cmd):
            print("didn't find " + cmd)
            return False
        else:
            return True

    @classmethod
    def dep_install(cls, dep):
        if platform == "linux" or platform == "linux2":
            print("environment: detected Linux, continuing...")
            subprocess.Popen('sudo apt-get install ' + dep + ' -y', shell=True).wait()
            # todo: maybe prompt for other package manager options

        elif platform == 'darwin':
            print("environment: detected osx, not completely tested yet, YMMV")
            if cls.is_installed('brew'):
                print('attempting brew install of ' + dep + '...... \n')
                subprocess.Popen('brew install' + dep, shell=True).wait()
            else:
                print("brew package manager not detected, attempting to install brew now...")
                brew_string = str(
                    '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)')
                subprocess.Popen(brew_string,
                                 shell=True).wait()

    @classmethod
    def ensure_dir(cls, dirname='image'):
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

    @classmethod
    def ensure_bins(cls):
        if not os.path.isdir('bin'):
            os.mkdir('bin')
            print('TODO: go fetch binaries from github plz')

    @classmethod
    def main_install(cls):
        if not cls.is_installed(cmd='wget'):
            cls.dep_install(dep='wget')

        if not cls.is_installed(cmd='qemu-system-arm'):
            cls.dep_install(dep='qemu-system-arm')

        if not cls.is_installed(cmd='dd'):
            cls.dep_install(dep='dd')

        if not cls.is_installed(cmd='nmap'):
            cls.dep_install(dep='nmap')

        if not cls.is_installed(cmd='p7zip'):
            cls.dep_install(dep='p7zip')

    @classmethod
    def unzip(cls, input, output):
        if input.split('.')[-1] == 'zip':
            with ZipFile(input, 'r') as zip_ref:
                zip_ref.extractall(output)
            sleep(.1)
            return 0
        elif input.split('.')[-1] == '7z':
            if not cls.is_installed(cmd='p7zip'):
                print('installing p7zip to extract this image...')
                cls.dep_install(dep='p7zip')
                cls.dep_install(dep='p7zip-full')
                sleep(.1)
            print('attempting to extract image from 7z...')
            cmd = str('7z e ' + input + ' -o' + output + '  -aoa')
            subprocess.Popen(cmd, shell=True).wait()
            sleep(.1)
            return 0
        elif 'gz' in input:
            print('attempting to extract image from .gz...')
            cmd = str('gunzip ' + input)
            subprocess.Popen(cmd, shell=True).wait()
            sleep(.1)
            return 0
        elif 'xz' in input:
            print('attempting to extract image from .xz...')
            cmd = str('unxz ' + input)
            subprocess.Popen(cmd, shell=True).wait()
            sleep(.1)
            return 0

    @classmethod
    def restart(cls):
        # behavior to cleanup & restart at main menu:
        for x in range(3):
            print('...\n')
            sleep(.1)
        print('complete. \n\n')
        clipi_path = os.path.abspath(__file__)
        sys.stdout.flush()
        os.execl(sys.executable, clipi_path, *sys.argv)

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
    def arg_true(cls, dic, arg):
        try:
            if dic[arg]:
                return True
        except KeyError:
            pass

    @classmethod
    def opt_kwargs(cls, **kwargs):
        return kwargs

    @classmethod
    def has_toml(cls):
        # soften argument / no argument
        try:
            if '.toml' in sys.argv[1]:
                return True
        except:
            return False

    @classmethod
    def all_args(cls):
        if cls.has_toml():
            etc_args = toml.load(sys.argv[1])
            return etc_args
        if os.path.isfile('etc/defaults.toml'):
            etc_args = toml.load('etc/defaults.toml')
            return etc_args
        if os.path.isfile('defaults.toml'):
            etc_args = toml.load('defaults.toml')
            return etc_args
        else:
            etc_args = cls.opt_kwargs(
                # provide some catch-all arguments just in case something goes horribly wrong
                qcow_size="+8G",
                mem_vers="256",
                mem_64="2048",
                aarch32="32",
                cpu32="arm1176",
                aarch64="64",
                cpu64="cortex-a53"
            )
            return etc_args
