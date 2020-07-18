#!/bin/bash
# a WIP by Jess Sullivan
# @ https://github.com/Jesssullivan/clipi
# @ https://transscendsurvival.org/

ip tuntap add tap0 mode tap
ip link add br0 type bridge
brctl addif br0 tap0
ifconfig br0 up
echo done