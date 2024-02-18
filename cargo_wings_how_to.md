
<h1 style="text-align: center;"> Indoor Cargo System </p>

![alt text](banner.png "Title")

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Mentioned Subjects](#mentioned-subjects)
- [Introduction](#introduction)
- [Components and Key Features](#components-and-key-features)
    - [-  How to implement Machine Learning Algorithms?](#---how-to-implement-machine-learning-algorithms)
    - [How to implement Task Allocation](#how-to-implement-task-allocation)
- [System Design](#system-design)
  - [Hardware Block Diagram](#hardware-block-diagram)
    - [Hardware Components](#hardware-components)
  - [Firmware](#firmware)
    - [Technology Stack](#technology-stack)
    - [Application Layer](#application-layer)
    - [Communication Ports](#communication-ports)
    - [Drivers](#drivers)
  - [Software](#software)
    - [Technology Stack](#technology-stack-1)
    - [Application Layer](#application-layer-1)
    - [Core Module](#core-module)
  - [Communication](#communication)
      - [Data Messages](#data-messages)
      - [Control Messages](#control-messages)
- [Challenges](#challenges)
- [Resources](#resources)
- [Product Links](#product-links)
- [Price List](#price-list)

<br>
<br>
<br>
<br>
<br>
<br>
<br>

# Mentioned Subjects

- Indoor Positioning

- UWB Technology

- Time Difference of Arrival (TDoA)

- Computer Vision

- Task Allocation


<br>
<br>

# Introduction

The ever-increasing demand for innovative solutions in logistics and transportation has paved the way for the development of novel systems designed to address the challenges posed by indoor cargo transport. This university graduation project explores the integration of DJI Tello drones and Ultra-Wideband (UWB) technology to create an indoor cargo transport system, with a primary focus on achieving precise positioning and efficient navigation within confined spaces.

Project Scope:
This project centers around the concept of creating a cost-effective and adaptable indoor cargo transport system that can be employed in various indoor environments, such as warehouses, factories, and research facilities. The project's primary objectives are:

- UWB-based Indoor Positioning: To develop a reliable indoor positioning system utilizing UWB technology, which will enable the drones to navigate accurately in GPS-denied environments.

- Integration with DJI Tello Drones: To interface UWB modules with ESP32 controllers and DJI Tello drones, establishing a communication link that allows real-time data exchange and control over Wi-Fi.

- Computer Vision Integration: To implement computer vision algorithms for object detection, with a specific focus on identifying and tracking individuals within the operating environment.


Expected Outcomes:
Upon completion of this project, we anticipate achieving the following outcomes:

- A functioning indoor cargo transport system capable of accurate positioning and obstacle avoidance.
- Insights into the practical applications of UWB technology in GPS-denied environments.
- A platform for further research and development in the field of indoor logistics and automation.

# Components and Key Features

**Swarm Drone Fleet**: Develop a fleet of autonomous drones capable of indoor navigation and cargo handling. The drones should be equipped with sensors for obstacle detection and avoidance.

**Machine Learning Algorithms**: Implement machine learning models for real-time decision-making and task allocation. These models should consider factors such as cargo weight, drone battery levels, optimal path planning, and dynamic re-routing in case of obstacles.

---

### -  How to implement Machine Learning Algorithms?

- Defining the Machine Learning Objectives:

    This includes path planning, task allocation, obstacle avoidance, and communication optimization.

- Data Collection and Preprocessing:

    Gathering relevant data for training and testing your machine learning models. This could involve indoor maps, drone sensor data, communication logs, and historical task allocation data.
    Preprocess the data to make it suitable for training. This may include data cleaning, feature engineering, and data augmentation.

- Model Selection and Development:

    Choose appropriate machine learning algorithms and models for each of the defined tasks. For example:
    Path Planning: You might use reinforcement learning or deep Q-networks.
    Task Allocation: This could involve optimization algorithms, reinforcement learning, or deep learning approaches.
    Communication Optimization: Investigate techniques for adaptive communication and data transmission strategies.

- Integration with Drone System:

    Develop interfaces to integrate your machine learning models with the drone system's control software.
    Implement real-time data exchange between the drones and the central control system to enable decision-making based on model predictions.

--- 


**Non-Ideal Communication Factors**: Investigate and model the communication challenges typically encountered indoors, such as signal interference, limited bandwidth, and signal dropout. Develop strategies to mitigate these challenges and ensure reliable communication among the drones and a central control system.

**Task Allocation**: Create an intelligent task allocation algorithm that optimizes the distribution of cargo delivery tasks among the drones. This algorithm should prioritize factors like minimizing delivery time, energy efficiency, and load balancing among the drones.

---

### How to implement Task Allocation

- Defining the Task Allocation Problem:

     It's about allocating cargo delivery tasks among a swarm of drones while considering factors like minimizing delivery time, energy efficiency, and load balancing.

- Collecting Data:

    Gathering data related to the tasks to be allocated and the capabilities of the drones. This might include the location of delivery points, cargo weights, drone performance data, and battery levels.

- Objective Function:

    Create an objective function that combines the optimization objectives. For example, you can use a weighted sum of delivery time, energy consumption, and load balancing factors.

- Algorithm Selection:
    - Particle swarm optimization
    - Reinforcement learning (e.g., using deep - reinforcement learning for task allocation)
  

- Testing and Simulation


# System Design

<br>

![alt text](system_design.png "Title")

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

<br>
<br>
<br>

## Hardware Block Diagram

![alt text](hardware_block_diagram.png "Title")

### Hardware Components

- [DW1000 UWB (for Indoor Positioning)](https://datasheet.lcsc.com/lcsc/1810010514_DecaWave-DW1000-ITR7_C95490.pdf) 

- [VL53L0X Time-of-Flight Distance Sensor(for target distance mesauring)](https://www.pololu.com/file/0J1187/VL53L0X.pdf)

- [ESP32S3 (Controller)](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf)  


---

## Firmware

The firmware side responsible with communicating drones each other via WiFi and UWB Module, also sending the data of the distance sensors on the drones in the network to the control unit

### Technology Stack

- ESP-IDF
- Arduino 

### Application Layer

Baremetal firmware programming

### Communication Ports

- I2C
- UART
- SPI
- WiFi

### Drivers

- DW100 UWB Module Driver
- VL53L0X Distamce Sensor Driver

## Software
This side of the project will be responsible with processing incoming data from drones and sending control commands releted with processed data such as finding target person and target room with computer vision and indoor location positioning algorithms. 

![alt text](ui_design.png "Title")

### Technology Stack

- QT5 (Desktop App)
- Websocket (Communicating with Tello Drone)
- React (User interface library for Web App)
- Flask (Backend framework for core module communication)
- OpenCV (Image Processing)
- Tensorflow (Image Classification)

### Application Layer

*Features*

- Computer Vision System that classifies teachers
- An User Interface that interacts with Drone for manual control
- Cargo System (Starting Point, Target and Cargo) 

### Core Module 

*Features*

- Image Processing

- Classifying detected person

- Indoor Location Calculations with UWB Module

![alt text](locationing.png "Title")



## Communication
This section is about communication details for drone network and control unit network  

#### Data Messages

- Positional Data Messages (PDM): This channel is dedicated to transmitting real-time positional data from the DJI Tello drones to the central control unit (typically a PC). It carries critical information regarding the drone's location, altitude, orientation, and velocity, all obtained through the integrated UWB positioning system. The PDC ensures that the control unit has up-to-date information for accurate navigation and cargo transport.

- Camera Image Data Messages (CIDM): The CIDM facilitates the transfer of live camera images from the DJI Tello drones to the control unit. These images are essential for the computer vision module to detect and identify objects, especially individuals, within the operational environment. The high-resolution imagery allows for real-time analysis and decision-making.

- Control Feedback Messages (CFM): In a bidirectional manner, the CFM enables the control unit to send control commands and receive feedback from the drones. This channel plays a crucial role in maintaining constant communication with the drones, allowing for dynamic adjustments to their routes, speeds, and cargo handling, ensuring efficient cargo transport.


#### Control Messages

- Command Control Messages (CCM): The CCM serves as the primary channel for sending control commands from the central control unit to the DJI Tello drones. Commands include take-off, landing, navigation waypoints, cargo pickup and delivery instructions, and emergency stop commands. It ensures precise control over the drones' actions, ensuring they operate seamlessly within the indoor environment.

- Obstacle Avoidance Control Messages (OACM): To enhance safety during navigation, the OACM provides real-time obstacle detection and avoidance instructions. It allows the control unit to alert the drones of potential obstacles in their path and provides guidance on alternative routes or actions to avoid collisions.

- Emergency Control Messages (ECM): In unforeseen circumstances or emergencies, the ECM provides a direct channel for issuing immediate stop and emergency landing commands to the drones. This channel prioritizes safety and allows the control unit to react swiftly to unexpected situations.



# Challenges

The primary challenge of this project is to implement a robust and accurate indoor positioning system using Ultra-Wideband (UWB) technology to guide DJI Tello drones within confined indoor spaces. Specifically, this involves:

- UWB Module Integration: Integrating UWB modules with DJI Tello drones to enable precise location tracking and navigation capabilities. These modules will provide sub-centimeter accuracy in determining the drones' positions within the indoor environment.

- Positional Data Transmission: Establishing a reliable data channel for the real-time transmission of positional data from the UWB-equipped drones to the central control unit. This data will include information such as the drone's XYZ coordinates, orientation, and velocity, allowing for continuous monitoring and control.

- Obstacle Avoidance: Implementing algorithms and control mechanisms to leverage UWB data for obstacle avoidance. This involves detecting obstacles in the drones' flight path and adjusting their trajectories to avoid collisions while maintaining cargo transport efficiency.

- Adaptation to Dynamic Environments: Addressing the challenges posed by dynamic indoor environments where obstacles may move or change position. The system must be capable of real-time adjustments to account for such changes and ensure safe and efficient navigation.

- Validation and Calibration: Ensuring the accuracy and reliability of the UWB positioning system through calibration and testing in different indoor scenarios. This involves fine-tuning the UWB modules and validating their performance under various conditions.

# Resources

- [Real Time Location Ultra Wideband](https://iosoft.blog/2019/11/22/real-time-location-ultra-wideband/)
- [UWV with Rasperry Pi](https://medium.com/@newforestberlin/precise-realtime-indoor-localization-with-raspberry-pi-and-ultra-wideband-technology-decawave-191e4e2daa8c)
- [Ultra-Wideband](https://en.wikipedia.org/wiki/Ultra-wideband)
- [Ultra Wideband Indoor Positioning Technologies: Analysis and Recent Advances](https://www.mdpi.com/1424-8220/16/5/707)
- [Time Difference of Arrival](https://www.inpixon.com/technology/standards/time-difference-of-arrival)
- [ESP32 UWB Indoor Positioning Test](https://www.instructables.com/ESP32-UWB-Indoor-Positioning-Test/)
- [ESP32 DW1000 UWB Indoor Location Positioning System](https://how2electronics.com/esp32-dw1000-uwb-indoor-location-positioning-system/)
- [Artificial Intelligence with Python Computer Vision](https://www.tutorialspoint.com/artificial_intelligence_with_python/artificial_intelligence_with_python_computer_vision.htm)
- [Tello Programming](https://tello.oneoffcoder.com/index.html)
- [DW1000 Datasheet](https://www.qorvo.com/products/p/DWM1001-DEV)

# Product Links

- https://www.e-komponent.com/dwm1001-board-no-batteries
- https://orangepi.com/index.php?route=product/category&path=238_240
- https://market.samm.com/raspberry-pi-camera-3
- https://www.e-komponent.com/dwm1001-board-no-batteries
- https://www.robotistan.com/esp32-esp-32s-wifi-bluetooth-dual-mode-developement-board
- https://market.samm.com/raspberry-pi-icin-sim7600e-h-4g-hat-lte-cat-4
- https://www.robotistan.com/orange-pi-5b-8g64g


# Price List

![alt text](price_list.png "Title")