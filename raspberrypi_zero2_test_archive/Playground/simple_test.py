import tellopy
import time
from wifi import Cell, Scheme

def find_tello():
    for cell in Cell.all('wlan0'):
        if cell.ssid == 'TELLO':
            return cell
    return None

import tellopy
import time
from wifi import Cell, Scheme

def find_tello():
    for cell in Cell.all('wlan0'):
        if 'Tello' in cell.ssid:
            return cell
    return None

def main():
    tello_wifi = find_tello()
    if not tello_wifi:
        print("Tello not found in WiFi network")
        return

    drone = tellopy.Tello()
    try:
        drone.connect(tello_wifi.ssid)
        drone.wait_for_connection(10.0)
        print("Connected to Tello")

        drone.takeoff()
        print("Taking off...")
        time.sleep(3)  # You can adjust the duration here
        print("Landing...")
        drone.land()

    except Exception as ex:
        print(ex)
    finally:
        drone.quit()

if __name__ == "__main__":
    main()


