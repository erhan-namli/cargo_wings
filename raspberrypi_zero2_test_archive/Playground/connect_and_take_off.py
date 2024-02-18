import time 
import wifi
from tellopy import Tello

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
        return None

    # Get the strongest Tello access point
    strongest_ap = tello_aps[0]
    print("Connecting to {}...".format(strongest_ap.ssid))

    # Check if a connection profile for the Tello's WiFi network already exists
    existing_profile = wifi.Scheme.find('wlan0', strongest_ap.ssid)
    if existing_profile:
        print("A connection profile for {} already exists.".format(strongest_ap.ssid))
        return strongest_ap

    # Connect to the strongest Tello access point
    try:
        wifi.Scheme.for_cell('wlan0', strongest_ap.ssid, strongest_ap).save()
        time.sleep(5)  # Wait for the connection to establish
        print("Connected to Tello's WiFi network.")
        return strongest_ap
    except Exception as e:
        print("Failed to connect:", e)
        return None

# Function to connect to Tello, take off, wait, and land
def perform_flight():
    # Connect to the strongest Tello access point
    tello_ap = connect_to_strongest_tello_ap()

    if not tello_ap:
        print("Connection to Tello failed.")
        return

    # Connect to Tello
    drone = Tello()

    try:
        drone.connect()
    except Exception as e:
        print("Failed to connect to Tello:", e)
        return

    # Take off
    try:
        drone.takeoff()
        print("Tello has taken off.")
    except Exception as e:
        print("Failed to take off:", e)
        return

    # Wait for 5 seconds
    time.sleep(10)

    # Land
    try:
        drone.land()
        print("Tello has landed.")
    except Exception as e:
        print("Failed to land:", e)
        return

    # Disconnect from Tello
    try:
        drone.quit()
        print("Disconnected from Tello.")
    except Exception as e:
        print("Failed to disconnect from Tello:", e)

# Main function
def main():
    # Perform the flight operation
    perform_flight()

# Execute the main function
if __name__ == "__main__":
    main()
