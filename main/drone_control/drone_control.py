import sys

sys.path.append('/home/erhan/.local/lib/python3.9/site-packages')

import subprocess
import json
import time
import socket
import datetime

class State:
    WAITING_FOR_MESSAGE = 0
    WAITING_FOR_MISSION_START = 1
    MISSION_IN_PROGRESS = 2

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

def wait_message():
    UDP_IP = '192.168.1.255'
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    mission_matrix = None  # Initialize mission_matrix here

    while True:
        msg, addr = sock.recvfrom(1024)
        now = datetime.datetime.now()
        msg_str = msg.decode()  # Decode the bytes-like object into a string
        print('Time:', now, 'RECV', msg_str)
        rcvd_msg = f'Time: {now} RECV {msg_str}'

        # Parse incoming message and update mission matrix
        mission_matrix = parse_incoming_message(msg_str)

        # Check if the message contains a "command" key and its value is "run"
        try:
            msg_json = json.loads(msg_str)
            if "command" in msg_json and msg_json["command"] == "start":
                return State.WAITING_FOR_MISSION_START, mission_matrix
        except json.JSONDecodeError as e:
            print("Error decoding JSON message:", e)

        if mission_matrix:
            break

    return State.WAITING_FOR_MESSAGE, mission_matrix


def parse_incoming_message(json_data):
    global mission_matrix
    try:
        data = json.loads(json_data)
        mission_matrix = data.get("mission_matrix")

        if mission_matrix:
            # Update mission_matrix with the incoming matrix
            mission_matrix = mission_matrix
            print("Updated mission matrix:", mission_matrix)

            return mission_matrix

        else:
            print("No mission matrix found in the incoming message.")
    except json.JSONDecodeError as e:
        print("Error parsing incoming JSON message:", e)



def calculate_cost_matrix(mission_matrix, current_state, battery_level):
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
                normalized_cost = normalize_cost(cost, max_cost)
                # Adjust normalized cost based on battery level
                adjusted_cost = normalized_cost + (1 - normalized_cost) * (1 - battery_level / 100)
                # Limit the number of decimal places
                adjusted_cost = round(adjusted_cost, 4)
                cost_matrix[i][j] = adjusted_cost
            else:
                # Set a high cost for locations where no mission is assigned
                cost_matrix[i][j] = float('inf')

    return cost_matrix

def normalize_cost(cost, max_cost):
    # Normalize cost between 0 and 1
    return round(cost / max_cost, 4)  # Limit to 4 decimal places

def find_least_cost_mission(cost_matrix):
    min_cost = float('inf')
    min_i, min_j = -1, -1

    for i in range(len(cost_matrix)):
        for j in range(len(cost_matrix[0])):
            if cost_matrix[i][j] < min_cost:
                min_cost = cost_matrix[i][j]
                min_i, min_j = i, j

    return min_i, min_j

def main():
    # Run start_adhoc.sh
    run_shell_script("start_adhoc.sh")

    drone_ip_address = "192.168.1.3"

    send_json_packet("192.168.1.255", {"message_type": "status_information",
                                       "least_cost_mission": "None",
                                       "ip_address": drone_ip_address,
                                       "status": "WAITING",
                                       "traffic": "broadcast"})

    state = State.WAITING_FOR_MESSAGE
    mission_matrix = None

    while state != State.MISSION_IN_PROGRESS:
        state, mission_matrix = wait_message()

        if state == State.WAITING_FOR_MISSION_START:

            if mission_matrix is None:
                print("No mission matrix available.")
                break

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

            cost_matrix = calculate_cost_matrix(mission_matrix, current_state, battery_level)

            least_cost_mission = find_least_cost_mission(cost_matrix)

            print("least cost missions position", least_cost_mission)

            send_json_packet("192.168.1.255", {"message_type": "drone_mission_information",
                                                "least_cost_mission": least_cost_mission,
                                                "ip_address": drone_ip_address,
                                                "status": "WAITING",
                                                "traffic": "broadcast"})
            state = State.MISSION_IN_PROGRESS

        elif state == State.MISSION_IN_PROGRESS:

            print("least cost mission is", least_cost_mission, "goes to that location...")

    print("Mission in progress...")

if __name__ == "__main__":
    main()
