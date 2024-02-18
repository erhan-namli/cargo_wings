import os

def disconnect_wifi():
    try:
        # Execute the command to disconnect from the current WiFi network
        os.system('sudo nmcli dev disconnect wlan0')
        print("Disconnected from the current WiFi network.")
    except Exception as e:
        print("An error occurred while disconnecting:", e)

def change_wifi():
    try:
        # Disconnect from the current WiFi network
        disconnect_wifi()
        
        # Connect to the new WiFi network
        os.system('sudo nmcli dev wifi connect TELLO-B5997E password ""')

        print("Connected to the WiFi network TELLO-B5997E.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    change_wifi()

