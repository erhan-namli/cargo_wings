import pygame
import random

# Assuming 'load' function exists within 'gif_pygame' for loading GIF animations
from gif_pygame import load

def normalize_cost(cost, max_cost):
    return round(cost / max_cost, 4)

class Drone:
    def __init__(self, position, mission_matrix, battery_level, gif_path, assigned_missions):
        self.position = position
        self.mission_matrix = mission_matrix
        self.battery_level = battery_level
        self.assigned_missions = assigned_missions
        self.cost_matrix = self.calculate_cost_matrix(mission_matrix, position, battery_level)
        self.target_position = self.find_least_cost_mission(self.cost_matrix, assigned_missions)
        self.at_destination = False
        self.last_move_time = pygame.time.get_ticks() / 1000
        self.gif_animation = load(gif_path)

    def calculate_cost_matrix(self, mission_matrix, current_state, battery_level):
        rows, cols = len(mission_matrix), len(mission_matrix[0])
        cost_matrix = [[float('inf')] * cols for _ in range(rows)]
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
            current_x, current_y = self.position
            target_y, target_x = self.target_position

            # Determine the primary direction to move based on the greater distance
            delta_x = abs(target_x - current_x)
            delta_y = abs(target_y - current_y)

            if delta_x > delta_y:
                step_x = 1 if current_x < target_x else -1 if current_x > target_x else 0
                new_x = current_x + step_x
                new_y = current_y
            else:
                step_y = 1 if current_y < target_y else -1 if current_y > target_y else 0
                new_x = current_x
                new_y = current_y + step_y

            self.position = (new_x, new_y)
            self.check_destination()

            if self.at_destination:
                print(f"Drone reached the target at {self.position}")

    def check_destination(self):
        if self.position == self.target_position:
            self.at_destination = True
            print(f"Drone arrived at destination {self.position}")

class DroneSimulation:
    def __init__(self, size=(800, 600), gif_path='drone-flying.gif'):
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)
        pygame.display.set_caption('Drone Simulation Setup')
        self.clock = pygame.time.Clock()
        self.fps = 30

        self.grid_rows = 6
        self.grid_cols = 5
        self.mission_matrix = [[0 for _ in range(self.grid_cols)] for _ in range(self.grid_rows)]
        self.drone_positions = [(0, 1), (0, 2), (0, 3)]
        self.assigned_missions = []
        self.gif_path = gif_path
        self.drones = []
        self.setup_complete = False

    def setup_simulation(self):
        running = True
        while running:
            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.handle_events()

            pygame.display.flip()
            self.clock.tick(self.fps)

            if self.setup_complete:
                running = False

    def draw_grid(self):
        grid_width, grid_height = self.size[0] // self.grid_cols, self.size[1] // self.grid_rows
        for y in range(self.grid_rows):
            for x in range(self.grid_cols):
                rect = pygame.Rect(x * grid_width, y * grid_height, grid_width, grid_height)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
                if self.mission_matrix[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 255, 0), rect)
                if (x, y) in self.drone_positions:
                    pygame.draw.circle(self.screen, (0, 0, 255), rect.center, grid_width // 4)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter key to start the simulation
                    print("enter")

                    self.setup_complete = True

    def handle_mouse_click(self, position):
        x, y = position
        grid_width, grid_height = self.size[0] // self.grid_cols, self.size[1] // self.grid_rows
        column, row = x // grid_width, y // grid_height

        # Toggle between mission and drone placement
        if pygame.mouse.get_pressed()[0]:  # Left click
            if (column, row) not in self.drone_positions:
                self.mission_matrix[row][column] = 1 - self.mission_matrix[row][column]
        elif pygame.mouse.get_pressed()[2]:  # Right click
            if (column, row) in self.drone_positions:
                self.drone_positions.remove((column, row))
            else:
                self.drone_positions.append((column, row))

    def run(self):
        self.drones = [Drone(pos, self.mission_matrix, random.randint(50, 100), self.gif_path, self.assigned_missions) for pos in self.drone_positions]
        running = True
        while running:
            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.update_drones()

            pygame.display.flip()
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def update_drones(self):
        current_time = pygame.time.get_ticks() / 1000
        for drone in self.drones:
            if not drone.at_destination and current_time - drone.last_move_time >= 1:
                drone.move_towards_target()
                drone.last_move_time = current_time

            x, y = drone.position
            grid_width, grid_height = self.size[0] // self.grid_cols, self.size[1] // self.grid_rows
            drone_screen_x = x * grid_width
            drone_screen_y = y * grid_height
            drone.gif_animation.render(self.screen, (drone_screen_x, drone_screen_y))

# To run the simulation
sim = DroneSimulation()
sim.setup_simulation()
sim.run()
