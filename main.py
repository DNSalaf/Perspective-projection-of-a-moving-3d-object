import sys

from PyQt5.QtWidgets import QApplication
from controllers.MainController import MainController
from models.Actor import Actor
from models.Camera import Camera
from views.main.MainView import MainView


class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        # Setup Actors
        camera = Camera()
        actor = Actor(mesh_path='/home/alaf/Downloads/VisaoComp1-master/public/stl/link.STL')

        # Setup Controllers
        main_controller = MainController(
            actor=actor,
            camera=camera
        )

        # Setup Views
        self.main_view = MainView(controller=main_controller)
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
