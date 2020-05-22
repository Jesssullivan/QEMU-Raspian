*05/21/2020- completely rewritten w/ PyInquirer*
    
<br>
   
 ```shell script
# clone:
git clone https://github.com/Jesssullivan/QEMU-Raspian
cd QEMU-Raspian

# preheat:
pip install -r requirements.txt

# begin cooking some Pi:
python3 QEMU_Raspian.py
```

The general plan is to consolidate many more Raspberry Pi / Makerspace automation scripts into this convenient, shareable CLI layout with PyInquirer.

       
![Alt text](imgs.png?raw=true)
   
*if you just want some shell bits:*

```shell script
# make sure you've got qemu-arm and wget-
# for ubuntu:
sudo apt-get install qemu-system-arm -y
# or osx:
brew install qemu wget 

# snag the kernel bits:
wget https://raw.githubusercontent.com/dhruvvyas90/qemu-rpi-kernel/master/kernel-qemu-4.14.79-stretch -O kernel-qemu-4.14.79-stretch 
# (this one may take a while):
wget https://raw.githubusercontent.com/dhruvvyas90/qemu-rpi-kernel/master/versatile-pb.dtb -O versatile-pb.dtb

# get an image:
wget http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/2018-11-13-raspbian-stretch-lite.zip

# unzip the zipped image:
unzip "2018-11-13-raspbian-stretch-lite.zip" 

# convert to qcow for qemu goodness:
qemu-img convert -f raw -O qcow2 2018-11-13-raspbian-stretch-lite.img stretchlite.qcow2 && qemu-img resize stretchlite.qcow2 +8G

# launch from qcow:
qemu-system-arm -kernel kernel-qemu-4.14.79-stretch -cpu arm1176 -m 256 -M versatilepb -dtb versatile-pb.dtb -no-reboot -serial stdio -append "root=/dev/sda2 panic=1 rootfsrtype=ext4 rw" -hda stretchlite.qcow2
```

