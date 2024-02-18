import subprocess
import time
from lightdjitellopy import Tello

def is_connected_to_tello():
    # Check if connected to Tello by scanning available WiFi networks
    result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True)
    return "TELLO" in result.stdout

def disconnect_wifi():
    try:
        # Execute the command to disconnect from the current WiFi network
        subprocess.run(['sudo', 'nmcli', 'dev', 'disconnect', 'wlan0'])
        print("Disconnected from the current WiFi network.")
    except Exception as e:
        print("An error occurred while disconnecting:", e)

def change_wifi():
    try:
        # Disconnect from the current WiFi network if connected
        if not is_connected_to_tello():
            disconnect_wifi()
        
        # Connect to the new WiFi network
        subprocess.run(['sudo', 'nmcli', 'dev', 'wifi', 'connect', 'TELLO-B5997E', 'password', '""'])

        print("Connected to the WiFi network TELLO-B5997E.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    change_wifi()
    
    # Send forward command
    try:
        tello = Tello()
        tello.connect()
        tello.takeoff()
        tello.move_forward(100)
        tello.land()
        tello.closeSocket()
        tello.end()
    except Exception as e:
        print("An error occurred while sending command to Tello:", e)

