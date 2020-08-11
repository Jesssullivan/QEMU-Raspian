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
from kernel import kernel
from random import random
import os
import toml
import threading
import paramiko

"""
qemu.py:
controls various qemu-system functions
"""


class qemu(object):

    # for 32 bit guest use older, fairly reliable versatilepb instead if generic -virt device.
    # yes generic ARM virt is better and newer....xD

    @classmethod
    def construct_arm1176(cls, qcow='', bridge=False):
        cmd = str("qemu-system-arm " +
                  " -kernel " +
                  sources.do_arg(arg='kernel', default='bin/ARMv6/kernel-qemu-4.14.79-stretch') +
                  " -cpu " +
                  sources.do_arg(arg='cpu', default='arm1176') +
                  " -m " +
                  sources.do_arg(arg='m', default='256') +
                  # versitilepb is limited to 256M
                  # for 32 bit guest use older, fairly reliable versatilepb instead if generic -virt device.
                  # yes generic ARM virt is better and newer....xD
                  " -M " +
                  sources.do_arg(arg='M', default='versatilepb') +
                  " -dtb " +
                  sources.do_arg(arg='dtb', default='"bin/ARMv6/versatile-pb.dtb"') +
                  " -append " +
                  sources.do_arg(arg='append',
                                 default='"root=/dev/sda2 panic=1 rootfsrtype=ext4 rw" ') +
                  " -hda " + str(qcow) +
                  # `**args` is just a catch all for passing any other qemu stuff
                  sources.do_arg(arg='**args',
                                 default=" -no-reboot -serial stdio -net user,hostfwd=tcp::10022-:22 -net nic"
                                 )
                  )
        return cmd

    @classmethod
    def construct_arm64(cls, qcow='', bridge=False):

        cmd = str("qemu-system-aarch64 " +
                  " -kernel " +
                  sources.do_arg(arg='kernel', default="bin/ddebian/vmlinuz-4.19.0-9-arm64") +
                  " -initrd " +
                  sources.do_arg(arg='initrd', default="bin/ddebian/initrd.img-4.19.0-9-arm64") +
                  " -m " +
                  sources.do_arg(arg='m', default='2048') +
                  " -M " +
                  sources.do_arg(arg='M', default='virt') +
                  " -cpu " +
                  sources.do_arg(arg='cpu', default='cortex-a53') +
                  " -append " +
                  sources.do_arg(arg='append',
                                 default='"rw root=/dev/vda2 console=ttyAMA0 rootwait fsck.repair=yes memtest=1"') +
                  " -drive " +
                  " file=" + qcow + ",format=qcow2,id=hd-root " +
                  sources.do_arg(arg='**args',
                                 default=str("-no-reboot -serial stdio")
                                 )
                  )
        return cmd

    @staticmethod
    def construct_qemu_convert(img, qcow):
        cmd = str("qemu-img convert -f raw -O qcow2 " + img +
                  " " + qcow)
        return cmd

    @classmethod
    def do_qemu_expand(cls, qcow=''):
        xargs = sources.load_args()
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

            try:
                if os.path.isfile(names.any_img(image)):
                    subprocess.Popen(cls.construct_qemu_convert(img=names.any_img(image),
                                                                qcow=names.src_qcow(image)),
                                     shell=True).wait()
                    sleep(.25)
                    cls.do_qemu_expand(names.src_qcow(image))
            except:
                pass

        return names.any_qcow(image)

    @staticmethod
    def check_build_dirs(image):
        # `image` currently must the path of a *.img file
        if not os.path.isdir(names.src_dir(image)):
            os.mkdir(names.src_dir(image))

        if not os.path.isdir(names.src_build(image)):
            os.mkdir(names.src_build(image))

        if not os.path.isdir(names.src_mnt(image)):
            os.mkdir(names.src_mnt(image))

    @classmethod
    def copyto_qcow(cls, img='', file='', path='home/pi/'):

        if platform == 'darwin':
            print('OSX method not implemented yet, exiting')
            return 0

        print('copying to qcow2...')

        source = sources.get_source()
        qcow = names.any_qcow(image)

        mnt = names.src_mnt(image)
        cls.check_build_dirs(image)

        # qemu.copyto_qcow(img='stretch_lite', file='quick_sh/budgify.sh')
        # because these commands may be tied down to variable disk & indexing speed,
        # block each shell execution in clipi's thread w/ sleep()

        ops = {
            'verifying nbd...': subprocess.Popen('sudo modprobe nbd max_part=8', shell=True).wait(),
            'connecting qcow2 to nbd...': subprocess.Popen('sudo qemu-nbd --connect=/dev/nbd0 ' + qcow,
                                                           shell=True).wait(),
            'mounting qcow2...': subprocess.Popen('sudo mount /dev/nbd0p2 ' + mnt, shell=True).wait(),
            str('copying ' + file + '...'): subprocess.Popen('sudo cp -rf ' + file + ' ' + mnt + path,
                                                             shell=True).wait(),
            'unmounting qcow2...': subprocess.Popen('sudo umount ' + mnt, shell=True).wait(),
            'disconnecting nbd....': subprocess.Popen('sudo qemu-nbd -d /dev/nbd0',
                                                      shell=True).wait()
        }

        for operation in ops.keys():
            sleep(.1)
            print(operation)
            x = ops[operation]

    @classmethod
    def _ensure_ssh(cls, image):
        if sources.do_arg('ssh', True):
            cls.copyto_qcow(img=image, file='ssh')

    @classmethod
    def _ensure_wpa_supplicant(cls, image):
        if sources.do_arg('wpa_supplicant', False):
            cls.copyto_qcow(img=image, file='wpa_supplicant.conf')

    """
    The following network & bridging functions have not been reimplemented yet
    """

    @staticmethod
    def get_network_depends():
        if platform == 'darwin':
            print('cannot install network bridge depends on mac OSX')
            return 0
        else:
            print('make sure /network is ready to install....')
            subprocess.Popen('sudo chmod u+x network/apt_net_depends.sh', shell=True).wait()
            print('installing.....')
            subprocess.Popen('./network/apt_net_depends.sh', shell=True).wait()
            sleep(.1)
            print('done.')

    @staticmethod
    def new_mac():
        oui_bits = [0x52, 0x54, 0x00]
        for x in range(256):
            mac = oui_bits + [
                random.randint(0x00, 0xff),
                random.randint(0x00, 0xff),
                random.randint(0x00, 0xff)]
            return ':'.join(["%02x" % x for x in mac])

    @staticmethod
    def check_bridge():
        CLIPINET = "read CLIPINET <<< $(ip -o link | awk '$2 != " + '"lo:"' + " {print $2}')"
        if platform == 'darwin':
            print('bridge networking not available for mac OSX')
            quit()
        else:
            print('checking bridge network.....')
            subprocess.Popen(CLIPINET, shell=True).wait()

            subprocess.Popen('sudo chmod u+x network/up_bridge.sh', shell=True).wait()
            sleep(.1)
            subprocess.Popen('sudo ./network/up_bridge.sh', shell=True)
            sleep(.1)

    @staticmethod
    def _init(image):
        # "launch_qcow" is returned a .qcow2 after it has been verified to exist-
        # this way we can call to launch an image that we don't actually have yet,
        # letting qemu.ensure_img() go fetch & prepare a fresh one
        common.main_install()
        common.ensure_dir()
        common.ensure_bins()
        launch_qcow = qemu.ensure_img(image)
        qemu._ensure_ssh(image)
        qemu._ensure_wpa_supplicant(image)
        return launch_qcow

    @classmethod
    def launch(cls, image, use64=False, bridge=False):

        launch_qcow = cls._init(image)

        if use64:
            if bridge:
                print('launching ARM 64 bit emulation, bridged networking')
                proc, err = subprocess.Popen(cls.construct_arm64(qcow=launch_qcow),
                                             shell=True,
                                             stdout=subprocess.PIPE,
                                             stdin=subprocess.PIPE)
            else:
                print('launching ARM 64 bit emulation, SLiRP networking')
                proc, err = subprocess.Popen(cls.construct_arm64(qcow=launch_qcow,
                                                                 bridge=True),
                                             shell=True,
                                             stdout=subprocess.PIPE,
                                             stdin=subprocess.PIPE)

        else:
            if bridge:
                print('launching ARM 32 bit emulation, bridged networking')
                proc, err = subprocess.Popen(cls.construct_arm1176(qcow=launch_qcow),
                                             shell=True,
                                             stdout=subprocess.PIPE,
                                             stdin=subprocess.PIPE)
            else:
                print('launching ARM 32 bit emulation,  SLiRP networking')
                proc = subprocess.Popen(cls.construct_arm1176(qcow=launch_qcow,
                                                              bridge=True),
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE)
        return proc

    @classmethod
    def _t_ssh(cls, usr='pi', pwd='raspberry', port=10022):

        print('starting ssh client...')
        conn = False
        err_ct = 0

        ip = 'localhost'
        ssh_cmd = 'sshpass -p ' + pwd + ' ssh ' + usr + '@' + ip + ' -p ' + str(port)

        while not conn and err_ct <= 12:
            sleep(1)
            try:
                p = subprocess.Popen(ssh_cmd,
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE)
                p.communicate('mike')[0].rstrip()

                # conn = True

            except ConnectionResetError:
                print('Connection Error, continuing...')
                err_ct += 1
                sleep(1)
                pass

            except:
                err_ct += 1
                sleep(1)
                pass

    @classmethod
    def _t_interact(cls, image, file):

        print('initializing image...')
        cls._init(image)

        sleep(.1)
        print('writing ' + file.__str__() + '...')
        cls.copyto_qcow(img=image, file=file)

        sleep(.1)
        print('checking guest...')

        if sources.do_arg('use64', False):
            use64 = True
        else:
            use64 = False

        if sources.do_arg('bridge', False):
            bridge = True
        else:
            bridge = False

        print('starting guest...')
        cls.launch(image=image, use64=use64, bridge=bridge)
        sleep(2)

    @classmethod
    def guest_t(cls, image, file):
        t = threading.Thread(target=cls._t_interact(image, file))
        return t

    @classmethod
    def ssh_t(cls, usr='pi', pwd='raspberry', port=10022):
        t = threading.Thread(target=cls._t_ssh(usr, pwd, port))
        return t


if __name__ == '__main__':

    image = sources.get_source()['stretch_lite']
    print('testing image: ' + names.src_img(image))

    common.main_install()
    common.ensure_dir()
    common.ensure_bins()
    qemu.ensure_img(image)

    print('starting guest launcher thread...')
    guest = qemu.guest_t(image, file='quick_sh/budgify.sh')
    guest.start()
    sleep(10)

    print('starting ssh control thread...')
    ssh = qemu.ssh_t()
    ssh.start()

