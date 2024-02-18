import subprocess
import time

def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode(), error.decode()

def configure_adhoc_network(interface, ssid, ip_address, netmask):
    # Set interface to ad-hoc mode
    execute_command(f"sudo iw dev {interface} set type ibss")

    # Set IP address and netmask
    execute_command(f"sudo ip addr add {ip_address}/{netmask} dev {interface}")

    # Bring up the interface
    execute_command(f"sudo ip link set {interface} up")

    # Create ad-hoc network
    execute_command(f"sudo iw dev {interface} ibss join {ssid} {frequency}")

    # Restart DHCP service (optional)
    execute_command("sudo systemctl restart dnsmasq")

if __name__ == "__main__":
    wlan_interface = "wlan0"
    adhoc_ssid = "MyAdHocNetwork"
    adhoc_ip_address = "192.168.1.1"
    adhoc_netmask = "255.255.255.0"
    frequency = "2.4GHz"  # You can change this to match your Wi-Fi dongle's frequency band

    print("Configuring ad-hoc network...")
    configure_adhoc_network(wlan_interface, adhoc_ssid, adhoc_ip_address, adhoc_netmask)
    print("Ad-hoc network configured.")

