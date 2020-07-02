
#!/bin/bash
# @ https://github.com/Jesssullivan/clipi
# @ https://transscendsurvival.org/
#
# stuff needed to build & cross compile 64 bit kernel
# super great info @:
# tal.org/tutorials/raspberry-pi3-build-64-bit-kernel

echo -e "getting gcc @ 8.4.0...."
wget https://ftp.gnu.org/gnu/gcc/gcc-8.4.0/gcc-8.4.0.tar.xz
tar xf gcc-8.4.0.tar.xz
mkdir gcc-out
