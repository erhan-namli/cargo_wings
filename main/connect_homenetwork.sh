#!/bin/bash

# Restarting the network manager
sudo systemctl restart networking

# Obtain an IP address using DHCP
echo "Obtaining an IP address using DHCP..."
sudo dhclient wlan0

echo "Connected to homenetwork_plus."
