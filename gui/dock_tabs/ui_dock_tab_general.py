from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsMessageLog

from ...core.data.data_manager import ProjectDataManager
from .view.ui_dock_tab_general_base import DockTabGeneralBase
from ...core.data.images_manager import ImagesPathManager


class DockTabGeneral(DockTabGeneralBase):
    def load_data(self):
        self.load_data_from_database()
        self.load_edit_button()
        self.load_gas()
        self.load_areas()
        self.load_images()

    def reload(self):
        self.load_data()

    def load_gas(self):
        if self.calculation is None:
            self.lb_vazao_value.setText('0 ' + self.tr('m³/dia'))
            self.lb_co2_emission_value.setText('0 ' + self.tr('kg CO2e/dia'))
            return

        self.lb_vazao_value.setText(
            self.utils.formatNum2Dec(self.calculation.getDailyFlowBiogas()) + self.tr(' m³/dia'))
        self.lb_co2_emission_value.setText(
            self.utils.formatNum2Dec(self.calculation.getEmissionGasCarbonicEquivalentDaily()) + self.tr(
                ' kg CO2e/dia'))

    def load_areas(self):
        if self.calculation is None:
            self.lb_area_value.setText('0 ' + self.tr('m²'))
            self.lb_usable_area_value.setText('0 ' + self.tr('m²'))
            return

        self.lb_area_value.setText(
            self.utils.formatNum1Dec(self.calculation.getConstructedAreaTotal()) + self.tr(' m²'))
        self.lb_usable_area_value.setText(
            self.utils.formatNum1Dec(self.calculation.getAreaUtilTotal()) + self.tr(' m²'))
        if ProjectDataManager.get_project_config().should_calculate_area == False:
            self.lb_area.hide()
            self.lb_area_value.hide()
        else:
            self.lb_area.show()
            self.lb_area_value.show()

    def load_images(self):
        self.images_stack_widget.clear()
        if self.project_config is None or self.project_data is None:
            return

        # Retrieves a dictionary with all dock-images paths
        manager = ImagesPathManager(n_compart=self.project_data.numCompartRac,
                                    has_sedimentation_tank=self.project_config.has_sedimentation_tank)
        paths = manager.get_dock_images().values()

        # Creates n widgets for the images and define the pixmaps
        img_widgets = [QLabel() for _ in range(len(paths))]
        pixmaps = [QPixmap(path) for path in paths]
        app = QApplication.instance()
        allScreen = app.primaryScreen()
        geometry = allScreen.availableGeometry()
        for i in range(len(pixmaps)):
            pixmaps[i] = pixmaps[i].scaledToWidth(geometry.width() / 5.0, Qt.SmoothTransformation)

        # Inserts the images into the widgets and add them to the widget stack
        for img_widget, pixmap in zip(img_widgets, pixmaps):
            img_widget.setPixmap(pixmap)
            self.images_stack_widget.add_widget(img_widget)
