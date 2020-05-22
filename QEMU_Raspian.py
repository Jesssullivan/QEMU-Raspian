#!/usr/bin/env python
"""
Emulate & organize a variety of common ARM Raspbian distributions with QEMU
Written by Jess Sullivan
@ https://github.com/Jesssullivan/QEMU-Raspian
@ https://transscendsurvival.org/
"""
from __future__ import print_function, unicode_literals
from time import sleep
import sys
import os
from sys import platform
from PyInquirer import prompt
import subprocess
from zipfile import ZipFile

# locations, names for image / iso files:
stretch_lite = "http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/2018-11-13-raspbian-stretch-lite.zip"
stretch_desktop = "http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-04-09/'2019-04-08-raspbian-stretch.zip"
buster_lite = "http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2019-09-30/2019-09-26-raspbian-buster-lite.zip"
buster_desktop = " http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-09-30/2019-07-10-raspbian-buster.zip"


def src_zip(img_text):
    return img_text.split('/')[-1]


def src_img(img_text):
    return src_zip(img_text).split('.zip')[0] + '.img'


def src_qcow(img_text):
    return src_zip(img_text).split('.zip')[0] + '.qcow2'


def src_name(img_text):
    return src_zip(img_text).split('.zip')[0]


def ask_opts_1():
    opts_1 = {
        'type': 'list',
        'name': 'opts_1',
        'message': 'Options:',
        'choices': ['Launch a standard Pi emulation',
                    'Coming soon: Launch some emulations w/ virtual network bridge',
                    'Check / install dependencies',
                    'Coming soon: Other stuff xD']
    }
    answers = prompt(opts_1)
    return answers['opts_1']


def launch_std():
    launches = {
        'type': 'list',
        'name': 'launches',
        'message': 'would you like....',
        'choices': ['Raspbian Stretch-lite?',
                    'Raspbian Stretch-desktop?',
                    'Raspbian Buster-lite?',
                    'Raspbian Buster-desktop?']
    }
    answers = prompt(launches)
    return answers['launches']


def unzip(input, output):
    with ZipFile(input, 'r') as zip_ref:
        zip_ref.extractall(output)


# qemu depends, setup functions:
class QSetup(object):

    @classmethod
    def is_installed(cls, cmd):
        print('checking if qemu-system-arm and wget are present...')
        from shutil import which
        if not which(cmd):
            print("didn't find " + cmd)
            return False
        else:
            return True

    @classmethod
    def ask_brew(cls):
        brewYN = {
            'type': 'list',
            'name': 'brew',
            'message': 'install Brew?',
            'choices': ['Yes',
                        'No'],
        }
        result = prompt(brewYN)
        if result == 'Yes':
            return True
        else:
            return False

    @classmethod
    def dep_install(cls, dep):
        if platform == "linux" or platform == "linux2":
            print("environment: detected Linux, continuing...")
            subprocess.Popen('sudo apt-get install ' + dep + ' -y', shell=True).wait()
            # todo: prompt for other package manager options
        elif platform == 'darwin':
            print("environment: detected osx, not completely tested yet, YMMV")
            if not cls.is_installed('brew'):
                print("brew package manager not detected either, would you like to install brew now?")
                if cls.ask_brew():
                    brew_string = str(
                        '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)')
                    subprocess.Popen(brew_string,
                                     shell=True).wait()

    @classmethod
    def ensure_dir(cls, dirname='qemu'):
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

    @classmethod
    def ensure_bins(cls):  # todo: make all this directory handling less brittle
        if not os.path.isdir('bin'):
            os.mkdir('bin')
            print('TODO: go fetch binaries from github plz')

    @classmethod
    def main_install(cls):
        if not cls.is_installed(cmd='wget'):
            cls.dep_install(dep='wget')
        if not cls.is_installed(cmd='qemu-system-arm'):
            cls.dep_install(dep='qemu-system-arm')


class launcher(object):

    @classmethod
    def construct_qemu_execute(cls,
                               bin='bin/kernel-qemu-4.14.79-stretch',
                               qcow=''):
        cmd = str("qemu-system-arm -kernel " + bin +
                  " -cpu arm1176 -m 256 -M versatilepb -dtb bin/versatile-pb.dtb -no-reboot -serial stdio -append " +
                  '"root=/dev/sda2 panic=1 rootfsrtype=ext4 rw" -hda ' +
                  qcow)
        return cmd

    @classmethod
    def construct_qemu_convert(cls, img, qcow):
        cmd = str("qemu-img convert -f raw -O qcow2 " + img +
                  " " + qcow)
        return cmd

    @classmethod
    def do_qemu_expand(cls, qcow):
        cmd = str("qemu-img resize " + qcow + " +8G")
        subprocess.Popen(cmd, shell=True).wait()
        sleep(.1)
        return 0

    @classmethod
    def ensure_img(cls, image):
        image_dir = os.path.join('qemu/', src_name(image))
        image_zip = os.path.join(image_dir, src_zip(image))
        image_img = os.path.join(image_dir, src_img(image))
        image_qcow = os.path.join(image_dir, src_qcow(image))

        for x in range(7):

            if not os.path.exists(image_dir):
                os.mkdir(image_dir)

            if os.path.isfile(image_qcow):
                return image_qcow

            if os.path.isfile(image_img):
                subprocess.Popen(cls.construct_qemu_convert(img=image_img,
                                                            qcow=image_qcow),
                                 shell=True).wait()
                sleep(.25)
                cls.do_qemu_expand(image_qcow)

            if os.path.isfile(image_zip):
                unzip(image_zip, image_dir)

            else:
                subprocess.Popen(str('wget -O' + image_zip + ' ' + image),
                                 shell=True).wait()
                sleep(.25)

        return image_qcow

    @classmethod
    def launch(cls, image=stretch_lite):
        QSetup.main_install()
        QSetup.ensure_bins()
        launch_qcow = cls.ensure_img(image)
        subprocess.Popen(cls.construct_qemu_execute(qcow=launch_qcow),
                         shell=True).wait()


def main():
    op1 = ask_opts_1()
    if op1 == 'Launch a standard Pi emulation':
        # check if we are able to run:
        QSetup.main_install()
        # check for emulation dir
        QSetup.ensure_dir()

        response = launch_std()

        if response == 'Raspbian Stretch-lite?':
            launcher.launch(stretch_lite)

        if response == 'Raspbian Stretch-desktop?':
            launcher.launch(stretch_desktop)

        if response == 'Raspbian Buster-lite?':
            launcher.launch(buster_lite)

        if response == 'Raspbian Buster-desktop?':
            launcher.launch(buster_desktop)

    if op1 == 'Check / install dependencies':
        print(str('checking wget & qemu depends for your ' +
                  platform + ' - based machine....'))
        QSetup.main_install()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('keyboard interrupt, exiting...')
        sys.exit(1)
