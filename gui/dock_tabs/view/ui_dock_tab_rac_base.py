from typing import Union, Tuple, List

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QLabel, QGroupBox, QVBoxLayout, QGridLayout

from ..base.ui_dock_tab_edit_button_base import DockTabEditButtonBase
from ...ui_rep_entrance_data import RepEntranceDataUI


class DockTabRacBase(DockTabEditButtonBase):
    EDIT_DATA_RANGE = RepEntranceDataUI.RANGE_RAC_DATA

    # We must rewrite the tr method, because at runtime, the default self.translate calls within the context of the
    # inherited child class, however, pylupdate reads the python file without executing it, putting the context in
    # translation as the parent class
    # noinspection PyMethodMayBeStatic
    def translate(self, msg, disambiguation=None, n=-1):
        return QCoreApplication.translate(DockTabRacBase.__name__, msg, disambiguation, n)

    def __init__(self, dock):
        super().__init__(dock)
        self.gb_rac_data = QGroupBox()
        self.vb_main_layout = QVBoxLayout()
        self.lb_lengthRac = QLabel()
        self.lb_length_rac_value = QLabel()
        self.gl_rac_data = QGridLayout()
        self.lb_width_rac_value = QLabel()
        self.lb_depth_rac_value = QLabel()
        self.lb_num_compart_value = QLabel()
        self.lb_concentration_DQO_rac_value = QLabel()
        self.lb_efficiency_DQO_rac_value = QLabel()
        self.lb_concentration_DBO_rac_value = QLabel()
        self.lb_efficiency_DBO_rac_value = QLabel()
        self.gl_image_rac = QGridLayout()
        self.gb_image_rac = QGroupBox()
        self.lb_image_rac = QLabel()

    def tab_start_ui(self):
        self.pb_edit_data.setText(self.translate('Editar dados'))
        self.pb_edit_data.setFixedSize(100, 25)
        self.vb_main_layout.addWidget(self.pb_edit_data)
        self.gb_rac_data.setTitle(self.translate('Parâmetros calculados:'))
        self.lb_lengthRac.setText(self.translate('Comprimento dos compartimentos do RAC'))
        self.lb_lengthRac.setWordWrap(True)
        self.lb_length_rac_value.setText('0' + self.translate(' m'))
        self.lb_length_rac_value.setFont(self.utils.formatBoldText())
        self.gl_rac_data.addWidget(self.lb_lengthRac, 0, 0)
        self.gl_rac_data.addWidget(self.lb_length_rac_value, 0, 1, Qt.AlignLeft)

        q_larguraRac = QLabel(self.translate('Largura adotada para os compartimentos do RAC'))
        q_larguraRac.setWordWrap(True)
        self.lb_width_rac_value.setText('0' + self.translate(' m'))
        self.lb_width_rac_value.setFont(self.utils.formatBoldText())
        self.gl_rac_data.addWidget(q_larguraRac, 1, 0)
        self.gl_rac_data.addWidget(self.lb_width_rac_value, 1, 1, Qt.AlignLeft)

        q_depthRac = QLabel(self.translate('Altura útil do RAC'))
        q_depthRac.setWordWrap(True)
        self.lb_depth_rac_value.setText('0' + self.translate(' m'))
        self.lb_depth_rac_value.setFont(self.utils.formatBoldText())
        self.gl_rac_data.addWidget(q_depthRac, 2, 0)
        self.gl_rac_data.addWidget(self.lb_depth_rac_value, 2, 1, Qt.AlignLeft)

        q_numCompartRac = QLabel(self.translate('Número de compartimentos do RAC'))
        q_numCompartRac.setWordWrap(True)
        self.lb_num_compart_value.setText('0' + self.translate(' unid.'))
        self.lb_num_compart_value.setFont(self.utils.formatBoldText())
        self.gl_rac_data.addWidget(q_numCompartRac, 3, 0)
        self.gl_rac_data.addWidget(self.lb_num_compart_value, 3, 1, Qt.AlignLeft)

        lb_concentrationDQORac = QLabel(self.translate('Concentração de DQO no efluente final'))
        lb_concentrationDQORac.setWordWrap(True)
        self.lb_concentration_DQO_rac_value.setText('0' + self.translate(' g/m³'))
        self.lb_concentration_DQO_rac_value.setFont(self.utils.formatBoldText())
        self.gl_rac_data.addWidget(lb_concentrationDQORac, 4, 0)
        self.gl_rac_data.addWidget(self.lb_concentration_DQO_rac_value, 4, 1, Qt.AlignLeft)

        lb_fficiencyDQORac = QLabel(self.translate('Eficiência de remoção total de DQO no processo'))
        lb_fficiencyDQORac.setWordWrap(True)
        self.lb_efficiency_DQO_rac_value.setText('0' + self.translate(' %'))
        self.lb_efficiency_DQO_rac_value.setFont(self.utils.formatBoldText())
        self.gl_rac_data.addWidget(lb_fficiencyDQORac, 5, 0)
        self.gl_rac_data.addWidget(self.lb_efficiency_DQO_rac_value, 5, 1, Qt.AlignLeft)

        lb_concentrationDBORac = QLabel(self.translate('Concentração de DBO no efluente final'))
        lb_concentrationDBORac.setWordWrap(True)
        self.lb_concentration_DBO_rac_value.setText('0' + self.translate(' g/m³'))
        self.lb_concentration_DBO_rac_value.setFont(self.utils.formatBoldText())
        self.gl_rac_data.addWidget(lb_concentrationDBORac, 6, 0)
        self.gl_rac_data.addWidget(self.lb_concentration_DBO_rac_value, 6, 1, Qt.AlignLeft)

        lb_efficiencyDBORac = QLabel(self.translate('Eficiência de remoção total de DBO no processo'))
        lb_efficiencyDBORac.setWordWrap(True)
        self.lb_efficiency_DBO_rac_value.setText('0' + self.translate(' %'))
        self.lb_efficiency_DBO_rac_value.setFont(self.utils.formatBoldText())
        self.gl_rac_data.addWidget(lb_efficiencyDBORac, 7, 0)
        self.gl_rac_data.addWidget(self.lb_efficiency_DBO_rac_value, 7, 1, Qt.AlignLeft)
        self.gl_rac_data.setColumnMinimumWidth(1, 2)

        self.gb_rac_data.setLayout(self.gl_rac_data)
        self.vb_main_layout.addWidget(self.gb_rac_data)

        self.gl_image_rac.addWidget(self.lb_image_rac, 0, 0, 1, 2, Qt.AlignHCenter)
        self.gb_image_rac.setLayout(self.gl_image_rac)
        self.vb_main_layout.addWidget(self.gb_image_rac)
        self.vb_main_layout.addStretch()
        self.setLayout(self.vb_main_layout)

        self.load_data()
