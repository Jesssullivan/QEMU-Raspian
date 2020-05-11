import subprocess
import os
from sys import argv
from time import sleep
import random
from os import geteuid

help_str = str("\n " +
               " use -rm to remove QEMU file from this dir \n " +
               " use -h to see this message again \n " +
               " build image with ``` qemu-img convert -f qcow2 -O raw file.qcow2 file.img ``` \n\n " +
               " supply arg 'stretch' for standard stretch release \n " +
               " supply arg 'stretchlite' for stretchlite release [default] \n " +
               " supply arg 'buster' for standard buster release  \n " +
               " supply arg 'busterlite' for busterlite release \n ")

# global pb:
wget_pb = "wget https://raw.githubusercontent.com/dhruvvyas90/qemu-rpi-kernel/master/versatile-pb.dtb -O versatile-pb.dtb"

buster = dict(
    name='buster',
    kern_loc="wget https://raw.githubusercontent.com/dhruvvyas90/qemu-rpi-kernel/master/kernel-qemu-4.19.50-buster -O kernel-qemu-4.19.50-buster",
    url="wget http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-09-30/",
    zip='2019-07-10-raspbian-buster.zip file.zip',
    fs='2019-07-10-raspbian-buster.img',
    qcow='buster.qcow2'
)

busterlite = dict(
    name='busterlite',
    kern_loc="wget https://raw.githubusercontent.com/dhruvvyas90/qemu-rpi-kernel/master/kernel-qemu-4.19.50-buster -O ",
    kern='kernel-qemu-4.19.50-buster',
    url="wget http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2019-09-30/",
    zip='2019-09-26-raspbian-buster-lite.zip',
    fs='2019-09-26-raspbian-buster-lite.img',
    qcow='busterlite.qcow2'
)

stretch = dict(
    name='stretch',
    kern_loc="wget https://raw.githubusercontent.com/dhruvvyas90/qemu-rpi-kernel/master/kernel-qemu-4.14.79-stretch -O ",
    kern='kernel-qemu-4.14.79-stretch',
    url="wget http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-04-09/",
    zip='2019-04-08-raspbian-stretch.zip',
    fs='2019-04-08-raspbian-stretch.img',
    qcow='stretch.qcow2'
)

stretchlite = dict(
    name='stretchlite',
    kern_loc="wget https://raw.githubusercontent.com/dhruvvyas90/qemu-rpi-kernel/master/kernel-qemu-4.14.79-stretch -O kernel-qemu-4.14.79-stretch",
    url="wget http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/2018-11-13-raspbian-stretch-lite.zip",
    fs='2018-11-13-raspbian-stretch-lite.img',
    qcow='stretchlite.qcow2'
)


def bash(cmd):
    proc = subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE)
    return proc.pid


def ispid(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        print('cannot kill ')
        return False
    else:
        return True


def rm():  # benefit of the doubt- some other file could be in here besides this script
    for file in os.listdir(os.curdir):
        if file.endswith('.qcow2') or \
                file.endswith('.zip') or \
                file.endswith('.img') or \
                file.startswith('wget') or \
                file.startswith('kernel'):
            os.remove(file)


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

    if os.path.exists(rtype['qcow']):
        bash(str("qemu-system-arm -kernel " + rtype['kern'] +
                       " -cpu arm1176 -m 256 -M versatilepb " +
                       " -dtb " + 'versatile-pb.dtb ' + "-no-reboot " +
                       ' -serial stdio -append "root=/dev/sda2 panic=1 rootfsrtype=ext4 rw" ' +
                       " -hda " + rtype['qcow']))
        return 0

    if os.path.exists(rtype['fs']):
        doconvert = bash(str('qemu-img convert -f raw -O qcow2 2018-11-13-raspbian-stretch-lite.img stretchlite.qcow2 && qemu-img resize ' + ' stretchlite.qcow2 ' + ' +8G '))
        while not ispid(doconvert):
            sleep(1)
            print("converting files")

    elif os.path.exists(rtype['zip']):
        dozip = bash(str(' unzip -p ' + rtype['zip']))
        while not ispid(dozip):
            sleep(1)
            print("converting compressed files")
    else:
        getfiles = bash(str(rtype['kern_loc'] +
                rtype['kern'] + ' && ' +
                rtype['url'] +
                rtype['zip']))

        while not ispid(getfiles):
            sleep(1)
            print("getting files")

        return 1


if __name__ == '__main__':

    if geteuid() != 0:
        print('Are you root?  Please use sudo to launch.')
        quit()

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

    while main(rtype) != 0:
        print("continuing....")
        sleep(2)
        print("....\n")
        main(rtype)

