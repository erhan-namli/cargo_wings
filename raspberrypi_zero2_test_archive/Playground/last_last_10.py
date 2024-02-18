import socket
import time

# Tello IP and port
tello_address = ('192.168.10.1', 8889)

# Create a UDP connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a local address and port
sock.bind(('0.0.0.0', 9000))

# Function to send Tello commands
def send_command(command):
    sock.sendto(command.encode(), tello_address)
    print("Sent command:", command)
    time.sleep(1)  # Wait for Tello to process the command

# Takeoff
send_command("command")  # Enter command mode
send_command("takeoff")

# Move forward by 30 centimeters
send_command("forward 30")

# Land
send_command("land")

