# Drone Control System for Mission Optimization

This repository contains the code for a drone control system designed for mission optimization using Raspberry Pi Zero devices. The system includes both ground control and drone agent functionalities, allowing for mission distribution, drone control, and communication over a network.

## System Overview

The system operates with a ground control server sending mission maps to all connected Raspberry Pi Zero devices. Each drone calculates its cost matrix upon receiving the mission map. Drones then autonomously take off to complete the assigned mission with the lowest cost. Upon completion, drones switch to ad-hoc network mode to allow ground control direct access for camera image processing and QR code scanning.

## Features

- **Mission Distribution**: Ground control broadcasts the mission map to all drones.
- **Cost Calculation**: Drones calculate a cost matrix to determine the most efficient mission to undertake.
- **Ad-hoc Networking**: Post-mission, drones switch to ad-hoc mode for direct communication with ground control.
- **QR Code Scanning**: Ground control can access drone cameras to scan QR codes.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.9 or newer
- PyQt5
- OpenCV for Python
- djitellopy library for controlling DJI Tello drones
- pyzbar for QR code decoding

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/drone-control-system.git
   cd drone-control-system

2. Install the required dependencies:

```bash
pip install PyQt5 opencv-python-headless djitellopy pyzbar
```

## Usage

### Ground Control
To start the ground control interface, run:

```bash
python ground_control.py
```

### Drone Agent
On each Raspberry Pi Zero, run:

```bash
python agent_control.py
```