import numpy as np

from models.Axis import Axis


class Object:
    def __init__(
            self,
            coordinate: np.ndarray = None
    ):
        if coordinate is None:
            coordinate = np.zeros(3)

        self.coordinate = coordinate
        self.axis = Axis(coordinate=coordinate)
        self.previous_movement_matrix = np.eye(4)

    def draw(self, plot_axis):
        # Draws the object axis
        self.axis.draw(plot_axis)

    def move(
            self,
            movement_matrix: np.ndarray
    ):
        # Updates the current object position according to the movement matrix
        coordinate = np.ones(4)
        coordinate[0:3] = self.coordinate
        coordinate = np.dot(movement_matrix, coordinate.T)
        self.coordinate = coordinate[0: 3]

        # Updates the axis base and coordinate as well
        self.axis.coordinate = coordinate[0: 3]
        self.axis.base = movement_matrix[0:3, 0:3]

        # Stores the previous movement made
        self.previous_movement_matrix = movement_matrix
