import time
import tellopy

# Constants
FORWARD_SPEED_CM_S = 30  # speed of the drone in centimeters per second

# Connect to the Tello drone
drone = tellopy.Tello()

def forward(distance_cm):
    # Calculate approximate time to travel distance_cm
    travel_time = distance_cm / FORWARD_SPEED_CM_S

    # Start the flight
    drone.takeoff()

    # Wait for the drone to stabilize after takeoff
    time.sleep(2)

    # Move forward
    drone.forward(50)  # Move forward at 50 cm/s (maximum speed)
    time.sleep(travel_time)  # Adjust duration for desired distance
    drone.forward(0)  # Stop moving forward

    # Land the drone
    drone.land()

    # Wait for the drone to land
    time.sleep(2)

try:
    drone.connect()
    drone.wait_for_connection(10.0)

    forward(10)  # Move forward by 10 centimeters

finally:
    # Ensure the drone connection is properly closed
    drone.quit()

