#!/bin/bash
# a WIP by Jess Sullivan
# @ https://github.com/Jesssullivan/clipi
# @ https://transscendsurvival.org/
#
# permiss & run:
# sudo chmod u+x virt.sh
# ./virt.sh

# brctl addbr br0
read IPETH0 <<< $(ip -o link | awk '$2 != "lo:" {print $2}')
echo ${IPETH0//:}

# sep tap0:
ip link add br0 type bridge
ifconfig br0 up
sudo tunctl -u $(whoami)
sudo brctl addif br0 tap1
sudo ip link set dev br0 up
sudo ip link set dev tap0 up

# start dhclient:
echo -e "staring dhclient..."
sudo dhclient br0

echo done