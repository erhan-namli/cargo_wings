import pygame
import random
from gif_pygame import load
def normalize_cost(cost, max_cost):
    # Normalize cost between 0 and 1
    return round(cost / max_cost, 4)  # Limit to 4 decimal places

class Drone:
    def __init__(self, position, mission_matrix, battery_level, gif_path, assigned_missions):
        self.position = position
        self.mission_matrix = mission_matrix
        self.battery_level = battery_level
        self.assigned_missions = assigned_missions
        self.cost_matrix = self.calculate_cost_matrix(mission_matrix, position, battery_level)
        self.target_position = self.find_least_cost_mission(self.cost_matrix, assigned_missions)
        self.at_destination = False
        self.last_move_time = pygame.time.get_ticks() / 1000  # Initialize last move time
        # Assume load function exists for loading GIFs
        self.gif_animation = load(gif_path)  # Load the GIF file as an animation

    def calculate_cost_matrix(self, mission_matrix, current_state, battery_level):
        rows, cols = len(mission_matrix), len(mission_matrix[0])
        cost_matrix = [[float('inf')] * cols for _ in range(rows)]

        # Current state is (row, column)
        current_row, current_col = current_state

        for y in range(rows):
            for x in range(cols):
                if mission_matrix[y][x] == 1 and (y, x) not in self.assigned_missions:
                    distance = abs(x - current_col) + abs(y - current_row)
                    normalized_cost = normalize_cost(distance, rows + cols)
                    adjusted_cost = normalized_cost + (1 - normalized_cost) * (1 - battery_level / 100)
                    cost_matrix[y][x] = round(adjusted_cost, 4)

        return cost_matrix

    def find_least_cost_mission(self, cost_matrix, assigned_missions):
        min_cost = float('inf')
        min_pos = (-1, -1)

        for y in range(len(cost_matrix)):
            for x in range(len(cost_matrix[y])):
                if cost_matrix[y][x] < min_cost and (y, x) not in assigned_missions:
                    min_cost = cost_matrix[y][x]
                    min_pos = (y, x)

        if min_pos != (-1, -1):
            assigned_missions.append(min_pos)
        return min_pos

    def move_towards_target(self):
        if not self.at_destination and self.target_position:
            # Current position in x, y format
            current_x, current_y = self.position
            target_y, target_x = self.target_position

            step_x = 1 if current_x < target_x else -1 if current_x > target_x else 0
            step_y = 1 if current_y < target_y else -1 if current_y > target_y else 0

            new_x = current_x + step_x
            new_y = current_y + step_y

            self.position = (new_x, new_y)  # Update position as (x, y)
            self.check_destination()

            if self.at_destination:
                print(f"Drone reached the target at {self.position}")
            else:
                # Uncomment to see movement details
                # print(f"Drone moving to {self.position}")
                pass
    def check_destination(self):
        if self.position == self.target_position:
            self.at_destination = True
            #print(f"Drone arrived at destination {self.position}")

    def print_assigned_missions(self):
        print(f"Drone at position {self.position} has assigned missions: {self.assigned_missions}")



class DroneSimulation:
    def __init__(self, mission_matrix, drone_positions, size=(800, 600), gif_path='drone-flying.gif'):
        pygame.init()
        self.mission_matrix = mission_matrix
        self.size = size

        self.screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)  # Ensure double buffering

        #self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Drone Simulation')
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.assigned_missions = []

        self.drones = [
            Drone(pos, mission_matrix, random.randint(50, 100), gif_path, self.assigned_missions)
            for pos in drone_positions
        ]

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

            if not running or all(drone.at_destination for drone in self.drones):
                # Print the assigned missions once all drones have reached their destination
                self.print_assigned_missions()

    def draw_grid(self):
        rows, cols = len(self.mission_matrix), len(self.mission_matrix[0])
        grid_width, grid_height = self.size[0] // cols, self.size[1] // rows
        for y in range(rows):
            for x in range(cols):
                rect = pygame.Rect(x * grid_width, y * grid_height, grid_width, grid_height)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
                if self.mission_matrix[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 255, 0), rect)

    def update_drones(self):
        current_time = pygame.time.get_ticks() / 1000
        for drone in self.drones:
            if not drone.at_destination and current_time - drone.last_move_time >= 1:
                drone.move_towards_target()
                drone.last_move_time = current_time
                drone.print_assigned_missions()  # Print each drone's assigned missions

            x, y = drone.position
            grid_width, grid_height = self.size[0] // len(self.mission_matrix[0]), self.size[1] // len(
                self.mission_matrix)
            drone_screen_x = x * grid_width
            drone_screen_y = y * grid_height

            drone.gif_animation.render(self.screen, (drone_screen_x, drone_screen_y))

    def print_assigned_missions(self):
        #print("Assigned missions:")
        for mission in self.assigned_missions:
            #print(mission)
            pass

    def end_simulation(self):
        pygame.quit()

# To run the simulation, uncomment and use the following lines:
mission_matrix = [[1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 1, 0], [1, 0, 0, 1, 0], [1, 1, 0, 1, 0], [0, 0, 0, 1, 0]]
drone_positions = [(2, 0), (2, 3), (1, 0)]
sim = DroneSimulation(mission_matrix, drone_positions)
sim.run()