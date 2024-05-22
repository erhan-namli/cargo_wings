#!/bin/bash

sudo ifconfig wlan0 down
sleep 1 # making the computer wait for a second
wpa_cli terminate
sleep 1
# Disable ad-hoc mode
sudo iwconfig wlan0 mode managed

# Connect to the "TELLO-B5997E" SSID
sudo iwconfig wlan0 essid "TELLO-FE1FB2"
sudo dhclient wlan0

echo "Connected to TELLO-FE1FB2 SSID."
