#!/bin/bash
#Change Wifi into AdHoc mode

sudo ifconfig wlan0 down
sleep 1 # making the computer wait for a second
wpa_cli terminate
sleep 1
sudo iwconfig wlan0 mode ad-hoc
sleep 1
sudo iwconfig wlan0 essid RPiAdHoc
sleep 1
sudo iwconfig wlan0 key off
sleep 1
sudo iwconfig wlan0 channel 1
sleep 1

#Set IP Address on RPi

sudo ifconfig wlan0 up
sudo ifconfig wlan0 192.168.1.5 ## Agent 1 IP
