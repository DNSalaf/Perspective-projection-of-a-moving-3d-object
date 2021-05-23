from math import pi, cos, sin

import numpy as np

from models.Actor import Actor
from models.Axis import Axis
from models.Camera import Camera


class MainController:
    def __init__(self, actor: Actor, camera: Camera):
        self.actor = actor
        self.camera = camera
        self.world_axis = Axis()

    def update_camera_params(
            self,
            f: float = 1,
            sx: float = 1,
            sy: float = 1,
            so: float = 0,
            ox: float = 0,
            oy: float = 0,
    ):
        self.camera.f = f
        self.camera.sx = sx
        self.camera.sy = sy
        self.camera.so = so
        self.camera.ox = ox
        self.camera.oy = oy

    def move_camera(
            self,
            target_coordinate: np.ndarray = None,
            rotation_angle: float = None,
            rotation_axis: str = None,
            reference_axis: str = None
    ):
        self.move_object(
            self.camera,
            target_coordinate,
            rotation_angle,
            rotation_axis,
            reference_axis
        )

    def move_actor(
            self,
            target_coordinate: np.ndarray = None,
            rotation_angle: float = None,
            rotation_axis: str = None,
            reference_axis: str = None
    ):
        self.move_object(
            self.actor,
            target_coordinate,
            rotation_angle,
            rotation_axis,
            reference_axis
        )

    def draw_camera_view(self, plot_axis):
        plot_axis.clear()
        self.camera.get_camera_view(plot_axis, self.actor)
        plot_axis.invert_yaxis()

    def draw_world_components(self, plot_axis):
        plot_axis.clear()
        self.world_axis.draw(plot_axis)
        self.actor.draw(plot_axis)
        self.camera.draw(plot_axis)

    def move_object(
            self,
            object: [Actor, Camera],
            target_coordinate: np.ndarray = None,
            rotation_angle: float = None,
            rotation_axis: str = None,
            reference_axis: str = None
    ):
        # Sets the world axis as the default reference axis
        if reference_axis is None:
            reference_axis = 'world'

        # Sets the target point to 0, if its not declared
        if target_coordinate is None:
            target_coordinate = np.zeros(3)

        # Gets the axis thats the movement is related to
        if reference_axis == 'actor':
            axis_coordinate = self.actor.axis.coordinate
        elif reference_axis == 'camera':
            axis_coordinate = self.camera.axis.coordinate
        else:
            axis_coordinate = np.zeros(3)

        # Gets the reverse of the previous movement matrix
        reverse_movement_matrix = self.get_reverse_movement_matrix(
            movement_matrix=object.previous_movement_matrix
        )

        object.move(reverse_movement_matrix)

        # Get's the next movement matrix
        if type(object).__name__ == reference_axis.capitalize():
            # Rotates the object at his own axis
            rotation_matrix = self.get_movement_matrix(
                rotation_angle=rotation_angle,
                rotation_axis=rotation_axis
            )

            # Moves the object according to its bases
            translation_matrix = self.get_movement_matrix(target_point=target_coordinate)
            movement_matrix = np.dot(translation_matrix, rotation_matrix)
        else:
            # Moves the object back to the reference axis
            target_coordinate = np.dot(self.get_rotation_matrix(rotation_angle, rotation_axis), target_coordinate.T)
            neg_translation_matrix = self.get_movement_matrix(target_point=target_coordinate-axis_coordinate)

            # Rotates the object at the selected axis
            rotation_matrix = self.get_movement_matrix(
                rotation_angle=rotation_angle,
                rotation_axis=rotation_axis
            )

            # Moves the object to it's final position
            pos_translation_matrix = self.get_movement_matrix(target_point=axis_coordinate)

            # Gets the new movement matrix
            movement_matrix = np.linalg.multi_dot([
                pos_translation_matrix,
                rotation_matrix,
                neg_translation_matrix
            ])

        object.move(movement_matrix)

    def get_movement_matrix(
            self,
            current_point: np.ndarray = np.zeros(3),
            target_point: np.ndarray = np.zeros(3),
            rotation_angle: float = 0,
            rotation_axis: str = None,
    ):
        movement_matrix = np.eye(4)
        movement_matrix[0:3, 3] = target_point - current_point
        movement_matrix[0:3, 0:3] = self.get_rotation_matrix(rotation_angle, rotation_axis)

        return movement_matrix

    def get_rotation_matrix(
            self,
            rotation_angle: float = 0,
            rotation_axis: str = None
    ):
        # Generates the new movement matrix according to the params given
        if rotation_angle is not None:
            rotation_angle = self.__degrees_to_radians(rotation_angle)

        if rotation_axis == 'x':
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, cos(rotation_angle), -sin(rotation_angle)],
                [0, sin(rotation_angle), cos(rotation_angle)]
            ])
        elif rotation_axis == 'y':
            rotation_matrix = np.array([
                [cos(rotation_angle), 0, -sin(rotation_angle)],
                [0, 1, 0],
                [sin(rotation_angle), 0, cos(rotation_angle)]
            ])
        else:
            rotation_matrix = np.array([
                [cos(rotation_angle), -sin(rotation_angle), 0],
                [sin(rotation_angle), cos(rotation_angle), 0],
                [0, 0, 1]
            ])

        return rotation_matrix

    def get_reverse_movement_matrix(
            self,
            movement_matrix: np.ndarray
    ):
        # Generates the reverse of a movement matrix
        reverse_movement_matrix = np.eye(4)
        previous_rotation_matrix = movement_matrix[0:3, 0:3]
        previous_translation_vector = movement_matrix[0:3, 3]

        # Reverts the previous movement
        reverse_movement_matrix[0:3, 0:3] = previous_rotation_matrix.T
        reverse_movement_matrix[0:3, 3] = - np.dot(previous_rotation_matrix.T, previous_translation_vector)

        return reverse_movement_matrix

    def __degrees_to_radians(self, degrees: float):
        return pi * degrees / 180
