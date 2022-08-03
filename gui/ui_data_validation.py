from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QColor
from qgis.PyQt.QtCore import Qt, QLocale
from qgis.PyQt.QtWidgets import (QLabel, QDialog, QTableWidgetItem, QTableWidget, QMessageBox,
                                 QAbstractItemView, QStyledItemDelegate, QPushButton, QGridLayout,
                                 QSpinBox, QDoubleSpinBox, QApplication)

from .dock_tabs.view.ui_dock_tab_sedimentation_tank_base import DockTabSedimentationTankBase
from .ui_rep_entrance_data import RepEntranceDataUI
from ..core.data.data_manager import ProjectDataManager
from ..core.data_validation import DataValidation
from ..core.data.entrance_data import ProjectData
from ..core.march_calculation import MarchCalculation
from ..utils.utils import Utils


class DataValidationUI:
    EDIT_DATA_RANGE = range(8, 12)

    def translate(self, msg, disambiguation=None, n=-1):
        return QCoreApplication.translate(DataValidationUI.__name__, msg, disambiguation, n)

    def __init__(self):
        self.utils = Utils()
        self.screen = QDialog()
        self.layout = QGridLayout()  # QVBoxLayout()
        self.table = QTableWidget()
        self.title = 'SaniHUB DWATS'
        self.ui_rep_entrance_data = RepEntranceDataUI()
        self.has_sedimentation_tank = False
        self.loc = QLocale()
        self.pb_save_edit = QPushButton()
        self.lb_dataEnt = QLabel()
        self.validation = DataValidation()
        self.pb_save_edit.setText(self.translate('Editar Dados'))
        self.edit_data_clicked_listeners = []
        # self.pb_save_edit.setFixedSize(100, 25)

    def show_dialog_validation(self):
        self.layout.addWidget(self.table, 0, 0)
        self.layout.addWidget(self.get_edit_push_button(), 1, 0, Qt.AlignRight)
        self.load_table()
        self.screen.setLayout(self.layout)
        app = QApplication.instance()
        allScreen = app.primaryScreen()
        geometry = allScreen.availableGeometry()
        self.screen.setGeometry(((geometry.width() - (self.table.horizontalHeader().length()) * 1.1) / 2.0),
                                (geometry.height() - self.table.verticalHeader().length() * 1.8) / 2.0,
                                self.table.horizontalHeader().length() * 1.055,
                                self.table.verticalHeader().length() * (1.44 if self.has_sedimentation_tank else 2.0))
        self.screen.setWindowTitle(self.title + ' - ' + self.translate('Verificação de conformidades do projeto'))
        self.screen.exec_()

    def on_edit_data_clicked(self, func):
        self.edit_data_clicked_listeners.append(func)

    def load_table(self):
        col_labels = [self.translate('Item'), self.translate('Valor'), self.translate('Unidade'),
                      self.translate('Orientação'), self.translate('Status'), self.translate('Correção')]

        table_data = []  # criamos aqui uma tabela 4 x n, onde n é a quantidade de conformidades

        self.has_sedimentation_tank = ProjectDataManager.get_project_config().has_sedimentation_tank
        if self.has_sedimentation_tank:
            table_data.append(
                [self.translate('Largura do Tanque de Sedimentação'),
                 self.utils.formatNum1Dec(ProjectDataManager.get_project_data().getWidthTank()),
                 self.translate('m'),
                 self.validation.validation_dimensions_ts()[1],
                 self.validation.validation_dimensions_ts()[0]
                 ]
            )

        calculation = MarchCalculation(ProjectDataManager.get_project_data(),
                                       ProjectDataManager.get_project_config().should_import_rede_basica)
        table_data.append(
            [self.translate('Velocidade ascensional '),
             self.utils.formatNum2Dec(calculation.get_climb_speed()),
             self.translate('m/h'),
             self.validation.validation_climb_speed()[1],
             self.validation.validation_climb_speed()[0]
             ]
        )
        table_data.append(
            [self.translate('Tempo de detenção hidráulica para o reator anaeróbio'),
             self.utils.formatNum2Dec(calculation.get_hydraulic_holding_time_rac()),
             self.translate('h'),
             self.validation.validation_hydraulic_holding_time_rac()[1],
             self.validation.validation_hydraulic_holding_time_rac()[0]
             ]
        )

        if self.has_sedimentation_tank:
            table_data.append(
                [self.translate('Tempo de detenção hidráulica para o tanque de sedimentação'),
                 self.utils.formatNum2Dec(calculation.get_hydraulic_holding_time_sedimentation_tank()),
                 self.translate('h'),
                 self.validation.validation_hydraulic_holding_time_sedimentation_tank()[1],
                 self.validation.validation_hydraulic_holding_time_sedimentation_tank()[0]
                 ]
            )

        n = len(table_data)
        self.table.setRowCount(n)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(col_labels)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 60)
        self.table.setColumnWidth(2, 60)
        self.table.setColumnWidth(3, 300)
        self.table.setColumnWidth(4, 90)
        # self.table.setColumnWidth(5, 100)
        self.table.setWordWrap(True)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # does not allow table editing
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # used to select entire rows instead of just the cell
        delegate = AlignDelegate(self.table)  # whole column alignment
        self.table.setItemDelegateForColumn(1, delegate)
        self.table.setItemDelegateForColumn(2, delegate)
        self.table.setItemDelegateForColumn(4, delegate)
        # self.table.setItemDelegateForColumn(5, delegate)

        for i, data in enumerate(table_data):
            self.table.setItem(i, 0, QTableWidgetItem(data[0]))
            self.table.setItem(i, 1, QTableWidgetItem(data[1]))
            self.table.setItem(i, 2, QTableWidgetItem(data[2]))
            self.table.setItem(i, 3, QTableWidgetItem(data[3]))
            item = QTableWidgetItem(
                self.translate('Conforme') if data[4] else self.translate('Não conforme'))
            item.setBackground(QColor(128, 255, 128) if data[4] else QColor(255, 128, 128))
            self.table.setItem(i, 4, item)
        # self.table.setSpan(0, 5, 4, 1)
        # self.table.setCellWidget(0, 5, self.get_edit_push_button())

        self.table.resizeRowsToContents()
        # self.screen.setGeometry(300, 30, 640, 430)

    def get_edit_push_button(self):
        button = QPushButton()

        def when_clicked():
            for func in self.edit_data_clicked_listeners:
                func()

        button.setText(self.translate("Editar Dados"))
        button.setFixedSize(110, 25)
        button.clicked.connect(when_clicked)
        return button

    def reload(self):
        self.load_table()


class AlignDelegate(QStyledItemDelegate):

    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
