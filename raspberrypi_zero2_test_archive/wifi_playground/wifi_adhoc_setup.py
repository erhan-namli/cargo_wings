import subprocess
import time

def run_command(command):
    subprocess.run(command.split())

def main():
    # Change Wifi into AdHoc mode
    run_command("sudo ifconfig wlan0 down")
    time.sleep(0.5)
    run_command("wpa_cli terminate")
    time.sleep(0.5)
    run_command("sudo iwconfig wlan0 mode ad-hoc")
    time.sleep(1)
    run_command("sudo iwconfig wlan0 essid RPiAdHoc")
    time.sleep(0.5)
    run_command("sudo iwconfig wlan0 key off")
    time.sleep(0.5)
    run_command("sudo iwconfig wlan0 channel 1")
    time.sleep(0.5)

    # Set IP Address on RPi
    run_command("sudo ifconfig wlan0 up")
    run_command("sudo ifconfig wlan0 192.168.1.2")

if __name__ == "__main__":
    main()


