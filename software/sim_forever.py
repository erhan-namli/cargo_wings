import pygame
import random
import json
import matplotlib.pyplot as plt
from gif_pygame import load

def normalize_cost(cost, max_cost):
    return round(cost / max_cost, 4)

class Drone:
    next_id = 1

    def __init__(self, position, mission_matrix, gif_path, assigned_missions):
        self.id = Drone.next_id
        Drone.next_id += 1

        self.position = position
        self.new_position = None
        self.mission_matrix = mission_matrix
        self.battery_level = 100
        self.assigned_missions = assigned_missions
        self.second_assigned_missions = assigned_missions
        self.backup_assigned_missions = None
        self.cost_matrix = None
        self.backup_cost_matrix = None
        self.target_position = None
        self.second_target_position = None
        self.at_destination = False
        self.primary_target_reached = False
        self.last_move_time = pygame.time.get_ticks() / 1000
        self.gif_animation = load(gif_path)
        self.flight_time = 0

    def calculate_cost_matrix(self, mission_matrix, current_state, battery_level, drones):
        rows, cols = len(mission_matrix), len(mission_matrix[0])
        cost_matrix = [[float('inf')] * cols for _ in range(rows)]
        current_col, current_row = current_state

        for y in range(rows):
            for x in range(cols):
                if isinstance(mission_matrix[y][x], str) and mission_matrix[y][x].startswith("Task"):
                    task_number = int(mission_matrix[y][x].split()[1])
                    distance = abs(x - current_col) + abs(y - current_row)
                    distance_cost = normalize_cost(distance, rows + cols)
                    battery_cost = 1 - battery_level / 100
                    adjusted_cost = distance_cost * 0.6 + battery_cost * 0.4
                    cost_matrix[y][x] = round(adjusted_cost, 4)

        self.cost_matrix = cost_matrix
        return cost_matrix

    # Diğer Drone yöntemleri...

class DroneSimulation:
    def __init__(self, size=(800, 600), gif_path='drone-flying.gif'):
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)
        pygame.display.set_caption('Drone Simulation Setup')
        self.clock = pygame.time.Clock()
        self.fps = 30

        self.grid_rows = 6
        self.grid_cols = 9
        self.mission_matrix = [[0 for _ in range(self.grid_cols)] for _ in range(self.grid_rows)]

        self.drone_positions = [(3, 1), (3, 2), (3, 3)]

        self.assigned_missions = []
        self.gif_path = gif_path
        self.drones = []
        self.setup_complete = False

        self.debug_area_height = 150
        self.debug_font = pygame.font.Font(None, 24)

    def draw_grid(self):
        grid_width, grid_height = self.size[0] // self.grid_cols, (self.size[1] - self.debug_area_height) // self.grid_rows
        for y in range(self.grid_rows):
            for x in range(self.grid_cols):
                rect = pygame.Rect(x * grid_width, y * grid_height, grid_width, grid_height)
                
                color = (200, 200, 200)
                is_primary_target_reached = any(drone.primary_target_reached and drone.target_position == (y, x) for drone in self.drones)
                is_secondary_target_reached = any(drone.at_destination and drone.second_target_position == (y, x) for drone in self.drones)
                
                if is_primary_target_reached:
                    color = (0, 0, 255)
                elif is_secondary_target_reached:
                    color = (0, 0, 255)
                elif self.mission_matrix[y][x] == 1:
                    color = (0, 255, 0)

                pygame.draw.rect(self.screen, color, rect, 1)
                if (x, y) in self.drone_positions:
                    pygame.draw.circle(self.screen, (0, 0, 255), rect.center, grid_width // 4)

    def display_debug_info(self, messages):
        base_y = self.size[1] - self.debug_area_height
        pygame.draw.rect(self.screen, (0, 0, 0), (0, base_y, self.size[0], self.debug_area_height))

        for i, message in enumerate(messages):
            text_surface = self.debug_font.render(message, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, base_y + i * 20))

        for i, drone in enumerate(self.drones):
            battery_message = f'Drone {drone.id} Battery Level: {drone.battery_level}%'
            flight_time_message = f'Drone {drone.id} Flight Time: {drone.flight_time:.2f} seconds'
            text_surface_battery = self.debug_font.render(battery_message, True, (255, 255, 255))
            text_surface_flight_time = self.debug_font.render(flight_time_message, True, (255, 255, 255))
            self.screen.blit(text_surface_flight_time, (10, base_y + (i+2) * 20))
            self.screen.blit(text_surface_battery, (10, base_y + (i+5) * 20))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.setup_complete = True

    def handle_mouse_click(self, position):
        x, y = position
        grid_width, grid_height = self.size[0] // self.grid_cols, (self.size[1] - self.debug_area_height) // self.grid_rows
        column, row = x // grid_width, y // grid_height

        if pygame.mouse.get_pressed()[0]:
            if (column, row) not in self.drone_positions:
                self.mission_matrix[row][column] = 1 - self.mission_matrix[row][column]
        elif pygame.mouse.get_pressed()[2]:
            if (column, row) in self.drone_positions:
                self.drone_positions.remove((column, row))
            else:
                self.drone_positions.append((column, row))

    def update_drones(self):
        current_time = pygame.time.get_ticks() / 1000
        for drone in self.drones:
            if not drone.at_destination and current_time - drone.last_move_time >= 1:
                drone.move_towards_target()
                drone.last_move_time = current_time

            x, y = drone.position
            grid_width, grid_height = self.size[0] // self.grid_cols, (self.size[1] - self.debug_area_height) // self.grid_rows
            drone_screen_x = x * grid_width
            drone_screen_y = y * grid_height
            drone.gif_animation.render(self.screen, (drone_screen_x, drone_screen_y))

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

    def randomize_positions(self, num_drones, num_missions):
        all_positions = [(y, x) for y in range(self.grid_rows) for x in range(self.grid_cols)]
        random.shuffle(all_positions)

        drone_positions = all_positions[:num_drones]
        mission_positions = all_positions[num_drones:num_drones + num_missions]

        self.drone_positions = drone_positions
        for y, x in mission_positions:
            self.mission_matrix[y][x] = 1

    def run(self):
        pass

