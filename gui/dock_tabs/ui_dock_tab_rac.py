from PyQt5.QtGui import QPixmap
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtCore import Qt

from ...core.data.images_manager import ImagesPathManager
from .view.ui_dock_tab_rac_base import DockTabRacBase


class DockTabRac(DockTabRacBase):
    def load_data(self):
        self.load_data_from_database()
        self.load_edit_button()
        self.load_rac_data()
        self.load_images()

    def load_rac_data(self):
        if self.project_data is None or self.calculation is None:
            self.lb_length_rac_value.setText('0 ' + self.tr('m'))
            self.lb_width_rac_value.setText('0 ' + self.tr('m'))
            self.lb_concentration_DQO_rac_value.setText('0 ' + self.tr('g/m³'))
            self.lb_efficiency_DQO_rac_value.setText('0 ' + self.tr('%'))
            self.lb_concentration_DBO_rac_value.setText('0 ' + self.tr('g/m³'))
            self.lb_efficiency_DBO_rac_value.setText('0 ' + self.tr('%'))
            return
        self.lb_length_rac_value.setText(
            self.utils.formatNum1Dec(self.calculation.getLengthCompartmentRAC()) + ' ' + self.tr('m'))
        self.lb_width_rac_value.setText(
            self.utils.formatNum1Dec(self.calculation.getWidthAdoptedCompartmentRAC()) + ' ' + self.tr('m'))
        self.lb_depth_rac_value.setText(self.utils.formatNum1Dec(self.project_data.getDepthOutRac()) + ' ' + self.tr('m'))
        self.lb_num_compart_value.setText(str(self.project_data.getNumCompartRAC()) + ' ' + self.tr('unid.'))
        self.lb_concentration_DQO_rac_value.setText(
            self.utils.formatNum2Dec(self.calculation.getConcentrationDQOEffluentFinal()) + ' ' + self.tr('g/m³'))
        self.lb_efficiency_DQO_rac_value.setText(
            self.utils.formatNum2Dec(self.calculation.getEfficiencyRemovalTotalDQOProcess() * 100) + ' ' + self.tr(
                '%'))
        self.lb_concentration_DBO_rac_value.setText(
            self.utils.formatNum2Dec(self.calculation.getConcentrationDBOEffluentFinal()) + ' ' + self.tr('g/m³'))
        self.lb_efficiency_DBO_rac_value.setText(
            self.utils.formatNum2Dec(self.calculation.getEfficiencyRemovalTotalDBOProcess() * 100) + ' ' + self.tr(
                '%'))

    def load_images(self):
        if self.project_data is None or self.project_config is None:
            return
        images_manager = ImagesPathManager(n_compart=self.project_data.numCompartRac,
                                           has_sedimentation_tank=self.project_config.has_sedimentation_tank)
        path_tank = images_manager.get_dock_images()['corteCC']
        app = QApplication.instance()
        allScreen = app.primaryScreen()
        geometry = allScreen.availableGeometry()
        img_pixmap = QPixmap(path_tank)
        img_pixmap = img_pixmap.scaledToWidth(geometry.width()/5.8, Qt.SmoothTransformation)
        self.lb_image_rac.setPixmap(img_pixmap)

    def reload(self):
        self.load_data()
