import numpy as np


class Axis:
    def __init__(
            self,
            length: float = 10,
            base: np.ndarray = None,
            coordinate: np.ndarray = None
    ):
        if base is None:
            base = np.eye(3)
        if coordinate is None:
            coordinate = np.zeros(3)

        self.base = base
        self.length = length
        self.coordinate = coordinate

    def draw(self, plot_axis):
        plot_axis.quiver(
            self.coordinate[0],
            self.coordinate[1],
            self.coordinate[2],
            self.base[0][0],
            self.base[0][1],
            self.base[0][2],
            color='red',
            pivot='tail',
            length=self.length
        )

        plot_axis.quiver(
            self.coordinate[0],
            self.coordinate[1],
            self.coordinate[2],
            self.base[1][0],
            self.base[1][1],
            self.base[1][2],
            color='green',
            pivot='tail',
            length=self.length
        )

        plot_axis.quiver(
            self.coordinate[0],
            self.coordinate[1],
            self.coordinate[2],
            self.base[2][0],
            self.base[2][1],
            self.base[2][2],
            color='blue',
            pivot='tail',
            length=self.length
        )
