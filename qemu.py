#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

from common import *

"""
qemu.py:
controls various qemu-system functions
"""


class qemu(object):

    @classmethod
    def construct_arm1176_execute(cls,
                               bin='bin/kernel-qemu-4.14.79-stretch',
                               qcow=''):
        cmd = str("qemu-system-aarch64 -kernel " + bin +
                  " -cpu arm1176 -m 256 -M versatilepb -dtb bin/versatile-pb.dtb -no-reboot -serial stdio -append " +
                  '"root=/dev/sda2 panic=1 rootfsrtype=ext4 rw" -hda ' +
                  qcow)
        return cmd

    @classmethod
    def construct_arm64_execute(cls, qcow=''):
        cmd = str("qemu-system-aarch64 -M virt -m 2048 -cpu cortex-a53 " + \
                  "-kernel bin/installer-linux -initrd bin/installer-initrd.gz " +
                  "-no-reboot -serial stdio -append " +
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

        for x in range(10):

            if os.path.isfile(names.src_qcow(image)):
                return names.src_qcow(image)

            if not os.path.exists(names.src_dir(image)):
                os.mkdir(names.src_dir(image))

            if not os.path.exists(names.src_dir(image)):
                os.mkdir(names.src_dir(image))

            if not os.path.isfile(image):
                subprocess.Popen(str('wget -O ' + names.src_local(image) + ' ' + image),
                                 shell=True).wait()
                sleep(.25)

            if os.path.isfile(names.src_img(image)):
                subprocess.Popen(cls.construct_qemu_convert(img=names.src_img(image),
                                                            qcow=names.src_qcow(image)),
                                 shell=True).wait()
                sleep(.25)
                cls.do_qemu_expand(names.src_qcow(image))

            if os.path.isfile(names.src_zip(image)):
                unzip(names.src_zip(image), names.src_dir(image))

            if os.path.isfile(names.src_7z(image)):
                print('unzipping')
                unzip(names.src_7z(image), names.src_dir(image))

        return names.src_qcow(image)

    @classmethod
    def launch(cls, image):
        main_install()
        ensure_bins()
        launch_qcow = cls.ensure_img(image)
        subprocess.Popen(cls.construct_arm1176_execute(qcow=launch_qcow),
                         shell=True).wait()

