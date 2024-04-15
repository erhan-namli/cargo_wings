import pygame
import random
from gif_pygame import load

def calculate_cost_matrix(mission_matrix, current_state, battery_level):
    rows, cols = len(mission_matrix), len(mission_matrix[0])
    cost_matrix = [[float('inf')] * cols for _ in range(rows)]

    current_x, current_y = current_state

    for y in range(rows):
        for x in range(cols):
            if mission_matrix[y][x] == 1:
                distance = abs(x - current_x) + abs(y - current_y)
                cost_matrix[y][x] = distance  # Simple cost based on distance

    return cost_matrix

def normalize_cost(cost, max_cost):
    # Normalize cost between 0 and 1
    return round(cost / max_cost, 4)  # Limit to 4 decimal places


# Define the function to find the least cost mission
def find_least_cost_mission(cost_matrix, assigned_missions):
    min_cost = float('inf')
    min_pos = (-1, -1)

    for y in range(len(cost_matrix)):
        for x in range(len(cost_matrix[y])):
            if cost_matrix[y][x] < min_cost and (y, x) not in assigned_missions:
                min_cost = cost_matrix[y][x]
                min_pos = (y, x)

    return min_pos

class Drone:
    def __init__(self, position, mission_matrix, gif_path):
        self.position = position
        self.mission_matrix = mission_matrix

        self.battery_level = random.randint(50, 100)
        self.cost_matrix = calculate_cost_matrix(mission_matrix, position, self.battery_level)

        self.target_position = self.find_target_position()
        self.at_destination = False
        self.last_move_time = pygame.time.get_ticks() / 1000  # Initialize last move time

        self.gif_animation = load(gif_path)  # Load the GIF file as an animation
    def find_target_position(self):
        for y, row in enumerate(self.mission_matrix):
            for x, value in enumerate(row):
                if value == 1:
                    print(f"Target found at ({x}, {y})")
                    return (x, y)
        return None

    def move_towards_target(self):
        if not self.at_destination and self.target_position:
            current_x, current_y = self.position
            target_x, target_y = self.target_position

            print(f"Moving drone from ({current_x}, {current_y}) towards ({target_x}, {target_y})")

            # Determine the step to take towards the target
            step_x = 1 if current_x < target_x else -1 if current_x > target_x else 0
            step_y = 1 if current_y < target_y else -1 if current_y > target_y else 0

            # Update position towards the target
            new_x = current_x + step_x
            new_y = current_y + step_y

            # Ensure the new position is within the mission matrix bounds
            new_x = max(0, min(new_x, len(self.mission_matrix[0]) - 1))
            new_y = max(0, min(new_y, len(self.mission_matrix) - 1))

            self.position = (new_x, new_y)
            self.check_destination()

            if self.at_destination:
                print(f"Drone reached the target at {self.position}")
            else:
                print(f"Drone moving to {self.position}")

    def check_destination(self):
        if self.position == self.target_position:
            self.at_destination = True
            print(f"Drone arrived at destination {self.position}")

    def assign_mission(self, available_missions):
        self.target_position = find_least_cost_mission(self.cost_matrix, available_missions)
        if self.target_position != (-1, -1):
            available_missions.remove(self.target_position)

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

class DroneSimulation:
    def __init__(self, mission_matrix, drone_positions, size=(800, 600), gif_path='drone-flying.gif'):
        pygame.init()
        self.mission_matrix = mission_matrix
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Drone Simulation')
        self.clock = pygame.time.Clock()
        self.fps = 30  # Frames per second

        # Load the drone image
        #drone_image = pygame.image.load(gif_path)
        #drone_image = pygame.transform.scale(drone_image, (100, 100))  # Adjust size as needed

        # Initialize drones with the animated GIF
        self.drones = [Drone(pos, mission_matrix, gif_path) for pos in drone_positions]

    def run(self):
                running = True
                while running:
                    self.clock.tick(self.fps)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False

                    self.screen.fill((255, 255, 255))
                    self.draw_grid()
                    self.update_drones()
                    pygame.display.flip()

    def draw_grid(self):
        rows, cols = len(self.mission_matrix), len(self.mission_matrix[0])
        grid_width, grid_height = self.size[0] // cols, self.size[1] // rows
        for i in range(rows):
            for j in range(cols):
                rect = pygame.Rect(j * grid_width, i * grid_height, grid_width, grid_height)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
                if self.mission_matrix[i][j] == 1:
                    pygame.draw.rect(self.screen, (0, 255, 0), rect)

    def update_drones(self):
        current_time = pygame.time.get_ticks() / 1000
        for drone in self.drones:
            if not drone.at_destination and current_time - drone.last_move_time >= 1:
                drone.move_towards_target()
                drone.last_move_time = current_time

            # Render the drone GIF at its current position
            x, y = drone.position
            grid_width, grid_height = self.size[0] // len(self.mission_matrix[0]), self.size[1] // len(self.mission_matrix)
            drone_screen_x = x * grid_width
            drone_screen_y = y * grid_height
            drone.gif_animation.render(self.screen, (drone_screen_x, drone_screen_y))

    def end_simulation(self):
        pygame.quit()

# To run the simulation, uncomment the following lines
# Example usage

mission_matrix = [
    [0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0]
]

drone_positions = [(0, 0), (1, 1), (2, 2)]
sim = DroneSimulation(mission_matrix, drone_positions)
sim.run()

