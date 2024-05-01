import pygame
import random
import json

import numpy as np

from scipy.optimize import linear_sum_assignment
# Assuming 'load' function exists within 'gif_pygame' for loading GIF animations
from gif_pygame import load

def normalize_cost(cost, max_cost):
    return round(cost / max_cost, 4)

class Drone:
    next_id = 1

    def __init__(self, position, mission_matrix, gif_path, assigned_missions):
        self.id = Drone.next_id
        Drone.next_id += 1

        self.position = position
        self.mission_matrix = mission_matrix

        self.mission_matrix_old = [[1 if isinstance(cell, str) and cell.startswith("Task") else cell for cell in row] for row in mission_matrix]
        print("MM",self.mission_matrix_old)

        self.battery_level = 100
        self.assigned_missions = assigned_missions
        self.cost_matrix= None
        self.cost_matrix_old = self.calculate_cost_matrix_old(self.mission_matrix_old, position, self.battery_level)
        self.target_position = self.find_least_cost_mission_old(self.cost_matrix_old, assigned_missions)
        self.at_destination = False
        self.last_move_time = pygame.time.get_ticks() / 1000
        self.gif_animation = load(gif_path)
        self.flight_time = 0


    def calculate_cost_matrix_old(self, mission_matrix, current_state, battery_level):
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

    def find_least_cost_mission_old(self, cost_matrix, assigned_missions):
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

    def calculate_cost_matrix(self, mission_matrix, current_state, battery_level, drones):
        rows, cols = len(mission_matrix), len(mission_matrix[0])
        cost_matrix = [[float('inf')] * cols for _ in range(rows)]
        current_row, current_col = current_state

        for y in range(rows):
            for x in range(cols):
                if isinstance(mission_matrix[y][x], str) and mission_matrix[y][x].startswith("Task"):
                    task_number = int(mission_matrix[y][x].split()[1])  # Görev numarasını al
                    distance = abs(x - current_col) + abs(y - current_row)
                    distance_cost = normalize_cost(distance, rows + cols)
                    battery_cost = 1 - battery_level / 100
                    adjusted_cost = distance_cost * 0.6 + battery_cost * 0.4
                    cost_matrix[y][x] = round(adjusted_cost, 4)

        # Maliyet matrisini diğer dronlara paylaş
        for drone in drones:
            if drone.id != self.id:
                drone.receive_cost_matrix(self.id, cost_matrix)

        self.cost_matrix = cost_matrix  # Dönüş değeri olarak cost_matrix'i atayalım
        return cost_matrix

    def receive_cost_matrix(self, sender_id, cost_matrix):
        # JSON formatına dönüştür ve diğer dronun maliyet matrisini al
        json_data = json.dumps({'sender_id': sender_id, 'cost_matrix': cost_matrix})
        # Burada, JSON verisini almak için bir işlem gerçekleştirilebilir
        # Örneğin, diğer dronun maliyet matrisini almak için bir ağ bağlantısı kurulabilir

    def find_least_cost_mission(self, combined_cost_matrix, assigned_missions):
        # Eğer atanacak görev kalmadıysa (-1, -1) döndür
        if not combined_cost_matrix:
            print("No missions to assign.")
            return

        # Combined cost matrisini numpy dizisine dönüştür
        cost_array = np.array(combined_cost_matrix)

        # lineer toplam atama algoritmasını kullanarak minimum maliyet eşleşmesi bul
        row_indices, col_indices = linear_sum_assignment(cost_array)

        # Eşleşme bulunamazsa (-1, -1) döndür
        if len(row_indices) == 0 or len(col_indices) == 0:
            print("No assignment found.")
            return

        # Toplam maliyeti hesapla
        total_cost = cost_array[row_indices, col_indices].sum()
        print(f"Minimum total cost: {total_cost}")

        # Atanmış görevleri saklamak için bir sözlük oluştur
        assigned_tasks = {}

        # Her bir dronun hangi göreve atanacağını ekrana yazdır
        for i, (drone_index, mission_index) in enumerate(zip(row_indices, col_indices)):
            drone_id = drone_index + 1
            mission_number = mission_index + 1
            print(f"Drone {drone_id} assigned to mission {mission_number}.")
            # Atanmış görevleri sözlüğe ekle
            assigned_tasks[drone_id] = mission_number

        # Atanmış görevleri döndür
        return assigned_tasks

    def get_assigned_task_for_drone(self, assigned_tasks, drone_id):
        if drone_id in assigned_tasks:
            return assigned_tasks[drone_id]
        else:
            #print(f"Drone {drone_id} has not been assigned any mission.")
            return None

    def move_towards_target(self, assigned_tasks, mission_matrix):
        if not self.at_destination and self.target_position:
            current_x, current_y = self.position
            target_y, target_x = self.target_position

            delta_x = abs(target_x - current_x)
            delta_y = abs(target_y - current_y)

            step_x = 0  # Default değer ataması
            step_y = 0  # Default değer ataması

            if delta_x > delta_y:
                step_x = 1 if current_x < target_x else -1 if current_x > target_x else 0
            else:
                step_y = 1 if current_y < target_y else -1 if current_y > target_y else 0

            # Calculate time taken to move one unit distance
            time_taken_for_one_unit = 1  # Initial assumption: 1 second
            if step_x != 0 or step_y != 0:
                time_taken_for_one_unit += 5  # Increase by 5 seconds for each unit distance

            # Batarya seviyesini güncelle: Her bir adımda %2 azalt
            self.battery_level -= 2
            if self.battery_level < 0:
                self.battery_level = 0

            new_x = current_x + step_x
            new_y = current_y + step_y

            self.position = (new_x, new_y)
            self.flight_time += time_taken_for_one_unit  # Toplam uçuş süresini güncelle
            self.check_destination()

            # Dronun kendi ID'sine göre atanmış görev numarasını al
            assigned_task = self.get_assigned_task_for_drone(assigned_tasks, self.id)

            if assigned_task is not None:
                # Eğer dronun atanmış bir görevi varsa, hedef konumu o görevin koordinatlarına ayarla
                target_position = self.get_task_position(assigned_task, mission_matrix)
                if target_position is not None:
                    self.target_position = target_position

    def get_task_position(self, task_number, mission_matrix):
        # Görev numarasından konumu al
        for y, row in enumerate(mission_matrix):
            for x, cell in enumerate(row):
                if cell == f"Görev {task_number}":
                    return x, y
        print(f"Görev {task_number} konumu bulunamadı.")
        return None


    def check_destination(self):
        if self.position[::-1] == self.target_position:
            self.at_destination = True

    def is_mission_completed(self):
        return self.at_destination

    def print_cost_matrix(self):
        if self.cost_matrix:
            print(f"Drone {self.id} Cost Matrix:")
            for row in self.cost_matrix:
                print(row)
            print()

    def calculate_combined_cost_matrix(self, drones):
        combined_cost_matrix = []

        # Drone ID'si 1'den başlayarak her bir drone için cost matrisindeki değerleri tek bir satıra ekleyelim
        for drone_id in range(1, len(drones) + 1):
            combined_row = []

            # Her bir dronun cost matrisindeki değerleri tek tek inceleyip, sonsuzdan farklı olanları combined cost matrisine ekleyelim
            for drone in drones:
                if drone.id == drone_id:
                    for row_index in range(len(drone.cost_matrix)):
                        row = drone.cost_matrix[row_index]
                        if any(value != float('inf') for value in row):
                            combined_row.extend([value for value in row if value != float('inf')])

            # Eğer bu drone için bir maliyet bulunduysa, combined cost matrisine ekleyelim
            if combined_row:
                combined_cost_matrix.append(combined_row)

        return combined_cost_matrix
    

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

        self.drone_positions = [(1, 1), (3, 2), (0, 3)]

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
                is_target_and_completed = any(drone.is_mission_completed() and drone.target_position == (y, x) for drone in self.drones)
                if is_target_and_completed:
                    color = (0, 0, 255)  # Change to blue if the mission is completed

                elif (x, y) in self.drone_positions:
                    pygame.draw.circle(self.screen, (0, 0, 255), rect.center, grid_width // 4)

                elif self.mission_matrix[y][x] == 1:
                    color = (0, 255, 0)  # Green for mission locations
                else:
                    color = (200, 200, 200)  # Default color for grid
                pygame.draw.rect(self.screen, color, rect, 1)

    def display_debug_info(self, messages):
        base_y = self.size[1] - self.debug_area_height
        pygame.draw.rect(self.screen, (0, 0, 0), (0, base_y, self.size[0], self.debug_area_height))

        for i, message in enumerate(messages):
            text_surface = self.debug_font.render(message, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, base_y + i * 20))

        # Her bir dronun batarya seviyesini ve uçuş süresini göster
        for i, drone in enumerate(self.drones):
            battery_message = f'Drone {drone.id} Battery Level: {drone.battery_level}%'
            flight_time_message = f'Drone {drone.id} Flight Time: {drone.flight_time:.2f} seconds'
            text_surface_battery = self.debug_font.render(battery_message, True, (255, 255, 255))
            text_surface_flight_time = self.debug_font.render(flight_time_message, True, (255, 255, 255))
            self.screen.blit(text_surface_flight_time, (10, base_y + (i+2) * 20))
            self.screen.blit(text_surface_battery, (10, base_y + (i+5) * 20))

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

        if pygame.mouse.get_pressed()[0]:  # Left click
            if (column, row) not in self.drone_positions:
                self.mission_matrix[row][column] = 1 - self.mission_matrix[row][column]
        elif pygame.mouse.get_pressed()[2]:  # Right click
            if (column, row) in self.drone_positions:
                self.drone_positions.remove((column, row))
            else:
                self.drone_positions.append((column, row))

    def find_least_cost_mission(self, combined_cost_matrix, assigned_missions):
        if not combined_cost_matrix:
            print("No missions to assign.")
            return

        cost_array = np.array(combined_cost_matrix)
        row_indices, col_indices = linear_sum_assignment(cost_array)

        if len(row_indices) == 0 or len(col_indices) == 0:
            print("No assignment found.")
            return

        total_cost = cost_array[row_indices, col_indices].sum()
        print(f"Minimum total cost: {total_cost}")

        assigned_tasks = {}

        for i, (drone_index, mission_index) in enumerate(zip(row_indices, col_indices)):
            drone_id = drone_index + 1
            mission_number = mission_index + 1
            print(f"Drone {drone_id} assigned to mission {mission_number}.")
            assigned_tasks[drone_id] = mission_number

        return assigned_tasks

    def run(self):
        # Her bir görevi numaralandır
        task_number = 1
        for row in range(len(self.mission_matrix)):
            for col in range(len(self.mission_matrix[row])):
                if self.mission_matrix[row][col] == 1:
                    self.mission_matrix[row][col] = f"Task {task_number}"
                    task_number += 1

        # Her bir dronu oluştur ve kendi maliyet matrisini hesapla
        self.drones = [Drone(pos, self.mission_matrix, self.gif_path, self.assigned_missions) for pos in self.drone_positions]
        # Ardından, her bir dronun kendi maliyet matrisini diğer dronlarla paylaşmasını sağla
        for drone in self.drones:
            drone.calculate_cost_matrix(self.mission_matrix, drone.position, drone.battery_level, self.drones)

        # Birleştirilmiş maliyet matrisini oluştur
        combined_cost_matrix = []

