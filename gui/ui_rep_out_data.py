from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt, QLocale, QProcess
from qgis.PyQt.QtWidgets import (QAction, QLabel, QDialog, QApplication,
                                 QFileDialog, QDialogButtonBox, QTableWidgetItem, QTableWidget, QTextBrowser,
                                 QMessageBox, QWidget, QAbstractItemView, QStyledItemDelegate, QScrollArea,
                                 QTabWidget, QFormLayout, QHBoxLayout, QRadioButton, QVBoxLayout, QFrame,
                                 QButtonGroup, QPushButton, QGridLayout, QStackedLayout, QSpinBox,
                                 QDoubleSpinBox, QAbstractButton)
from ..core.march_calculation import MarchCalculation
from ..utils.utils import Utils
from ..core.data.data_manager import ProjectDataManager

class RepOutDataGeneralUI:
    screen = QDialog()
    layout = QVBoxLayout()
    table = QTableWidget()
    title = ''
    marchCalculation = False  # EntradaDados()
    loc = QLocale()
    utils = Utils()
    sedimentationTank = False
    lb_dataOut = QLabel()

    # noinspection PyMethodMayBeStatic
    def translate(self, msg, disambiguation=None, n=-1):
        return QCoreApplication.translate(RepOutDataGeneralUI.__name__, msg, disambiguation, n)

    def showReportOutGeneral(self):
        # self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.horizontalHeader()  # .hide()
        self.table.verticalHeader()  # .hide()
        app = QApplication.instance()
        allScreen = app.primaryScreen()
        geometry = allScreen.availableGeometry()
        self.screen.setGeometry(((geometry.width() - (self.table.horizontalHeader().length()) * 1.1) / 2.0),
                                (geometry.height() - self.table.verticalHeader().length() * 1.4) / 2.0,
                                self.table.horizontalHeader().length() * 1.055,
                                self.table.verticalHeader().length() * 1.25)
        self.screen.exec_()

    def loadReportOutGeneral(self, calculation, title, sedimentationTank):
        self.marchCalculation = calculation
        self.title = title
        self.sedimentationTank = sedimentationTank
        self.screen.setWindowTitle(str(self.title + self.translate(' - Relatório de Saída de Dados')))
        self.lb_dataOut.setText(self.translate('Dados de saída:'))
        self.layout.addWidget(self.lb_dataOut)
        self.loadTable()
        self.layout.addWidget(self.table)
        self.screen.setLayout(self.layout)
        self.screen.setGeometry(350, 50, 550, 200)

    def loadTable(self):
        colLabels = [self.translate('Parâmetro'), self.translate('Valor'), self.translate('Unidade')]
        if self.sedimentationTank:
            if ProjectDataManager.get_project_config().should_calculate_area:
                self.table.setRowCount(12)
            else:
                self.table.setRowCount(11)
        else:
            if ProjectDataManager.get_project_config().should_calculate_area:
                self.table.setRowCount(10)
            else:
                self.table.setRowCount(9)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(colLabels)
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 120)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # does not allow table editing
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # Used to select entire rows instead of just the cell
        delegate = AlignDelegate(self.table)  # whole column alignment
        self.table.setItemDelegateForColumn(1, delegate)
        self.table.setItemDelegateForColumn(2, delegate)
        i = 0
        if self.sedimentationTank == True:
            self.table.setItem(i, 0, QTableWidgetItem(self.translate('Comprimento do tanque de sedimentação')))
            self.table.setItem(i, 1, QTableWidgetItem(
                self.utils.formatNum1Dec(self.marchCalculation.getLengthTankSedimentation())))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m')))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(self.translate('Volume do tanque de sedimentação')))
            self.table.setItem(i, 1, QTableWidgetItem(
                self.utils.formatNum1Dec(self.marchCalculation.getVolumeTankSedimentation())))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
            i += 1

        self.table.setItem(i, 0, QTableWidgetItem(self.translate('Comprimento dos compartimentos do RAC')))
        self.table.setItem(i, 1,
                           QTableWidgetItem(self.utils.formatNum1Dec(self.marchCalculation.getLengthCompartmentRAC())))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m')))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(self.translate('Largura adotada para os compartimentos do RAC')))
        self.table.setItem(i, 1, QTableWidgetItem(
            self.utils.formatNum1Dec(self.marchCalculation.getWidthAdoptedCompartmentRAC())))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m')))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(self.translate('Concentração de DQO no efluente final')))
        self.table.setItem(i, 1, QTableWidgetItem(
            self.utils.formatNum2Dec(self.marchCalculation.getConcentrationDQOEffluentFinal())))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('g/m³')))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(self.translate('Eficiência de remoção total de DQO no processo')))
        self.table.setItem(i, 1, QTableWidgetItem(
            str(round(self.marchCalculation.getEfficiencyRemovalTotalDQOProcess() * 100))))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('%')))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(self.translate('Concentração de DBO no efluente final')))
        self.table.setItem(i, 1, QTableWidgetItem(
            self.utils.formatNum2Dec(self.marchCalculation.getConcentrationDBOEffluentFinal())))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('g/m³')))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(self.translate('Eficiência de remoção total de DBO no processo')))
        self.table.setItem(i, 1, QTableWidgetItem(
            str(round(self.marchCalculation.getEfficiencyRemovalTotalDBOProcess() * 100))))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('%')))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(self.translate('Vazão diária de biogás')))
        self.table.setItem(i, 1, QTableWidgetItem(self.utils.formatNum2Dec(self.marchCalculation.getDailyFlowBiogas())))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³/dia')))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(self.translate('Emissão de gás carbônico equivalente diária')))
        self.table.setItem(i, 1, QTableWidgetItem(
            self.utils.formatNum2Dec(self.marchCalculation.getEmissionGasCarbonicEquivalentDaily())))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('kg CO2e/dia')))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(self.translate('Área útil total')))
        self.table.setItem(i, 1, QTableWidgetItem(self.utils.formatNum1Dec(self.marchCalculation.getAreaUtilTotal())))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m²')))

        if not ProjectDataManager.get_project_config().should_calculate_area:
            return

        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(self.translate('Área construída total')))
        self.table.setItem(i, 1,
                           QTableWidgetItem(self.utils.formatNum1Dec(self.marchCalculation.getConstructedAreaTotal())))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m²')))
        


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
