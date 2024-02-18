import socket

def receive_message():
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Bind the socket to the port
        s.bind(('0.0.0.0', 12345))  # Use any available IP address and port 12345

        print("Listening for messages...")

        # Receive messages indefinitely
        while True:
            # Receive data from the socket
            data, addr = s.recvfrom(1024)  # Buffer size is 1024 bytes
            print("Received message:", data.decode())

if __name__ == "__main__":
    receive_message()
