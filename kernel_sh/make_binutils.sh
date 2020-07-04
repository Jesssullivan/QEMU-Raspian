#!/bin/bash
# @ https://github.com/Jesssullivan/clipi
# @ https://transscendsurvival.org/
#
# stuff needed to build & cross compile 64 bit kernel
# super great info from:
# tal.org/tutorials/raspberry-pi3-build-64-bit-kernel

# this file is copied to binutils-obj by kernel.py

../binutils-2.34/configure --prefix=/opt/aarch64 --target=aarch64-linux-gnu --disable-nls
make -j4
sudo make install
export PATH=$PATH:/opt/aarch64/bin/
