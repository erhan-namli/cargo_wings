import subprocess
import json
import time
import socket
import datetime
from lightdjitellopy import Tello

class State:
    WAITING_FOR_MESSAGE = 0
    WAITING_FOR_MISSION_START = 1
    MISSION_IN_PROGRESS = 2

class DroneController:
    def __init__(self):
        self.state = State.WAITING_FOR_MESSAGE
        self.mission_matrix = None
        self.drone_ip_address = "192.168.1.3"

    def run_shell_script(self, script_name):
        try:
            subprocess.run(['./{}'.format(script_name)], shell=True, check=True)
            print("Successfully ran {}".format(script_name))
        except subprocess.CalledProcessError as e:
            print("Error running {}: {}".format(script_name, e))

    def send_json_packet(self, ip_address, json_data):
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

    def wait_message(self):
        UDP_IP = '192.168.1.255'
        UDP_PORT = 5005
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))

        while True:
            msg, addr = sock.recvfrom(1024)
            now = datetime.datetime.now()
            print('Time:', now, 'RECV', msg.decode())
            rcvd_msg = f'Time: {now} RECV {msg.decode()}'

            # Parse incoming message and update mission matrix
            self.parse_incoming_message(msg.decode())

            # Check if the message contains a "command" key and its value is "run"
            if "command" in msg and msg["command"] == "start":
                self.state = State.WAITING_FOR_MISSION_START
                break

            if self.mission_matrix:
                break

    def parse_incoming_message(self, json_data):
        try:
            data = json.loads(json_data)
            self.mission_matrix = data.get("mission_matrix")

            if self.mission_matrix:
                # Update self.mission_matrix with the incoming matrix
                self.mission_matrix = self.mission_matrix
                print("Updated mission matrix:", self.mission_matrix)

            else:
                print("No mission matrix found in the incoming message.")
        except json.JSONDecodeError as e:
            print("Error parsing incoming JSON message:", e)

    def main(self):
        # Run start_adhoc.sh
        self.run_shell_script("start_adhoc.sh")

        self.send_json_packet("192.168.1.255", {"message_type": "status_information",
                                                "command": "none",
                                                "least_cost_mission": "None",
                                                "ip_address": self.drone_ip_address,
                                                "status": "WAITING",
                                                "traffic": "broadcast"})

        while True:
            if self.state == State.WAITING_FOR_MESSAGE:
                print("Waiting for a message...")
                self.wait_message()
                self.state = State.WAITING_FOR_MISSION_START

            elif self.state == State.WAITING_FOR_MISSION_START:

                print(self.mission_matrix)

                # Define starting position
                start_x = 0
                start_y = 0
                # Define movement distance
                distance = 20  # 10 cm between each row and column index
                # Save starting position
                current_x = start_x
                current_y = start_y
                # Loop through the mission_matrix
                battery_level = 70
                current_state = (current_x, current_y)

                cost_matrix = self.calculate_cost_matrix(self.mission_matrix, current_state, battery_level)

                least_cost_mission = self.find_least_cost_mission(cost_matrix)

                print("least cost missions position", least_cost_mission)

                self.send_json_packet("192.168.1.255", {"message_type": "drone_mission_information",
                                                        "least_cost_mission": least_cost_mission,
                                                        "ip_address": self.drone_ip_address,
                                                        "status": "WAITING",
                                                        "traffic": "broadcast"})

                self.state = State.MISSION_IN_PROGRESS

            elif self.state == State.MISSION_IN_PROGRESS:
                # Waiting for mission start message
                self.wait_message()  ## if the message comes from ground and says start_mission start to fly and do the job

                print(self.mission_matrix)

                print("MISSION HAS STARTED")
                break  # End the loop after mission is completed

    def calculate_cost_matrix(self, mission_matrix, current_state, battery_level):
        rows = len(mission_matrix)
        cols = len(mission_matrix[0])
        cost_matrix = [[0] * cols for _ in range(rows)]

        current_x, current_y = current_state
        max_cost = 2 * (rows + cols)  # Maximum possible cost

        for i in range(rows):
            for j in range(cols):
                if mission_matrix[i][j] == 1:
                    # Calculate cost based on Manhattan distance from current state to mission location
                    cost = abs(i - current_y) + abs(j - current_x)
                    normalized_cost = self.normalize_cost(cost, max_cost)
                    # Adjust normalized cost based on battery level
                    adjusted_cost = normalized_cost + (1 - normalized_cost) * (1 - battery_level / 100)
                    # Limit the number of decimal places
                    adjusted_cost = round(adjusted_cost, 4)
                    cost_matrix[i][j] = adjusted_cost
                else:
                    # Set a high cost for locations where no mission is assigned
                    cost_matrix[i][j] = float('inf')

        return cost_matrix

    def normalize_cost(self, cost, max_cost):
        # Normalize cost between 0 and 1
        return round(cost / max_cost, 4)  # Limit to 4 decimal places

    def find_least_cost_mission(self, cost_matrix):
        min_cost = float('inf')
        min_i, min_j = -1, -1

        for i in range(len(cost_matrix)):
            for j in range(len(cost_matrix[0])):
                if cost_matrix[i][j] < min_cost:
                    min_cost = cost_matrix[i][j]
                    min_i, min_j = i, j

        return min_i, min_j

if __name__ == "__main__":
    controller = DroneController()
    controller.main()
