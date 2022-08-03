from typing import Union, Tuple, List

from PyQt5.QtWidgets import QPushButton
from qgis.core import QgsMessageLog

from .ui_dock_tab_loader import DockTabLoader
from ....core.march_calculation import MarchCalculation
from ....core.march_calculation_without_tank import MarchCalculationWithoutTank
from ....core.data.data_manager import ProjectDataManager
from .ui_dock_tab_base import DockTab
from ...ui_rep_entrance_data import RepEntranceDataUI


class DockTabEditButtonBase(DockTabLoader):
    title = 'SaniHUB DWATS'

    def __init__(self, dock):
        super().__init__(dock)

        self.rep_entrance_data = RepEntranceDataUI()
        self.pb_edit_data = QPushButton()
        self.pb_edit_data.clicked.connect(self.edit_data_clicked)
        self.rep_entrance_data.pb_saveEditEnt.clicked.connect(self.save_button_clicked)

    @property
    @classmethod
    def EDIT_DATA_RANGE(cls) -> Union[Tuple[int], List[int]]:
        raise NotImplementedError

    def tab_start_ui(self):
        raise NotImplementedError

    def edit_data_clicked(self):
        self.rep_entrance_data.showReportEntrance(self.EDIT_DATA_RANGE)

    def save_button_clicked(self):
        if self.rep_entrance_data.saveChanges():
            ProjectDataManager.save_project_data(self.rep_entrance_data.entrance)
            self.dock_reload()
            
    def load_edit_button(self):
        project_data = ProjectDataManager.get_project_data()
        if project_data is None:
            self.pb_edit_data.setEnabled(False)
            return
        project_config = ProjectDataManager.get_project_config()

        self.pb_edit_data.setEnabled(True)
        self.rep_entrance_data.loadReportEntrance(project_data,
                                                  project_config.has_sedimentation_tank,
                                                  project_config.should_import_rede_basica,
                                                  self.title)
