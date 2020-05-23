#!/usr/bin/env python3
"""
Emulate, organize, burn, manage a variety of distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/QEMU-Raspian
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


# methods do.* are generic, shared among classes
class do(object):

    @classmethod
    def src_zip(cls, img_text):
        return img_text.split('/')[-1]

    @classmethod
    def src_img(cls, img_text):
        return cls.src_zip(img_text).split('.zip')[0] + '.img'

    @classmethod
    def src_qcow(cls, img_text):
        return cls.src_zip(img_text).split('.zip')[0] + '.qcow2'

    @classmethod
    def src_name(cls, img_text):
        return cls.src_zip(img_text).split('.zip')[0]

    @classmethod
    def unzip(cls, input, output):
        with ZipFile(input, 'r') as zip_ref:
            zip_ref.extractall(output)

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


class Utilities(object):

    @classmethod
    def nmap_search(cls):

        print('Uses nmap to find local Pi devices by MAC address....')
        # just to make sure nmap is available
        QSetup.main_install()

        # find the first two ip quadrants from which to increment:
        get_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        get_socket.connect(("8.8.8.8", 80))
        ip_quad = str(get_socket.getsockname()[0]).split('.')
        get_socket.close()

        # execute nmap:
        print('\n ...starting search for Pi devices, this may take a while... \n')
        cmd = "sudo nmap -sP " \
              + ip_quad[0] + \
              "." + ip_quad[1] + ".1.1/24" + \
              " | awk '/^Nmap/{ip=$NF}/B8:27:EB/{print ip}'"
        subprocess.Popen(cmd, shell=True).wait()
        print('\n ...search complete. \n')

    @classmethod
    def add_to_bash(cls):
        print('adding alias....')
        clipi_line = "\\'~/.clipi/clipi.py\\'"

        if platform == "linux" or platform == "linux2":
            print("environment: detected Linux, continuing...")
            cmd = "echo alias clipi=" + clipi_line + " >> ~/.bashrc "
            subprocess.Popen(cmd, shell=True).wait()

        if platform == 'darwin':
            print("environment: detected Mac OSX, continuing...")
            cmd = "echo alias clipi=" + clipi_line + " >> ~/.bash_profile "
            subprocess.Popen(cmd, shell=True).wait()

    @classmethod
    def bash_alias_update(cls):
        # adds .directory for bash version, separate from git:
        if not os.path.exists('~/.clipi'):
            subprocess.Popen("mkdir ~/.clipi", shell=True).wait()

        print('copying clipi.py to ~/.clipi ....')
        subprocess.Popen('sudo cp -rf ' + os.path.relpath('clipi.py') +
                         ' ~/.clipi/clipi.py', shell=True).wait()

        print('copying sources.py to ~.clipi ....')
        subprocess.Popen('sudo cp -rf ' + os.path.relpath('sources.py') +
                         ' ~/.clipi/sources.py', shell=True).wait()

    subprocess.Popen('sudo chmod 775 ~/.clipi/clipi.py', shell=True).wait()


class ddWriter(object):

    @classmethod
    def what_disk(cls):
        # prompt following image selection for target disk
        target = {
            'type': 'input',
            'name': 'target',
            'message': "please type the target disk's system name, such as `sdb` or sdc`",
            'default': "sdc"
        }
        response = prompt(target)
        return response['target']

    @classmethod
    def dd_write(cls, sd_disk, image):
        print('preparing to write out image, unmount target....')
        umount_cmd = str('umount /dev/' + sd_disk + ' 2>/dev/null || true')
        subprocess.Popen(umount_cmd, shell=True).wait()
        sleep(.1)
        print('writing to target....')
        sleep(.1)
        dd_cmd = str('sudo dd if=' + image + ' of=/dev/' + sd_disk + ' bs=1048576')
        print('writing to target....')
        subprocess.Popen(dd_cmd, shell=True).wait()
        sleep(.1)
        print('completed write, syncing....')
        subprocess.Popen('sync ', shell=True).wait()
        print('finished xD \n ' +
              'to pre-enable wifi and ssh, reinsert sd_disk, then ' +
              'copy file `ssh` and a configured `wpa_supplicant.conf` to /boot :)')


# setup functions:
class QSetup(object):

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
    def ask_brew(cls):
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
                print("brew package manager not detected, would you like to install brew now?")
                if cls.ask_brew():
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
        image_dir = os.path.join('image/', do.src_name(image))
        image_zip = os.path.join(image_dir, do.src_zip(image))
        image_img = os.path.join(image_dir, do.src_img(image))
        image_qcow = os.path.join(image_dir, do.src_qcow(image))

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
                do.unzip(image_zip, image_dir)

            else:
                subprocess.Popen(str('wget -O' + image_zip + ' ' + image),
                                 shell=True).wait()
                sleep(.25)

        return image_qcow

    @classmethod
    def launch(cls, image):
        QSetup.main_install()
        QSetup.ensure_bins()
        launch_qcow = cls.ensure_img(image)
        subprocess.Popen(cls.construct_qemu_execute(qcow=launch_qcow),
                         shell=True).wait()


def ask_opts_1():
    opts_1 = {
        'type': 'list',
        'name': 'opts_1',
        'message': 'Options:',
        'choices': [
            'Launch a Pi emulation',
            'Burn a bootable disk image',
            'Find Pi devices on this network',
            'Utilities...'
        ]
    }
    answers = prompt(opts_1)
    return answers['opts_1']


## Menus ##

def utils_menu():
    utils_1 = {
        'type': 'list',
        'name': 'utils_1',
        'message': 'Options:',
        'choices': [
            'Cleanup...',
            'Install clipi as alias',
            'Check / install dependencies',
            'TODO: Launch some emulations w/ virtual network bridge'
        ]
    }
    answers = prompt(utils_1)
    return answers['utils_1']


def launch_std():
    launches = {
        'type': 'list',
        'name': 'launches',
        'message': 'Select an image....',
        'choices': source
    }
    answers = prompt(launches)
    return source[answers['launches']]


def menu():  # this is the main, initial menu
    op1 = ask_opts_1()
    if op1 == 'Launch a Pi emulation':
        # check if we are able to run:
        QSetup.main_install()
        # check for emulation dir
        QSetup.ensure_dir()
        response = launch_std()
        launcher.launch(response)

    if op1 == 'Burn a bootable disk image':
        print('Follow the prompts: select and image')
        QSetup.main_install()
        QSetup.ensure_dir()
        response_image = launch_std()
        target_disk = ddWriter.what_disk()
        launcher.ensure_img(response_image)
        image_dir = os.path.join('image/', do.src_name(response_image))
        result = os.path.join(image_dir, do.src_img(response_image))
        ddWriter.dd_write(sd_disk=target_disk, image=result)
        do.restart()

    if op1 == 'Find Pi devices on this network':
        Utilities.nmap_search()
        do.restart()

    if op1 == 'Utilities...':
        print('Additional settings:')
        response = utils_menu()  # shows utils_menu() menu

        if response == 'Cleanup...':
            # double checks w/ a confirm:
            rm = {
                'type': 'confirm',
                'message': 'Are you sure? (This completely removes the /image directory!)',
                'name': 'continue',
                'default': True,
            }
            checked = prompt(rm)
            if checked:
                # removes as admin from shell to avoid a wonky super python user xD
                subprocess.Popen('sudo rm -rf image', shell=True).wait()
                do.restart()

        if response == 'Install clipi as alias':
            print('Adds `clipi` alias to your shell \n' +
                  '( Also copies clipi.py & sources.py to ~/.clipi)')
            # double checks w/ a confirm:
            alias = {
                'type': 'confirm',
                'message': "Are you sure? \n "
                           "(You'll need to restart or source this shell for this change to take effect)",
                'name': 'continue',
                'default': True,
            }
            checked = prompt(alias)
            if checked:
                Utilities.bash_alias_update()
                Utilities.add_to_bash()
                print('please source or restart your shell for changes to take effect')

        if response == 'Check / install dependencies':
            print(str('checking all clipi.py depends for your ' +
                      platform + ' - based machine....'))
            QSetup.main_install()
            do.restart()


if __name__ == '__main__':
    try:
        menu()
    except KeyboardInterrupt:
        print('keyboard interrupt, exiting...')
        sys.exit(1)
