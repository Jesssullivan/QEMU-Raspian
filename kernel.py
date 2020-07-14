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
import os
import toml
import re

"""
kernel.py:
ramdisk & kernel related utilities
-   controls fdisk -l utility to inspect partitions & sectors from image.
-   install, prepare, make cross compile stuff for making 64 bit kernel- 
-   gcc- only really pertains to building a new kernel from source- for most purposes just use any of the existing binaries)
"""


class kernel(object):

    def __init__(self):
        if platform == 'darwin':
            print("environment: detected osx- aborting.  feel free to contribute osx methods...")
            quit()
            
        if platform == "linux":
            print("environment: detected Linux, continuing with apt-get...")

        if platform == "linux2":
            print("environment: detected Linux, continuing with apt-get.....\n" +
                  "please feel free to contribute methods for alternative package managers :)")

        if platform == "linux":
            print("environment: detected Linux, continuing with apt-get...")

    @staticmethod
    def depends():
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
        if not os.path.isdir(names.src_dir(image)):
            os.mkdir(names.src_dir(image))
        if not os.path.isdir(names.src_build(image)):
            os.mkdir(names.src_build(image))
        if not os.path.isdir(names.src_mnt(image)):
            os.mkdir(names.src_mnt(image))

    """
    @classmethod
    def get_kernel(cls):
        cmd = 'git clone --depth=1 -b rpi-4.19.y https://github.com/raspberrypi/linux.git'
    """

    @classmethod
    def replace_fstab(cls, image):
        # `image` currently must the path of a *.img file (not the source.toml name)
        kernel.check_build_dirs(image=image)
        # mount must use short path names due to file name encryption silliness
        # https://bugs.launchpad.net/ecryptfs/+bug/344878 lol
        if not os.path.isdir('.pi'):
            os.mkdir('.pi')
        if not os.path.isdir('.pi/mnt'):
            os.mkdir('.pi/mnt')

        try:
            disk = kernel.fdisk_read(names.src_img(image))['.img2']
            fblock = int(disk['Start']) * 512

            cmd_cp_in = str('sudo cp -rf ' + names.src_img(image) + ' ' + '.pi/pi.img')
            subprocess.Popen(cmd_cp_in, shell=True, stdout=subprocess.PIPE).wait()
            print('completed copy in attempt....')
            sleep(.5)

            cmd_mnt = str('sudo mount -o offset=' +
                          str(fblock) + ' ' +
                          '.pi/pi.img .pi/mnt')
            subprocess.Popen(cmd_mnt, shell=True, stdout=subprocess.PIPE)
            print('completed mount attempt....')
            sleep(.5)

            cmd_fstab = 'sudo cp -f kernel_sh/fstab .pi/mnt/etc/fstab'
            subprocess.Popen(cmd_fstab, shell=True, stdout=subprocess.PIPE)
            sleep(.1)
            print('completed replace fstab attempt....')

            cmd_umnt = str('sudo umount .pi/mnt')
            subprocess.Popen(cmd_umnt, shell=True, stdout=subprocess.PIPE).wait()
            print('completed unmount.')

            cmd_cp_out = str('sudo cp -rf .pi/pi.img ' + names.src_img(image))
            subprocess.Popen(cmd_cp_out, shell=True, stdout=subprocess.PIPE)
            print('completed copy attempt....')

        except TypeError:
            sleep(.2)
            print('moving on from fdisk....')
            pass

    @staticmethod
    def fdisk_setup():
        if sys.platform == 'darwin':
            print('detected osx, checking fdisk in gptfdisk via brew...')
        if sys.platform == "linux" or sys.platform == "linux2":
            print('checking fdisk...')
        common.dep_install(dep='fdisk', brew_dep='gptfdisk')
        sleep(.1)

    @staticmethod
    def fdisk_read(image):
        # ensure we've got fdisk- not sure yet if this works from osx via gptfdisk
        cmd = str('fdisk -l ' + image)

        # read fdisk -l output:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        result = proc.stdout.read().__str__()

        # figure out what type we should iterate with when looking via file / part contained within image-
        # (plz only use .img for now)
        if '.iso' in result:
            iter = '.iso'
        # not sure it this one will work......
        if '.qcow2' in result:
            iter = '.qcow2'
        else:
            iter = '.img'

        # chop up fdisk results by file / partition:
        parts = re.findall(r'' + iter + '\d', result)

        disk = {}
        for p in parts:
            # sub dict 'part' will contain fdisk -l output values:
            part = {}
            # get just the number words:
            line = result.split(p)[1]
            words = re.split(r'\s+', line)
            # place each word into 'part':
            part['Start'] = words[1]
            part['End'] = words[2]
            part['Sectors'] = words[3]
            part['Size'] = words[4]
            part['Id'] = words[5]
            part['Format'] = words[6].split('\\n')[0]
            # stick this part into 'disk', move onto next disk part:
            disk[p] = part
        return disk
