import socket
import subprocess
import time

# Function to connect to the hotspot
def connect_to_hotspot(ssid, password):
    subprocess.run(["sudo", "nmcli", "device", "wifi", "connect", ssid, "password", password])

# Function to send a message to another device
def send_message(message, ip_address, port):
    print("Sending message:", message)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip_address, port))
        s.sendall(message.encode())
        print("Message sent successfully.")

# Main function
def main():
    # Connect to the hotspot
    ssid = "MyPiHotspotTello"
    password = "MySecretPassword"
    connect_to_hotspot(ssid, password)

    # Wait for connection to establish
    time.sleep(5)  # Adjust as needed
    
    # IP address and port of the receiving Raspberry Pi
    receiver_ip = "192.168.4.1"  # Example IP address, change as per your setup
    receiver_port = 12345  # Example port, change as per your setup
    
    # Message to send
    message = "Hello from the sender Raspberry Pi!"
    
    # Send the message to the receiver
    send_message(message, receiver_ip, receiver_port)

# Execute the main function
if __name__ == "__main__":
    main()

