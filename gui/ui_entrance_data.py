from PyQt5.QtGui import QPixmap
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt, QLocale, QProcess
from qgis.PyQt.QtWidgets import (QAction, QLabel, QDialog, QApplication,
                                 QFileDialog, QDialogButtonBox, QTableWidgetItem, QTableWidget, QTextBrowser,
                                 QMessageBox, QWidget, QAbstractItemView, QStyledItemDelegate, QScrollArea,
                                 QTabWidget, QFormLayout, QHBoxLayout, QRadioButton, QVBoxLayout, QFrame,
                                 QButtonGroup, QPushButton, QGridLayout, QStackedLayout, QSpinBox,
                                 QDoubleSpinBox, QAbstractButton, QGroupBox)
from qgis._core import QgsMessageLog

from ..utils.utils import Utils
from ..utils.icons import icon_warning, icon_info
from .custom_widgets.widgets import (HalfPrecisionDoubleSpinBox, ThousandsSeparatorSpinBox, NextPreviousStackedWidget,
                                     FormLayoutWithIcon)
from ..utils.limits import *  # Min and max values of input variables
from ..core.data.models import ProjectData, FromRedeBasicaData
from ..core.march_calculation import MarchCalculation


def translate(msg, disambiguation=None, n=-1):
    return QCoreApplication.translate("EntranceDataUI", msg, disambiguation, n)


def get_info_icon(tooltip):
    icon = QLabel()
    icon.setPixmap(QPixmap(icon_info))
    icon.setToolTip(tooltip)
    return icon


def get_warning_icon(decimals=2, min_value=0, max_value=None):
    utils = Utils()
    if decimals == 1:
        func = utils.formatNum1Dec
    elif decimals == 2:
        func = utils.formatNum2Dec
    else:
        func = lambda x: str(x)

    if max_value is None:
        warning = translate(f"Valor mínimo: ") + func(min_value)
    else:
        warning = translate("Limite dos valores de entrada: mín: ") + func(min_value) + translate(" e máx: ") + func(
            max_value)

    icon = QLabel()
    icon.setPixmap(QPixmap(icon_warning))
    icon.setToolTip(warning)
    return icon


