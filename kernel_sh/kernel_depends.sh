#!/bin/bash
# @ https://github.com/Jesssullivan/clipi
# @ https://transscendsurvival.org/
#
# stuff needed to build & cross compile 64 bit kernel
# super great info @:
# tal.org/tutorials/raspberry-pi3-build-64-bit-kernel

echo -e "installing build & cross compile lib depends w/ apt-get...."
apt-get install build-essential libgmp-dev libmpfr-dev libmpc-dev libisl-dev -y
apt-get install libncurses5-dev bc git-core bison flex -y
echo -e "\n double-checking texinfo install before make binutils... \n"
apt-get install texinfo -y
echo -e "\n double-checking gcc-aarch64-linux-gnu... \n"
apt-get install gcc-aarch64-linux-gnu -y
echo -e "\n double-checking libguestfs-tools for guestfish... \n"
apt install libguestfs-tools

echo -e "all set with depends..."



