from typing import Optional

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPalette, QColor
from qgis.PyQt.QtCore import Qt, QLocale
from qgis.PyQt.QtWidgets import (QLabel, QDialog, QTableWidgetItem, QTableWidget, QMessageBox, QAbstractItemView,
                                 QStyledItemDelegate, QApplication,
                                 QPushButton, QGridLayout, QSpinBox,
                                 QDoubleSpinBox)
from qgis.core import QgsMessageLog

from ..core.data.data_manager import ProjectDataManager
from ..core.data.models import ProjectData, FromRedeBasicaData
from qgis.core import QgsProject
from ..gui.custom_widgets.widgets import ThousandsSeparatorSpinBox, HalfPrecisionDoubleSpinBox
from ..utils.utils import Utils
from ..utils.limits import *



class RepEntranceDataUI:
    def translate(self, msg, disambiguation=None, n=-1):
        return QCoreApplication.translate(RepEntranceDataUI.__name__, msg, disambiguation, n)

    RANGE_ALL_DATA = range(0, 28)
    RANGE_GENERAL_DATA = range(0, 14)
    RANGE_SEDIMENTATION_TANK_DATA = range(14, 18)
    RANGE_RAC_DATA = range(18, 22)

    def __init__(self):
        self.utils = Utils()
        self.screen = QDialog()
        self.layout = QGridLayout()  # QVBoxLayout()
        self.table = QTableWidget()
        self.title = ''
        self.entrance: Optional[ProjectData] = None  # EntradaDados()
        self.sedimentationTank = False
        self.should_import_rede_basica = False
        self.loc = QLocale()
        self.pb_saveEditEnt = QPushButton()
        self.lb_dataEnt = QLabel()

        maximum = 9999999
        self.sb_initial_population = ThousandsSeparatorSpinBox()
        self.sb_initial_population.setMaximum(maximum)
        self.sb_final_population = ThousandsSeparatorSpinBox()
        self.sb_final_population.setMaximum(maximum)
        self.dsb_infiltration_flow = QDoubleSpinBox()
        self.dsb_infiltration_flow.setMaximum(maximum)
        self.dsb_maximum_horly_sludge_flow_initial = QDoubleSpinBox()
        self.dsb_maximum_horly_sludge_flow_initial.setMaximum(maximum)
        self.dsb_maximum_horly_sludge_flow_final = QDoubleSpinBox()
        self.dsb_maximum_horly_sludge_flow_final.setMaximum(maximum)
        self.dsb_average_strictly_domestic_flow_initial = QDoubleSpinBox()
        self.dsb_average_strictly_domestic_flow_initial.setMaximum(maximum)
        self.dsb_average_strictly_domestic_flow_final = QDoubleSpinBox()
        self.dsb_average_strictly_domestic_flow_final.setMaximum(maximum)
        self.dsb_consWater = QDoubleSpinBox()
        self.dsb_consWater.setMaximum(maximum)
        self.dsb_dqoEntr = QDoubleSpinBox()
        self.dsb_dqoEntr.setMaximum(maximum)
        self.dsb_dboEntr = QDoubleSpinBox()
        self.dsb_dboEntr.setMaximum(maximum)

        self.dsb_tdh = QDoubleSpinBox()
        self.dsb_tdh.setDecimals(1)
        self.dsb_tdh.setRange(MIN_TDH, MAX_TDH)
        self.sb_intervalTime = QSpinBox()
        self.sb_intervalTime.setRange(MIN_TIME_REMOVAL_SLUDGE, maximum)
        self.dsb_widthTank = HalfPrecisionDoubleSpinBox()
        self.dsb_widthTank.setRange(MIN_SEDIMENTATION_TANK_WIDTH, maximum)
        self.dsb_depthTank = HalfPrecisionDoubleSpinBox()  # Altura útil
        self.dsb_depthTank.setRange(MIN_SEDIMENTATION_TANK_DEPTH, MAX_SEDIMENTATION_TANK_DEPTH)

        self.dsb_depthOutRac = HalfPrecisionDoubleSpinBox()
        self.sb_numCompartRac = QSpinBox()
        self.sb_numCompartRac.setRange(MIN_NUM_COMPART_RAC, MAX_NUM_COMPART_RAC)
        self.dsb_widthShafts = HalfPrecisionDoubleSpinBox()
        self.dsb_widthShafts.setRange(MIN_WIDTH_SHAFTS, maximum)
        self.dsb_tempOperReactor = QDoubleSpinBox()
        self.dsb_tempOperReactor.setMaximum(maximum)
        self.dsb_tempOperReactor.setDecimals(1)

        self.dsb_k1 = QDoubleSpinBox()
        self.dsb_k1.setMaximum(maximum)
        self.dsb_k2 = QDoubleSpinBox()
        self.dsb_k2.setMaximum(maximum)
        self.dsb_coefReturn = QDoubleSpinBox()
        self.dsb_coefReturn.setMaximum(maximum)
        self.dsb_tempDigestSludge = QDoubleSpinBox()
        self.dsb_tempDigestSludge.setMaximum(maximum)
        self.dsb_tempDigestSludge.setDecimals(1)

        self.dsb_relSolidDQO = QDoubleSpinBox()
        self.dsb_velFlowAscendant = QDoubleSpinBox()
        self.dsb_cofProductionSolid = QDoubleSpinBox()
        self.dsb_concentrMethaneBiogas = QDoubleSpinBox()
        self.dsb_functionPotentialCH4 = QDoubleSpinBox()
        self.dsb_factorCorrecMethaneMCF = QDoubleSpinBox()

    def showReportEntrance(self, lines):
        if self.entrance is None:
            return
        if self.should_import_rede_basica:
            red_basica = ProjectDataManager.get_from_rede_basica_data()
            self.dsb_maximum_horly_sludge_flow_initial.setValue(red_basica.maximum_horly_sludge_flow_initial)
            self.dsb_maximum_horly_sludge_flow_initial.setAlignment(Qt.AlignHCenter)
            self.dsb_maximum_horly_sludge_flow_final.setValue(red_basica.maximum_horly_sludge_flow_final)
            self.dsb_maximum_horly_sludge_flow_final.setAlignment(Qt.AlignHCenter)
            self.dsb_average_strictly_domestic_flow_initial.setValue(red_basica.average_strictly_domestic_flow_initial)
            self.dsb_average_strictly_domestic_flow_initial.setAlignment(Qt.AlignHCenter)
            self.dsb_average_strictly_domestic_flow_final.setValue(red_basica.average_strictly_domestic_flow_final)
            self.dsb_average_strictly_domestic_flow_final.setAlignment(Qt.AlignHCenter)
            self.dsb_infiltration_flow.setValue(red_basica.infiltration_flow)
            self.dsb_infiltration_flow.setAlignment(Qt.AlignHCenter)
        else:
            self.sb_initial_population.setValue(self.entrance.getInitialPopulation())
            self.sb_final_population.setValue(self.entrance.final_population)
            self.sb_initial_population.setAlignment(Qt.AlignHCenter)
            self.sb_final_population.setAlignment(Qt.AlignHCenter)
            self.dsb_infiltration_flow.setValue(self.entrance.final_infiltration_flow)
            self.dsb_infiltration_flow.setAlignment(Qt.AlignHCenter)
            self.dsb_consWater.setValue(self.entrance.getConsWater())
            self.dsb_consWater.setAlignment(Qt.AlignHCenter)

        self.dsb_dqoEntr.setValue(self.entrance.getConcentrationDQOEntrance())
        self.dsb_dqoEntr.setAlignment(Qt.AlignHCenter)
        self.dsb_dboEntr.setValue(self.entrance.getConcentrationDBOEntrance())
        self.dsb_dboEntr.setAlignment(Qt.AlignHCenter)

        if self.sedimentationTank:
            self.dsb_tdh.setValue(self.entrance.getTdh())
            self.dsb_tdh.setAlignment(Qt.AlignHCenter)
            self.sb_intervalTime.setValue(self.entrance.getIntervalTimeRemovalSludge())
            self.sb_intervalTime.setAlignment(Qt.AlignHCenter)
            self.dsb_widthTank.setValue(self.entrance.getWidthTank())
            self.dsb_widthTank.setAlignment(Qt.AlignHCenter)
            self.dsb_depthTank.setValue(self.entrance.getDepthTank())
            self.dsb_depthTank.setAlignment(Qt.AlignHCenter)

        self.dsb_depthOutRac.setValue(self.entrance.getDepthOutRac())
        self.dsb_depthOutRac.setAlignment(Qt.AlignHCenter)
        self.sb_numCompartRac.setValue(self.entrance.getNumCompartRAC())
        self.sb_numCompartRac.setAlignment(Qt.AlignHCenter)
        self.dsb_widthShafts.setValue(self.entrance.getWidthShafts())
        self.dsb_widthShafts.setAlignment(Qt.AlignHCenter)
        self.dsb_tempOperReactor.setValue(self.entrance.getTempOperReactor())
        self.dsb_tempOperReactor.setAlignment(Qt.AlignHCenter)

        self.dsb_k1.setValue(self.entrance.getK1CoefDayMaxConsume())
        self.dsb_k1.setAlignment(Qt.AlignHCenter)
        self.dsb_k2.setValue(self.entrance.getK2CoefDayMaxConsume())
        self.dsb_k2.setAlignment(Qt.AlignHCenter)
        self.dsb_coefReturn.setValue(self.entrance.getCoefReturn())
        self.dsb_coefReturn.setAlignment(Qt.AlignHCenter)
        self.dsb_tempDigestSludge.setValue(self.entrance.getTempDigestSludge())
        self.dsb_tempDigestSludge.setAlignment(Qt.AlignHCenter)

        self.dsb_relSolidDQO.setValue(self.entrance.getRelSolidSedimentableDQO())
        self.dsb_relSolidDQO.setAlignment(Qt.AlignHCenter)
        self.dsb_relSolidDQO.setEnabled(False)
        self.dsb_velFlowAscendant.setValue(self.entrance.getVelAscendingFlowMax())
        self.dsb_velFlowAscendant.setAlignment(Qt.AlignHCenter)
        self.dsb_velFlowAscendant.setEnabled(False)
        self.dsb_cofProductionSolid.setValue(self.entrance.getCoefProductionSolid())
        self.dsb_cofProductionSolid.setAlignment(Qt.AlignHCenter)
        self.dsb_cofProductionSolid.setEnabled(False)
        self.dsb_concentrMethaneBiogas.setValue(self.entrance.getConcentrationMethaneBiogas() * 100)
        self.dsb_concentrMethaneBiogas.setAlignment(Qt.AlignHCenter)
        self.dsb_concentrMethaneBiogas.setEnabled(False)
        self.dsb_functionPotentialCH4.setValue(self.entrance.getFunctionPotentialCH4())
        self.dsb_functionPotentialCH4.setAlignment(Qt.AlignHCenter)
        self.dsb_functionPotentialCH4.setEnabled(False)
        self.dsb_factorCorrecMethaneMCF.setValue(self.entrance.getFactorCorrectMethaneMCF())
        self.dsb_factorCorrecMethaneMCF.setAlignment(Qt.AlignHCenter)
        self.dsb_factorCorrecMethaneMCF.setEnabled(False)
        for i in range(self.table.rowCount()):
            self.table.hideRow(i)
        for i in lines:
            self.table.showRow(i)
        self.table.horizontalHeader()  # .hide()
        self.table.verticalHeader()  # .hide()
        dialogWidth = self.table.horizontalHeader().length() + 30
        if len(lines) > 17:
            dialogHeight = self.table.verticalHeader().length() * 0.8
        elif len(lines) == 4:
            dialogHeight = self.table.verticalHeader().length() * 1.8
        else:
            dialogHeight = self.table.verticalHeader().length() * 1.3
        if self.sedimentationTank == False:
            self.table.hideRow(14)
            self.table.hideRow(15)
            self.table.hideRow(16)
            self.table.hideRow(17)
        if self.should_import_rede_basica:
            self.table.hideRow(0)
            self.table.hideRow(1)
            self.table.hideRow(2)
        else:
            self.table.hideRow(3)
            self.table.hideRow(4)
            self.table.hideRow(5)
            self.table.hideRow(6)
        self.table.verticalHeader().setVisible(False)
        app = QApplication.instance()
        allScreen = app.primaryScreen()
        geometry = allScreen.availableGeometry()
        self.screen.setGeometry(((geometry.width() - (self.table.horizontalHeader().length()) * 1.1) / 2.0),
                                (geometry.height() - self.table.verticalHeader().length() * 0.82) / 2.0,
                                self.table.horizontalHeader().length() * 1.055,
                                self.table.verticalHeader().length() *
                                (0.85 if self.table.verticalHeader().length() > 300 else 1.6))
        self.screen.exec_()


    def loadReportEntrance(self, entrada, tank, should_import_rede_basica, title):
        self.entrance = entrada
        self.sedimentationTank = tank
        self.should_import_rede_basica = should_import_rede_basica
        self.title = title
        self.screen.setWindowTitle(self.title + ' - ' + self.translate('Alterar dados de entrada'))
        self.lb_dataEnt.setText(self.translate('Dados de entrada:'))
        self.layout.addWidget(self.lb_dataEnt, 0, 0)
        self.pb_saveEditEnt.setText(self.translate('Salvar'))
        self.layout.addWidget(self.pb_saveEditEnt, 0, 1, Qt.AlignRight)
        # if self.openFile == True:
        #	self.getValuesFile()
        self.loadTable()
        self.layout.addWidget(self.table, 1, 0, 1, 2)
        self.screen.setLayout(self.layout)
        self.screen.setGeometry(350, 50, 550, 200)

    def loadTable(self):
        colLabels = [self.translate('Parâmetro'), self.translate('Valor'), self.translate('Unidade'),
                     self.translate('Forma de entrada'), self.translate('Limites')]
        # if self.sedimentationTank == True:
        self.table.setRowCount(28)
        # else:
        #	self.table.setRowCount(18)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(colLabels)
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 120)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # does not allow table editing
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # Used to select entire rows instead of just the cell
        delegate = AlignDelegate(self.table)  # whole column alignment
        self.table.setItemDelegateForColumn(1, delegate)
        self.table.setItemDelegateForColumn(2, delegate)
        self.table.setItemDelegateForColumn(3, delegate)
        self.table.setItemDelegateForColumn(4, delegate)

        def lim_str(min_v, max_v=None):
            if max_v is not None:
                return f'[ {min_v} - {max_v} ]'
            else:
                return f'[ {min_v} - * ]'

        tableInfo = [[self.translate('População atendida inicial'), self.sb_initial_population, self.translate('hab'),
                      self.translate('Obrigatório'), '-'],
                     [self.translate('População atendida final'), self.sb_final_population, self.translate('hab'),
                      self.translate('Obrigatório'), '-'],
                     [self.translate('Consumo percapita de água'), self.dsb_consWater, self.translate('l/hab.dia'),
                      self.translate('Obrigatório'), '-'],
                     [self.translate('Vazão de esgoto sanitário máxima horária de início de plano'),
                      self.dsb_maximum_horly_sludge_flow_initial, self.translate('l/s'), self.translate('Obrigatório'),
                      '-'],
                     [self.translate('Vazão de esgoto sanitário máxima horária de final de plano'),
                      self.dsb_maximum_horly_sludge_flow_final, self.translate('l/s'), self.translate('Obrigatório'),
                      '-'],
                     [self.translate('Vazão média de início de plano estritamente doméstica'),
                      self.dsb_average_strictly_domestic_flow_initial, self.translate('l/s'),
                      self.translate('Obrigatório'), '-'],
                     [self.translate('Vazão média de final de plano estritamente doméstica'),
                      self.dsb_average_strictly_domestic_flow_final, self.translate('l/s'),
                      self.translate('Obrigatório'), '-'],
                     [self.translate('Vazão de infiltração de final de plano'), self.dsb_infiltration_flow,
                      self.translate('l/s'), self.translate('Obrigatório'), '-'],
                     [self.translate('Coeficiente de retorno'), self.dsb_coefReturn, '-', self.translate('Sugerido'),
                      '-'],
                     [self.translate('K1 (coef. dia max consumo)'), self.dsb_k1, '-', self.translate('Sugerido'), '-'],
                     [self.translate('K2 (coef. hora max consumo)'), self.dsb_k2, '-', self.translate('Sugerido'), '-'],
                     [self.translate('Temperatura mínima para digestão do lodo'), self.dsb_tempDigestSludge,
                      self.translate('ºC'), self.translate('Sugerido'), '-'],
                     [self.translate('Concentração DQO entrada'), self.dsb_dqoEntr, self.translate('g/m³ ou mg/l'),
                      self.translate('Obrigatório'), '-'],
                     [self.translate('Concentração DBO entrada'), self.dsb_dboEntr, self.translate('g/m³ ou mg/l'),
                      self.translate('Obrigatório'), '-'],
                     [self.translate('Tempo de detenção hidraúlica - TDH'), self.dsb_tdh, self.translate('h'),
                      self.translate('Obrigatório'),
                      lim_str(MIN_TDH, MAX_TDH)],
                     [self.translate('Intervalo de tempo para remoção do lodo'), self.sb_intervalTime,
                      self.translate('meses'), self.translate('Obrigatório'),
                      lim_str(MIN_TIME_REMOVAL_SLUDGE)],
                     [self.translate('Largura do tanque de sedimentação'), self.dsb_widthTank, self.translate('m'),
                      self.translate('Obrigatório'),
                      lim_str(MIN_SEDIMENTATION_TANK_WIDTH)],
                     [self.translate('Altura útil do tanque de sedimentação'), self.dsb_depthTank, self.translate('m'),
                      self.translate('Obrigatório'),
                      lim_str(MIN_SEDIMENTATION_TANK_DEPTH, MAX_SEDIMENTATION_TANK_DEPTH)],
                     [self.translate('Altura útil do RAC'), self.dsb_depthOutRac,
                      self.translate('m'), self.translate('Obrigatório'), '-'],
                     [self.translate('Número de compartimentos do RAC'), self.sb_numCompartRac, self.translate('unid.'),
                      self.translate('Obrigatório'),
                      lim_str(MIN_NUM_COMPART_RAC, MAX_NUM_COMPART_RAC)],
                     [self.translate('Largura dos shafts'), self.dsb_widthShafts, self.translate('m'),
                      self.translate('Obrigatório'), lim_str(MIN_WIDTH_SHAFTS)],
                     [self.translate('Temperatura de operação do reator'), self.dsb_tempOperReactor,
                      self.translate('ºC'), self.translate('Obrigatório'), '-'],
                     [self.translate('Relação Sólidos Sedimentáveis / DQO'), self.dsb_relSolidDQO, '-',
                      self.translate('Valor padrão'), '-'],
                     [self.translate('Velocidade de fluxo ascendente máxima'), self.dsb_velFlowAscendant,
                      self.translate('m/h'), self.translate('Valor padrão'), '-'],
                     [self.translate('Coeficiente de produção de sólidos no sistema'), self.dsb_cofProductionSolid,
                      self.translate('kgDQO lodo/ kgDQO aplicada'), self.translate('Valor padrão'), '-'],
                     [self.translate('Concentração de metano no biogás'), self.dsb_concentrMethaneBiogas,
                      self.translate('%'), self.translate('Valor padrão'), '-'],
                     [self.translate('Função do potencial máximo de produção de CH4 a partir da matéria orgânica'),
                      self.dsb_functionPotentialCH4, self.translate('Kg CH4/Kg DBO'), self.translate('Valor Padrão'),
                      '-'],
                     [self.translate(
                         'Fator de correção de metano para sistemas de tratamento de águas residuárias por reatores '
                         'anaeróbios - MCF'), self.dsb_factorCorrecMethaneMCF, '-', self.translate('Valor Padrão'),
                         '-']]


        self.dsb_maximum_horly_sludge_flow_initial.setEnabled(False)
        self.dsb_maximum_horly_sludge_flow_final.setEnabled(False)

        self.dsb_average_strictly_domestic_flow_initial.valueChanged.connect(self.set_maximum_by_average_initial)
        self.dsb_average_strictly_domestic_flow_final.valueChanged.connect(self.set_maximum_by_average_final)

        for i in range(len(tableInfo)):
            self.table.setItem(i, 0, QTableWidgetItem(self.translate(tableInfo[i][0])))
            self.table.setCellWidget(i, 1, tableInfo[i][1])
            self.table.setItem(i, 2, QTableWidgetItem(self.translate(tableInfo[i][2])))
            self.table.setItem(i, 3, QTableWidgetItem(self.translate(tableInfo[i][3])))
            self.table.setItem(i, 4, QTableWidgetItem(self.translate(tableInfo[i][4])))

    def set_maximum_by_average_initial(self):
        self.set_maximum_by_average(
            self.dsb_maximum_horly_sludge_flow_initial, self.dsb_average_strictly_domestic_flow_initial)

    def set_maximum_by_average_final(self):
        self.set_maximum_by_average(
            self.dsb_maximum_horly_sludge_flow_final, self.dsb_average_strictly_domestic_flow_final)

    def set_maximum_by_average(self, dsb_maximum, dsb_average):
        if dsb_average.value() * 1.8 < dsb_maximum.value() or dsb_maximum.value() < dsb_average.value():
            dsb_maximum.setValue(dsb_average.value() * 1.8)

    def check_data_sedimentation_tank(self):
        if (self.dsb_tdh.value() != 0 and self.sb_intervalTime.value() != 0 and
                self.dsb_widthTank.value() != 0 and self.dsb_depthTank.value() != 0):
            return True

    def check_data_integration_redbasica(self):
        if (self.dsb_average_strictly_domestic_flow_initial.value() != 0 and
                self.dsb_average_strictly_domestic_flow_final.value() != 0 and
                self.dsb_maximum_horly_sludge_flow_initial.value() != 0 and
                self.dsb_maximum_horly_sludge_flow_final.value() != 0):
            return True

    def check_data_no_integration(self):
        if (self.sb_initial_population.value() != 0 and self.sb_final_population.value() != 0 and
                self.dsb_consWater.value() != 0):
            return True

    def check_data_general(self):
        if (self.dsb_infiltration_flow.value() != 0 and self.dsb_dqoEntr.value() != 0 and
                self.dsb_dboEntr.value() != 0 and self.dsb_depthOutRac.value() != 0 and
                self.sb_numCompartRac.value() != 0 and self.dsb_widthShafts.value() != 0 and
                self.dsb_tempOperReactor.value() != 0 and self.dsb_k1.value() != 0 and
                self.dsb_k2.value() != 0 and self.dsb_coefReturn.value() != 0 and
                self.dsb_tempDigestSludge.value() != 0):
            return True

    def checkData(self):
        if self.sedimentationTank and self.should_import_rede_basica:
            if (self.check_data_integration_redbasica() and self.check_data_sedimentation_tank() and
                    self.check_data_general()):
                return True
        elif self.sedimentationTank is not True and self.should_import_rede_basica:
            if self.check_data_integration_redbasica() and self.check_data_general():
                return True
        elif self.sedimentationTank and self.should_import_rede_basica is not True:
            if (self.check_data_no_integration() and self.check_data_sedimentation_tank() and
                    self.check_data_general()):
                return True
        elif self.sedimentationTank is not True and self.should_import_rede_basica is not True:
            if self.check_data_no_integration() and self.check_data_general():
                return True

    def check_exist_ETE(self):
        all_layers = [*QgsProject.instance().mapLayers().keys()]
        layer_txt = False
        layer = None
        for i in all_layers:
            layer_txt = i.startswith('SaniHUB_DWATS')
            if layer_txt:
                layer = i
                break
        return (layer_txt, layer)

    def remove_new_ETE(self):
        if self.check_exist_ETE()[0]:
            QgsProject.instance().removeMapLayer(self.check_exist_ETE()[1])
            QgsProject.instance().reloadAllLayers()
            return True
        else:
            return

    def saveChanges(self):
        if self.checkData() == True:
            # TODO: set save route for integration with redbasica, without saving population
            if self.should_import_rede_basica:
                ProjectDataManager.save_from_rede_basica_data(
                    FromRedeBasicaData(
                        maximum_horly_sludge_flow_initial=self.dsb_maximum_horly_sludge_flow_initial.value(),
                        maximum_horly_sludge_flow_final=self.dsb_maximum_horly_sludge_flow_final.value(),
                        average_strictly_domestic_flow_initial=self.dsb_average_strictly_domestic_flow_initial.value(),
                        average_strictly_domestic_flow_final=self.dsb_average_strictly_domestic_flow_final.value(),
                        infiltration_flow=self.dsb_infiltration_flow.value(),
                    )
                )
            else:
                self.entrance.setInitialPopulation(self.sb_initial_population.value())
                self.entrance.final_population = self.sb_final_population.value()
                self.entrance.setConsWater(self.dsb_consWater.value())
                self.entrance.final_infiltration_flow = self.dsb_infiltration_flow.value()
            self.entrance.setConcentrationDQOEntrance(self.dsb_dqoEntr.value())
            self.entrance.setConcentrationDBOEntrance(self.dsb_dboEntr.value())

            if self.sedimentationTank == True:
                self.entrance.setTdh(self.dsb_tdh.value())
                self.entrance.setIntervalTimeRemovalSludge(self.sb_intervalTime.value())
                self.entrance.setWidthTank(self.dsb_widthTank.value())
                self.entrance.setDepthTank(self.dsb_depthTank.value())

            self.entrance.setDepthOutRac(self.dsb_depthOutRac.value())
            self.entrance.setNumCompartRac(self.sb_numCompartRac.value())
            self.entrance.setWidthShafts(self.dsb_widthShafts.value())
            self.entrance.setTempOperReactor(self.dsb_tempOperReactor.value())

            self.entrance.setK1CoefDayMaxConsume(self.dsb_k1.value())
            self.entrance.setK2CoefDayMaxConsume(self.dsb_k2.value())
            self.entrance.setCoefReturn(self.dsb_coefReturn.value())
            self.entrance.setTempDigestSludge(self.dsb_tempDigestSludge.value())
            self.screen.close()

            if self.remove_new_ETE():
                self.utils.showDialog(self.title, self.translate('Os dados da ETE foram atualizados. '
                                                                 'O desenho do mapa foi removido. \nFavor inserir '
                                                                 'novamente.'), QMessageBox.Information)
            else:
                self.utils.showDialog(self.title, self.translate('Dados alterados com sucesso!'),
                                                                 QMessageBox.Information)
            return True
        else:
            self.utils.showDialog(self.title, self.translate('Dados não alterados - existem campos zerados!'),
                                                             QMessageBox.Critical)
            return False


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignHCenter
