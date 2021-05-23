import numpy as np
from mpl_toolkits.mplot3d import art3d
from stl import mesh

from models.Object import Object


class Actor(Object):
    def __init__(
            self,
            mesh_path: str,
            coordinate: np.ndarray = None,
    ):
        # Obtains the actor mesh vectors and points
        object_mesh = mesh.Mesh.from_file(mesh_path)
        x = object_mesh.x.flatten()
        y = object_mesh.y.flatten()
        z = object_mesh.z.flatten()
        self.mesh_vectors = object_mesh.vectors
        self.mesh_matrix = np.array([x.T, y.T, z.T, np.ones(x.size)])

        # Init object
        super().__init__(coordinate=coordinate)

    def draw(self, plot_axis):
        # Draws the actor mesh surfaces and lines
        plot_axis.plot(self.mesh_matrix[0, :], self.mesh_matrix[1, :], self.mesh_matrix[2, :], 'b')
        # plot_axis.add_collection3d(art3d.Poly3DCollection(self.mesh_vectors))
        # plot_axis.add_collection3d(art3d.Line3DCollection(
        #     self.mesh_vectors,
        #     colors='k',
        #     linewidths=0.2,
        #     linestyles='-'
        # ))

        # Draws the object axis
        super().draw(plot_axis)

    def move(
            self,
            movement_matrix: np.ndarray = None,
    ):
        # Updates the actor mesh matrix
        self.mesh_matrix = np.dot(movement_matrix, self.mesh_matrix)

        # Updates the actor axis coordinates
        super().move(movement_matrix=movement_matrix)
