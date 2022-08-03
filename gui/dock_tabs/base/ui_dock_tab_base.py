from PyQt5.QtWidgets import QWidget, QPushButton

from ....utils.utils import Utils


class DockTab(QWidget):
    """
        The base class of all dock tabs.
    """
    def __init__(self, dock):
        super().__init__()
        self.dock = dock
        self.utils = Utils()
        self.should_reload = False  # Usado pelo dock para recarregar as abas quando necessário.

    def dock_reload(self):
        self.reload()
        self.dock.reload()

    def tab_start_ui(self):
        """Method called within dock to start and setup the tab ui. All tabs must implement this and
        load their layout."""
        raise NotImplementedError

    def load_data(self):
        """Method called when generating the GUI, we load the information from the database and insert it in the tab."""
        pass

    def set_logic(self):
        """Method called to define user input logic."""
        pass

    def reload(self):
        """ Method called by the dock to reload tab information, based on current project data."""
        pass
