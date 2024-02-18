import subprocess

def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode(), error.decode()

def configure_adhoc_network(interface, ssid, ip_address, netmask):
    # Set up ad-hoc network configuration
    config = f"""
    auto {interface}
    iface {interface} inet static
        address {ip_address}
        netmask {netmask}
        wireless-mode ad-hoc
        wireless-essid {ssid}
    """

    # Write configuration to /etc/network/interfaces
    with open("/etc/network/interfaces", "a") as file:
        file.write(config)

    # Restart networking service
    execute_command("sudo systemctl restart networking")

if __name__ == "__main__":
    wlan_interface = "wlan0"
    adhoc_ssid = "MyAdHocNetwork"
    adhoc_ip_address = "192.168.1.1"
    adhoc_netmask = "255.255.255.0"

    print("Configuring ad-hoc network...")
    configure_adhoc_network(wlan_interface, adhoc_ssid, adhoc_ip_address, adhoc_netmask)
    print("Ad-hoc network configured.")

