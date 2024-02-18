import wifi

# Function to scan for DJI Tello's access points
def scan_for_tello_aps():
    # Scan for available WiFi networks
    networks = wifi.Cell.all('wlan0')

    # Filter networks to find DJI Tello's access points
    tello_aps = [network for network in networks if network.ssid.startswith("TELLO-")]

    # Print the SSIDs of DJI Tello's access points
    print("DJI Tello Access Points:")
    for ap in tello_aps:
        print(ap.ssid)

# Main function
def main():
    # Scan for DJI Tello's access points
    scan_for_tello_aps()

# Execute the main function
if __name__ == "__main__":
    main()

