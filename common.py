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
import requests
import xml.etree.ElementTree as ET
import xmltodict

# pip install:
import toml

bin_url = "http://clipi-bins.s3.amazonaws.com/"


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
            print('adding /bin....')
            os.mkdir('bin')
            sleep(.2)

            print('fetching binary list from S3....')
            index = requests.get(bin_url).content
            with open('bin/index.xml', 'wb') as f:
                f.write(index)
            sleep(.2)

            print('parsing response....')
            with open('bin/index.xml') as fd:
                doc = xmltodict.parse(fd.read())
            sleep(.2)

            print('downloading....')
            Keys = doc['ListBucketResult']['Contents']
            for f in Keys:
                item = f['Key']
                cmd = str("wget -O bin/" + item + " " + bin_url + item)
                subprocess.Popen(cmd, shell=True).wait()
            sleep(.2)
            print('done.')

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
        except:
            pass

    @classmethod
    def opt_kwargs(cls, **kwargs):
        return kwargs
