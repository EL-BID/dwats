from typing import Optional, Union

from ....core.data.models import *
from ....core.data.entrance_data import ProjectData
from ....core.data.data_manager import ProjectDataManager
from ....core.march_calculation import MarchCalculation
from ....core.march_calculation_without_tank import MarchCalculationWithoutTank
from .ui_dock_tab_base import DockTab


class DockTabLoader(DockTab):
    def tab_start_ui(self):
        raise NotImplementedError

    def __init__(self, dock):
        super().__init__(dock)
        self.project_data: Optional[ProjectData] = None
        self.calculation: Optional[Union[MarchCalculation, MarchCalculationWithoutTank]] = None
        self.project_config: Optional[ProjectConfig] = None
        self.project_info: Optional[ProjectInfo] = None
        self.costs: Optional[Costs] = None

    def load_data_from_database(self):
        self.project_data = None
        self.calculation = None
        self.project_config = None
        self.project_info = None
        self.costs = None

        if ProjectDataManager.is_project_config_loaded() and ProjectDataManager.is_project_data_loaded():
            self.project_config = ProjectDataManager.get_project_config()
            self.project_data = ProjectDataManager.get_project_data()
            if self.project_config.has_sedimentation_tank:
                self.calculation = MarchCalculation(ProjectDataManager.get_project_data(),
                                                    self.project_config.should_import_rede_basica)
            else:
                self.calculation = MarchCalculationWithoutTank(ProjectDataManager.get_project_data(),
                                                               self.project_config.should_import_rede_basica)

        if ProjectDataManager.is_project_info_loaded():
            self.project_info = ProjectDataManager.get_project_info()

        if ProjectDataManager.is_costs_loaded():
            self.costs = ProjectDataManager.get_project_costs_data()
