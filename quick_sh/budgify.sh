#!/usr/bin/env bash

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] ERROR: User must be root, try again with sudo?"
  exit 1
fi

# Do the installation
HARDWARE_PACKAGES="libgles1 libopengl0 libxvmc1 pi-bluetooth libgpiod-dev python3-libgpiod python3-gpiozero"

echo -e "\nInstalling Budgie....\n"
apt install ubuntu-budgie-desktop -y
snap install ubuntu-budgie-welcome --classic

echo -e " \nInstalling hardware packages...\n"
apt install -y "${HARDWARE_PACKAGES}"

echo -e "finishing network config..."
  # Disable cloud-init from managing the network
echo "network: {config: disabled}" > /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg

cat <<EOM > /etc/netplan/01-network-manager-all.yaml
# Let NetworkManager manage all devices on this system
network:
  version: 2
  renderer: NetworkManager
EOM

# Disable Wifi Powersaving to improve Pi WiFi performance
if [ -e /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf ]; then
  sed -i 's/wifi.powersave = 3/wifi.powersave = 2/' /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf
fi
echo -e "Budgify script is done!\nxD"


sudo shutdown now