#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

from common import *
from common import common as com

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
    def src_img(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.')[0] + '.img')

    @classmethod
    def src_zip(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.')[0] + '.zip')

    @classmethod
    def src_7z(cls, img_text):
        return str(names.src_dir(img_text) + '/' + names.src_name(img_text).split('.')[0] + '.7z')

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