class DataFormBase(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = FormLayoutWithIcon()
        self.setLayout(self.layout)

    def verify(self):
        raise NotImplementedError

    def prepare_form(self):
        pass


class IntroDataBase(DataFormBase):
    def __init__(self):
        super().__init__()
        maximum = 9999999

        self.dsb_k1 = QDoubleSpinBox()
        self.dsb_k2 = QDoubleSpinBox()
        self.dsb_coef_return = QDoubleSpinBox()

        self.dsb_k1.setMaximum(maximum)
        self.dsb_k2.setMaximum(maximum)
        self.dsb_coef_return.setMaximum(maximum)

        self.dsb_k1.setValue(1.2)
        self.dsb_k2.setValue(1.5)
        self.dsb_coef_return.setValue(0.8)

        self.__lb_infoIcons = []
        for _ in range(3):
            self.__lb_infoIcons.append(
                get_info_icon(translate("Este é um dado sugerido, utilizar este valor ou alterar"))
            )

        self.layout.add_row(QLabel(translate("Dados gerais:")))
        self.setLayout(self.layout)

    def verify(self):
        return 0 not in {self.dsb_k1.value(), self.dsb_k2.value(),
                         self.dsb_coef_return.value()}

    def prepare_form(self):
        self.layout.add_row(QLabel(translate("K1 (coef. dia max consumo)")), self.dsb_k1, self.__lb_infoIcons[0])
        self.layout.add_row(QLabel(translate("K2 (coef. hora max consumo)")), self.dsb_k2, self.__lb_infoIcons[1])
        self.layout.add_row(QLabel(translate("Coeficiente de retorno")), self.dsb_coef_return, self.__lb_infoIcons[2])
        self.layout.add_stretch()


class IntroDataNoIntegration(IntroDataBase):
    def __init__(self):
        super().__init__()
        maximum = 99999
        self.sb_initial_population = ThousandsSeparatorSpinBox()
        self.sb_final_population = ThousandsSeparatorSpinBox()
        self.dsb_consWater = QDoubleSpinBox()
        self.dsb_infiltration_flow = QDoubleSpinBox()

        self.sb_initial_population.setMaximum(maximum)
        self.sb_final_population.setMaximum(maximum)
        self.dsb_consWater.setMaximum(maximum)
        self.dsb_infiltration_flow.setMaximum(maximum)

        self.sb_initial_population.setSuffix(translate(' hab'))
        self.sb_final_population.setSuffix(translate(' hab'))
        self.dsb_consWater.setSuffix(translate(' l/hab.dia'))
        self.dsb_infiltration_flow.setSuffix(translate(' l/s'))

        self.prepare_form()

    def prepare_form(self):
        self.layout.add_row(QLabel(translate('População atendida inicial')), self.sb_initial_population)
        self.layout.add_row(QLabel(translate('População atendida final')), self.sb_final_population)
        self.layout.add_row(QLabel(translate("Consumo percapita de água")), self.dsb_consWater)
        self.layout.add_row(QLabel(translate("Vazão de infiltração de final de plano")), self.dsb_infiltration_flow)
        super().prepare_form()

    def verify(self):
        return 0 not in {self.sb_initial_population.value(), self.dsb_infiltration_flow.value(),
                         self.sb_final_population.value(), self.dsb_consWater.value()} and super().verify()


class IntroDataIntegration(IntroDataBase):
    """
        This class must be called with the values used when collecting the flows from rede basica.
    """
    def __init__(self):
        super().__init__()
        self.prepare_form()


class InfoDataNoIntegration(DataFormBase):
    def __init__(self, intro_data_no_integration: IntroDataNoIntegration):
        super().__init__()

        self.intro_data_no_integration = intro_data_no_integration
        self.strictly_domestic_average_flow_initial = QDoubleSpinBox()
        self.strictly_domestic_average_flow_final = QDoubleSpinBox()
        self.infiltration_flow = QDoubleSpinBox()

        self.strictly_domestic_average_flow_initial.setSuffix(' m³/dia')
        self.strictly_domestic_average_flow_final.setSuffix(' m³/dia')
        self.infiltration_flow.setSuffix(' m³/s')

        self.strictly_domestic_average_flow_initial.setEnabled(False)
        self.strictly_domestic_average_flow_final.setEnabled(False)
        self.prepare_form()

    def prepare_form(self):
        self.layout.add_row(QLabel(self.tr("Vazão estritamente doméstica média diária de início de plano")),
                            self.strictly_domestic_average_flow_initial,
                            get_info_icon('Esse foi um dado derivado do trecho selecionado'))
        self.layout.add_row(QLabel(self.tr("Vazão estritamente doméstica média diária de final de plano")),
                            self.strictly_domestic_average_flow_final,
                            get_info_icon('Esse foi um dado derivado do trecho selecionado')
                            )
        self.layout.add_row(QLabel(self.tr('Vazão de infiltração de final de plano')),
                            self.infiltration_flow)

        self.layout.add_stretch()

    def verify(self):
        return 0 not in {self.strictly_domestic_average_flow_initial,  self.strictly_domestic_average_flow_final,
                         self.infiltration_flow}

    def precalculate_values(self):
        calculation = MarchCalculation(ProjectData(
            self.intro_data_no_integration.dsb
        ))
        calculation.strictly_domestic_max_initial_plan_hour_flow()


class ExtraDataForm(DataFormBase):
    def __init__(self):
        super().__init__()

        maximum = 9999999
        self.dsb_sludge_digestion_temperature = QDoubleSpinBox()
        self.dsb_dqo_entrance = QDoubleSpinBox()
        self.dsb_dbo_entrance = QDoubleSpinBox()

        self.dsb_sludge_digestion_temperature.setValue(20.0)
        self.dsb_sludge_digestion_temperature.setMaximum(maximum)
        self.dsb_sludge_digestion_temperature.setDecimals(1)
        self.dsb_dbo_entrance.setMaximum(maximum)
        self.dsb_dqo_entrance.setMaximum(maximum)

        self.dsb_sludge_digestion_temperature.setSuffix(translate(' ºC'))
        self.dsb_dqo_entrance.setSuffix(translate(' g/m³'))
        self.dsb_dbo_entrance.setSuffix(translate(' g/m³'))

        self.temp_icon = QLabel()

        self.layout.add_row(QLabel(translate("Dados complementares:")))
        self.prepare_form()

    def prepare_form(self):
        self.layout.add_row(QLabel('Temperatura mínima para digestão do lodo - [ºC]'),
                            self.dsb_sludge_digestion_temperature,
                            get_info_icon(translate("Este é um dado sugerido, utilizar este valor ou alterar"))
                            )
        self.layout.add_row(QLabel('Concentração DQO entrada'),
                            self.dsb_dqo_entrance)
        self.layout.add_row(QLabel('Concentração DBO entrada'),
                            self.dsb_dbo_entrance)
        self.layout.add_stretch()

    def verify(self):
        return 0 not in {self.dsb_sludge_digestion_temperature.value(), self.dsb_dqo_entrance.value(),
                         self.dsb_dbo_entrance.value()}


class TankDataForm(DataFormBase):
    def __init__(self):
        super().__init__()
        self.dsb_tdh = QDoubleSpinBox()
        self.sb_sludge_removal_interval = QSpinBox()
        self.dsb_tank_width = HalfPrecisionDoubleSpinBox()
        self.dsb_tank_depth = HalfPrecisionDoubleSpinBox()

        self.dsb_tdh.setRange(MIN_TDH, MAX_TDH)
        self.sb_sludge_removal_interval.setMinimum(MIN_TIME_REMOVAL_SLUDGE)
        self.dsb_tank_width.setMinimum(MIN_SEDIMENTATION_TANK_WIDTH)
        self.dsb_tank_depth.setRange(MIN_SEDIMENTATION_TANK_DEPTH, MAX_SEDIMENTATION_TANK_DEPTH)

        self.dsb_tdh.setSuffix(translate(' h'))
        self.sb_sludge_removal_interval.setSuffix(translate(' meses'))
        self.dsb_tank_width.setSuffix(translate(' m'))
        self.dsb_tank_depth.setSuffix(translate(' m'))

        self.layout.add_row(QLabel(translate("Dados do Tanque de Sedimentação:")))
        self.prepare_form()

    def prepare_form(self):
        self.layout.add_row(
            QLabel(translate('Tempo de detenção hidráulica - TDH')),
            self.dsb_tdh,
            get_warning_icon(decimals=2, min_value=MIN_TDH, max_value=MAX_TDH)
        )
        self.layout.add_row(
            QLabel(translate('Intervalo de tempo para remoção do lodo')),
            self.sb_sludge_removal_interval,
            get_warning_icon(decimals=0, min_value=MIN_TIME_REMOVAL_SLUDGE),
        )
        self.layout.add_row(
            QLabel(translate('Largura do tanque de sedimentação')),
            self.dsb_tank_width,
            get_warning_icon(decimals=2, min_value=MIN_SEDIMENTATION_TANK_WIDTH)
        )
        self.layout.add_row(
            QLabel(translate('Altura útil do tanque de sedimentação')),
            self.dsb_tank_depth,
            get_warning_icon(decimals=2, min_value=MIN_SEDIMENTATION_TANK_DEPTH, max_value=MAX_SEDIMENTATION_TANK_DEPTH)
        )
        self.layout.add_stretch()

    def verify(self):
        return 0 not in {self.dsb_tdh.value(), self.sb_sludge_removal_interval.value(), self.dsb_tank_width.value(),
                         self.dsb_tank_depth.value()}


class RacDataForm(DataFormBase):
    def __init__(self, has_sedimentation_tank=False):
        super().__init__()
        self.has_sedimentation_tank = has_sedimentation_tank
        self.dsb_rac_depth = HalfPrecisionDoubleSpinBox()
        self.sb_num_rac = QSpinBox()
        self.dsb_width_shafts = HalfPrecisionDoubleSpinBox()
        self.dsb_rac_temperature = QDoubleSpinBox()

        self.sb_num_rac.setRange(MIN_NUM_COMPART_RAC, MAX_NUM_COMPART_RAC)
        self.dsb_width_shafts.setMinimum(MIN_WIDTH_SHAFTS)

        self.dsb_rac_depth.setSuffix(translate(' m'))
        self.sb_num_rac.setSuffix(translate(' unid'))
        self.dsb_width_shafts.setSuffix(translate(' m'))
        self.dsb_rac_temperature.setSuffix(translate(' ºC'))

        self.dsb_rac_temperature.setDecimals(1)

        self.layout.add_row(QLabel(translate("Dados RAC e Reator:")))
        self.prepare_form()

    def prepare_form(self):
        if self.has_sedimentation_tank:
            self.layout.add_row(
                QLabel(translate("Altura útil do RAC")),
                self.dsb_rac_depth,
                get_info_icon(translate("É recomendado que a altura útil do RAC seja igual a altura útil do "
                                        "tanque de sedimentação."))
            )
        else:
            self.layout.add_row(
                QLabel(translate("Altura útil do RAC")),
                self.dsb_rac_depth
            )
        self.layout.add_row(
            QLabel(translate("Número de compartimentos do RAC")),
            self.sb_num_rac,
            get_warning_icon(0, MIN_NUM_COMPART_RAC, MAX_NUM_COMPART_RAC)
        )
        self.layout.add_row(
            QLabel(translate("Largura dos shafts")),
            self.dsb_width_shafts,
            get_warning_icon(2, MIN_WIDTH_SHAFTS)
        )
        self.layout.add_row(
            QLabel(translate("Temperatura de operação do reator")),
            self.dsb_rac_temperature
        )
        self.layout.add_stretch()

    def verify(self):
        return 0 not in {self.dsb_rac_depth.value(), self.sb_num_rac.value(), self.dsb_width_shafts, self.dsb_rac_temperature}


class EntranceDataUI:

    utils = Utils()

    def __init__(self, title, has_sedimentation_tank=False, from_rede_basica=None):
        self.title = title
        self.screen = QDialog()

        self.stacked_layouts = NextPreviousStackedWidget(False)

        self.has_sedimentation_tank = has_sedimentation_tank
        self.rede_basica_import = from_rede_basica is not None
        self.from_rede_basica = from_rede_basica  # None if the import is not wanted
        self.load_forms()

        self.stacked_layouts.pb_previous_image.setText(translate("Voltar"))
        self.stacked_layouts.pb_next_image.setText(translate("Avançar"))
        self.stacked_layouts.pb_next_image.clicked.disconnect()
        self.stacked_layouts.pb_next_image.clicked.connect(self.on_next)

        self.on_conclude_listeners = []

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_layouts)
        self.screen.setLayout(layout)

    def add_on_conclude_listener(self, func):
        self.on_conclude_listeners.append(func)

    def on_next(self):
        n = self.stacked_layouts.sw_images.count()
        index = self.stacked_layouts.sw_images.currentIndex()

        if not self.stacked_layouts.sw_images.widget(index).verify():
            icon = QMessageBox.Warning
            self.utils.showDialog(translate('Entrada dados de entrada'),
                                  translate('Todas os campos devem ser preenchidos.'), icon)
            return
        if index == n - 1:
            for func in self.on_conclude_listeners:
                func()
            self.screen.close()
        else:
            self.stacked_layouts.go_for_next_image()

    def get_project_data(self) -> ProjectData:
        rac_widget = intro_widget = tank_widget = extra_widget = None

        for i in range(self.stacked_layouts.sw_images.count()):
            widget = self.stacked_layouts.sw_images.widget(i)
            if isinstance(widget, RacDataForm):
                rac_widget = widget
            elif isinstance(widget, IntroDataBase):
                intro_widget = widget
            elif isinstance(widget, TankDataForm):
                tank_widget = widget
            elif isinstance(widget, ExtraDataForm):
                extra_widget = widget

        project_data = ProjectData(
            concentrationDQOEntrance=extra_widget.dsb_dqo_entrance.value(),
            concentrationDBOEntrance=extra_widget.dsb_dbo_entrance.value(),
            depthOutRac=rac_widget.dsb_rac_depth.value(),
            numCompartRac=rac_widget.sb_num_rac.value(),
            widthShafts=rac_widget.dsb_width_shafts.value(),
            tempOperReactor=rac_widget.dsb_rac_temperature.value(),
            tempDigestSludge=extra_widget.dsb_sludge_digestion_temperature.value(),
            k1CoefDayMaxConsume=intro_widget.dsb_k1.value(),
            k2CoefDayMaxConsume=intro_widget.dsb_k2.value(),
            coefReturn=intro_widget.dsb_coef_return.value()
        )

        if self.has_sedimentation_tank:
            project_data.depthTank = tank_widget.dsb_tank_depth.value()
            project_data.widthTank = tank_widget.dsb_tank_width.value()
            project_data.intervalTimeRemovalSludge = tank_widget.sb_sludge_removal_interval.value()
            project_data.tdh = tank_widget.dsb_tdh.value()


        if isinstance(intro_widget, IntroDataNoIntegration):
            project_data.initial_population = intro_widget.sb_initial_population.value()
            project_data.final_population = intro_widget.sb_final_population.value()
            project_data.consWater = intro_widget.dsb_consWater.value()
            project_data.final_infiltration_flow = intro_widget.dsb_infiltration_flow.value()
        # We save the import data elsewhere, FromRedeBasicaData

        return project_data

    def on_current_index_change(self):
        index = self.stacked_layouts.sw_images.currentIndex()
        self.set_window_title(index)
        if index == self.stacked_layouts.sw_images.count() - 1:
            self.stacked_layouts.pb_next_image.setText(translate("Concluir"))
        else:
            self.stacked_layouts.pb_next_image.setText(translate("Avançar"))
        self.stacked_layouts.sw_images.currentWidget().layout.focus_first()

    def set_window_title(self, index):
        self.screen.setWindowTitle(
            self.title + translate(' - Entrada de dados - ') +
            f'{index + 1}/{self.stacked_layouts.sw_images.count()}'
        )

    def load_forms(self):
        self.stacked_layouts.clear()
        if self.rede_basica_import:
            QgsMessageLog.logMessage("Carregando form rede básica", "EntranceData2")
            self.stacked_layouts.add_widget(IntroDataIntegration())
        else:
            QgsMessageLog.logMessage("Carregando form normal", "EntranceData2")
            self.stacked_layouts.add_widget(IntroDataNoIntegration())
        QgsMessageLog.logMessage("Carregando form Dados complementares", "EntranceData2")
        self.stacked_layouts.add_widget(ExtraDataForm())

        if self.has_sedimentation_tank:
            QgsMessageLog.logMessage("Carregando form tanque sedimentação", "EntranceData2")
            self.stacked_layouts.add_widget(TankDataForm())

        QgsMessageLog.logMessage("Carregando form RAC", "EntranceData2")
        self.stacked_layouts.add_widget(RacDataForm(self.has_sedimentation_tank))
        QgsMessageLog.logMessage(f"Quantidade widgets: {self.stacked_layouts.sw_images.count()}")
        self.stacked_layouts.sw_images.setCurrentIndex(0)
        self.set_window_title(0)
        self.stacked_layouts.pb_next_image.clicked.connect(self.on_current_index_change)
        self.stacked_layouts.pb_previous_image.clicked.connect(self.on_current_index_change)

    def set_options(self, has_sedimentation_tank: bool, from_rede_basica: FromRedeBasicaData = None):
        rede_basica_import = from_rede_basica is not None
        if has_sedimentation_tank != self.has_sedimentation_tank or self.rede_basica_import != rede_basica_import:
            QgsMessageLog.logMessage(f"Reloading, sedimentation: {has_sedimentation_tank}", "UI ENTRANCE DATA")
            self.has_sedimentation_tank = has_sedimentation_tank
            self.rede_basica_import = rede_basica_import
            self.from_rede_basica = from_rede_basica
            self.load_forms()

    def show_screen(self):
        self.screen.close()
        self.stacked_layouts.sw_images.widget(0).layout.focus_first()
        self.screen.show()
