from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QGroupBox, QLabel, QGridLayout

from ..base.ui_dock_tab_edit_button_base import DockTabEditButtonBase
from ...ui_rep_entrance_data import RepEntranceDataUI


class DockTabSedimentationTankBase(DockTabEditButtonBase):
    EDIT_DATA_RANGE = RepEntranceDataUI.RANGE_SEDIMENTATION_TANK_DATA

    # We must rewrite the tr method, because at runtime, the default self.translate calls within the context of the
    # inherited child class, however, pylupdate reads the python file without executing it, putting the context in
    # translation as the parent class
    # noinspection PyMethodMayBeStatic
    def translate(self, msg, disambiguation=None, n=-1):
        return QCoreApplication.translate(DockTabSedimentationTankBase.__name__, msg, disambiguation, n)

    def __init__(self, dock):
        super().__init__(dock)
        self.vb_main_layout = QVBoxLayout()
        self.gb_tank_data = QGroupBox()
        self.lb_length = QLabel()
        self.lb_length_value = QLabel()
        self.gl_data_tank = QGridLayout()
        self.lb_volume = QLabel()
        self.lb_volume_value = QLabel()
        self.lb_width_tank = QLabel()
        self.lb_width_tank_value = QLabel()
        self.lb_depth_tank = QLabel()
        self.lb_depth_tank_value = QLabel()
        self.lb_tank_image = QLabel()
        self.gl_tank_image = QGridLayout()
        self.gb_tank_image = QGroupBox()
        self.set_logic()

    def tab_start_ui(self):
        self.pb_edit_data.setText(self.translate('Editar dados'))
        self.pb_edit_data.setFixedSize(100, 25)
        self.vb_main_layout.addWidget(self.pb_edit_data)

        self.gb_tank_data.setTitle(self.translate('Parâmetros calculados:'))
        self.lb_length.setText(self.translate('Comprimento do tanque de sedimentação'))
        self.lb_length.setWordWrap(True)
        self.lb_length_value.setText('0 ' + self.translate('m'))
        self.lb_length_value.setFont(self.utils.formatBoldText())
        self.gl_data_tank.addWidget(self.lb_length, 0, 0)
        self.gl_data_tank.addWidget(self.lb_length_value, 0, 1, Qt.AlignLeft)
        self.lb_volume.setText(self.translate('Volume do tanque de sedimentação'))
        self.lb_volume.setWordWrap(True)
        self.lb_volume_value.setText('0 ' + self.translate('m³'))
        self.lb_volume_value.setFont(self.utils.formatBoldText())
        self.gl_data_tank.addWidget(self.lb_volume, 1, 0)
        self.gl_data_tank.addWidget(self.lb_volume_value, 1, 1, Qt.AlignLeft)

        self.lb_width_tank.setText(self.translate('Largura do tanque de sedimentação'))
        self.lb_width_tank.setWordWrap(True)
        self.lb_width_tank_value.setText('0 ' + self.translate(' m'))
        self.lb_width_tank_value.setFont(self.utils.formatBoldText())
        self.gl_data_tank.addWidget(self.lb_width_tank, 2, 0)
        self.gl_data_tank.addWidget(self.lb_width_tank_value, 2, 1, Qt.AlignLeft)

        self.lb_depth_tank.setText(self.translate('Altura útil do tanque de sedimentação'))
        self.lb_depth_tank.setWordWrap(True)
        self.lb_depth_tank_value.setText('0 ' + self.translate('m'))
        self.lb_depth_tank_value.setFont(self.utils.formatBoldText())
        self.gl_data_tank.addWidget(self.lb_depth_tank, 3, 0)
        self.gl_data_tank.addWidget(self.lb_depth_tank_value, 3, 1, Qt.AlignLeft)

        self.gl_data_tank.setVerticalSpacing(10)
        self.gl_data_tank.setColumnMinimumWidth(1, 2)
        self.gb_tank_data.setLayout(self.gl_data_tank)
        self.vb_main_layout.addWidget(self.gb_tank_data)
        self.gl_tank_image.addWidget(self.lb_tank_image, 0, 0, 1, 2, Qt.AlignHCenter)
        self.gb_tank_image.setLayout(self.gl_tank_image)
        self.vb_main_layout.addWidget(self.gb_tank_image)
        self.vb_main_layout.addStretch()
        self.setLayout(self.vb_main_layout)
        self.load_data()
