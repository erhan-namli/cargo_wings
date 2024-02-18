import time
import tellopy

# Constants
FORWARD_SPEED_CM_S = 30  # speed of the drone in centimeters per second
FORWARD_DISTANCE_CM = 30  # distance to move forward in centimeters

# Calculate approximate time to travel FORWARD_DISTANCE
travel_time = FORWARD_DISTANCE_CM / FORWARD_SPEED_CM_S

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
    drone.set_pitch(50)  # Adjust pitch value for desired speed
    time.sleep(travel_time)  # Adjust duration for desired distance

    # Land the drone
    drone.land()

    # Wait for the drone to land
    time.sleep(2)

finally:
    # Ensure the drone connection is properly closed
    drone.quit()

