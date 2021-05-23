import numpy as np
from models.Actor import Actor
from models.Object import Object


class Camera(Object):

    def __init__(
            self,
            f: float = 1,
            sx: float = 1,
            sy: float = 1,
            so: float = 0,
            ox: float = 0,
            oy: float = 0,
            coordinate: np.ndarray = None
    ):
        self.f = f
        self.sx = sx
        self.sy = sy
        self.so = so
        self.ox = ox
        self.oy = oy

        # Adds the camera mesh
        self.mesh_matrix = np.array([
            [-5, -5, 0, 1],
            [-5, 5, 0, 1],
            [-5, 5, 5, 1],
            [-5, 5, 0, 1],
            [5, 5, 0, 1],
            [5, 5, 5, 1],
            [5, 5, 0, 1],
            [5, -5, 0, 1],
            [5, -5, 5, 1],
            [5, -5, 0, 1],
            [-5, -5, 0, 1],
            [-5, -5, 5, 1],
            [-5, 5, 5, 1],
            [5, 5, 5, 1],
            [5, -5, 5, 1],
            [-5, -5, 5, 1],
        ]).T

        super().__init__(coordinate)

    def move(
            self,
            movement_matrix: np.ndarray
    ):
        # Moves the camera mesh
        self.mesh_matrix = np.dot(movement_matrix, self.mesh_matrix)

        # Moves the actor axis
        super().move(movement_matrix)

    def draw(self, plot_axis):
        # Updates the camera mesh matrix
        plot_axis.plot(self.mesh_matrix[0, :], self.mesh_matrix[1, :], self.mesh_matrix[2, :], 'b')

        # Draws the camera axis
        super().draw(plot_axis)

    def get_camera_view(self, plot_axis, actor: Actor):
        # Plotting the 2D image projection from the camera point of view
        intrinsic_parameter_matrix = self.get_intrinsic_parameter_matrix()
        projection_matrix = np.zeros([3, 4])
        projection_matrix[0:3, 0:3] = np.eye(3)

        # Projects the actor at a 2D plane
        projected_actor = np.zeros([3, actor.mesh_matrix.shape[1]])
        for index in range(projected_actor.shape[1]):
            point_coordinate = np.ones(4)
            point_coordinate[0:3] = actor.mesh_matrix[0:3, index] - self.axis.coordinate
            point_coordinate[0:3] = np.dot(self.axis.base, point_coordinate[0:3].T)
            z = point_coordinate[2]
            if z <= 0:
                continue

            projected_point = np.linalg.multi_dot([
                intrinsic_parameter_matrix,
                projection_matrix,
                point_coordinate.T
            ])
            projected_actor[:, index] = projected_point / z

        # Draws the camera view at the corresponding axis
        plot_axis.plot(projected_actor[0, :], projected_actor[1, :], 'b')
        plot_axis.set_xlim([-10, 10])
        plot_axis.set_ylim([-10, 10])

    def get_intrinsic_parameter_matrix(self):
        return np.array([
            [(self.f * self.sx), (self.f * self.so), self.ox],
            [0, (self.f * self.sy), self.oy],
            [0, 0, 1]
        ])