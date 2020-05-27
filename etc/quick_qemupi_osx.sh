#
# a simplified shell script to launch small Raspberry Pi emulations w/ qemu
# uses package manager brew for osx
# @ https://github.com/Jesssullivan/clipi
# @ https://transscendsurvival.org/
#
# permiss & run:
# sudo chmod u+x quick_qemupi_osx.sh
# ./quick_qemupi_osx.sh
#
# Note, the arm1176 cpu + 256 memory are derivative of the older versatile-pb.dtb used here.
#
# It is probably a good idea to just jump to aarch64 sooner than later xD

# please make sure you have brew, if not get it like this:
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

# for osx:
brew install qemu-system-arm
brew install wget

# snag the kernel bits:
wget https://github.com/Jesssullivan/clipi/raw/master/bin/kernel-qemu-4.14.79-stretch

# (this one may take a while):
wget https://github.com/Jesssullivan/clipi/raw/master/bin/versatile-pb.dtb

# get an image:
wget http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-04-09/2019-04-08-raspbian-stretch.zip

# unzip the zip:
unzip "2019-04-08-raspbian-stretch.zip"

# convert to qcow for qemu goodness:
qemu-img convert -f raw -O qcow2 2019-04-08-raspbian-stretch.img stretch.qcow2 && qemu-img resize stretch.qcow2 +8G

# launch from qcow:
qemu-system-arm -kernel kernel-qemu-4.14.79-stretch -cpu arm1176 -m 256 -M versatilepb -dtb versatile-pb.dtb -no-reboot -serial stdio -append "root=/dev/sda2 panic=1 rootfsrtype=ext4 rw" -hda stretch.qcow2
