from typing import Union, Tuple, List

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from qgis.PyQt.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QRadioButton, QButtonGroup, \
    QDialog, QVBoxLayout, QLayout, QWidget, QSizePolicy, QMessageBox, QTabWidget
from qgis._core import QgsFeatureRequest
from qgis.core import QgsMessageLog, QgsProject

from .ui_dock_tab_home_head_layout import HeadFormLayout
from ....utils.utils import Utils
from ....utils.icons import icon_save, icon_rep_PDF, icon_edit, icon_add
from ...ui_entrance_data import EntranceDataUI

from ..base.ui_dock_tab_edit_button_base import DockTabEditButtonBase
from ...ui_rep_entrance_data import RepEntranceDataUI
from ...ui_rep_out_data import RepOutDataGeneralUI
from ....gui.ui_data_validation import DataValidationUI


class DockTabHomeBase(DockTabEditButtonBase):
    """Sets the home dock gui.
    Here we just define how the layout will be, without any logic."""

    EDIT_DATA_RANGE = RepEntranceDataUI.RANGE_ALL_DATA

    title = 'SaniHUB DWATS'

    # We must rewrite the tr method, because at runtime, the default self.translate calls within the context of the
    # inherited child class, however, pylupdate reads the python file without executing it, putting the context in
    # translation as the parent class
    # noinspection PyMethodMayBeStatic
    def translate(self, msg, disambiguation=None, n=-1):
        return QCoreApplication.translate(DockTabHomeBase.__name__, msg,  disambiguation, n)

    def set_logic(self):
        """Insere a lógica de controle da aba. A ser implementada pelos controladores que
            herdam essa classe."""
        pass

    def __init__(self, dock, iface):
        super().__init__(dock)
        self.iface = iface
        self.screenEntrance = EntranceDataUI(self.title)
        self.screenHead = QDialog()

        self.hBoxOut = QGridLayout()
        self.pb_show_data_out = QPushButton()
        self.gb_dataOutput = QGroupBox()
        self.hBoxEnt = QHBoxLayout()
        self.pb_insert = QPushButton()
        self.dadosEnt = QGroupBox()

        self.gl_options = QGridLayout()
        self.gb_options = QGroupBox()

        self.lb_shouldCalculateArea = QLabel()
        self.hbl_shouldCalculateArea = QHBoxLayout()
        self.bg_shouldCalculateArea = QButtonGroup()

        self.rb_areaNo = QRadioButton()
        self.rb_areaYes = QRadioButton()
        self.lb_hasTank = QLabel()

        self.hbl_hasTank = QHBoxLayout()
        self.bg_hasTank = QButtonGroup()
        self.rb_tankNo = QRadioButton()
        self.rb_tankYes = QRadioButton()

        self.lb_shouldImport = QLabel()
        self.hbl_shouldImport = QHBoxLayout()
        self.bg_shouldImport = QButtonGroup()
        self.rb_import_no = QRadioButton()
        self.rb_import_yes = QRadioButton()

        self.gb_import_red_basica = QGroupBox()
        self.gl_layout_red_basica = QGridLayout()
        self.lb_txt_max_flow_hour_start_plan = QLabel()
        self.lb_value_max_flow_hour_start_plan = QLabel()
        self.lb_txt_max_flow_hour_final_plan = QLabel()
        self.lb_value_max_flow_hour_final_plan = QLabel()
        self.lb_txt_avg_flow_strictly_domestic_start_plan = QLabel()
        self.lb_value_avg_flow_strictly_domestic_start_plan = QLabel()
        self.lb_txt_avg_flow_strictly_domestic_final_plan = QLabel()
        self.lb_value_avg_flow_strictly_domestic_final_plan = QLabel()
        self.lb_txt_infiltration_flow = QLabel()
        self.lb_value_infiltration_flow = QLabel()
        self.flow_iter = 0
        self.flow_start = 0
        self.flow_final = 0
        self.flow_domestic_start = 0
        self.flow_domestic_final = 0
        self.flow_infiltration = 0


        #self.pb_add_flow = QPushButton()
        self.pb_save_flows = QPushButton()
        #self.flow_initial = None
        self.flow_final = None
        self.previous_layer = None

        self.lb_instructions = QLabel()

        self.headLayout = HeadFormLayout()
        self.lb_designerHead = QLabel()
        self.lb_localHead = QLabel()
        self.gl_project = QGridLayout()
        self.lb_nameProjectHead = QLabel()
        self.pb_editHeadProject = QPushButton()
        self.lb_designer = QLabel()
        self.lb_local = QLabel()
        self.lb_nameProject = QLabel()
        self.gb_dataProject = QGroupBox()
        self.vb_layout = QVBoxLayout()
        self.gb_buttonsControl = QWidget()
        self.hbl_buttonsControl = QHBoxLayout()
        self.pb_export_PDF = QPushButton()
        self.pb_saveAsAllProject = QPushButton()
        self.pb_saveAllProject = QPushButton()
        self.rep_out = RepOutDataGeneralUI()
        self.data_validation = DataValidationUI()
        self.pb_validation = QPushButton()
        self.utils = Utils()
        self.set_logic()

    def tab_start_ui(self):
        #self.__start_actions_ui()    # Iniciamos os botões de Salvar, Salvar Projeto, Salvar relatório
        self.__start_head_edit_ui()  # Iniciamos o layout de editar o cabeçalho do projeto e sua preview.
        self.__start_options_ui()    # Iniciamos o layout de opções, (deve importar, tanque sedimentação etc...)
        self.__start_input_ui()      # Iniciamos os botões de entrada (Inserir, Editar)
        self.__start_output_ui()     # Iniciamos os botões de saída
        self.vb_layout.addStretch()
        self.setLayout(self.vb_layout)

        self.load_data()

    def __start_actions_ui(self):
        self.pb_saveAllProject.setIcon(QIcon(icon_save))
        self.pb_saveAllProject.setText(self.translate('Salvar'))
        self.pb_saveAllProject.setFixedSize(100, 25)
        self.pb_saveAllProject.setToolTip(self.translate('Salvar projeto'))
        self.pb_saveAsAllProject.setIcon(QIcon(icon_save))
        self.pb_saveAsAllProject.setText(self.translate('Salvar como'))
        self.pb_saveAsAllProject.setFixedSize(100, 25)
        self.pb_saveAsAllProject.setToolTip(self.translate('Salvar projeto criando um novo arquivo'))
        self.pb_export_PDF.setIcon(QIcon(icon_rep_PDF))
        self.pb_export_PDF.setText(self.translate('Relatório'))
        self.pb_export_PDF.setFixedSize(100, 25)
        self.pb_export_PDF.setToolTip(self.translate('Exportar Relatório de resumo de dimensionamento PDF'))
        self.hbl_buttonsControl.addWidget(self.pb_saveAllProject)
        self.hbl_buttonsControl.addWidget(self.pb_saveAsAllProject)
        self.hbl_buttonsControl.addWidget(self.pb_export_PDF)
        self.gb_buttonsControl.setLayout(self.hbl_buttonsControl)
        self.vb_layout.addWidget(self.gb_buttonsControl)

    def __start_head_edit_ui(self):
        self.gb_dataProject.setTitle(self.translate('Dados do Projeto'))
        self.lb_nameProject.setText('---')
        self.lb_nameProject.setFont(self.utils.formatBoldText())
        self.lb_local.setText('---')
        self.lb_local.setFont(self.utils.formatBoldText())
        self.lb_designer.setText('---')
        self.lb_designer.setFont(self.utils.formatBoldText())
        self.pb_editHeadProject.setIcon(QIcon(icon_edit))
        self.pb_editHeadProject.setFixedSize(20, 20)
        self.pb_editHeadProject.setToolTip(self.translate('Editar cabeçalho do projeto'))
        self.lb_nameProjectHead.setText(self.translate('Projeto:'))
        self.gl_project.addWidget(self.lb_nameProjectHead, 0, 0)
        self.gl_project.addWidget(self.lb_nameProject, 0, 1)
        self.gl_project.addWidget(self.pb_editHeadProject, 0, 2)
        self.lb_localHead.setText(self.translate('Local:'))
        self.gl_project.addWidget(self.lb_localHead, 1, 0)
        self.gl_project.addWidget(self.lb_local, 1, 1)
        self.lb_designerHead.setText(self.translate('Projetista:'))
        self.gl_project.addWidget(self.lb_designerHead, 2, 0)
        self.gl_project.addWidget(self.lb_designer, 2, 1)
        self.gl_project.setColumnMinimumWidth(1, 150)
        self.gb_dataProject.setLayout(self.gl_project)
        self.vb_layout.addWidget(self.gb_dataProject)
        self.screenHead.setWindowTitle(self.translate('Editar cabeçalho do projeto'))
        self.screenHead.setLayout(self.headLayout)
        self.screenHead.setGeometry(470, 280, 350, 150)

    def __start_options_ui(self):
        self.lb_instructions.setText(self.translate(
            'Para iniciar o projeto é necessário inserir alguns dados. Para isso siga as instruções abaixo:'))
        self.lb_instructions.setWordWrap(True)
        self.gb_options.setTitle(self.translate("Opções do projeto"))
        self.gl_options.addWidget(self.lb_instructions, 0, 0, 1, 2, Qt.AlignVCenter)  # linha 0, coluna 0, ocupa 1 linha, ocupa 2 colunas
        self.rb_import_yes.setText(self.translate('Sim'))
        self.rb_import_no.setText(self.translate('Não'))
        self.bg_shouldImport.addButton(self.rb_import_yes)
        self.bg_shouldImport.addButton(self.rb_import_no)
        self.hbl_shouldImport.addWidget(self.rb_import_yes)
        self.hbl_shouldImport.addWidget(self.rb_import_no)
        self.lb_shouldImport.setText(self.translate('Deseja importar informações de um projeto do SaniHub RedBasica?'))
        self.lb_shouldImport.setWordWrap(True)
        self.gl_options.addWidget(self.lb_shouldImport, 3, 0, Qt.AlignVCenter)
        self.gl_options.addLayout(self.hbl_shouldImport, 3, 1)
        
        self.gb_import_red_basica.setTitle(self.translate('Dados RedBasica'))
        self.lb_txt_max_flow_hour_start_plan.setText(self.translate('Vazão de esgoto sanitário máxima horária de '
                                                                    'início de plano:'))
        self.lb_txt_max_flow_hour_start_plan.setWordWrap(True)
        self.gl_layout_red_basica.addWidget(self.lb_txt_max_flow_hour_start_plan, 0, 0, Qt.AlignVCenter)
        self.lb_value_max_flow_hour_start_plan.setText('N/A')
        self.gl_layout_red_basica.addWidget(self.lb_value_max_flow_hour_start_plan, 0, 1, Qt.AlignCenter)
        self.lb_txt_max_flow_hour_final_plan.setText(self.translate('Vazão de esgoto sanitário máxima horária de '
                                                                    'final de plano:'))
        self.lb_txt_max_flow_hour_final_plan.setWordWrap(True)
        self.gl_layout_red_basica.addWidget(self.lb_txt_max_flow_hour_final_plan, 1, 0, Qt.AlignVCenter)
        self.lb_value_max_flow_hour_final_plan.setText('N/A')
        self.gl_layout_red_basica.addWidget(self.lb_value_max_flow_hour_final_plan, 1, 1, Qt.AlignCenter)
        self.lb_txt_avg_flow_strictly_domestic_start_plan.setText(self.translate('Vazão média de início de plano '
                                                                                 'estritamente doméstica:'))
        self.lb_txt_avg_flow_strictly_domestic_start_plan.setWordWrap(True)
        self.gl_layout_red_basica.addWidget(self.lb_txt_avg_flow_strictly_domestic_start_plan, 2, 0, Qt.AlignVCenter)
        self.lb_value_avg_flow_strictly_domestic_start_plan.setText('N/A')
        self.gl_layout_red_basica.addWidget(self.lb_value_avg_flow_strictly_domestic_start_plan, 2, 1, Qt.AlignCenter)
        self.lb_txt_avg_flow_strictly_domestic_final_plan.setText(self.translate('Vazão média de final de plano '
                                                                                 'estritamente doméstica'))
        self.lb_txt_avg_flow_strictly_domestic_final_plan.setWordWrap(True)
        self.gl_layout_red_basica.addWidget(self.lb_txt_avg_flow_strictly_domestic_final_plan, 3, 0, Qt.AlignVCenter)
        self.lb_value_avg_flow_strictly_domestic_final_plan.setText('N/A')
        self.gl_layout_red_basica.addWidget(self.lb_value_avg_flow_strictly_domestic_final_plan, 3, 1, Qt.AlignCenter)
        self.lb_txt_infiltration_flow.setText(self.translate('Vazão de infiltração'))
        self.gl_layout_red_basica.addWidget(self.lb_txt_infiltration_flow, 4, 0, Qt.AlignVCenter)
        self.lb_value_infiltration_flow.setText('N/A')
        self.gl_layout_red_basica.addWidget(self.lb_value_infiltration_flow, 4, 1, Qt.AlignCenter)
        self.lb_txt_max_flow_hour_start_plan.setMinimumHeight(45)
        self.lb_txt_max_flow_hour_final_plan.setMinimumHeight(45)
        self.lb_txt_avg_flow_strictly_domestic_start_plan.setMinimumHeight(10)
        self.lb_txt_avg_flow_strictly_domestic_final_plan.setMinimumHeight(10)
        self.lb_txt_infiltration_flow.setMinimumHeight(5)
        self.gl_layout_red_basica.setVerticalSpacing(20)
        self.gb_import_red_basica.setLayout(self.gl_layout_red_basica)
        self.gl_options.addWidget(self.gb_import_red_basica, 4, 0, 1, 2, Qt.AlignVCenter)
        self.gb_import_red_basica.hide()
        self.rb_import_yes.toggled.connect(self.show_import_red_basica)
        self.rb_import_no.toggled.connect(self.hide_import_red_basica)

        # Ativado quando usuário seleciona outra camada.
        if self.project_data is None:
            self.iface.layerTreeView().currentLayerChanged.connect(self.current_active_layer_changed)

        self.rb_tankYes.setText(self.translate('Sim'))
        self.rb_tankNo.setText(self.translate('Não'))
        self.bg_hasTank.addButton(self.rb_tankYes)
        self.bg_hasTank.addButton(self.rb_tankNo)
        self.hbl_hasTank.addWidget(self.rb_tankYes)
        self.hbl_hasTank.addWidget(self.rb_tankNo)
        self.hbl_hasTank.addSpacing(2)
        self.lb_hasTank.setText(self.translate('Deseja dimensionar o tanque de sedimentação?'))
        self.lb_hasTank.setWordWrap(True)
        self.gl_options.addWidget(self.lb_hasTank, 5, 0, Qt.AlignVCenter)
        self.gl_options .addLayout(self.hbl_hasTank, 5, 1)
        self.rb_areaYes.setText(self.translate('Sim'))
        self.rb_areaNo.setText(self.translate('Não'))
        self.bg_shouldCalculateArea.addButton(self.rb_areaYes)
        self.bg_shouldCalculateArea.addButton(self.rb_areaNo)
        self.hbl_shouldCalculateArea.addWidget(self.rb_areaYes)
        self.hbl_shouldCalculateArea.addWidget(self.rb_areaNo)
        self.hbl_shouldCalculateArea.addSpacing(2)  # add espaço abaixo do layout
        self.lb_shouldCalculateArea.setText(self.translate('Deseja calcular a área construída total do projeto?'))
        self.lb_shouldCalculateArea.setWordWrap(True)
        self.gl_options.addWidget(self.lb_shouldCalculateArea, 6, 0, Qt.AlignVCenter)
        self.gl_options.addLayout(self.hbl_shouldCalculateArea, 6, 1)
        self.gb_options.setLayout(self.gl_options)
        self.vb_layout.addWidget(self.gb_options)
        self.lb_instructions.setMinimumHeight(45)
        self.lb_shouldImport.setMinimumHeight(55)
        self.lb_hasTank.setMinimumHeight(45)
        self.lb_shouldCalculateArea.setMinimumHeight(45)
        self.gl_options.setVerticalSpacing(20)

    def __start_input_ui(self):
        self.dadosEnt.setTitle(self.translate('Dados de Entrada'))
        self.pb_insert.setText(self.translate('Inserir'))
        self.pb_insert.setFixedSize(115, 25)
        self.pb_edit_data.setText(self.translate('Editar'))
        self.pb_edit_data.setFixedSize(115, 25)
        self.hBoxEnt.addWidget(self.pb_insert)
        self.hBoxEnt.addWidget(self.pb_edit_data)
        self.dadosEnt.setLayout(self.hBoxEnt)
        self.vb_layout.addWidget(self.dadosEnt)

    def __start_output_ui(self):
        self.gb_dataOutput.setTitle(self.translate('Dados de Saída'))

        self.pb_show_data_out.setText(self.translate('Visualizar'))
        self.pb_show_data_out.setFixedSize(115, 25)

        self.hBoxOut.addWidget(self.pb_show_data_out, 0, 0)  # , Qt.AlignLeft)

        self.pb_export_PDF.setIcon(QIcon(icon_rep_PDF))
        self.pb_export_PDF.setText(self.translate('Relatório'))
        self.pb_export_PDF.setFixedSize(115, 25)
        self.pb_export_PDF.setToolTip(self.translate('Exportar Relatório de resumo de dimensionamento PDF'))

        self.hBoxOut.addWidget(self.pb_export_PDF, 0, 1)
        self.pb_validation.setText(self.translate('Verificação de conformidades'))
        self.pb_validation.setFixedSize(220, 25)

        self.hBoxOut.addWidget(self.pb_validation, 1, 0, 1, 2, Qt.AlignHCenter)

        self.hBoxOut.setColumnMinimumWidth(1, 2)

        self.gb_dataOutput.setLayout(self.hBoxOut)

        self.vb_layout.addWidget(self.gb_dataOutput)
        #self.vb_layout.setRowStretch(7, 20)
        #self.vb_layout.setVerticalSpacing(12)

    def show_import_red_basica(self, checked):
        if not checked or self.project_data is not None:
            return
        if self.iface.activeLayer() is not None:
            self.rb_import_yes.setCheckable(True)
            self.gb_import_red_basica.show()
        else:
            self.rb_import_yes.setCheckable(False)
            icon = QMessageBox.Information
            self.utils.showDialog(self.title, self.translate('Uma camada ativa de mapa deve estar previamente '
                                                             'aberta para selecionar esta opção.'), icon)

    def hide_import_red_basica(self, checked):
        if not checked:
            return
        self.gb_import_red_basica.hide()

    def current_active_layer_changed(self):
        #try:  # dá erro quando abre novo projeto, por algum motivo.
        #    if self.previous_layer is not None:
        #        self.previous_layer.selectionChanged.disconnect(self.show_selection_change_atributes)
        #except RuntimeError:
        #    pass

        layer_active = self.iface.activeLayer()
        if layer_active is not None and layer_active.name() != 'SaniHUB DWATS':
            layer = QgsProject.instance().mapLayersByName(layer_active.name())[0]
            layer.selectionChanged.connect(self.show_selection_change_atributes)
            self.previous_layer = layer
        QgsMessageLog.logMessage("Camada alterada", "current layer changed")

    def show_selection_change_atributes(self, selected):
        # Se não queremos importar, não devemos fazer nada.
        if self.rb_import_no.isChecked() or not self.dock.tabWidget.isVisible():
            return

        print('foi por aqui')
        QgsMessageLog.logMessage("Show selection change attributes", "Called")
        layer_active = self.iface.activeLayer()
        if layer_active is not None:
            layer = QgsProject.instance().mapLayersByName(layer_active.name())[0]
            if len(selected) > 0 and self.rb_import_yes.isChecked():
                for id in selected:
                    flow_features = layer.getFeatures(QgsFeatureRequest().setFilterFid(id))
                    idx_flow_start = layer.fields().lookupField('Q_i')
                    idx_flow_final = layer.fields().lookupField('Q_f')
                    idx_flow_domestic_start = layer.fields().lookupField('Qmed_i')
                    idx_flow_domestic_final = layer.fields().lookupField('Qmed_f')
                    idx_flow_infiltration = layer.fields().lookupField('Q_inf')
                    if (idx_flow_start != -1 and idx_flow_final != -1 and idx_flow_domestic_start != -1 and
                        idx_flow_domestic_final != -1 and idx_flow_infiltration != -1):
                        flow_iter = next(flow_features)
                        self.flow_start = float(flow_iter.attributes()[idx_flow_start])
                        self.flow_final = float(flow_iter.attributes()[idx_flow_final])
                        self.flow_domestic_start = float(flow_iter.attributes()[idx_flow_domestic_start])
                        self.flow_domestic_final = float(flow_iter.attributes()[idx_flow_domestic_final])
                        self.flow_infiltration = float(flow_iter.attributes()[idx_flow_infiltration])
                        self.lb_value_max_flow_hour_start_plan.setText(str(self.utils.formatNum2Dec(self.flow_start)))
                        self.lb_value_max_flow_hour_final_plan.setText(str(self.utils.formatNum2Dec(self.flow_final)))
                        self.lb_value_avg_flow_strictly_domestic_start_plan.setText(str(self.utils.formatNum2Dec(
                                                                                            self.flow_domestic_start)))
                        self.lb_value_avg_flow_strictly_domestic_final_plan.setText(str(self.utils.formatNum2Dec(
                                                                                            self.flow_domestic_final)))
                        self.lb_value_infiltration_flow.setText(str(self.utils.formatNum2Dec(self.flow_infiltration)))