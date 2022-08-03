from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QWidget
from qgis.core import QgsMessageLog

from ...core.data.data_manager import ProjectDataManager
from ...core.costs import CostsCalculator
from ...core.data.models import Costs
from .view.ui_dock_tab_costs_base import DockTabCostsBase


class DockTabCosts(DockTabCostsBase):
    def __init__(self, dock):
        super().__init__(dock)
        self.costs_calculator: Optional[CostsCalculator] = None
        self.loaded_from_db = False

    def set_logic(self):
        self.pb_report_costs.clicked.connect(self.showReportCosts)
        self.sb_soil.valueChanged.connect(self.on_data_changed)
        self.sb_concrete.valueChanged.connect(self.on_data_changed)
        self.sb_rock.valueChanged.connect(self.on_data_changed)
        self.sb_masonry.valueChanged.connect(self.on_data_changed)
        self.dsb_pipe_depth.valueChanged.connect(self.on_data_changed)
        self.dsb_pipe_diameter.valueChanged.connect(self.on_data_changed)
        self.sb_final_population.valueChanged.connect(self.on_data_changed)
        self.rb_show_data_costs.toggled.connect(self.on_rb_costs_toggle)
        self.repOutCosts.pb_saveEditCosts.clicked.connect(self.on_services_cost_update)

    def load_data(self):
        if ProjectDataManager.get_project_config().should_import_rede_basica:
            self.lb_population.show()
            self.lb_final_population.show()
            self.sb_final_population.show()
        self.load_data_from_database()
        self.rb_show_data_costs.setChecked(ProjectDataManager.get_project_config().should_show_costs)
        self.load_costs_calculations()
        self.load_costs_calculator()
        self.load_user_input()
        self.load_costs_values()
        self.loaded_from_db = True

    def load_costs_calculator(self):
        if ProjectDataManager.get_project_config().should_import_rede_basica:
            self.project_data.final_population = self.sb_final_population.value()
            self.costs_calculator = CostsCalculator(costs=self.costs, entranceData=self.project_data,
                                                    calculation=self.calculation,
                                                    final_population=self.sb_final_population.value())
        else:
            self.costs_calculator = CostsCalculator(costs=self.costs, entranceData=self.project_data,
                                                calculation=self.calculation)

    def load_user_input(self):
        if self.costs is not None:
            self.dsb_pipe_depth.setValue(self.costs.entrance_pipe_depth)
            self.dsb_pipe_diameter.setValue(self.costs.entrance_pipe_diameter)
            self.sb_soil.setValue(self.costs.soil)
            self.sb_rock.setValue(self.costs.rock)
            self.sb_concrete.setValue(self.costs.concrete)
            self.sb_masonry.setValue(self.costs.masonry)
            self.sb_final_population.setValue(self.costs.final_population)
        else:
            self.dsb_pipe_depth.setValue(0)
            self.dsb_pipe_diameter.setValue(0)
            self.sb_soil.setValue(100)
            self.sb_rock.setValue(0)
            self.sb_concrete.setValue(100)
            self.sb_masonry.setValue(0)
            self.sb_final_population.setValue(0)

    def load_costs_values(self):
        if self.costs is not None:
            self.setCosts()
            has_sedimentation = self.project_config is not None and self.project_config.has_sedimentation_tank
            should_import_rede_basica = self.project_config.should_import_rede_basica
            if has_sedimentation and should_import_rede_basica is not True:
                self.lb_st_costs_value.setText(
                    'USD ' + self.utils.formatNum2Dec(
                        self.costs_calculator.getTotalCostsTS() / self.project_data.final_population))
            elif has_sedimentation and should_import_rede_basica:
                self.lb_st_costs_value.setText('USD ' + self.utils.formatNum2Dec(
                    self.costs_calculator.getTotalCostsTS() / self.sb_final_population.value()))
            if should_import_rede_basica is not True:
                self.lb_reactor_costs_value.setText('USD ' + self.utils.formatNum2Dec(
                    self.costs_calculator.getTotalCostsReactor() / self.project_data.final_population))
                self.lb_total_costs_value.setText(
                    'USD ' + self.utils.formatNum2Dec(self.costs_calculator.costPerInhabitant(
                        has_sedimentation, self.project_data.final_population)))
            elif should_import_rede_basica:
                self.lb_reactor_costs_value.setText('USD ' + self.utils.formatNum2Dec(
                    self.costs_calculator.getTotalCostsReactor() / self.sb_final_population.value()))
                self.lb_total_costs_value.setText(
                    'USD ' + self.utils.formatNum2Dec(self.costs_calculator.costPerInhabitant(
                        has_sedimentation, self.sb_final_population.value())))
        else:
            self.lb_st_costs_value.setText('0')
            self.lb_reactor_costs_value.setText('0')
            self.lb_total_costs_value.setText('0')

    def load_costs_calculations(self):
        if self.project_config is not None and self.project_config.should_show_costs:
            if self.project_config.has_sedimentation_tank:
                self.lb_st_costs.show()
                self.lb_st_costs_value.show()
            else:
                self.lb_st_costs.hide()
                self.lb_st_costs_value.hide()
            self.lb_total_costs.show()
            self.lb_total_costs_value.show()
            self.lb_reactor_costs.show()
            self.lb_reactor_costs_value.show()
        else:
            self.lb_st_costs.hide()
            self.lb_st_costs_value.hide()
            self.lb_total_costs.hide()
            self.lb_total_costs_value.hide()
            self.lb_reactor_costs.hide()
            self.lb_reactor_costs_value.hide()

    def reload(self):
        self.loaded_from_db = False
        self.load_data()

    def on_rb_costs_toggle(self, checked: bool):
        if not self.loaded_from_db:
            return
        if checked and not self.checkDataCosts():
            icon = QMessageBox.Critical
            self.rb_show_data_costs.setChecked(False)
            if ProjectDataManager.get_project_config().should_import_rede_basica:
                self.utils.showDialog(self.title,
                                      self.translate(
                                          'População final de plano, diâmetro e profundidade da tubulação '
                                          'devem ser informados!'),
                                      icon)
            else:
                self.utils.showDialog(self.title,
                                      self.translate('Diâmetro e profundidade da tubulação devem ser informados!'),
                                      icon)

            return

        if self.project_config is not None:
            self.project_config.should_show_costs = checked
            ProjectDataManager.save_project_config(self.project_config)
            if ProjectDataManager.get_project_config().should_import_rede_basica:
                if self.checkDataCosts():
                    self.project_data.final_population = self.sb_final_population.value()
                    ProjectDataManager.save_project_data(self.project_data)
                    ProjectDataManager.save_project_costs(self.costs)
                    self.dock_reload()
                    self.load_costs_calculations()
            else:
                self.dock_reload()
                self.load_costs_calculations()

    def on_data_changed(self):
        if not self.loaded_from_db:
            return
        tmp_costs = Costs(
            concrete=self.sb_concrete.value(),
            masonry=self.sb_masonry.value(),
            soil=self.sb_soil.value(),
            rock=self.sb_rock.value(),
            final_population=self.sb_final_population.value(),
            entrance_pipe_depth=self.dsb_pipe_depth.value(),
            entrance_pipe_diameter=self.dsb_pipe_diameter.value(),
            services=ProjectDataManager.get_project_costs_data().services
        )
        if self.costs is None:
            tmp_costs.services = Costs().services

        if tmp_costs != self.costs:
            self.costs = tmp_costs
            ProjectDataManager.save_project_costs(tmp_costs)
            self.dock.reload()

        if ProjectDataManager.get_project_config().should_import_rede_basica:
            if self.sb_final_population.value() == 0:
                self.rb_show_data_costs.setChecked(False)
            else:
                project_data = ProjectDataManager.get_project_data()
                project_data.final_population = self.sb_final_population.value()
                ProjectDataManager.save_project_data(project_data)

        if self.checkDataCosts():
            #if self.dsb_pipe_depth.value() == 0 or self.dsb_pipe_diameter.value() == 0:
            self.rb_show_data_costs.setChecked(False)

    def on_services_cost_update(self):
        self.repOutCosts.saveChanges()
        services = [self.repOutCosts.costs.getVlItem01(),
                    self.repOutCosts.costs.getVlItem02(),
                    self.repOutCosts.costs.getVlItem03(),
                    self.repOutCosts.costs.getVlItem04(),
                    self.repOutCosts.costs.getVlItem05(),
                    self.repOutCosts.costs.getVlItem06(),
                    self.repOutCosts.costs.getVlItem07(),
                    self.repOutCosts.costs.getVlItem08(),
                    self.repOutCosts.costs.getVlItem09(),
                    self.repOutCosts.costs.getVlItem10(),
                    self.repOutCosts.costs.getVlItem11(),
                    self.repOutCosts.costs.getVlItem12(),
                    self.repOutCosts.costs.getVlItem13(),
                    self.repOutCosts.costs.getVlItem14(),
                    self.repOutCosts.costs.getVlItem15(),
                    self.repOutCosts.costs.getVlItem16(),
                    self.repOutCosts.costs.getVlItem17()]
        if self.costs is not None:
            self.costs.services = services
        ProjectDataManager.save_project_costs(self.costs)
        self.dock_reload()
        self.load_costs_values()

    def checkDataCosts(self):
        if ProjectDataManager.get_project_config().should_import_rede_basica:
            return ((self.dsb_pipe_depth.value() != 0 and self.dsb_pipe_diameter.value() != 0 and
                     self.sb_final_population.value() != 0)
                    and (self.sb_soil.value() != 0 or self.sb_rock.value() != 0)
                    and (self.sb_concrete.value() != 0 or self.sb_masonry.value() != 0))
        else:
            return ((self.dsb_pipe_depth.value() != 0 and self.dsb_pipe_diameter.value())
                    and (self.sb_soil.value() != 0 or self.sb_rock.value() != 0)
                    and (self.sb_concrete.value() != 0 or self.sb_masonry.value() != 0))

    def setCosts(self):
        if self.costs_calculator is not None:
            self.costs_calculator.loadData(costs=self.costs, calculation=self.calculation,
                                           entranceData=self.project_data)
        else:
            self.load_costs_calculator()

    def showReportCosts(self):
        if self.checkDataCosts():
            self.setCosts()
            # TODO verificar se project config é não nula
            self.repOutCosts.loadReportCosts(self.costs_calculator, self.project_config.has_sedimentation_tank,
                                             self.title)
            self.repOutCosts.showReportCosts()
        elif self.loaded_from_db:
            icon = QMessageBox.Critical
            self.utils.showDialog(self.title,
                                  self.tr('Diâmetro e profundidade da tubulação devem ser informados!'), icon)
