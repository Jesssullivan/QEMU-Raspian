#!/bin/bash

# run prior to multi-guest QEMU networking-
#
# brings UP virtual bridge br0 instead of default interface.
#
# device enp0s3 is default under VirtualBox NAT.  substitutes for ``` eth0 ```
#
# init.d - network-manager is default on ubuntu Budgie distro-
# ``` networking ``` is listed in kvm info

/etc/mach_init.d/network-manager restart

sleep 1

ip link add br0 type bridge

echo ' adding bridge br0 ...'

sleep 1

ip link set enp0s3 master br0

echo 'setting enp0s3 --> master bridge br0 ... '

sleep 1

echo ' complete '