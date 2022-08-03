from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QPushButton, QVBoxLayout, QSpinBox, QDoubleSpinBox, QLabel, \
    QCheckBox

from ..base.ui_dock_tab_loader import DockTabLoader
from ...custom_widgets.widgets import ThousandsSeparatorSpinBox
from ...ui_rep_out_costs import RepOutDataCostsUI


class DockTabCostsBase(DockTabLoader):
    title = 'SaniHUB DWATS'

    # We must rewrite the tr method, because at runtime, the default self.translate calls within the context of the
    # inherited child class, however, pylupdate reads the python file without executing it, putting the context in
    # translation as the parent class
    # noinspection PyMethodMayBeStatic
    def translate(self, msg, disambiguation=None, n=-1) -> object:
        return QCoreApplication.translate(DockTabCostsBase.__name__, msg, disambiguation, n)

    def __init__(self, dock):
        super().__init__(dock)
        maximum = 9999999
        maxPerc = 100
        self.lb_txtEntrance = QLabel()
        self.lb_txtPipe = QLabel()
        self.lb_st_costs = QLabel()
        self.lb_st_costs_value = QLabel()
        self.lb_reactor_costs = QLabel()
        self.lb_reactor_costs_value = QLabel()
        self.lb_total_costs = QLabel()
        self.lb_total_costs_value = QLabel()
        self.lb_pipe_depth = QLabel()
        self.lb_pipe_diameter = QLabel()
        self.lb_terrain_type = QLabel()
        self.lb_soil = QLabel()
        self.lb_rock = QLabel()
        self.lb_txtWallMaterial = QLabel()
        self.lb_concrete = QLabel()
        self.lb_masonry = QLabel()
        self.dsb_pipe_depth = QDoubleSpinBox()
        self.dsb_pipe_depth.setMaximum(maximum)
        self.dsb_pipe_depth.setDecimals(2)
        self.dsb_pipe_depth.setSuffix(self.translate(' m'))
        self.dsb_pipe_diameter = QDoubleSpinBox()
        self.dsb_pipe_diameter.setMaximum(maximum)
        self.dsb_pipe_diameter.setDecimals(3)
        self.dsb_pipe_diameter.setSuffix(self.translate(' m'))
        self.sb_soil = QSpinBox()
        self.sb_soil.setMaximum(maxPerc)
        self.sb_soil.setSuffix(self.translate(' %'))
        self.sb_rock = QSpinBox()
        self.sb_rock.setMaximum(maxPerc)
        self.sb_rock.setSuffix(self.translate(' %'))
        self.sb_concrete = QSpinBox()
        self.sb_concrete.setMaximum(maxPerc)
        self.sb_concrete.setSuffix(self.translate(' %'))
        self.sb_masonry = QSpinBox()
        self.sb_masonry.setMaximum(maxPerc)
        self.sb_masonry.setSuffix(self.translate(' %'))
        self.lb_population = QLabel()
        self.lb_final_population = QLabel()
        self.sb_final_population = ThousandsSeparatorSpinBox()
        self.sb_final_population.setMaximum(maximum)

        self.rb_show_data_costs = QCheckBox()
        self.pb_report_costs = QPushButton()

        self.vb_layoutCosts = QVBoxLayout()
        self.gl_layoutCostsPipe = QGridLayout()
        self.gl_layoutCostsTerrain = QGridLayout()
        self.gb_costsPipe = QGroupBox()
        self.gb_costsTerrain = QGroupBox()
        self.repOutCosts = RepOutDataCostsUI()

        self.set_logic()

    def tab_start_ui(self):
        self.lb_txtEntrance.setText(self.translate('Para calcular os custos do projeto, preencher os dados abaixo:'))
        self.lb_txtEntrance.setWordWrap(True)
        self.vb_layoutCosts.addWidget(self.lb_txtEntrance)
        self.lb_population.setText(self.translate('População:'))
        self.lb_population.setFont(self.utils.formatBoldText())
        self.lb_final_population.setText(self.translate('População final de plano'))
        self.gl_layoutCostsPipe.addWidget(self.lb_population, 0, 0, 1, 2)
        self.gl_layoutCostsPipe.addWidget(self.lb_final_population, 1, 0)
        self.gl_layoutCostsPipe.addWidget(self.sb_final_population, 1, 1)
        self.lb_population.hide()
        self.lb_final_population.hide()
        self.sb_final_population.hide()
        self.lb_txtPipe.setText(self.translate('Tubulação:'))
        self.lb_txtPipe.setFont(self.utils.formatBoldText())
        self.gl_layoutCostsPipe.addWidget(self.lb_txtPipe, 2, 0, 1, 2)
        self.lb_pipe_depth.setText(self.translate('Profundidade tubulação de entrada'))
        self.lb_pipe_depth.setWordWrap(True)
        self.gl_layoutCostsPipe.addWidget(self.lb_pipe_depth, 3, 0)
        self.gl_layoutCostsPipe.addWidget(self.dsb_pipe_depth, 3, 1)
        self.lb_pipe_diameter.setText(self.translate('Diâmetro nominal da tubulação de entrada'))
        self.lb_pipe_diameter.setWordWrap(True)
        self.gl_layoutCostsPipe.addWidget(self.lb_pipe_diameter, 4, 0)
        self.gl_layoutCostsPipe.addWidget(self.dsb_pipe_diameter, 4, 1)
        self.lb_terrain_type.setText(self.translate('Tipo de terreno:'))
        self.lb_terrain_type.setFont(self.utils.formatBoldText())
        self.gl_layoutCostsPipe.addWidget(self.lb_terrain_type, 5, 0, 1, 2)
        self.lb_soil.setText(self.translate('Solo'))
        self.gl_layoutCostsPipe.addWidget(self.lb_soil, 6, 0)
        self.sb_soil.setValue(100)
        self.gl_layoutCostsPipe.addWidget(self.sb_soil, 6, 1)
        self.lb_rock.setText(self.translate('Rocha'))
        self.gl_layoutCostsPipe.addWidget(self.lb_rock, 7, 0)
        self.gl_layoutCostsPipe.addWidget(self.sb_rock, 7, 1)
        self.lb_txtWallMaterial.setText(self.translate('Material das paredes:'))
        self.lb_txtWallMaterial.setFont(self.utils.formatBoldText())
        self.gl_layoutCostsPipe.addWidget(self.lb_txtWallMaterial, 8, 0, 1, 2)
        self.lb_concrete.setText(self.translate('Concreto'))
        self.gl_layoutCostsPipe.addWidget(self.lb_concrete, 9, 0)
        self.sb_concrete.setValue(100)
        self.gl_layoutCostsPipe.addWidget(self.sb_concrete, 9, 1)
        self.lb_masonry.setText(self.translate('Alvenaria'))
        self.gl_layoutCostsPipe.addWidget(self.lb_masonry, 10, 0)
        self.gl_layoutCostsPipe.addWidget(self.sb_masonry, 10, 1)
        #self.lb_population.setText(self.translate('População:'))
        #self.lb_population.setFont(self.utils.formatBoldText())
        #self.lb_final_population.setText(self.translate('População final de plano'))
        #self.gl_layoutCostsPipe.addWidget(self.lb_population, 9, 0, 1, 2)
        #self.gl_layoutCostsPipe.addWidget(self.lb_final_population, 10, 0)
        #self.gl_layoutCostsPipe.addWidget(self.sb_final_population, 10, 1)
        #self.lb_population.hide()
        #self.lb_final_population.hide()
        #self.sb_final_population.hide()
        self.rb_show_data_costs.setText(self.translate('Ver custos'))
        self.pb_report_costs.setText(self.translate('Editar'))
        self.pb_report_costs.setFixedSize(100, 25)
        self.gl_layoutCostsPipe.addWidget(self.rb_show_data_costs, 11, 1, 1, 2, Qt.AlignHCenter)
        self.gl_layoutCostsPipe.addWidget(self.pb_report_costs, 11, 0, 1, 2, Qt.AlignLeft)
        self.gl_layoutCostsPipe.setColumnMinimumWidth(0, 180)

        self.lb_st_costs.setText(self.translate('Valor do Tanque de Sedimentação por habitante (USD/Hab)'))
        self.lb_st_costs.setWordWrap(True)
        self.lb_st_costs_value.setText('USD 0')

        self.gl_layoutCostsPipe.addWidget(self.lb_st_costs, 12, 0, Qt.AlignLeft)
        self.gl_layoutCostsPipe.addWidget(self.lb_st_costs_value, 12, 1, Qt.AlignHCenter)
        self.lb_st_costs.hide()
        self.lb_st_costs_value.hide()

        self.lb_reactor_costs.setText(self.translate('Valor do Reator Compartimentado por habitante (USD/Hab)'))
        self.lb_reactor_costs.setWordWrap(True)
        self.lb_reactor_costs_value.setText('USD 0')
        self.gl_layoutCostsPipe.addWidget(self.lb_reactor_costs, 13, 0, Qt.AlignLeft)
        self.gl_layoutCostsPipe.addWidget(self.lb_reactor_costs_value, 13, 1, Qt.AlignHCenter)

        self.lb_total_costs.setText(self.translate('Valor da ETE (TS + Reator) por habitante (USD/Hab)'))
        self.lb_total_costs.setWordWrap(True)
        self.lb_total_costs_value.setText('USD 0')
        self.lb_total_costs.setFont(self.utils.formatBoldText())
        self.lb_total_costs_value.setFont(self.utils.formatBoldText())
        self.gl_layoutCostsPipe.addWidget(self.lb_total_costs, 14, 0, Qt.AlignLeft)
        self.gl_layoutCostsPipe.addWidget(self.lb_total_costs_value, 14, 1, Qt.AlignHCenter)
        self.gb_costsPipe.setLayout(self.gl_layoutCostsPipe)

        self.vb_layoutCosts.addWidget(self.gb_costsPipe)
        self.vb_layoutCosts.addStretch()
        self.setLayout(self.vb_layoutCosts)

        self.sb_soil.valueChanged.connect(self.valueChangeRock)
        self.sb_rock.valueChanged.connect(self.valueChangeSoil)
        self.sb_concrete.valueChanged.connect(self.valueChangeMasonry)
        self.sb_masonry.valueChanged.connect(self.valueChangeConcrete)

        sp_retain = self.lb_reactor_costs_value.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.lb_st_costs.setSizePolicy(sp_retain)
        self.lb_st_costs_value.setSizePolicy(sp_retain)
        self.lb_total_costs.setSizePolicy(sp_retain)
        self.lb_total_costs_value.setSizePolicy(sp_retain)
        self.lb_reactor_costs.setSizePolicy(sp_retain)
        self.lb_reactor_costs_value.setSizePolicy(sp_retain)

    def valueChangeRock(self):
        self.sb_rock.setValue(100 - self.sb_soil.value())

    def valueChangeSoil(self):
        self.sb_soil.setValue(100 - self.sb_rock.value())

    def valueChangeConcrete(self):
        self.sb_concrete.setValue(100 - self.sb_masonry.value())

    def valueChangeMasonry(self):
        self.sb_masonry.setValue(100 - self.sb_concrete.value())
