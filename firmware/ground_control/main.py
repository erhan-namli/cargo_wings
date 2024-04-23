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

    def connect_tello_ap(self):

        run_shell_script("connect_tello.sh")

    def connect_homenetwork(self):

        run_shell_script("connect_homenetwork.sh")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
