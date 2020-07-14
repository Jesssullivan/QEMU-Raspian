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
import sys
from sys import platform
from time import sleep
from zipfile import ZipFile
import requests
from shutil import which
import xmltodict


class common(object):

    bin_url = "http://clipi-bins.s3.amazonaws.com/"

    @staticmethod
    def is_installed(cmd):
        print('checking if ' + cmd + ' is present...')
        if not which(cmd):
            print("didn't find " + cmd)
            return False
        else:
            return True

    @classmethod
    def dep_install(cls, dep, brew_dep=None):

        if platform == "linux" or platform == "linux2":
            print("environment: detected Linux, continuing with apt-get....")
            subprocess.Popen('sudo apt-get install ' + dep + ' -y', shell=True).wait()
            # todo: maybe prompt for other package manager options

        if brew_dep is None:
            brew_dep = dep

        elif platform == 'darwin':
            print("environment: detected osx, not completely tested yet, YMMV")
            if cls.is_installed('brew'):
                print('attempting brew install of ' + brew_dep + '...... \n')
                subprocess.Popen('brew install' + brew_dep, shell=True).wait()
            else:
                print("brew package manager not detected, attempting to install brew now...")
                brew_string = str(
                    '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)')
                subprocess.Popen(brew_string,
                                 shell=True).wait()

    @staticmethod
    def ensure_dir(dirname='image'):
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

    @classmethod
    def ensure_bins(cls):
        if not os.path.isdir('bin'):
            print('adding /bin....')
            os.mkdir('bin')
            sleep(.2)

            print('fetching binary list from S3....')
            index = requests.get(cls.bin_url).content
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
                cmd = str("wget -O bin/" + item + " " + cls.bin_url + item)
                subprocess.Popen(cmd, shell=True).wait()
            sleep(.2)
            print('done.')

    @classmethod
    def main_install(cls):
        if not cls.is_installed(cmd='wget'):
            cls.dep_install(dep='wget')

        if not cls.is_installed(cmd='qemu-system-arm'):
            cls.dep_install(dep='qemu-system-arm')

        if not cls.is_installed(cmd='qemu-system-aarch64'):
            cls.dep_install(dep='qemu-system-aarch64')

        if not cls.is_installed(cmd='dd'):
            cls.dep_install(dep='dd')

        if not cls.is_installed(cmd='nmap'):
            cls.dep_install(dep='nmap')

        if not cls.is_installed(cmd='p7zip'):
            cls.dep_install(dep='p7zip')

        # if not cls.is_installed(cmd='texinfo'):
            # cls.dep_install(dep='texinfo')

        # if not cls.is_installed(cmd='qemu-system-aarch64'):
        #    cls.dep_install(dep='qemu-system-aarch64')

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

    @staticmethod
    def restart(execute=None):
        clipi_path = os.path.abspath(__file__).split('<')[0]
        print('...\n')
        sleep(.1)
        print('...\n')
        sys.stdout.flush()
        if execute is None:
            cmd = 'python3 ' + clipi_path + 'clipi.py '
        else:
            cmd = 'python3 ' + clipi_path + 'clipi.py ' + str(execute)
        print(cmd)
        proc = subprocess.Popen(cmd, shell=True)
        print('re-executed clipi! ' +
              '\n - @ pid ' + str(proc.pid))

    @classmethod
    def cleanup(cls):
        # removes as admin from shell to avoid a wonky super python user xD
        subprocess.Popen('sudo rm -rf image .pi', shell=True).wait()
        print()
        for x in range(3):
            print('...\n')
            sleep(.1)
        print('complete. \n\n')

