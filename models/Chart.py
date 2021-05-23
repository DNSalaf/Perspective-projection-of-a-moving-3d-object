import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
matplotlib.use('Qt5Agg')


class Chart(FigureCanvas):

    def __init__(
        self,
        width: int = 10,
        height: int = 10,
        dpi: int = 100,
        projection: str = None,
        title: str = None,
        ion: bool = False,
        aspect: str = None
    ):
        fig = plt.figure(figsize=(width, height), dpi=dpi)
        if title is not None:
            plt.title(title)
        if ion:
            plt.ion()

        axis = plt.axes(projection=projection)

        self.axis = axis
        super().__init__(fig)

        if aspect == 'equal':
            self.__axis_equal_3D()
        elif aspect is not None:
            self.axis.set_aspect(aspect)

    def axis_equal(self):
        if self.axis.name == '3d':
            self.__axis_equal_3D()
        else:
            self.axis.set_aspect('equal')

    def __axis_equal_3D(self):
        extents = np.array([getattr(self.axis, 'get_{}lim'.format(dim))() for dim in 'xyz'])
        sz = extents[:, 1] - extents[:, 0]
        centers = np.mean(extents, axis=1)
        maxsize = max(abs(sz))
        r = maxsize / 2
        for ctr, dim in zip(centers, 'xyz'):
            getattr(self.axis, 'set_{}lim'.format(dim))(ctr - r, ctr + r)
