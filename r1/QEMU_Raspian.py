import subprocess
import os
from sys import argv
from time import sleep
import random

help_str = str("\n " +
               " use -rm to remove QEMU file from this dir \n " +
               " use -h to see this message again \n " +
               " build image with ``` qemu-img convert -f qcow2 -O raw file.qcow2 file.img ``` \n\n " +
               " supply arg 'stretch' for standard stretch release \n " +
               " supply arg 'stretchlite' for stretchlite release [default] \n " +
               " supply arg 'buster' for standard buster release  \n " +
               " supply arg 'busterlite' for busterlite release \n ")

# global pb:
vers_pb = "versatile-pb.dtb"
wget_pb = "wget https://github.com/dhruvvyas90/qemu-rpi-kernel/raw/master/versatile-pb.dtb -O versatile-pb.dtb"

buster = dict(
    name='buster',
    kern_loc="wget https://github.com/dhruvvyas90/qemu-rpi-kernel/blob/master/kernel-qemu-4.19.50-buster?raw=true -O ",
    kern='kernel-qemu-4.19.50-buster',
    url="wget http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-09-30/",
    zip='2019-07-10-raspbian-buster.zip',
    fs='2019-07-10-raspbian-buster.img',
    qcow='buster.qcow2'
)

busterlite = dict(
    name='busterlite',
    kern_loc="wget https://github.com/dhruvvyas90/qemu-rpi-kernel/blob/master/kernel-qemu-4.19.50-buster?raw=true -O ",
    kern='kernel-qemu-4.19.50-buster',
    url="wget http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2019-09-30/",
    zip='2019-09-26-raspbian-buster-lite.zip',
    fs='2019-09-26-raspbian-buster-lite.img',
    qcow='busterlite.qcow2'
)

stretch = dict(
    name='stretch',
    kern_loc="wget https://github.com/dhruvvyas90/qemu-rpi-kernel/blob/master/kernel-qemu-4.14.79-stretch?raw=true -O ",
    kern='kernel-qemu-4.14.79-stretch',
    url="wget http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-04-09/",
    zip='2019-04-08-raspbian-stretch',
    fs='2019-04-08-raspbian-stretch.img',
    qcow='stretch.qcow2'
)

stretchlite = dict(
    name='stretchlite',
    kern_loc="wget https://github.com/dhruvvyas90/qemu-rpi-kernel/blob/master/kernel-qemu-4.14.79-stretch?raw=true -O ",
    kern='kernel-qemu-4.14.79-stretch',
    url="wget http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/",
    zip='2018-11-13-raspbian-stretch-lite',
    fs='2018-11-13-raspbian-stretch-lite.img',
    qcow='stretchlite.qcow2'
)


def bash(cmd):
    proc = subprocess.Popen(cmd,
                            shell=True,
                            executable='/bin/bash',
                            stdout=subprocess.PIPE,
                            encoding='utf-8')
    return proc.pid


def rm():  # benefit of the doubt- some other file could be in here besides this script
    for file in os.listdir(os.curdir):
        if file.endswith('.qcow2') or \
                file.endswith('.zip') or \
                file.endswith('.img') or \
                file.endswith('.dtb') or \
                file.startswith('wget') or \
                file.startswith('kernel'):
            os.remove(file)


def rand_hex(l: int, return_string=''):
    for char in range(l):
        return_string = return_string + (random.choice("0123456789ABCDEF"))
    return return_string


def newmac():
    mac = ''
    for pair in range(5):
        mac += rand_hex(2) + ':'
    mac += rand_hex(2)
    return mac


def bash(cmd):
    proc = subprocess.Popen(cmd,
                            shell=True,
                            executable='/bin/bash',
                            stdout=subprocess.PIPE,
                            encoding='utf-8')
    return proc.pid


def argtype():
    try:
        if len(argv) == 2:
            use = True
        elif len(argv) == 1:
            print(help_str)
            use = False
        else:
            print('command takes 0 or 1 args!')
            raise SystemExit
    except:
        print('arg error...')
        raise SystemExit
    return use


def main(rtype):

    command = ' '
    my_mac = newmac()
    """
    if not os.path.exists(rtype['qcow']):

        if not os.path.exists(rtype['fs']):

            if not os.path.exists(rtype['zip']):

                if not os.path.exists(rtype['kern']):

                    if not os.path.exists(vers_pb):

                        command += str(wget_pb + ' && ')

                    command += str(rtype['kern_loc'] + rtype['kern'] + ' && ')

                command += str(rtype['url'] + rtype['zip'] + ' && ')

            command += str(' unzip ' + rtype['zip'] + ' && ')
    """

    command += str('qemu-img convert -f raw -O qcow2 ' + rtype['fs'] + ' ' + rtype['qcow'] + ' && ' +
                       'qemu-img resize ' + rtype['qcow'] + ' +16G && ')

    command += str("qemu-system-arm -kernel " + buster['kern'] +
                   " -cpu arm1176 -m 256 -M versatilepb " +
                   " -dtb " + 'versatile-pb.dtb ' + "-no-reboot " +
                   ' -serial stdio -append "root=/dev/sda2 panic=1 rootfsrtype=ext4 rw" ' +
                   " -hda " + buster['qcow'])

    # print(str('command = ' + command))  # debug only
    bash(command)

    # providing a small buffer here w/ sleep:
    print('waiting ... ')
    sleep(1)
    print('waiting ... ')
    sleep(1)
    print('done.')


if __name__ == '__main__':

    rtype = ''

    if not argtype():

        rtype = stretchlite  # default behavior

    else:
        # releases:
        if str(argv[1]) == 'stretch':
            rtype = stretch
        elif str(argv[1]) == 'stretchlite':
            rtype = stretchlite
        elif str(argv[1]) == 'buster':
            rtype = buster
        elif str(argv[1]) == 'busterlite':
            rtype = busterlite

        # to exit:
        elif str(argv[1]) == '-h':
            print(help_str)
            raise SystemExit

        elif str(argv[1]) == '-rm':
            rm()
            raise SystemExit

        else:
            print("\n \
                  ARG ERROR: please use arg ' -h' to list options. \n")
            raise SystemExit

    main(rtype)
