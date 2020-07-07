#!/bin/bash
# @ https://github.com/Jesssullivan/clipi
# @ https://transscendsurvival.org/
#
# stuff to build & cross compile 64 bit kernel
# super great info from:
# tal.org/tutorials/raspberry-pi3-build-64-bit-kernel

# this file is copied to gcc-out by kernel.py

../gcc-6.4.0/configure --prefix=/opt/aarch64 --target=aarch64-linux-gnu --with-newlib --without-headers \
 --disable-nls --disable-shared --disable-threads --disable-libssp --disable-decimal-float \
 --disable-libquadmath --disable-libvtv --disable-libgomp --disable-libatomic \
 --enable-languages=c

make all-gcc -j4
sudo make install-gcc