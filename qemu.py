#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

from common import *
from names import names

# import threading

"""
qemu.py:
controls various qemu-system functions
"""


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
                  ' "root=/dev/sda2 panic=1 rootfsrtype=ext4 rw" -hda ' +
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

        for x in range(10):
            try:
                if not os.path.exists(names.src_dir(image)):
                    os.mkdir(names.src_dir(image))

                if not names.any_qcow(image) is None:
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
            except:
                pass

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

        if common.arg_true(dic=xargs, arg='use64'):
            subprocess.Popen(cls.construct_arm64_execute(qcow=launch_qcow),
                             shell=True).wait()
        else:
            subprocess.Popen(cls.construct_arm1176_execute(qcow=launch_qcow),
                             shell=True).wait()
