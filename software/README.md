# Cargo Drone Swarm Project

This repository contains the Python code for a Cargo Drone Swarm simulation project developed as a graduation project. The simulation uses DJI Tello drones and is built with Python and Pygame. The project models the behavior of drones as they navigate a grid to complete assigned missions, optimizing their paths based on various cost metrics.

## Project Overview

The Cargo Drone Swarm project simulates a fleet of autonomous drones that navigate through a defined grid area to perform missions. Each drone in the swarm can communicate its calculated cost matrix with others to optimize mission assignments based on distance, battery levels, and other factors. The simulation visualizes the movement of drones and mission completion in real-time.

## Features

- Drone movement simulation in a grid-based environment.
- Dynamic cost matrix calculation for mission assignments.
- Real-time battery level and flight time tracking.
- Interactive grid where missions can be added or removed during simulation.

## Prerequisites

Before running the simulation, ensure you have the following installed:
- Python 3.8 or higher
- Pygame
- Additional libraries as required (e.g., gif_pygame for GIF animations)

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/cargo-drone-swarm.git
cd cargo-drone-swarm
```

Install the required Python libraries:

```bash
pip install pygame
pip install gif_pygame
```

## Usage

To start the simulation, run the following command from the project directory:

```bash
python drone_simulation.py
```

Use the mouse to interact with the simulation:

- Left-click on a grid cell to toggle mission assignments.
- Right-click to place or remove drones from the grid.

Press Enter to start the simulation after setting up the initial state.

## Configuration

The DroneSimulation class can be configured with different grid sizes and drone parameters. Modify the DroneSimulation constructor in the drone_simulation.py file to change the simulation settings.