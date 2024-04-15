import subprocess
import json
import time
import socket
import datetime
from lightdjitellopy import Tello

global mission_matrix

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

def move_tello(tello, direction, distance):
    if distance == 0:
        return  # Skip movement commands if distance is zero

    # Check if the drone has landed, then takeoff again
    if tello.is_flying is False:
        tello.takeoff()

    if direction == 'up':
        tello.move_up(distance)
    elif direction == 'down':
        tello.move_down(distance)
    elif direction == 'left':
        tello.move_left(distance)
    elif direction == 'right':
        tello.move_right(distance)
    elif direction == 'forward':
        tello.move_forward(distance)
    elif direction == 'backward':
        tello.move_back(distance)
    elif direction == 'rotate_clockwise':
        tello.rotate_clockwise(distance)
    elif direction == 'rotate_counter_clockwise':
        tello.rotate_counter_clockwise(distance)

def wait_message():
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
        parse_incoming_message(msg.decode())

        if mission_matrix:
            break

        # You can perform actions based on the received message here

def parse_incoming_message(json_data):

    global mission_matrix
    try:
        data = json.loads(json_data)
        mission_matrix = data.get("mission_matrix")

        if mission_matrix:
            # Update self.mission_matrix with the incoming matrix
            mission_matrix = mission_matrix
            print("Updated mission matrix:", mission_matrix)

        else:
            print("No mission matrix found in the incoming message.")
    except json.JSONDecodeError as e:
        print("Error parsing incoming JSON message:", e)

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

def main():
    # Run start_adhoc.sh
    run_shell_script("start_adhoc.sh")

    # Wait for message
    print("Waiting for a message...")
    wait_message()

    print(mission_matrix)

    # Run connect_tello.sh
    run_shell_script("connect_tello.sh")

    # Initialize Tello
    tello = Tello()
    tello.connect()
    tello.takeoff()

    # Define starting position
    start_x = 0
    start_y = 0
    # Define movement distance
    distance = 20  # 10 cm between each row and column index
    # Save starting position
    current_x = start_x
    current_y = start_y
    # Loop through the mission_matrix
    for i in range(len(mission_matrix)):
        for j in range(len(mission_matrix[0])):
            if mission_matrix[i][j] == 1:
                # Calculate target position
                target_x = start_x + j * distance
                target_y = start_y + i * distance

                # Calculate movement offsets
                dx = target_x - current_x
                dy = target_y - current_y

                # Determine the direction to move horizontally
                if dx > 0:
                    horizontal_direction = 'right'
                else:
                    horizontal_direction = 'left'
                # Determine the direction to move vertically
                if dy > 0:
                    vertical_direction = 'forward'
                else:
                    vertical_direction = 'backward'

                # Move Tello to target position
                move_tello(tello, horizontal_direction, abs(dx))  # Move horizontally
                move_tello(tello, vertical_direction, abs(dy))  # Move vertically

                # Update current position
                current_x = target_x
                current_y = target_y
                # Land Tello
                tello.land()
                time.sleep(5)  # Wait for 5 seconds before the next movement
    # End Tello connection
    tello.end()

if __name__ == "__main__":
    main()