# Drone ID'si 1'den başlayarak her bir drone için cost matrisindeki değerleri tek bir satıra ekleyelim
        for drone_id in range(1, len(self.drones) + 1):
            combined_row = []

            # Her bir dronun cost matrisindeki değerleri tek tek inceleyip, sonsuzdan farklı olanları combined cost matrisine ekleyelim
            for drone in self.drones:
                if drone.id == drone_id:
                    for row_index in range(len(drone.cost_matrix)):
                        row = drone.cost_matrix[row_index]
                        if any(value != float('inf') for value in row):
                            combined_row.extend([value for value in row if value != float('inf')])

    # Eğer bu drone için bir maliyet bulunduysa, combined cost matrisine ekleyelim
            if combined_row:
                combined_cost_matrix.append(combined_row)


        # Maliyet matrisini ekrana yazdır
        print("Combined Cost Matrix:")
        for row in combined_cost_matrix:
            print(row)
        print()

        assigned_positions = self.find_least_cost_mission(combined_cost_matrix, self.assigned_missions)
        print("Assigned positions:", assigned_positions) 

        row_indices = [drone_id - 1 for drone_id in assigned_positions.keys()]
        col_indices = [task_number - 1 for task_number in assigned_positions.values()]

        # cost_array'i yeniden oluşturalım
        cost_array = np.array(combined_cost_matrix)

        # Doğru parametreleri ileterek linear_sum_assignment fonksiyonunu çağıralım
        row_indices, col_indices = linear_sum_assignment(cost_array[row_indices][:, col_indices])


        if assigned_positions is not None:
            row_indices = [drone_id - 1 for drone_id in assigned_positions.keys()]
            col_indices = [task_number - 1 for task_number in assigned_positions.values()]
            # Toplam maliyeti hesapla
            total_cost = sum(combined_cost_matrix[row][col] for row, col in zip(row_indices, col_indices))
            print(f"Minimum total cost: {total_cost}")

            # Her bir dronun hangi göreve atandığını ekrana yazdır
            for i, (drone_index, mission_index) in enumerate(zip(row_indices, col_indices)):
                print(f"Drone {drone_index + 1} assigned to mission {mission_index + 1}.")

        # Her bir dronun ayrı ayrı maliyet matrisini ekrana yazdır
        for drone in self.drones:
            drone.print_cost_matrix()

        running = True
        while running:
            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.update_drones()

            debug_messages = [
                f'Chosen Missions: {self.assigned_missions}',
                f'Mission Matrix: {self.mission_matrix}'
            ]
            self.display_debug_info(debug_messages)

            pygame.display.flip()
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        

    def update_drones(self):
        current_time = pygame.time.get_ticks() / 1000
        for drone in self.drones:
            if not drone.at_destination and current_time - drone.last_move_time >= 1:
                # Burada move_towards_target metodunu çağırırken eksik argümanları veriyor olabilirsiniz
                # Bu nedenle, move_towards_target metodunu çağırırken eksik olan argümanları ekleyelim
                drone.move_towards_target(self.assigned_missions, self.mission_matrix)
                drone.last_move_time = current_time

            x, y = drone.position
            grid_width, grid_height = self.size[0] // self.grid_cols, (self.size[1] - self.debug_area_height) // self.grid_rows
            drone_screen_x = x * grid_width
            drone_screen_y = y * grid_height
            drone.gif_animation.render(self.screen, (drone_screen_x, drone_screen_y))

# To run the simulation
sim = DroneSimulation()
sim.setup_simulation()
sim.run()