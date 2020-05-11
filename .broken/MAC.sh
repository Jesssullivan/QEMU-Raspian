#!/bin/bash
#
# generate random MAC address
# new mac address is echo'd --> stdout PIPE for QEMU_Raspian.py

hexchars="0123456789ABCDEF"

end=$( for i in {1..6} ; do echo -n ${hexchars:$(( $RANDOM % 16 )):1} ; done | sed -e 's/\(..\)/:\1/g' )

echo 00:60:2F$end
