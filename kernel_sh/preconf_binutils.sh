#!/bin/bash
# @ https://github.com/Jesssullivan/clipi
# @ https://transscendsurvival.org/
#
# stuff to build & cross compile 64 bit kernel
# super great info @:
# tal.org/tutorials/raspberry-pi3-build-64-bit-kernel

sudo mkdir /opt/aarch64
echo -e "getting binutils...."
wget https://ftp.gnu.org/gnu/binutils/binutils-2.34.tar.bz2

echo -e "completed attempt to fetch binutils, uncompressing...."
tar xf binutils-2.34.tar.bz2
mkdir binutils-obj
echo -e "all set preparing to make binutils @ /binutils-obj/..."
