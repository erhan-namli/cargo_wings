import sys

sys.path.append('/home/erhan/.local/lib/python3.9/site-packages')

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from cargo_wings_ui import Ui_MainWindow
import subprocess
import json
import time
import socket
from djitellopy import Tello
import cv2
from pyzbar.pyzbar import decode
import threading
import socket
import datetime

TELLO_SCRIPT_MAPPING = {
    1: "connect_tello1.sh",
    2: "connect_tello2.sh",
    3: "connect_tello3.sh"
}


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
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(json_string.encode(), (udp_ip, udp_port))

        print("Sent JSON packet to {}: {}".format(ip_address, json_string))
    except Exception as e:
        print("Error sending JSON packet: {}".format(e))
    finally:
        sock.close()


def listen_for_drone_messages(callback):
    UDP_IP = '0.0.0.0'
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind((UDP_IP, UDP_PORT))

    mission_matrix = None  # Initialize mission_matrix here

    print("Thread started")

    while True:
        msg, addr = sock.recvfrom(1024)
        now = datetime.datetime.now()
        msg_str = msg.decode()  # Decode the bytes-like object into a string
        print('Time:', now, 'RECV', msg_str)
        rcvd_msg = f'Time: {now} RECV {msg_str}'

        # Check if the message contains a "command" key and its value is "start"
        try:
            msg_json = json.loads(msg_str)

            print(msg_json["message_type"])

            if msg_json["message_type"] == "drone_mission_information":
                callback(msg_json)

        except json.JSONDecodeError as e:
            print("Error decoding JSON message:", e)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.mission_matrix = []

        self.ui.btn_take_picture.clicked.connect(self.take_picture_and_scan_qr_code)

        self.ui.btn_connect_tello_ap.clicked.connect(self.connect_tello_ap)

        self.ui.btn_connect_homenetwork.clicked.connect(self.connect_homenetwork)

        self.ui.btn_start_adhoc.clicked.connect(self.start_adhoc)

        self.ui.btn_adhoc_mission.clicked.connect(self.adhoc_mission)

        self.ui.btn_start_mission.clicked.connect(self.start_mission)

        self.ui.btn_scan_drones.clicked.connect(self.start_scanning_drones)

        threading.Thread(target=listen_for_drone_messages, args=(self.handle_drone_message,), daemon=True).start()

    def start_scanning_drones(self):

        try:
            # Interface name might be different, common ones are 'wlan0' or 'eth0', check your system
            interface_name = 'wlan0'
            
            # Run the `iwlist` command to scan for networks
            result = subprocess.run(
                ['sudo', 'iwlist', interface_name, 'scan'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                # Parse the output to find SSIDs
                lines = result.stdout.split('\n')
                tello_ssids = []
                for line in lines:
                    if "ESSID:" in line:
                        ssid = line.split('"')[1]  # Extract SSID name
                        if ssid.startswith('TELLO'):
                            tello_ssids.append(ssid)
                
                if tello_ssids:
                    self.ui.drone_list_widget.addItems(tello_ssids)
                    print("Found TELLO networks:")
                    for ssid in tello_ssids:
                        print(ssid)
                    # Optionally update a list widget or another UI element
                else:
                    print("No TELLO networks found.")
            else:
                print("Error scanning for Wi-Fi networks:", result.stderr)

        except Exception as e:
            print("An error occurred while scanning Wi-Fi networks:", e)

    def handle_drone_message(self, message):
        # Handle received message from drone
        print("buraya geldi...")
        #print("Mission completed by drone at tello name:", message["tello_name"])
        # Perform QR code check

        ## Connect to tello

        print("debug_erhan " , message['least_cost_mission'])

        mission_location = message['least_cost_mission']

        if(mission_location == [0, 0]):
            self.ui.rb_00.setChecked(True)
        if(mission_location == [0, 1]):
            self.ui.rb_01.setChecked(True)
        if(mission_location == [0, 2]):
            self.ui.rb_02.setChecked(True)
        if(mission_location == [1, 0]):
            self.ui.rb_10.setChecked(True)
        if(mission_location == [1, 1]):
            self.ui.rb_11.setChecked(True)
        if(mission_location == [1, 2]):
            self.ui.rb_12.setChecked(True)
        if(mission_location == [2, 0]):
            self.ui.rb_20.setChecked(True)
        if(mission_location == [2, 1]):
            self.ui.rb_21.setChecked(True)
        if(mission_location == [2, 2]):
            self.ui.rb_22.setChecked(True)
        if(mission_location == [3, 0]):
            self.ui.rb_30.setChecked(True)
        if(mission_location == [3, 1]):
            self.ui.rb_31.setChecked(True)
        if(mission_location == [3, 2]):
            self.ui.rb_32.setChecked(True)

        #if(message["tello_name"] == "TELLO-B5997E"):

            #connect_tello_ap(1)

        #elif(message["tello_name"] == "TELLO-5CF682"):

            #connect_tello_ap(2)

        ## Take picture and scan_qr_code

        #self.take_picture_and_scan_qr_code()

    def start_mission(self):

        ip_address = "192.168.1.255"
        send_json_packet(ip_address, {"message_type": "ground_start_mission_information",
                                      "mission_matrix": self.mission_matrix,
                                      "command": "start",
                                      "traffic": "broadcast"})

                                      
    def adhoc_mission(self):

        self.mission_matrix = [[int(self.ui.btn_qr1.isChecked()),
                               int(self.ui.btn_qr2.isChecked()),
                               int(self.ui.btn_qr3.isChecked())],
                               [int(self.ui.btn_qr4.isChecked()),
                                int(self.ui.btn_qr5.isChecked()),
                                int(self.ui.btn_qr6.isChecked())],
                               [int(self.ui.btn_qr7.isChecked()),
                                int(self.ui.btn_qr8.isChecked()),
                                int(self.ui.btn_qr9.isChecked())],
                               [int(self.ui.btn_qr10.isChecked()),
                                int(self.ui.btn_qr11.isChecked()),
                                int(self.ui.btn_qr12.isChecked())]
                               ]

        ip_address = "192.168.1.255"

        send_json_packet(ip_address, {"mission_matrix": self.mission_matrix,
                                      "message_type" :"info",
                                      "command": "wait"})



    def send_json_packet(ip_address, json_data):
        # Convert dictionary to JSON string
        json_string = json.dumps(json_data)
        # Send JSON packet to specified IP address using UDP
        udp_ip = ip_address
        udp_port = 5005  # Choose a suitable port
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable
            sock.sendto(json_string.encode(), (udp_ip, udp_port))
            print("Sent JSON packet to {}: {}".format(ip_address, json_string))
        except Exception as e:
            print("Error sending JSON packet: {}".format(e))
        finally:
            sock.close()
    def start_adhoc(self):

        run_shell_script("start_adhoc.sh")

        pass


    def take_picture(self):

        pass

    def take_picture_and_scan_qr_code(self):

        # Print message when the button is clicked
        tello = Tello()
        tello.connect()
        tello.streamon()

        # Adjust this value as needed
        num_frames = 1  # Number of frames to capture

        # Open the video stream
        vidcap = cv2.VideoCapture(tello.get_udp_video_address())

        # Loop through frames
        for count in range(num_frames):
            success, frame = vidcap.read()
            if success:

                # Decode QR codes
                decoded_objects = decode(frame)

                if decoded_objects:
                    # QR codes found, print their data
                    for obj in decoded_objects:
                        print("Data:", obj.data.decode('utf-8'))
                        print("Type:", obj.type)
                        print()
                else:
                    print("No QR codes found in the frame.")

                cv2.imwrite("frame_%d.jpg" % count, frame)

            else:
                print('Failed to capture frame %d' % count)

        # Release resources
        tello.streamoff()
        vidcap.release()

    def connect_tello_ap(self, tello_number):

        if(tello_number==1):

            run_shell_script("connect_tello.sh")

        elif(tello_number==2):

            run_shell_script("connect_tello2.sh")

        elif(tello_number==3):

            run_shell_script("connect_tello3.sh")

    def connect_homenetwork(self):

        run_shell_script("connect_homenetwork.sh")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
