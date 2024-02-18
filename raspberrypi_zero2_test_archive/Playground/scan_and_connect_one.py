import wifi
import time

# SSID prefix of the DJI Tello's WiFi network
tello_ssid_prefix = "TELLO-"

# Function to scan for DJI Tello's access points
def scan_for_tello_aps():
    # Scan for available WiFi networks
    networks = wifi.Cell.all('wlan0')

    # Filter networks to find DJI Tello's access points
    tello_aps = [network for network in networks if network.ssid.startswith(tello_ssid_prefix)]

    # Sort the Tello access points based on signal strength (strongest first)
    tello_aps.sort(key=lambda x: x.signal, reverse=True)

    return tello_aps

# Function to connect to the strongest Tello access point
def connect_to_strongest_tello_ap():
    # Scan for DJI Tello's access points
    tello_aps = scan_for_tello_aps()

    if not tello_aps:
        print("No DJI Tello access points found.")
        return False

    # Get the strongest Tello access point
    strongest_ap = tello_aps[0]
    print(f"Connecting to {strongest_ap.ssid}...")

    # Connect to the strongest Tello access point
    try:
        wifi.Scheme.for_cell('wlan0', strongest_ap.ssid, strongest_ap).save()
        time.sleep(2)  # Wait for the connection to establish
        print("Connected to Tello's WiFi network.")
        return True
    except Exception as e:
        print("Failed to connect:", e)
        return False

# Main function
def main():
    # Connect to the strongest Tello access point
    connected = connect_to_strongest_tello_ap()

    if connected:
        print("Connection successful!")
    else:
        print("Connection failed.")

# Execute the main function
if __name__ == "__main__":
    main()

