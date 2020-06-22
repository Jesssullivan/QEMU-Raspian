#!/bin/sh

# host networking depends:
#
# TODO: script ``` interfaces ``` & ``` qemu-ifup ```replacement files for host
#
# run as admin prior to host network configuration

apt install bridge-utils -y

sleep .5

apt install uml-utilities -y

sleep .5

ip link add br0 type bridge  # possiply redundant to UP script

sleep .5

echo 'finished public bridge br0 setup'