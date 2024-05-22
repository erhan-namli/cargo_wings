# Communication Structure

## Tello Agent JSON Messages

| Purpose                   | Destination IP | Message Type               | Key Fields                                                                                         |
|---------------------------|----------------|----------------------------|----------------------------------------------------------------------------------------------------|
| Status Information        | 192.168.1.255  | status_information         | least_cost_mission: "None"<br>ip_address: drone_ip_address<br>status: "WAITING"<br>traffic: "broadcast" |
| Drone Mission Information | 192.168.1.255  | drone_mission_information  | name: ""<br>least_cost_mission: least_cost_mission<br>ip_address: drone_ip_address<br>status: "WAITING"<br>traffic: "broadcast" |
| Mission Completed         | 192.168.1.255  | mission_completed          | tello_name: "TELLO-B5997E"                                                                         |
| QR Code Check             | 192.168.1.255  | qr_code_check              | tello_name: "TELLO-B5997E"                                                                         |
| Battery Status            | 192.168.1.255  | battery_status             | tello_name: "TELLO-B5997E"<br>battery_level: "75%"                                                 |
| GPS Location Update       | 192.168.1.255  | gps_update                 | tello_name: "TELLO-B5997E"<br>latitude: "37.7749"<br>longitude: "-122.4194"                        |

## Ground Control JSON Messages

| Purpose                       | Destination IP | Message Type                           | Key Fields                                                                                     |
|-------------------------------|----------------|----------------------------------------|------------------------------------------------------------------------------------------------|
| Start Mission Information     | ip_address     | ground_start_mission_information       | mission_matrix: self.mission_matrix<br>command: "start"<br>traffic: "broadcast"                |
| Information Wait Command      | ip_address     | info                                   | mission_matrix: self.mission_matrix<br>command: "wait"                                         |
| Mission Status Update         | ip_address     | mission_status                         | mission_id: "12345"<br>status: "in_progress"                                                   |
| Emergency Stop Command        | ip_address     | emergency_stop                         | mission_id: "12345"<br>reason: "obstacle_detected"                                             |
| Data Request                  | ip_address     | data_request                           | request_type: "sensor_data"<br>time_range: "last_5_minutes"                                    |
| Configuration Update          | ip_address     | config_update                          | config_id: "67890"<br>new_settings: { "max_speed": "10m/s", "altitude_limit": "30m" }           |
