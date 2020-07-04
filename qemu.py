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


"""
qemu.py:
controls various qemu-system functions
prepares disk image source for emulation- also isolates disk image kernel & ramdisk 
"""


class qemu(object):

    @classmethod
    def construct_arm1176_execute(cls, qcow=''):
        cmd = str("qemu-system-aarch64 -kernel image/kernel8.img" +
                  " -cpu " +
                  sources.do_arg(arg='cpu64', default='cortex-a53') +
                  " -m " +
                  sources.do_arg(arg='mem_64', default='2048') +
                  " -M " +
                  # for 32 bit guest use older, fairly reliable versatilepb instead if generic -virt device.
                  # yes generic ARM virt is better and newer....xD
                  sources.do_arg(arg='device64', default='virt') +
                  " -no-reboot -serial stdio -append " +
                  '"init=/dev/sda2 panic=1 rootfsrtype=ext4 rw" -hda ' +
                  qcow)
        return cmd

    @classmethod
    def construct_arm64_execute(cls, qcow=''):
        cmd = str('qemu-system-aarch64 -kernel ' +
                  sources.do_arg(arg='kernel', default='') +
                  " -m " +
                  sources.do_arg(arg='mem_64', default='2048') +
                  " -M " +
                  sources.do_arg(arg='device64', default='virt') +
                  " -cpu " +
                  sources.do_arg(arg='cpu64', default='cortex-a53') +
                  " -serial stdio" +
                  "-append " +
                  sources.do_arg(arg='append',
                                 default='"rw root=/dev/vda2 console=ttyAMA0 loglevel=8 rootwait fsck.repair=yes memtest=1"') +
                  " -drive file=" + qcow + ",if=sd,id=hd-root")
        return cmd

    # TODO: implement these network bridge methods
    # (guest to guest bridging)
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

    @classmethod
    def launch(cls, image):
        common.main_install()
        common.ensure_dir()
        common.ensure_bins()
        # "launch_qcow" is returned a .qcow2 after it has been verified to exist-
        # this way we can call to launch an image that we don't actually have yet,
        # letting qemu.ensure_img() go fetch & prepare a fresh one
        launch_qcow = qemu.ensure_img(image)
        try:
            if sources.has_conf():
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

        # TODO: better to build kernel / ramdisk elsewhere then add generic aarch64 method
        # (see kernel.py for bits and whatnot on this)
        """
        if conf:
            if arg_true('use64'):
                print('launching 64 bit emulation ' + launch_qcow)
                subprocess.Popen(cls.construct_arm64_execute(qcow=launch_qcow),
                                 shell=True).wait()
                quit()
        """

        print('launching ARM 1176 emulation @ ' + launch_qcow)
        subprocess.Popen(cls.construct_arm1176_execute(qcow=launch_qcow),
                         shell=True).wait()
        quit()
