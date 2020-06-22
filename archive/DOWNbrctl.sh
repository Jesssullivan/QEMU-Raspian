#!/bin/bash

# run after close / to reset multi-guest QEMU networking-
#
# brings DOWN virtual bridge br0, replaces with default interface.
#
# init.d - network-manager is default on ubuntu Budgie distro-
# ``` networking ``` is listed in kvm info

/etc/mach_init.d/network-manager restart

sleep 1

ip link delete br0 type bridge

/etc/mach_init.d/network-manager restart

echo 'reconfiguring host network-manager ... '

sleep 1

echo ' complete '