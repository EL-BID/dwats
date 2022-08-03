from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt, QLocale, QProcess
from qgis.PyQt.QtWidgets import (QAction, QLabel, QDialog, QApplication,
                                 QFileDialog, QDialogButtonBox, QTableWidgetItem, QTableWidget, QTextBrowser,
                                 QMessageBox, QWidget, QAbstractItemView, QStyledItemDelegate, QScrollArea,
                                 QTabWidget, QFormLayout, QHBoxLayout, QRadioButton, QVBoxLayout, QFrame,
                                 QButtonGroup, QPushButton, QGridLayout, QStackedLayout, QSpinBox,
                                 QDoubleSpinBox, QAbstractButton)
# from ..core.march_calculation import MarchCalculation
from ..core.costs import CostsCalculator
from ..utils.utils import Utils


class RepOutDataCostsUI():
    screen = QDialog()
    layout = QGridLayout()
    table = QTableWidget()
    title = ''
    loc = QLocale()
    utils = Utils()
    costs: CostsCalculator = CostsCalculator()
    sedimentationTank = False
    pb_saveEditCosts = QPushButton()
    lb_costs = QLabel()

    max = 9999999

    dsb_item01_unity_dollar_TS = QDoubleSpinBox()
    dsb_item02_unity_dollar_TS = QDoubleSpinBox()
    dsb_item03_unity_dollar_TS = QDoubleSpinBox()
    dsb_item04_unity_dollar_TS = QDoubleSpinBox()
    dsb_item05_unity_dollar_TS = QDoubleSpinBox()
    dsb_item06_unity_dollar_TS = QDoubleSpinBox()
    dsb_item07_unity_dollar_TS = QDoubleSpinBox()
    dsb_item08_unity_dollar_TS = QDoubleSpinBox()
    dsb_item09_unity_dollar_TS = QDoubleSpinBox()
    dsb_item10_unity_dollar_TS = QDoubleSpinBox()
    dsb_item11_unity_dollar_TS = QDoubleSpinBox()
    dsb_item12_unity_dollar_TS = QDoubleSpinBox()
    dsb_item13_unity_dollar_TS = QDoubleSpinBox()
    dsb_item14_unity_dollar_TS = QDoubleSpinBox()
    dsb_item15_unity_dollar_TS = QDoubleSpinBox()
    dsb_item16_unity_dollar_TS = QDoubleSpinBox()

    dsb_item01_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item02_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item03_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item04_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item05_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item06_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item07_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item08_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item09_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item10_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item11_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item12_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item13_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item14_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item15_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item16_unity_dollar_reactor = QDoubleSpinBox()
    dsb_item17_unity_dollar_reactor = QDoubleSpinBox()

    dsb_list_entrance = [dsb_item01_unity_dollar_TS, dsb_item02_unity_dollar_TS, dsb_item03_unity_dollar_TS,
                         dsb_item04_unity_dollar_TS,
                         dsb_item05_unity_dollar_TS, dsb_item06_unity_dollar_TS, dsb_item07_unity_dollar_TS,
                         dsb_item08_unity_dollar_TS,
                         dsb_item09_unity_dollar_TS, dsb_item10_unity_dollar_TS, dsb_item11_unity_dollar_TS,
                         dsb_item12_unity_dollar_TS,
                         dsb_item13_unity_dollar_TS, dsb_item14_unity_dollar_TS, dsb_item15_unity_dollar_TS,
                         dsb_item16_unity_dollar_TS,
                         dsb_item01_unity_dollar_reactor, dsb_item02_unity_dollar_reactor,
                         dsb_item03_unity_dollar_reactor, dsb_item04_unity_dollar_reactor,
                         dsb_item05_unity_dollar_reactor, dsb_item06_unity_dollar_reactor,
                         dsb_item07_unity_dollar_reactor, dsb_item08_unity_dollar_reactor,
                         dsb_item09_unity_dollar_reactor, dsb_item10_unity_dollar_reactor,
                         dsb_item11_unity_dollar_reactor, dsb_item12_unity_dollar_reactor,
                         dsb_item13_unity_dollar_reactor, dsb_item14_unity_dollar_reactor,
                         dsb_item15_unity_dollar_reactor, dsb_item16_unity_dollar_reactor,
                         dsb_item17_unity_dollar_reactor]

    for i in dsb_list_entrance:
        i.setMaximum(max)
        i.setAlignment(Qt.AlignHCenter)
        i.setGroupSeparatorShown(True)

    # noinspection PyMethodMayBeStatic
    def translate(self, msg, disambiguation=None, n=-1):
        return QCoreApplication.translate(RepOutDataCostsUI.__name__, msg, disambiguation, n)

    def showReportCosts(self):
        dialogWidth = self.table.horizontalHeader().length() * 1.05
        if self.sedimentationTank:
            dialogHeight = self.table.verticalHeader().length() * 0.45
        else:
            dialogHeight = self.table.verticalHeader().length() * 0.8
        self.table.verticalHeader().setVisible(False)
        #self.screen.setFixedSize(dialogWidth, dialogHeight)
        app = QApplication.instance()
        allScreen = app.primaryScreen()
        geometry = allScreen.availableGeometry()
        self.screen.setGeometry(((geometry.width() - (self.table.horizontalHeader().length()) * 1.1) / 2.0),
                                (geometry.height() - self.table.verticalHeader().length() *
                                 (0.48 if self.sedimentationTank else 0.82)) / 2.0,
                                self.table.horizontalHeader().length() * 1.055,
                                self.table.verticalHeader().length() *
                                (0.5 if self.sedimentationTank else 0.85))
        self.screen.exec_()

    def loadReportCosts(self, costs, tank, title):
        self.costs = costs
        self.sedimentationTank = tank
        self.title = title
        self.screen.setWindowTitle(self.title + self.translate(' - Custos'))
        self.pb_saveEditCosts.setText(self.translate('Salvar'))
        self.pb_saveEditCosts.setFixedSize(100, 25)
        self.layout.addWidget(self.pb_saveEditCosts, 0, 0, Qt.AlignRight)
        self.loadTable()
        self.layout.addWidget(self.table, 1, 0)
        self.screen.setLayout(self.layout)
        #app = QApplication.instance()
        #allScreen = app.primaryScreen()
        #geometry = allScreen.availableGeometry()
        #self.screen.setGeometry(((geometry.width() - (self.screen.frameGeometry().width() * 1.2)) / 2.0),
        #                        (geometry.height() - self.screen.frameGeometry().height()) / 3.0,
        #                        self.screen.frameGeometry().width(), self.screen.frameGeometry().height())


    def loadTable(self):
        colLabels = [self.translate('Item'), self.translate('Descrição dos serviços'), self.translate('Unidade'),
                     self.translate('Qtd.'), self.translate('Preço unitário USD'), self.translate('Valor USD')]
        if self.sedimentationTank:
            self.table.setRowCount(41)
        else:
            self.table.setRowCount(21)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(colLabels)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 110)
        self.table.setColumnWidth(5, 110)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # does not allow table editing
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # Used to select entire rows instead of just the cell
        delegate = AlignDelegate(self.table)  # whole column alignment
        self.table.setItemDelegateForColumn(0, delegate)
        self.table.setItemDelegateForColumn(2, delegate)
        self.table.setItemDelegateForColumn(3, delegate)
        self.table.setItemDelegateForColumn(5, delegate)

        self.dsb_item01_unity_dollar_TS.setValue(self.costs.getVlItem01())
        self.dsb_item02_unity_dollar_TS.setValue(self.costs.getVlItem02())
        self.dsb_item03_unity_dollar_TS.setValue(self.costs.getVlItem03())
        self.dsb_item04_unity_dollar_TS.setValue(self.costs.getVlItem04())
        self.dsb_item05_unity_dollar_TS.setValue(self.costs.getVlItem05())
        self.dsb_item06_unity_dollar_TS.setValue(self.costs.getVlItem06())
        self.dsb_item07_unity_dollar_TS.setValue(self.costs.getVlItem07())
        self.dsb_item08_unity_dollar_TS.setValue(self.costs.getVlItem08())
        self.dsb_item09_unity_dollar_TS.setValue(self.costs.getVlItem09())
        self.dsb_item10_unity_dollar_TS.setValue(self.costs.getVlItem10())
        self.dsb_item11_unity_dollar_TS.setValue(self.costs.getVlItem11())
        self.dsb_item12_unity_dollar_TS.setValue(self.costs.getVlItem12())
        self.dsb_item13_unity_dollar_TS.setValue(self.costs.getVlItem13())
        self.dsb_item14_unity_dollar_TS.setValue(self.costs.getVlItem14())
        self.dsb_item15_unity_dollar_TS.setValue(self.costs.getVlItem15())
        self.dsb_item16_unity_dollar_TS.setValue(self.costs.getVlItem16())

        self.dsb_item01_unity_dollar_reactor.setValue(self.costs.getVlItem01())
        self.dsb_item02_unity_dollar_reactor.setValue(self.costs.getVlItem02())
        self.dsb_item03_unity_dollar_reactor.setValue(self.costs.getVlItem03())
        self.dsb_item04_unity_dollar_reactor.setValue(self.costs.getVlItem04())
        self.dsb_item05_unity_dollar_reactor.setValue(self.costs.getVlItem05())
        self.dsb_item06_unity_dollar_reactor.setValue(self.costs.getVlItem06())
        self.dsb_item07_unity_dollar_reactor.setValue(self.costs.getVlItem07())
        self.dsb_item08_unity_dollar_reactor.setValue(self.costs.getVlItem08())
        self.dsb_item09_unity_dollar_reactor.setValue(self.costs.getVlItem09())
        self.dsb_item10_unity_dollar_reactor.setValue(self.costs.getVlItem10())
        self.dsb_item11_unity_dollar_reactor.setValue(self.costs.getVlItem11())
        self.dsb_item12_unity_dollar_reactor.setValue(self.costs.getVlItem12())
        self.dsb_item13_unity_dollar_reactor.setValue(self.costs.getVlItem13())
        self.dsb_item14_unity_dollar_reactor.setValue(self.costs.getVlItem14())
        self.dsb_item15_unity_dollar_reactor.setValue(self.costs.getVlItem15())
        self.dsb_item16_unity_dollar_reactor.setValue(self.costs.getVlItem16())
        self.dsb_item17_unity_dollar_reactor.setValue(self.costs.getVlItem17())

        i = 0
        if self.sedimentationTank:
            self.table.setItem(i, 0, QTableWidgetItem(self.translate('TANQUE DE SEDIMENTAÇÃO')))
            self.table.setSpan(i, 0, 1, 6)
            self.table.item(i, 0).setFont(self.utils.formatBoldText())
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(self.translate('MOVIMENTO DE SOLO E ROCHA')))
            self.table.setSpan(i, 0, 1, 6)
            self.table.item(i, 0).setFont(self.utils.formatBoldText())
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 1)))
            self.table.setItem(i, 1, QTableWidgetItem(self.translate(
                'ESCAV. MECANIZ. DE VALAS - ESGOTO - EM SOLO DE 2a CAT. EXECUTADA ENTRE AS PROFUND. DE 4 A 6,00m')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem01TS())))
            self.table.setCellWidget(i, 4, self.dsb_item01_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem01TS() * self.dsb_item01_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 1)))
            self.table.setItem(i, 1, QTableWidgetItem(self.translate(
                'ESCAV. DE VALAS - ESGOTO - EM ROCHA BRANDA EXECUTADA ENTRE AS PROFUND. DE 4 A6,00 m, C/ USO DE ROMPEDOR PNEUMATICO')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem02TS())))
            self.table.setCellWidget(i, 4, self.dsb_item02_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem02TS() * self.dsb_item02_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 1)))
            self.table.setItem(i, 1, QTableWidgetItem(self.translate('CARGA E DESCARGA DE SOLO')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem03TS())))
            self.table.setCellWidget(i, 4, self.dsb_item03_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem03TS() * self.dsb_item03_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 1)))
            self.table.setItem(i, 1, QTableWidgetItem(
                self.translate('MOVIMENTO DE TRANSPORTE DE SOLO, EM CAMINHAO BASCULANTE')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³xKm')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem04TS())))
            self.table.setCellWidget(i, 4, self.dsb_item04_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem04TS() * self.dsb_item04_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 1)))
            self.table.setItem(i, 1, QTableWidgetItem(self.translate('CARGA E DESCARGA DE ROCHA')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem05TS())))
            self.table.setCellWidget(i, 4, self.dsb_item05_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem05TS() * self.dsb_item05_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 1)))
            self.table.setItem(i, 1, QTableWidgetItem(
                self.translate('MOVIMENTO DE TRANSPORTE DE ROCHA, EM CAMINHAO BASCULANTE')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem06TS())))
            self.table.setCellWidget(i, 4, self.dsb_item06_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem06TS() * self.dsb_item06_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 1)))
            self.table.setItem(i, 1, QTableWidgetItem(self.translate(
                'EXEC. DE ATERRO EM VALAS/POCOS/CAVAS DE FUNDACAO, C/ FORNEC. DE SOLO, INCL.  LANCAM., ESPALHAM., COMPACT. C/PLACA VIBRATORIA, SOQUETE PNEUMATICO OU  SOQUETEMANUAL - DMT=20KM')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem07TS())))
            self.table.setCellWidget(i, 4, self.dsb_item07_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem07TS() * self.dsb_item07_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(self.translate('ESCORAMENTO')))
            self.table.setSpan(i, 0, 1, 6)
            self.table.item(i, 0).setFont(self.utils.formatBoldText())
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 2)))
            self.table.setItem(i, 1, QTableWidgetItem(
                self.translate('ESCORAMENTO CONTINUO COM PRACHA METALICA C/H ACIMA DE 3,0m')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m²')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem08TS())))
            self.table.setCellWidget(i, 4, self.dsb_item08_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem08TS() * self.dsb_item08_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(self.translate('ESTRUTURAS E FUNDACOES')))
            self.table.setSpan(i, 0, 1, 6)
            self.table.item(i, 0).setFont(self.utils.formatBoldText())
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 3)))
            self.table.setItem(i, 1, QTableWidgetItem(self.translate(
                'CONCRETO C/ CONSUMO MIN. DE CIMENTO DE 150Kg/m3, INCL. FORNEC. DE MAT., PRODUCAO, LANC., ADENS. E CURA')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem09TS())))
            self.table.setCellWidget(i, 4, self.dsb_item09_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem09TS() * self.dsb_item09_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 3)))
            self.table.setItem(i, 1, QTableWidgetItem(
                self.translate('FORMA PLANA EM COMP. RESINADO P/ RESERV. APOIADO - E=12MM ATE 3X')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m²')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem10TS())))
            self.table.setCellWidget(i, 4, self.dsb_item10_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem10TS() * self.dsb_item10_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 3)))
            self.table.setItem(i, 1, QTableWidgetItem(
                self.translate('CONCRETO FCK=25MPa, INCL. FORNEC. DOS  MAT., PRODUCAO, LANC.,ADENS. E CURA (LAJES)')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem11TS())))
            self.table.setCellWidget(i, 4, self.dsb_item11_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem11TS() * self.dsb_item11_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 3)))
            self.table.setItem(i, 1, QTableWidgetItem(
                self.translate('CONCRETO FCK=25MPa, INCL. FORNEC. DOS  MAT., PRODUCAO, LANC.,ADENS. E CURA (PAREDES)')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('Kg')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem12TS())))
            self.table.setCellWidget(i, 4, self.dsb_item12_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem12TS() * self.dsb_item12_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 3)))
            self.table.setItem(i, 1, QTableWidgetItem(
                self.translate('ACO CA-50, INCL. FORNEC., CORTE, DOBR. E COLOCACAO NAS PECAS')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('Kg')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem13TS())))
            self.table.setCellWidget(i, 4, self.dsb_item13_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem13TS() * self.dsb_item13_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 3)))
            self.table.setItem(i, 1, QTableWidgetItem(self.translate('CIMBRAMENTO P/ RESERVATORIOS APOIADOS')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem14TS())))
            self.table.setCellWidget(i, 4, self.dsb_item14_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem14TS() * self.dsb_item14_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 3)))
            self.table.setItem(i, 1, QTableWidgetItem(self.translate('TAMPA CONCRETO PREMOLDADO FCK=15,0 MPA E=15 CM')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m²')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem15TS())))
            self.table.setCellWidget(i, 4, self.dsb_item15_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem15TS() * self.dsb_item15_unity_dollar_TS.value())))
            i += 1
            self.table.setItem(i, 0, QTableWidgetItem(str(i - 3)))
            self.table.setItem(i, 1, QTableWidgetItem(
                self.translate('ALVENARIA DE VEDACAO C/ TIJOLO MACICO (COMUM) C/ e=20cm (MRR / RMS)')))
            self.table.setItem(i, 2, QTableWidgetItem(self.translate('m²')))
            self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem16TS())))
            self.table.setCellWidget(i, 4, self.dsb_item16_unity_dollar_TS)
            self.table.setItem(i, 5, QTableWidgetItem(
                self.utils.formatNum2Dec(self.costs.qtdItem16TS() * self.dsb_item16_unity_dollar_TS.value())))
            i += 1
            self.dsb_item01_unity_dollar_TS.valueChanged.connect(self.setItem01TS)
            self.dsb_item02_unity_dollar_TS.valueChanged.connect(self.setItem02TS)
            self.dsb_item03_unity_dollar_TS.valueChanged.connect(self.setItem03TS)
            self.dsb_item04_unity_dollar_TS.valueChanged.connect(self.setItem04TS)
            self.dsb_item05_unity_dollar_TS.valueChanged.connect(self.setItem05TS)
            self.dsb_item06_unity_dollar_TS.valueChanged.connect(self.setItem06TS)
            self.dsb_item07_unity_dollar_TS.valueChanged.connect(self.setItem07TS)
            self.dsb_item08_unity_dollar_TS.valueChanged.connect(self.setItem08TS)
            self.dsb_item09_unity_dollar_TS.valueChanged.connect(self.setItem09TS)
            self.dsb_item10_unity_dollar_TS.valueChanged.connect(self.setItem10TS)
            self.dsb_item11_unity_dollar_TS.valueChanged.connect(self.setItem11TS)
            self.dsb_item12_unity_dollar_TS.valueChanged.connect(self.setItem12TS)
            self.dsb_item13_unity_dollar_TS.valueChanged.connect(self.setItem13TS)
            self.dsb_item14_unity_dollar_TS.valueChanged.connect(self.setItem14TS)
            self.dsb_item15_unity_dollar_TS.valueChanged.connect(self.setItem15TS)
            self.dsb_item16_unity_dollar_TS.valueChanged.connect(self.setItem16TS)

        self.table.setItem(i, 0, QTableWidgetItem(self.translate('REATOR')))
        self.table.setSpan(i, 0, 1, 6)
        self.table.item(i, 0).setFont(self.utils.formatBoldText())
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(self.translate('MOVIMENTO DE SOLO E ROCHA')))
        self.table.setSpan(i, 0, 1, 6)
        self.table.item(i, 0).setFont(self.utils.formatBoldText())
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 1 if not self.sedimentationTank else i - 5)))
        self.table.setItem(i, 1, QTableWidgetItem(self.translate(
            'ESCAV. MECANIZ. DE VALAS - ESGOTO - EM SOLO DE 2a CAT. EXECUTADA ENTRE AS PROFUND. DE 4 A 6,00m')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem01Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item01_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem01Reactor() * self.dsb_item01_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 1 if not self.sedimentationTank else i - 5)))
        self.table.setItem(i, 1, QTableWidgetItem(self.translate(
            'ESCAV. DE VALAS - ESGOTO - EM ROCHA BRANDA EXECUTADA ENTRE AS PROFUND. DE 4 A6,00 m, C/ USO DE ROMPEDOR PNEUMATICO')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem02Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item02_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem02Reactor() * self.dsb_item02_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 1 if not self.sedimentationTank else i - 5)))
        self.table.setItem(i, 1, QTableWidgetItem(self.translate('CARGA E DESCARGA DE SOLO')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem03Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item03_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem03Reactor() * self.dsb_item03_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 1 if not self.sedimentationTank else i - 5)))
        self.table.setItem(i, 1,
                           QTableWidgetItem(self.translate('MOVIMENTO DE TRANSPORTE DE SOLO, EM CAMINHAO BASCULANTE')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³xKm')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem04Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item04_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem04Reactor() * self.dsb_item04_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 1 if not self.sedimentationTank else i - 5)))
        self.table.setItem(i, 1, QTableWidgetItem(self.translate('CARGA E DESCARGA DE ROCHA')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem05Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item05_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem05Reactor() * self.dsb_item05_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 1 if not self.sedimentationTank else i - 5)))
        self.table.setItem(i, 1,
                           QTableWidgetItem(self.translate('MOVIMENTO DE TRANSPORTE DE ROCHA, EM CAMINHAO BASCULANTE')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem06Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item06_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem06Reactor() * self.dsb_item06_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 1 if not self.sedimentationTank else i - 5)))
        self.table.setItem(i, 1, QTableWidgetItem(self.translate(
            'EXEC. DE ATERRO EM VALAS/POCOS/CAVAS DE FUNDACAO, C/ FORNEC. DE SOLO, INCL.  LANCAM., ESPALHAM., COMPACT. C/PLACA VIBRATORIA, SOQUETE PNEUMATICO OU  SOQUETEMANUAL - DMT=20KM')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem07Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item07_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem07Reactor() * self.dsb_item07_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(self.translate('ESCORAMENTO')))
        self.table.setSpan(i, 0, 1, 6)
        self.table.item(i, 0).setFont(self.utils.formatBoldText())
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 2 if not self.sedimentationTank else i - 6)))
        self.table.setItem(i, 1, QTableWidgetItem(
            self.translate('ESCORAMENTO CONTINUO COM PRACHA METALICA C/H ACIMA DE 3,0m')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m²')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem08Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item08_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem08Reactor() * self.dsb_item08_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(self.translate('ESTRUTURAS E FUNDACOES')))
        self.table.setSpan(i, 0, 1, 6)
        self.table.item(i, 0).setFont(self.utils.formatBoldText())
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 3 if not self.sedimentationTank else i - 7)))
        self.table.setItem(i, 1, QTableWidgetItem(self.translate(
            'CONCRETO C/ CONSUMO MIN. DE CIMENTO DE 150Kg/m3, INCL. FORNEC. DE MAT., PRODUCAO, LANC., ADENS. E CURA')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem09Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item09_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem09Reactor() * self.dsb_item09_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 3 if not self.sedimentationTank else i - 7)))
        self.table.setItem(i, 1, QTableWidgetItem(
            self.translate('FORMA PLANA EM COMP. RESINADO P/ RESERV. APOIADO - E=12MM ATE 3X')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m²')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem10Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item10_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem10Reactor() * self.dsb_item10_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 3 if not self.sedimentationTank else i - 7)))
        self.table.setItem(i, 1, QTableWidgetItem(
            self.translate('CONCRETO FCK=25MPa, INCL. FORNEC. DOS  MAT., PRODUCAO, LANC.,ADENS. E CURA (LAJES)')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem11Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item11_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem11Reactor() * self.dsb_item11_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 3 if not self.sedimentationTank else i - 7)))
        self.table.setItem(i, 1, QTableWidgetItem(
            self.translate('CONCRETO FCK=25MPa, INCL. FORNEC. DOS  MAT., PRODUCAO, LANC.,ADENS. E CURA (PAREDES)')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('Kg')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem12Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item12_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem12Reactor() * self.dsb_item12_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 3 if not self.sedimentationTank else i - 7)))
        self.table.setItem(i, 1, QTableWidgetItem(
            self.translate('ACO CA-50, INCL. FORNEC., CORTE, DOBR. E COLOCACAO NAS PECAS')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('Kg')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem13Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item13_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem13Reactor() * self.dsb_item13_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 3 if not self.sedimentationTank else i - 7)))
        self.table.setItem(i, 1, QTableWidgetItem(self.translate('CIMBRAMENTO P/ RESERVATORIOS APOIADOS')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m³')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem14Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item14_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem14Reactor() * self.dsb_item14_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 3 if not self.sedimentationTank else i - 7)))
        self.table.setItem(i, 1, QTableWidgetItem(self.translate('TAMPA CONCRETO PREMOLDADO FCK=15,0 MPA E=15 CM')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m²')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem15Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item15_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem15Reactor() * self.dsb_item15_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 3 if not self.sedimentationTank else i - 7)))
        self.table.setItem(i, 1, QTableWidgetItem(
            self.translate('ALVENARIA DE VEDACAO C/ TIJOLO MACICO (COMUM) C/ e=20cm (MRR / RMS)')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m²')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem16Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item16_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem16Reactor() * self.dsb_item16_unity_dollar_reactor.value())))
        i += 1
        self.table.setItem(i, 0, QTableWidgetItem(str(i - 3 if not self.sedimentationTank else i - 7)))
        self.table.setItem(i, 1, QTableWidgetItem(self.translate('CHICANAS EM PLACAS DE CONCRETO')))
        self.table.setItem(i, 2, QTableWidgetItem(self.translate('m²')))
        self.table.setItem(i, 3, QTableWidgetItem(self.utils.formatNum2Dec(self.costs.qtdItem17Reactor())))
        self.table.setCellWidget(i, 4, self.dsb_item17_unity_dollar_reactor)
        self.table.setItem(i, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem17Reactor() * self.dsb_item17_unity_dollar_reactor.value())))

        self.dsb_item01_unity_dollar_reactor.valueChanged.connect(self.setItem01Reactor)
        self.dsb_item02_unity_dollar_reactor.valueChanged.connect(self.setItem02Reactor)
        self.dsb_item03_unity_dollar_reactor.valueChanged.connect(self.setItem03Reactor)
        self.dsb_item04_unity_dollar_reactor.valueChanged.connect(self.setItem04Reactor)
        self.dsb_item05_unity_dollar_reactor.valueChanged.connect(self.setItem05Reactor)
        self.dsb_item06_unity_dollar_reactor.valueChanged.connect(self.setItem06Reactor)
        self.dsb_item07_unity_dollar_reactor.valueChanged.connect(self.setItem07Reactor)
        self.dsb_item08_unity_dollar_reactor.valueChanged.connect(self.setItem08Reactor)
        self.dsb_item09_unity_dollar_reactor.valueChanged.connect(self.setItem09Reactor)
        self.dsb_item10_unity_dollar_reactor.valueChanged.connect(self.setItem10Reactor)
        self.dsb_item11_unity_dollar_reactor.valueChanged.connect(self.setItem11Reactor)
        self.dsb_item12_unity_dollar_reactor.valueChanged.connect(self.setItem12Reactor)
        self.dsb_item13_unity_dollar_reactor.valueChanged.connect(self.setItem13Reactor)
        self.dsb_item14_unity_dollar_reactor.valueChanged.connect(self.setItem14Reactor)
        self.dsb_item15_unity_dollar_reactor.valueChanged.connect(self.setItem15Reactor)
        self.dsb_item16_unity_dollar_reactor.valueChanged.connect(self.setItem16Reactor)
        self.dsb_item17_unity_dollar_reactor.valueChanged.connect(self.setItem17Reactor)

    # ts
    def setItem01TS(self):
        self.table.setItem(2, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem01TS() * self.dsb_item01_unity_dollar_TS.value())))
        #A alteracao do valor de um item no TS implica que o mesmo valor seja aplicado no reator
        self.dsb_item01_unity_dollar_reactor.setValue(self.dsb_item01_unity_dollar_TS.value())

    def setItem02TS(self):
        self.table.setItem(3, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem02TS() * self.dsb_item02_unity_dollar_TS.value())))
        self.dsb_item02_unity_dollar_reactor.setValue(self.dsb_item02_unity_dollar_TS.value())

    def setItem03TS(self):
        self.table.setItem(4, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem03TS() * self.dsb_item03_unity_dollar_TS.value())))
        self.dsb_item03_unity_dollar_reactor.setValue(self.dsb_item03_unity_dollar_TS.value())

    def setItem04TS(self):
        self.table.setItem(5, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem04TS() * self.dsb_item04_unity_dollar_TS.value())))
        self.dsb_item04_unity_dollar_reactor.setValue(self.dsb_item04_unity_dollar_TS.value())

    def setItem05TS(self):
        self.table.setItem(6, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem05TS() * self.dsb_item05_unity_dollar_TS.value())))
        self.dsb_item05_unity_dollar_reactor.setValue(self.dsb_item05_unity_dollar_TS.value())

    def setItem06TS(self):
        self.table.setItem(7, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem06TS() * self.dsb_item06_unity_dollar_TS.value())))
        self.dsb_item06_unity_dollar_reactor.setValue(self.dsb_item06_unity_dollar_TS.value())

    def setItem07TS(self):
        self.table.setItem(8, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem07TS() * self.dsb_item07_unity_dollar_TS.value())))
        self.dsb_item07_unity_dollar_reactor.setValue(self.dsb_item07_unity_dollar_TS.value())

    def setItem08TS(self):
        self.table.setItem(10, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem08TS() * self.dsb_item08_unity_dollar_TS.value())))
        self.dsb_item08_unity_dollar_reactor.setValue(self.dsb_item08_unity_dollar_TS.value())

    def setItem09TS(self):
        self.table.setItem(12, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem09TS() * self.dsb_item09_unity_dollar_TS.value())))
        self.dsb_item09_unity_dollar_reactor.setValue(self.dsb_item09_unity_dollar_TS.value())

    def setItem10TS(self):
        self.table.setItem(13, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem10TS() * self.dsb_item10_unity_dollar_TS.value())))
        self.dsb_item10_unity_dollar_reactor.setValue(self.dsb_item10_unity_dollar_TS.value())

    def setItem11TS(self):
        self.table.setItem(14, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem11TS() * self.dsb_item11_unity_dollar_TS.value())))
        self.dsb_item11_unity_dollar_reactor.setValue(self.dsb_item11_unity_dollar_TS.value())

    def setItem12TS(self):
        self.table.setItem(15, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem12TS() * self.dsb_item12_unity_dollar_TS.value())))
        self.dsb_item12_unity_dollar_reactor.setValue(self.dsb_item12_unity_dollar_TS.value())

    def setItem13TS(self):
        self.table.setItem(16, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem13TS() * self.dsb_item13_unity_dollar_TS.value())))
        self.dsb_item13_unity_dollar_reactor.setValue(self.dsb_item13_unity_dollar_TS.value())

    def setItem14TS(self):
        self.table.setItem(17, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem14TS() * self.dsb_item14_unity_dollar_TS.value())))
        self.dsb_item14_unity_dollar_reactor.setValue(self.dsb_item14_unity_dollar_TS.value())

    def setItem15TS(self):
        self.table.setItem(18, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem15TS() * self.dsb_item15_unity_dollar_TS.value())))
        self.dsb_item15_unity_dollar_reactor.setValue(self.dsb_item15_unity_dollar_TS.value())

    def setItem16TS(self):
        self.table.setItem(19, 5, QTableWidgetItem(
            self.utils.formatNum2Dec(self.costs.qtdItem16TS() * self.dsb_item16_unity_dollar_TS.value())))
        self.dsb_item16_unity_dollar_reactor.setValue(self.dsb_item16_unity_dollar_TS.value())

    # reator

    def setItem01Reactor(self):
        self.table.setItem(2 if not self.sedimentationTank else 22, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem01Reactor() * self.dsb_item01_unity_dollar_reactor.value())))
        self.dsb_item01_unity_dollar_TS.setValue(self.dsb_item01_unity_dollar_reactor.value())

    def setItem02Reactor(self):
        self.table.setItem(3 if not self.sedimentationTank else 23, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem02Reactor() * self.dsb_item02_unity_dollar_reactor.value())))
        self.dsb_item02_unity_dollar_TS.setValue(self.dsb_item02_unity_dollar_reactor.value())

    def setItem03Reactor(self):
        self.table.setItem(4 if not self.sedimentationTank else 24, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem03Reactor() * self.dsb_item03_unity_dollar_reactor.value())))
        self.dsb_item03_unity_dollar_TS.setValue(self.dsb_item03_unity_dollar_reactor.value())

    def setItem04Reactor(self):
        self.table.setItem(5 if not self.sedimentationTank else 25, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem04Reactor() * self.dsb_item04_unity_dollar_reactor.value())))
        self.dsb_item04_unity_dollar_TS.setValue(self.dsb_item04_unity_dollar_reactor.value())

    def setItem05Reactor(self):
        self.table.setItem(6 if not self.sedimentationTank else 26, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem05Reactor() * self.dsb_item05_unity_dollar_reactor.value())))
        self.dsb_item05_unity_dollar_TS.setValue(self.dsb_item05_unity_dollar_reactor.value())

    def setItem06Reactor(self):
        self.table.setItem(7 if not self.sedimentationTank else 27, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem06Reactor() * self.dsb_item06_unity_dollar_reactor.value())))
        self.dsb_item06_unity_dollar_TS.setValue(self.dsb_item06_unity_dollar_reactor.value())

    def setItem07Reactor(self):
        self.table.setItem(8 if not self.sedimentationTank else 28, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem07Reactor() * self.dsb_item07_unity_dollar_reactor.value())))
        self.dsb_item07_unity_dollar_TS.setValue(self.dsb_item07_unity_dollar_reactor.value())

    def setItem08Reactor(self):
        self.table.setItem(10 if not self.sedimentationTank else 30, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem08Reactor() * self.dsb_item08_unity_dollar_reactor.value())))
        self.dsb_item08_unity_dollar_TS.setValue(self.dsb_item08_unity_dollar_reactor.value())

    def setItem09Reactor(self):
        self.table.setItem(12 if not self.sedimentationTank else 32, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem09Reactor() * self.dsb_item09_unity_dollar_reactor.value())))
        self.dsb_item09_unity_dollar_TS.setValue(self.dsb_item09_unity_dollar_reactor.value())

    def setItem10Reactor(self):
        self.table.setItem(13 if not self.sedimentationTank else 33, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem10Reactor() * self.dsb_item10_unity_dollar_reactor.value())))
        self.dsb_item10_unity_dollar_TS.setValue(self.dsb_item10_unity_dollar_reactor.value())

    def setItem11Reactor(self):
        self.table.setItem(14 if not self.sedimentationTank else 34, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem11Reactor() * self.dsb_item11_unity_dollar_reactor.value())))
        self.dsb_item11_unity_dollar_TS.setValue(self.dsb_item11_unity_dollar_reactor.value())

    def setItem12Reactor(self):
        self.table.setItem(15 if not self.sedimentationTank else 35, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem12Reactor() * self.dsb_item12_unity_dollar_reactor.value())))
        self.dsb_item12_unity_dollar_TS.setValue(self.dsb_item12_unity_dollar_reactor.value())

    def setItem13Reactor(self):
        self.table.setItem(16 if not self.sedimentationTank else 36, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem13Reactor() * self.dsb_item13_unity_dollar_reactor.value())))
        self.dsb_item13_unity_dollar_TS.setValue(self.dsb_item13_unity_dollar_reactor.value())

    def setItem14Reactor(self):
        self.table.setItem(17 if not self.sedimentationTank else 37, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem14Reactor() * self.dsb_item14_unity_dollar_reactor.value())))
        self.dsb_item14_unity_dollar_TS.setValue(self.dsb_item14_unity_dollar_reactor.value())

    def setItem15Reactor(self):
        self.table.setItem(18 if not self.sedimentationTank else 38, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem15Reactor() * self.dsb_item15_unity_dollar_reactor.value())))
        self.dsb_item15_unity_dollar_TS.setValue(self.dsb_item15_unity_dollar_reactor.value())

    def setItem16Reactor(self):
        self.table.setItem(19 if not self.sedimentationTank else 39, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem16Reactor() * self.dsb_item16_unity_dollar_reactor.value())))
        self.dsb_item16_unity_dollar_TS.setValue(self.dsb_item16_unity_dollar_reactor.value())

    def setItem17Reactor(self):
        self.table.setItem(20 if not self.sedimentationTank else 40, 5,
                           QTableWidgetItem(self.utils.formatNum2Dec(
                               self.costs.qtdItem17Reactor() * self.dsb_item17_unity_dollar_reactor.value())))

    def checkData(self):
        if (self.dsb_item01_unity_dollar_TS.value() != 0 and self.dsb_item02_unity_dollar_TS.value() != 0
                and self.dsb_item03_unity_dollar_TS.value() != 0 and self.dsb_item04_unity_dollar_TS.value() != 0
                and self.dsb_item05_unity_dollar_TS.value() != 0 and self.dsb_item06_unity_dollar_TS.value() != 0
                and self.dsb_item07_unity_dollar_TS.value() != 0 and self.dsb_item08_unity_dollar_TS.value() != 0
                and self.dsb_item09_unity_dollar_TS.value() != 0 and self.dsb_item10_unity_dollar_TS.value() != 0
                and self.dsb_item11_unity_dollar_TS.value() != 0 and self.dsb_item12_unity_dollar_TS.value() != 0
                and self.dsb_item13_unity_dollar_TS.value() != 0 and self.dsb_item14_unity_dollar_TS.value() != 0
                and self.dsb_item15_unity_dollar_TS.value() != 0 and self.dsb_item16_unity_dollar_TS.value() != 0
                and self.dsb_item01_unity_dollar_reactor.value() != 0 and self.dsb_item02_unity_dollar_reactor.value() != 0
                and self.dsb_item03_unity_dollar_reactor.value() != 0 and self.dsb_item04_unity_dollar_reactor.value() != 0
                and self.dsb_item05_unity_dollar_reactor.value() != 0 and self.dsb_item06_unity_dollar_reactor.value() != 0
                and self.dsb_item07_unity_dollar_reactor.value() != 0 and self.dsb_item08_unity_dollar_reactor.value() != 0
                and self.dsb_item09_unity_dollar_reactor.value() != 0 and self.dsb_item10_unity_dollar_reactor.value() != 0
                and self.dsb_item11_unity_dollar_reactor.value() != 0 and self.dsb_item12_unity_dollar_reactor.value() != 0
                and self.dsb_item13_unity_dollar_reactor.value() != 0 and self.dsb_item14_unity_dollar_reactor.value() != 0
                and self.dsb_item15_unity_dollar_reactor.value() != 0 and self.dsb_item16_unity_dollar_reactor.value() != 0
                and self.dsb_item17_unity_dollar_reactor.value() != 0):
            return True
        else:
            return False

    def saveChanges(self):
        if self.checkData():
            self.costs.setVlItem01(self.dsb_item01_unity_dollar_reactor.value())
            self.costs.setVlItem02(self.dsb_item02_unity_dollar_reactor.value())
            self.costs.setVlItem03(self.dsb_item03_unity_dollar_reactor.value())
            self.costs.setVlItem04(self.dsb_item04_unity_dollar_reactor.value())
            self.costs.setVlItem05(self.dsb_item05_unity_dollar_reactor.value())
            self.costs.setVlItem06(self.dsb_item06_unity_dollar_reactor.value())
            self.costs.setVlItem07(self.dsb_item07_unity_dollar_reactor.value())
            self.costs.setVlItem08(self.dsb_item08_unity_dollar_reactor.value())
            self.costs.setVlItem09(self.dsb_item09_unity_dollar_reactor.value())
            self.costs.setVlItem10(self.dsb_item10_unity_dollar_reactor.value())
            self.costs.setVlItem11(self.dsb_item11_unity_dollar_reactor.value())
            self.costs.setVlItem12(self.dsb_item12_unity_dollar_reactor.value())
            self.costs.setVlItem13(self.dsb_item13_unity_dollar_reactor.value())
            self.costs.setVlItem14(self.dsb_item14_unity_dollar_reactor.value())
            self.costs.setVlItem15(self.dsb_item15_unity_dollar_reactor.value())
            self.costs.setVlItem16(self.dsb_item16_unity_dollar_reactor.value())
            self.costs.setVlItem17(self.dsb_item17_unity_dollar_reactor.value())
            icon = QMessageBox.Information
            self.utils.showDialog(self.title, self.translate('Dados alterados com sucesso!'), icon)
            self.screen.close()
        else:
            icon = QMessageBox.Critical
            self.utils.showDialog(self.title, self.translate('Existe serviços com valores zerados.'), icon)


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
