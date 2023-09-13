
<h1 style="text-align: center;"> Indoor Cargo System </p>

![alt text](banner.png "Title")

# Table of Contents

- [Topics](#topics)

- [Introduction](#introduction)

- [System Design](#system-design)

    - [Hardware](#hardware-block-diagram)

    - [Firmware](#firmware)

    - [Software](#software)
    

    - [Core Module](#core-module-image-processing-and-control)

    - [Communication](#communication)


- [Challenges](#challenges)

- [Resources](#resources)

<br>
<br>
<br>

# Mentioned Subjects

- Indoor Positioning

- UWB Technology

- Time Difference of Arrival (TDoA)

- Computer Vision

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
<br>
<br>
<br>
<br>


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

#### Data Channels

- Positional Data Channel (PDC): This channel is dedicated to transmitting real-time positional data from the DJI Tello drones to the central control unit (typically a PC). It carries critical information regarding the drone's location, altitude, orientation, and velocity, all obtained through the integrated UWB positioning system. The PDC ensures that the control unit has up-to-date information for accurate navigation and cargo transport.

- Camera Image Data Channel (CIDC): The CIDC facilitates the transfer of live camera images from the DJI Tello drones to the control unit. These images are essential for the computer vision module to detect and identify objects, especially individuals, within the operational environment. The high-resolution imagery allows for real-time analysis and decision-making.

- Control Feedback Channel (CFC): In a bidirectional manner, the CFC enables the control unit to send control commands and receive feedback from the drones. This channel plays a crucial role in maintaining constant communication with the drones, allowing for dynamic adjustments to their routes, speeds, and cargo handling, ensuring efficient cargo transport.


#### Control Channels

- Command Control Channel (CCC): The CCC serves as the primary channel for sending control commands from the central control unit to the DJI Tello drones. Commands include take-off, landing, navigation waypoints, cargo pickup and delivery instructions, and emergency stop commands. It ensures precise control over the drones' actions, ensuring they operate seamlessly within the indoor environment.

- Obstacle Avoidance Control Channel (OACC): To enhance safety during navigation, the OACC provides real-time obstacle detection and avoidance instructions. It allows the control unit to alert the drones of potential obstacles in their path and provides guidance on alternative routes or actions to avoid collisions.

- Emergency Control Channel (ECC): In unforeseen circumstances or emergencies, the ECC provides a direct channel for issuing immediate stop and emergency landing commands to the drones. This channel prioritizes safety and allows the control unit to react swiftly to unexpected situations.



# Challenges

The primary challenge of this project is to implement a robust and accurate indoor positioning system using Ultra-Wideband (UWB) technology to guide DJI Tello drones within confined indoor spaces. Specifically, this involves:

- UWB Module Integration: Integrating UWB modules with DJI Tello drones to enable precise location tracking and navigation capabilities. These modules will provide sub-centimeter accuracy in determining the drones' positions within the indoor environment.

- Positional Data Transmission: Establishing a reliable data channel for the real-time transmission of positional data from the UWB-equipped drones to the central control unit. This data will include information such as the drone's XYZ coordinates, orientation, and velocity, allowing for continuous monitoring and control.

- Obstacle Avoidance: Implementing algorithms and control mechanisms to leverage UWB data for obstacle avoidance. This involves detecting obstacles in the drones' flight path and adjusting their trajectories to avoid collisions while maintaining cargo transport efficiency.

- Adaptation to Dynamic Environments: Addressing the challenges posed by dynamic indoor environments where obstacles may move or change position. The system must be capable of real-time adjustments to account for such changes and ensure safe and efficient navigation.

- Validation and Calibration: Ensuring the accuracy and reliability of the UWB positioning system through calibration and testing in different indoor scenarios. This involves fine-tuning the UWB modules and validating their performance under various conditions.

# Resources

- [Ultra-Wideband](https://en.wikipedia.org/wiki/Ultra-wideband)
- [Ultra Wideband Indoor Positioning Technologies: Analysis and Recent Advances](https://www.mdpi.com/1424-8220/16/5/707)
- [Time Difference of Arrival](https://www.inpixon.com/technology/standards/time-difference-of-arrival)
- [ESP32 UWB Indoor Positioning Test](https://www.instructables.com/ESP32-UWB-Indoor-Positioning-Test/)
- [ESP32 DW1000 UWB Indoor Location Positioning System](https://how2electronics.com/esp32-dw1000-uwb-indoor-location-positioning-system/)
- [Artificial Intelligence with Python Computer Vision](https://www.tutorialspoint.com/artificial_intelligence_with_python/artificial_intelligence_with_python_computer_vision.htm)
- [Tello Programming](https://tello.oneoffcoder.com/index.html)