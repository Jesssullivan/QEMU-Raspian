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
import socket

# pip install:
import toml
import xmltodict
from PyInquirer import prompt

bin_url = "http://clipi-bins.s3.amazonaws.com/"


class sources(object):

    # provides an option to provide sources.toml or add directly to dictionary

    @classmethod
    def get_source(cls):
        if os.path.isfile('sources.toml'):
            source = toml.load('sources.toml')
            return source

        if os.path.isfile('etc/sources.toml'):
            source = toml.load('etc/sources.toml')
            return source

        else:
            print("couldn't find sources.toml or etc/sources.toml, FYI")
            # catch all if sources.toml doesn't exist:
            source = {
                'stretch_lite': 'http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/2018-11-13'
                                '-raspbian-stretch-lite.zip',
                'stretch_desktop': 'http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-04-09/2019-04-08-raspbian'
                                   '-stretch.zip',
                'octoprint': 'https://octopi.octoprint.org/latest',
            }
            return source


class names(object):

    @classmethod
    def src_name(cls, img_text):
        return img_text.split('/')[-1]

    @classmethod
    def src_dir(cls, img_text):
        return str('image/' + cls.src_name(img_text)).split('.')[0]

    @classmethod
    def src_zip(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.zip')[0] + '.zip')

    @classmethod
    def src_img(cls, img_text):
        if '.zip' in img_text:
            return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.zip')[0] + '.img')
        if '.7z' in img_text:
            return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.7z')[0] + '.img')
        if '.gz' in img_text:
            return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.gz')[0] + '.img')

    @classmethod
    def src_7z(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.7z')[0] + '.7z')

    @classmethod
    def src_gz(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.img.gz')[0] + '.img.gz')

    @classmethod
    def src_xz(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.img.gz')[0] + '.img.xz')

    @classmethod
    def src_qcow(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.')[0] + '.qcow2')

    @classmethod
    def src_local(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text))

    @classmethod
    def src_output(cls, img_text):
        return str(cls.src_dir(img_text) +
                   '/output_' + names.src_dir(img_text) + '.img')

    @classmethod
    def any_img(cls, img_text):
        for file in os.listdir(names.src_dir(img_text)):
            if file.endswith(".img"):
                return os.path.join(names.src_dir(img_text), file)

    @classmethod
    def any_zip(cls, img_text):
        for file in os.listdir(names.src_dir(img_text)):
            if file.endswith(".zip"):
                return os.path.join(names.src_dir(img_text), file)

    @classmethod
    def any_qcow(cls, img_text):
        for file in os.listdir(names.src_dir(img_text)):
            if file.endswith(".qcow2"):
                return os.path.join(names.src_dir(img_text), file)

    @classmethod
    def any_7z(cls, img_text):
        for file in os.listdir(names.src_dir(img_text)):
            if file.endswith(".7z"):
                return os.path.join(names.src_dir(img_text), file)

    @classmethod
    def any_gz(cls, img_text):
        for file in os.listdir(names.src_dir(img_text)):
            if file.endswith(".gz"):
                return os.path.join(names.src_dir(img_text), file)

    @classmethod
    def any_xz(cls, img_text):
        for file in os.listdir(names.src_dir(img_text)):
            if file.endswith(".xz"):
                return os.path.join(names.src_dir(img_text), file)


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


class dd(object):

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
        xargs = common.all_args()
        common.main_install()
        common.ensure_dir()
        common.ensure_bins()
        img = sources.get_source()[image]
        qemu.ensure_img(img)
        print('preparing to write out image, unmount target....')
        umount_cmd = str('umount /dev/' + sd_disk + ' 2>/dev/null || true')
        subprocess.Popen(umount_cmd, shell=True).wait()
        sleep(.2)
        print('writing ' + names.any_img(image) + ' to target....')
        dd_cmd = str('sudo dd if=' + names.any_img(image) + ' of=/dev/' + sd_disk + ' bs=1048576')
        print('writing to target....')
        subprocess.Popen(dd_cmd, shell=True).wait()
        sleep(.1)
        print('completed write, syncing....')
        subprocess.Popen('sync ', shell=True).wait()
        print('finished xD \n ' +
              'to pre-enable wifi and ssh, reinsert sd_disk, then ' +
              'copy file `ssh` and a configured `wpa_supplicant.conf` to /boot :)')


class menus(object):

    @classmethod
    def main_menu(cls):
        menu_1 = {
            'type': 'list',
            'name': 'menu_1',
            'message': 'Options:',
            'choices': [
                'Launch a Pi emulation',
                'Burn a bootable disk image',
                'Find Pi devices on this network',
                'Utilities...'
            ]
        }
        answers = prompt(menu_1)
        return answers['menu_1']

    @classmethod
    def utils_menu(cls):
        utils_1 = {
            'type': 'list',
            'name': 'utils_1',
            'message': 'Options:',
            'choices': [
                'Cleanup...',
                'Check / install dependencies',
            ]
        }
        answers = prompt(utils_1)
        return answers['utils_1']

    @classmethod
    def launch_img(cls):
        launches = {
            'type': 'list',
            'name': 'launches',
            'message': 'Select an image....',
            'choices': sources.get_source()
        }
        answers = prompt(launches)
        source = sources.get_source()
        print('IMAGE = ' + source[answers['launches']])
        return source[answers['launches']]

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
    def ask_brew(cls):
        # on osx, use brew a the package manager of choice
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



class nmap(object):

    @classmethod
    def nmap_search(cls):
        print('Uses nmap to find local Pi devices by MAC address....')
        # just to make sure nmap is available
        common.main_install()

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


class qemu(object):

    @classmethod
    def construct_arm1176_execute(cls, qcow=''):
        xargs = common.all_args()
        cmd = str("qemu-system-aarch64 -kernel " +
                  xargs['bin'] +
                  " -cpu " +
                  xargs['cpu32'] +
                  " -m " +
                  xargs['mem_vers'] +
                  " -M versatilepb -dtb bin/versatile-pb.dtb -no-reboot -serial stdio -append " +
                  '"root=/dev/sda2 panic=1 rootfsrtype=ext4 rw" -hda ' +
                  qcow)
        return cmd

    @classmethod
    def construct_arm64_execute(cls, qcow=''):
        xargs = common.all_args()
        cmd = str("qemu-system-aarch64 -M virt -m " +
                  xargs['mem_64'] +
                  " -cpu " +
                  xargs['cpu64'] +
                  " -kernel bin/installer-linux -initrd bin/installer-initrd.gz " +
                  " -no-reboot -serial stdio -append " +
                  ' "root=/dev/sda2 panic=1 rootfsrtype=ext4 rw" ' +
                  " -k en-us " +
                  '-hda ' +
                  qcow)
        return cmd

    # TODO: implement these network bridge methods
    @classmethod
    def get_network_depends(cls):
        if platform == 'darwin':
            print('cannot install network bridge depends on mac OSX')
            return 0
        else:
            print('make sure /network is ready to install....')
            subprocess.Popen('sudo chmod u+x network/apt_depends.sh', shell=True).wait()
            print('installing.....')
            subprocess.Popen('./network/apt_depends.sh', shell=True).wait()
            sleep(.1)
            print('done.')

    @classmethod
    def start_dhclient(cls):
        if platform == 'darwin':
            print('cannot use dhclient networking on mac OSX')
            return 0
        else:
            print('launching dhclient thread.....')
            subprocess.Popen('sudo chmod u+x network/dhclient.sh', shell=True).wait()
            sleep(.25)
            subprocess.Popen('./network/dhclient.sh', shell=True).wait()
            sleep(.1)
            print('exited dhclient thread.')
            sleep(.1)

    @classmethod
    def construct_qemu_convert(cls, img, qcow):
        cmd = str("qemu-img convert -f raw -O qcow2 " + img +
                  " " + qcow)
        return cmd

    @classmethod
    def do_qemu_expand(cls, qcow=''):
        xargs = common.all_args()
        cmd = str("qemu-img resize " + qcow + " " + xargs['qcow_size'])
        subprocess.Popen(cmd, shell=True).wait()
        sleep(.1)
        return 0

    @classmethod
    def ensure_img(cls, image):

        unzip = False
        got = False  # once we've fetched an image, got=true:
        # don't go get it again while exhausting other options

        for x in range(12):
            if not os.path.exists(names.src_dir(image)):
                os.mkdir(names.src_dir(image))

            if names.any_qcow(image) is not None:
                return names.any_qcow(image)

            if not unzip:

                if not names.any_zip(image) is None:
                    print('checking .zip....')
                    common.unzip(names.any_zip(image), names.src_dir(image))
                    unzip = True

                if not names.any_7z(image) is None:
                    print('checking .7z....')
                    common.unzip(names.any_7z(image), names.src_dir(image))
                    unzip = True

                if not names.any_gz(image) is None:
                    print('checking .gz....')
                    common.unzip(names.any_gz(image), names.src_dir(image))
                    unzip = True

                if not names.any_xz(image) is None:
                    print('checking .xz....')
                    common.unzip(names.any_xz(image), names.src_dir(image))
                    unzip = True

            if not got:
                if '.zip' in image:
                    subprocess.Popen(str('wget -O ' + names.src_zip(image) + ' ' + image),
                                     shell=True).wait()
                    got = True

                if '.7z' in image:
                    subprocess.Popen(str('wget -O ' + names.src_7z(image) + ' ' + image),
                                     shell=True).wait()
                    got = True

                if '.gz' in image:
                    subprocess.Popen(str('wget -O ' + names.src_gz(image) + ' ' + image),
                                     shell=True).wait()
                    got = True

                if '.xz' in image:
                    subprocess.Popen(str('wget -O ' + names.src_xz(image) + ' ' + image),
                                     shell=True).wait()
                    got = True

                sleep(.25)

            if os.path.isfile(names.any_img(image)):
                subprocess.Popen(cls.construct_qemu_convert(img=names.any_img(image),
                                                            qcow=names.src_qcow(image)),
                                 shell=True).wait()
                sleep(.25)
                cls.do_qemu_expand(names.src_qcow(image))

        return names.any_qcow(image)

    @classmethod
    def launch(cls, image):
        xargs = common.all_args()
        common.main_install()
        common.ensure_dir()
        common.ensure_bins()
        # "launch_qcow" is returned a .qcow2 after it has been verified to exist-
        # this way we can call to launch an image that we don't actually have yet,
        # letting qemu.ensure_img() go fetch & prepare a fresh one
        launch_qcow = qemu.ensure_img(image)
        print(launch_qcow)

        if xargs['use64']:
            subprocess.Popen(cls.construct_arm64_execute(qcow=launch_qcow),
                             shell=True).wait()
        else:
            subprocess.Popen(cls.construct_arm1176_execute(qcow=launch_qcow),
                             shell=True).wait()


def main():
    try:
        if common.has_toml():
            config = toml.load(sys.argv[1])
            conf = True
        else:
            config = None
            conf = False
    except:
        config = None
        conf = False

    def arg_true(text):
        try:
            if config[text]:
                return True
        except KeyError:
            pass

    if conf:

        if arg_true('Launch a Pi emulation'):
            image = sources.get_source()[config['image']]
            qemu.launch(image)

        if arg_true('Burn a bootable disk image'):
            response_image = config['image']
            target_disk = config['target_disk']
            dd.dd_write(sd_disk=target_disk, image=response_image)

        if arg_true('Find Pi devices on this network'):
            nmap.nmap_search()

        if arg_true('Cleanup...'):
            common.cleanup()

        if arg_true('Check / install dependencies'):
            print(str('checking all clipi.py depends for your ' +
                      platform + ' - based machine....'))
            common.main_install()

    else:

        op1 = menus.main_menu()

        if op1 == 'Launch a Pi emulation':
            image = menus.launch_img()
            qemu.launch(image)

        if op1 == 'Burn a bootable disk image':
            print('Follow the prompts: select and image')
            response_image = menus.launch_img()
            target_disk = dd.what_disk()
            print("checking types....")
            dd.dd_write(sd_disk=target_disk, image=response_image)

        if op1 == 'Find Pi devices on this network':
            nmap.nmap_search()

        if op1 == 'Utilities...':
            print('Additional settings:')
            response = menus.utils_menu()  # shows utils_menu() menu

            if response == 'Cleanup...':
                # double checks w/ a confirm:
                common.cleanup()

            if response == 'Check / install dependencies':
                print(str('checking all clipi.py depends for your ' +
                          platform + ' - based machine....'))
                common.main_install()


if __name__ == '__main__':

    try:

        main()

    except KeyboardInterrupt:
        print('keyboard interrupt, exiting...')
        sys.exit(1)
