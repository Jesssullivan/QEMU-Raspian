#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

import platform
import subprocess
from common import *
from names import names
from sources import sources
from fdiskl import fdiskl
import os
import toml

"""
kernel.py:
install, prepare, make cross compile stuff for making 64 bit kernel
methods to build 64 bit images & emulations
"""


class kernel(object):

    def __init__(self):
        if platform == 'darwin':
            print("environment: detected osx- aborting.  feel free to contribute osx methods...")
            quit()

        if platform == "linux2":
            print("environment: detected Linux, continuing with apt-get.....\n" +
                  "please feel free to contribute methods for alternative package managers :)")

        if platform == "linux":
            print("environment: detected Linux, continuing with apt-get...")

    @classmethod
    def depends(cls):
        print('\npreparing kernel depends...\n')
        subprocess.Popen("sudo chmod u+x kernel_sh/kernel_depends.sh", shell=True).wait()

        print('\n preparing & installing kernel depends...\n')
        subprocess.Popen("sudo ./kernel_sh/kernel_depends.sh", shell=True).wait()

    @classmethod
    def build_binutils(cls):
        print('\n preparing preconf binutils...\n')
        subprocess.Popen("sudo chmod u+x kernel_sh/preconf_binutils.sh", shell=True).wait()
        subprocess.Popen("./kernel_sh/preconf_binutils.sh", shell=True).wait()

        sleep(.1)
        print('\n preparing binutils...\n')
        sleep(.1)

        common.ensure_dir(dirname='binutils-obj')
        subprocess.Popen("cp kernel_sh/make_binutils.sh binutils-obj/make_binutils.sh", shell=True).wait()
        subprocess.Popen("sudo chmod u+x binutils-obj/make_binutils.sh", shell=True).wait()

        sleep(.1)
        print('\nmaking binutils @ binutils-obj...\n')
        sleep(.1)

        subprocess.Popen("./binutils-obj/make_binutils.sh", shell=True).wait()

    @classmethod
    def build_gcc(cls):
        print('\n preparing preconf gcc...\n')
        subprocess.Popen("sudo chmod u+x kernel_sh/preconf_gcc.sh", shell=True).wait()
        subprocess.Popen("./kernel_sh/preconf_gcc.sh", shell=True).wait()

        sleep(.1)
        print('\n preparing gcc config...\n')
        sleep(.1)

        common.ensure_dir(dirname='gcc-out')
        subprocess.Popen("cp kernel_sh/make_gcc.sh gcc-out/make_gcc.sh", shell=True).wait()
        subprocess.Popen("sudo chmod u+x gcc-out/make_gcc.sh", shell=True).wait()

        sleep(.1)
        print('\n making gcc @ gcc-out...\n')
        sleep(.1)

        subprocess.Popen("./gcc-out/make_gcc.sh", shell=True).wait()

    @classmethod
    def check_build_dirs(cls, image):
        # `image` currently must the path of a *.img file
        #  todo: this should be less brittle
        if not os.path.isdir(names.src_dir(image)):
            os.mkdir(names.src_dir(image))
        if not os.path.isdir(names.src_build(image)):
            os.mkdir(names.src_build(image))
        if not os.path.isdir(names.src_mnt(image)):
            os.mkdir(names.src_mnt(image))

    @classmethod
    def mnt(cls, image, block=0, t='ext4'):
        # `image` currently must the path of a *.img file (not the source.toml name)
        kernel.check_build_dirs(image=image)
        fblock = block * 512
        cmd = str('sudo mount -o offset= ' +
                  str(fblock) +
                  ' -t ' + t + ' ' +
                  image + ' ' +
                  names.src_mnt(image))
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        print('completed mount attempt....')
