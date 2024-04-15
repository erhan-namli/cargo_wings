import subprocess
import json
import time
import socket
from lightdjitellopy import Tello

def run_shell_script(script_name):
    try:
        subprocess.run(['./{}'.format(script_name)], shell=True, check=True)
        print("Successfully ran {}".format(script_name))
    except subprocess.CalledProcessError as e:
        print("Error running {}: {}".format(script_name, e))

def send_json_packet(ip_address, json_data):
    # Convert dictionary to JSON string
    json_string = json.dumps(json_data)
    # Send JSON packet to specified IP address using UDP
    udp_ip = ip_address
    udp_port = 5005  # Choose a suitable port
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json_string.encode(), (udp_ip, udp_port))
        print("Sent JSON packet to {}: {}".format(ip_address, json_string))
    except Exception as e:
        print("Error sending JSON packet: {}".format(e))
    finally:
        sock.close()
 
def take_off_and_land():
    try:
        tello = Tello()
        tello.connect()
        tello.takeoff()
        print("Tello has taken off")
        time.sleep(4)  # Wait for 4 seconds
        tello.land()
        print("Tello has landed")
        tello.end()
    except Exception as e:
        print("Error during Tello operation: {}".format(e))

def main():
    # Run start_adhoc.sh
    run_shell_script("start_adhoc.sh")
    # Send JSON packet to 192.168.1.3
    ip_address = "192.168.1.3"
    send_json_packet(ip_address, {"message": "Dummy message"})
    # Wait for 5 seconds
    print("Waiting for 5 seconds...")
    time.sleep(5)
    # Run connect_tello.sh
    run_shell_script("connect_tello.sh")
    # Perform takeoff and landing with Tello drone
    take_off_and_land()

if __name__ == "__main__":
    main()
