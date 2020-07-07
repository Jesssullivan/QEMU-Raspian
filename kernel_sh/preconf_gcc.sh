
#!/bin/bash
# @ https://github.com/Jesssullivan/clipi
# @ https://transscendsurvival.org/
#
# stuff needed to build & cross compile 64 bit kernel
# super great info @:
# tal.org/tutorials/raspberry-pi3-build-64-bit-kernel

# later gcc not yet tested to work, ymmv:
# echo -e "getting gcc @ 8.4.0...."
# wget https://ftp.gnu.org/gnu/gcc/gcc-8.4.0/gcc-8.4.0.tar.xz

# sticking with 6.4.0 for now w/ binutils @ 2.29.1
echo -e "getting gcc @ 6.4.0...."
wget https://ftp.gnu.org/gnu/gcc/gcc-6.4.0/gcc-6.4.0.tar.xz

# todo: plz make these directories not absolute
tar xf gcc-6.4.0.tar.xz
mkdir gcc-out
