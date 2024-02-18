import time
import tellopy

# Constants
FORWARD_DISTANCE = 30  # in centimeters

# Connect to the Tello drone
drone = tellopy.Tello()

try:
    drone.connect()
    drone.wait_for_connection(10.0)

    # Start the flight
    drone.takeoff()

    # Wait for the drone to stabilize after takeoff
    time.sleep(2)

    # Move forward
    drone.move_forward(FORWARD_DISTANCE)

    # Calculate approximate time to travel FORWARD_DISTANCE
    # We assume Tello's speed is roughly 30 cm/s
    travel_time = FORWARD_DISTANCE / 30

    # Wait for the drone to finish moving forward
    time.sleep(travel_time)

    # Land the drone
    drone.land()

    # Wait for the drone to land
    time.sleep(2)

finally:
    # Ensure the drone connection is properly closed
    drone.quit()

