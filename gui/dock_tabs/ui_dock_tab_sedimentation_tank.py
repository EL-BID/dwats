from PyQt5.QtGui import QPixmap

from ...core.march_calculation import MarchCalculation
from .view.ui_dock_tab_sedimentation_tank_base import DockTabSedimentationTankBase
from ...core.data.data_manager import ProjectDataManager
from ...core.data.images_manager import ImagesPathManager


class DockTabSedimentationTank(DockTabSedimentationTankBase):
    def load_data(self):
        self.load_data_from_database()
        self.load_edit_button()
        self.load_tank_info()
        self.load_images()

    def load_tank_info(self):
        if self.project_data is None or self.project_config is None or not self.project_config.has_sedimentation_tank:
            self.lb_length_value.setText('0' + self.tr(' m'))
            self.lb_volume_value.setText('0' + self.tr(' m³'))
            self.lb_width_tank_value.setText('0' + self.tr(' m'))
            self.lb_depth_tank_value.setText('0' + self.tr(' m'))
            return

        self.lb_length_value.setText(
            self.utils.formatNum1Dec(self.calculation.getLengthTankSedimentation()) + self.tr(' m'))
        self.lb_volume_value.setText(
            self.utils.formatNum1Dec(self.calculation.getVolumeTankSedimentation()) + self.tr(' m³'))
        self.lb_width_tank_value.setText(self.utils.formatNum1Dec(self.project_data.getWidthTank()) + self.tr(' m'))
        self.lb_depth_tank_value.setText(self.utils.formatNum1Dec(self.project_data.getDepthTank()) + self.tr(' m'))

    def load_images(self):
        if self.project_data is None or self.project_config is None:
            return
        images_manager = ImagesPathManager(n_compart=self.project_data.numCompartRac,
                                           has_sedimentation_tank=self.project_config.has_sedimentation_tank)
        path_tank = images_manager.get_dock_images()['corteBB']
        self.lb_tank_image.setPixmap(QPixmap(path_tank))

    def reload(self):
        self.load_data()