class SimulationManager:
    def __init__(self, simulation):
        self.simulation = simulation

    def plot_mission_costs(self, results, num_drones):
        average_total_costs = [sum(filter(None, run['total_costs'])) / len(run['total_costs']) for run in results]
        average_flight_times = [sum(run['total_flight_times']) / len(run['total_flight_times']) for run in results]

        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.plot(range(len(results)), average_total_costs, label='Average Total Mission Costs')
        plt.xlabel('Simulation Runs')
        plt.ylabel('Costs')
        plt.title(f'Average Total Mission Costs over {num_drones} Drone Runs')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(range(len(results)), average_flight_times, label='Average Flight Times')
        plt.xlabel('Simulation Runs')
        plt.ylabel('Flight Time (s)')
        plt.title(f'Average Flight Times over {num_drones} Drone Runs')
        plt.legend()

        plt.tight_layout()
        plt.show()

    def run_simulation(self, num_drones, num_missions, num_runs=5):
        results = []

        for _ in range(num_runs):
            self.simulation.mission_matrix = [[0 for _ in range(self.simulation.grid_cols)] for _ in range(self.simulation.grid_rows)]
            self.simulation.randomize_positions(num_drones, num_missions)

            task_number = 0
            for row in range(len(self.simulation.mission_matrix)):
                for col in range(len(self.simulation.mission_matrix[row])):
                    if self.simulation.mission_matrix[row][col] == 1:
                        self.simulation.mission_matrix[row][col] = f"Task {task_number}"
                        task_number += 1

            task_count = task_number

            self.simulation.drones = [Drone(pos, self.simulation.mission_matrix, self.simulation.gif_path, self.simulation.assigned_missions) for pos in self.simulation.drone_positions]
            drone_count = len(self.simulation.drones)
            Flag = 0

            if task_count >= drone_count:
                if task_count > drone_count:
                    Flag = 1
                else:
                    Flag = 0

                for drone in self.simulation.drones:
                    drone.calculate_cost_matrix(self.simulation.mission_matrix, drone.position, drone.battery_level, self.simulation.drones)
                    drone.assign_missions(drone.cost_matrix)

                while any(drone.assigned_missions[0] == other_drone.assigned_missions[0] for drone in self.simulation.drones for other_drone in self.simulation.drones if drone != other_drone):
                    for drone in self.simulation.drones:
                        filename = f'drone_{drone.id}_assigned_mission.json'
                        drone.share_first_mission(filename.replace('assigned_mission', 'first_mission'), self.simulation.drones)

                    for drone in self.simulation.drones:
                        filename = f'drone_{drone.id}_first_mission.json'
                        other_drones = [other_drone for other_drone in self.simulation.drones if other_drone != drone]
                        for other_drone in other_drones:
                            other_drone.receive_first_mission(filename)

                    for drone in self.simulation.drones:
                        for other_drone in self.simulation.drones:
                            if drone != other_drone and drone.assigned_missions[0] == other_drone.assigned_missions[0]:
                                filename = f'cost_difference_matrix_{drone.id}to{other_drone.id}.json'
                                drone.send_cost_difference_matrix(drone.calculate_cost_difference_matrix(), other_drone.id)

                    for drone in self.simulation.drones:
                        for other_drone in self.simulation.drones:
                            if drone != other_drone and drone.assigned_missions[0] == other_drone.assigned_missions[0]:
                                filename = f'cost_difference_matrix_{other_drone.id}to{drone.id}.json'
                                other_drone.receive_cost_difference_matrix(filename)

                    for drone in self.simulation.drones:
                        for other_drone in self.simulation.drones:
                            if drone != other_drone and drone.assigned_missions[0] == other_drone.assigned_missions[0]:
                                drone.process_first_mission(drone.calculate_cost_difference_matrix(), other_drone.id)

                for drone in self.simulation.drones:
                    if drone.assigned_missions[0] != drone.position:
                        drone.target_position = drone.assigned_missions[0]
                        drone.at_destination = False
                    else:
                        drone.at_destination = False
                        drone.target_position = drone.assigned_missions[0]

                for drone in self.simulation.drones:
                    if Flag == 1:
                        drone.backup_assigned_missions = drone.assigned_missions
                        drone.backup_cost_matrix = drone.cost_matrix

            if task_count < drone_count or Flag == 1:
                if Flag == 0:
                    for drone in self.simulation.drones:
                        drone.calculate_cost_matrix(self.simulation.mission_matrix, drone.position, drone.battery_level, self.simulation.drones)
                        drone.assign_missions(drone.cost_matrix)

                elif Flag == 1:
                    for drone in self.simulation.drones:
                        row, col = drone.assigned_missions[0]
                        drone.mission_matrix[row][col] = 0

                    for drone in self.simulation.drones:
                        row2, col2 = drone.assigned_missions[0]
                        drone.new_position = col2, row2
                        drone.cost_matrix = drone.calculate_cost_matrix(self.simulation.mission_matrix, drone.new_position, drone.battery_level, self.simulation.drones)
                        drone.second_assign_missions(drone.cost_matrix)

                for drone in self.simulation.drones:
                    if not drone.second_assigned_missions:
                        pass
                    else:
                        drone.assigned_missions = drone.second_assigned_missions

                while any(drone.assigned_missions and other_drone.assigned_missions and drone.assigned_missions[0] == other_drone.assigned_missions[0] for drone in self.simulation.drones for other_drone in self.simulation.drones if drone != other_drone):
                    for drone in self.simulation.drones:
                        filename = f'drone_{drone.id}_first_mission.json'
                        drone.share_first_mission(filename.replace('assigned_mission', 'first_mission'), self.simulation.drones)

                    for drone in self.simulation.drones:
                        filename = f'drone_{drone.id}_first_mission.json'
                        other_drones = [other_drone for other_drone in self.simulation.drones if other_drone != drone]
                        for other_drone in other_drones:
                            other_drone.new_receive_first_mission(filename)

                    for drone in self.simulation.drones:
                        for other_drone in self.simulation.drones:
                            if drone.assigned_missions and other_drone.assigned_missions:
                                if drone != other_drone and drone.assigned_missions[0] == other_drone.assigned_missions[0]:
                                    filename = f'first_mission_cost_{drone.id}to{other_drone.id}.json'
                                    drone.share_first_mission_cost(filename, other_drone.id)
                                    first_mission_cost = drone.calculate_cost_of_first_mission()

                    for drone in self.simulation.drones:
                        for other_drone in self.simulation.drones:
                            if drone != other_drone and drone.assigned_missions and other_drone.assigned_missions:
                                if drone.assigned_missions[0] == other_drone.assigned_missions[0]:
                                    filename = f'first_mission_cost_{other_drone.id}to{drone.id}.json'
                                    other_drone.receive_first_mission_cost(filename)

                    for drone in self.simulation.drones:
                        for other_drone in self.simulation.drones:
                            if drone != other_drone and drone.assigned_missions and other_drone.assigned_missions:
                                if drone.assigned_missions[0] == other_drone.assigned_missions[0]:
                                    drone.process_first_mission_cost(drone.calculate_cost_of_first_mission, other_drone.id)

                for drone in self.simulation.drones:
                    if Flag == 0:
                        if not drone.assigned_missions:
                            drone.target_position = None
                            drone.at_destination = False
                        else:
                            if drone.assigned_missions[0] != drone.position:
                                drone.target_position = drone.assigned_missions[0]
                                drone.at_destination = False
                            else:
                                drone.at_destination = False
                                drone.target_position = drone.assigned_missions[0]
                    elif Flag == 1:
                        if not drone.assigned_missions:
                            drone.target_position = drone.backup_assigned_missions[0]
                            drone.second_target_position = drone.target_position
                            drone.at_destination = False
                        else:
                            if drone.assigned_missions[0] != drone.position:
                                drone.second_target_position = drone.assigned_missions[0]
                                drone.at_destination = False
                            else:
                                drone.at_destination = False
                                drone.second_target_position = drone.assigned_missions[0]

            self.simulation.update_drones()

            total_costs = [drone.calculate_cost_of_first_mission() for drone in self.simulation.drones]
            flight_times = [drone.flight_time for drone in self.simulation.drones]
            results.append({
                'total_costs': total_costs,
                'total_flight_times': flight_times
            })

        self.plot_mission_costs(results, num_drones)

    def run(self):
        num_drones_list = [3, 6, 12]
        num_missions_list = [5, 10, 20]

        for num_drones in num_drones_list:
            for num_missions in num_missions_list:
                print(f"Running simulation with {num_drones} drones and {num_missions} missions")
                self.run_simulation(num_drones, num_missions)

# To run the simulation
sim = DroneSimulation()
sim.setup_simulation()
manager = SimulationManager(sim)
manager.run()
