import vtk
import numpy as np

class DroneSimulator:
    def __init__(self, mission_matrix):
        self.mission_matrix = mission_matrix
        self.rows = len(mission_matrix)
        self.cols = len(mission_matrix[0])
        self.drone_pos = np.array([0.0, 0.0])
        self.drone_speed = 0.1

        # Create the renderer and render window
        self.renderer = vtk.vtkRenderer()
        self.render_window = vtk.vtkRenderWindow()
        self.render_window.SetSize(800, 600)
        self.render_window.AddRenderer(self.renderer)

        # Create the interactor
        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.render_window)

        # Create axes
        axes_actor = vtk.vtkAxesActor()
        self.renderer.AddActor(axes_actor)

    def move_drone(self):
        current_cell_x = int(self.drone_pos[0])
        current_cell_y = int(self.drone_pos[1])

        # Find the next mission point
        for i in range(current_cell_y, self.rows):
            for j in range(current_cell_x, self.cols):
                if self.mission_matrix[i][j] == 1:
                    next_mission_point = np.array([j, i])
                    direction = next_mission_point - self.drone_pos
                    norm = np.linalg.norm(direction)
                    if norm > 0:
                        direction /= norm  # Normalize only if norm is not zero
                        self.drone_pos += direction * self.drone_speed
                    return

    def run(self):
        # Create a plane source representing the ground
        ground_plane = vtk.vtkPlaneSource()
        ground_plane.SetResolution(10, 10)
        ground_plane_mapper = vtk.vtkPolyDataMapper()
        ground_plane_mapper.SetInputConnection(ground_plane.GetOutputPort())
        ground_plane_actor = vtk.vtkActor()
        ground_plane_actor.SetMapper(ground_plane_mapper)
        ground_plane_actor.GetProperty().SetColor(0.7, 0.7, 0.7)  # Gray color for the ground
        self.renderer.AddActor(ground_plane_actor)

        # Create a sphere representing the drone
        drone_sphere = vtk.vtkSphereSource()
        drone_sphere.SetRadius(0.1)
        drone_mapper = vtk.vtkPolyDataMapper()
        drone_mapper.SetInputConnection(drone_sphere.GetOutputPort())
        self.drone_actor = vtk.vtkActor()
        self.drone_actor.SetMapper(drone_mapper)
        self.drone_actor.GetProperty().SetColor(1, 0, 0)  # Red color for the drone
        self.renderer.AddActor(self.drone_actor)

        self.render_window.Render()

        # Move the drone and update the visualization
        for _ in range(100):  # Move the drone for 100 steps
            self.move_drone()
            self.drone_actor.SetPosition(self.drone_pos[0], self.drone_pos[1], 0)
            self.render_window.Render()

        self.interactor.Start()

if __name__ == "__main__":
    # Example mission matrix
    mission_matrix = np.array([
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ])

    simulator = DroneSimulator(mission_matrix)
    simulator.run()
