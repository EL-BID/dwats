from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QGroupBox, QLabel, QGridLayout, QStackedWidget, QLayout, \
    QBoxLayout, QWidget
from qgis.core import QgsMessageLog

from ..base.ui_dock_tab_edit_button_base import DockTabEditButtonBase
from ...custom_widgets.widgets import NextPreviousStackedWidget
from ...ui_rep_entrance_data import RepEntranceDataUI


class DockTabGeneralBase(DockTabEditButtonBase):
    title = 'SaniHUB DWATS'

    EDIT_DATA_RANGE = RepEntranceDataUI.RANGE_GENERAL_DATA

    # We must rewrite the tr method, because at runtime, the default self.translate calls within the context of the
    # inherited child class, however, pylupdate reads the python file without executing it, putting the context in
    # translation as the parent class
    # noinspection PyMethodMayBeStatic
    def translate(self, msg, disambiguation=None, n=-1):
        return QCoreApplication.translate(DockTabGeneralBase.__name__, msg, disambiguation, n)

    def __init__(self, dock):
        super().__init__(dock)

        self.vb_main_layout = QVBoxLayout()
        self.gb_dataGas = QGroupBox()

        self.g_layout_gas = QGridLayout()
        self.lb_vazao = QLabel()
        self.lb_vazao_value = QLabel()
        self.lb_co2_emission = QLabel()
        self.lb_co2_emission_value = QLabel()

        self.g_layout_areas = QGridLayout()
        self.lb_area = QLabel()
        self.lb_area_value = QLabel()
        self.lb_usable_area = QLabel()
        self.lb_usable_area_value = QLabel()
        self.dataAreas = QGroupBox()

        self.images_layout = QVBoxLayout()
        self.images_container = QGroupBox()

        self.images_stack_widget = NextPreviousStackedWidget()
        self.set_logic()

    def tab_start_ui(self):
        self.__start_edit_data_ui()
        self.__start_gas_ui()
        self.__start_area_ui()
        self.__start_images_ui()

        self.vb_main_layout.addStretch()
        self.setLayout(self.vb_main_layout)
        self.load_data()

    def __start_edit_data_ui(self):
        self.pb_edit_data.setText(self.translate('Editar dados'))
        self.pb_edit_data.setFixedSize(100, 25)
        self.vb_main_layout.addWidget(self.pb_edit_data)

    def __start_gas_ui(self):
        self.gb_dataGas.setTitle(self.translate('Parâmetros calculados:'))
        self.lb_vazao.setText(self.translate('Vazão diária de biogás'))
        self.lb_vazao.setWordWrap(True)
        self.lb_vazao_value.setText('0 ' + self.translate('m³/dia'))
        self.lb_vazao_value.setFont(self.utils.formatBoldText())
        self.g_layout_gas.addWidget(self.lb_vazao, 0, 0)
        self.g_layout_gas.addWidget(self.lb_vazao_value, 0, 1, Qt.AlignLeft)
        self.lb_co2_emission.setText(self.translate('Emissão de gás carbônico equivalente diária'))
        self.lb_co2_emission.setWordWrap(True)
        self.lb_co2_emission_value.setText('0 ' + self.translate('kg CO2e/dia'))
        self.lb_co2_emission_value.setFont(self.utils.formatBoldText())
        self.g_layout_gas.addWidget(self.lb_co2_emission, 1, 0)
        self.g_layout_gas.addWidget(self.lb_co2_emission_value, 1, 1, Qt.AlignLeft)
        self.g_layout_gas.setColumnMinimumWidth(1, 2)
        self.gb_dataGas.setLayout(self.g_layout_gas)
        self.vb_main_layout.addWidget(self.gb_dataGas)

    def __start_area_ui(self):
        self.lb_area.setText(self.translate('Área construída total'))
        self.lb_area.setWordWrap(True)
        self.lb_area_value.setText('0 ' + self.translate('m²'))
        self.lb_area_value.setFont(self.utils.formatBoldText())
        self.g_layout_areas.addWidget(self.lb_area, 0, 0)
        self.g_layout_areas.addWidget(self.lb_area_value, 0, 1, Qt.AlignLeft)
        self.lb_usable_area.setText(self.translate('Área útil total'))
        self.lb_usable_area.setWordWrap(True)
        self.lb_usable_area_value.setText('0 ' + self.translate('m²'))
        self.lb_usable_area_value.setFont(self.utils.formatBoldText())
        self.g_layout_areas.addWidget(self.lb_usable_area, 1, 0)
        self.g_layout_areas.addWidget(self.lb_usable_area_value, 1, 1, Qt.AlignLeft)
        self.g_layout_areas.setColumnMinimumWidth(1, 2)
        self.dataAreas.setLayout(self.g_layout_areas)
        # self.dataAreas.hide()
        self.vb_main_layout.addWidget(self.dataAreas)

    def __start_images_ui(self):
        self.images_layout.addWidget(self.images_stack_widget)
        self.images_container.setLayout(self.images_layout)
        self.vb_main_layout.addWidget(self.images_container, alignment=Qt.AlignCenter)




