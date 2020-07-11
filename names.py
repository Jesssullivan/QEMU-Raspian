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
names.py:
name & path handling
"""


class names(object):

    @classmethod
    def src_name(cls, img_text):
        return img_text.split('/')[-1]

    @classmethod
    def src_dir(cls, img_text):
        return str('image/' + cls.src_name(img_text)).split('.')[0]

    @classmethod
    def src_build(cls, img_text):  # /build/ is the destination used by arm64 when extracting kernel & ramdisk stuff
        return str('image/' + cls.src_name(img_text)).split('.')[0] + '/build/'

    @classmethod
    def src_kern(cls, img_text):
        return str('image/' + cls.src_name(img_text)).split('.')[0] + '/kern/'

    @classmethod
    def src_mnt(cls, img_text):  # /mnt/ is the mount point used by arm64 when extracting kernel & ramdisk stuff
        return str('image/' + cls.src_name(img_text)).split('.')[0] + '/mnt/'

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
        return False

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

