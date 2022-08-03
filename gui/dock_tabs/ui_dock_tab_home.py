from PyQt5.QtWidgets import QMessageBox
from qgis.core import QgsMessageLog, QgsProject

from ..ui_data_validation import DataValidationUI
from ...core.costs import CostsCalculator
from .view.ui_dock_tab_home_base import DockTabHomeBase
from ..ui_pdf_printer_preview import PrinterPreviewUI
from ...core.data.data_manager import ProjectDataManager
from ...core.data.entrance_data import ProjectData
from ...core.data.models import ProjectConfig, ProjectInfo, FromRedeBasicaData
from ...core.pdf_handlers.pdf_generator import PDFGenerator


class DockTabHome(DockTabHomeBase):
    """We define all the logic of the start dock here."""

    def __init__(self, dock, iface):
        super().__init__(dock, iface)
        self.printer_preview_dialog = PrinterPreviewUI()

    def set_logic(self):
        """Logic inserted after defining the layout and its relations in the base class."""
        self.pb_insert.clicked.connect(self.insert_data_pb)
        self.screenEntrance.add_on_conclude_listener(self.conclude_data_pb)
        self.pb_editHeadProject.clicked.connect(self.editHeadProject_pb)
        self.headLayout.set_on_save_pressed_event(self.saveEditHead_pb)

        self.pb_validation.clicked.connect(self.data_validation.show_dialog_validation)
        self.data_validation.on_edit_data_clicked(self.edit_data_validation)

        # TODO implementar importação da Sanibid
        # self.rb_import_yes.setChecked(False)
        # self.rb_import_no.setChecked(True)

        # self.rb_import_yes.setEnabled(False)
        # self.rb_import_no.setEnabled(False)

        self.pb_show_data_out.clicked.connect(lambda: self.rep_out.showReportOutGeneral())
        self.pb_export_PDF.clicked.connect(self.exportPDF_pb)

    def load_data(self):
        self.load_data_from_database()
        self.load_project_info()
        self.load_project_entrance_data()
        self.load_project_config()
        self.load_edit_button()
        self.load_out_data()
        self.load_action_bar_icons()
        self.load_printer_preview()
        self.load_data_validation()

    def reload(self):
        self.load_data()

    def exportPDF_pb(self):
        self.printer_preview_dialog.print_pdf()

    def load_out_data(self):
        if self.project_data is None:
            self.pb_show_data_out.setEnabled(False)
            return

        self.pb_show_data_out.setEnabled(True)
        self.rep_out.loadReportOutGeneral(self.calculation, self.title, self.project_config.has_sedimentation_tank)

    def load_printer_preview(self):
        if self.project_data is None:
            return
        if self.project_config is not None:
            if self.project_config.should_show_costs and self.costs is not None:
                costs_calculator = CostsCalculator(entranceData=self.project_data,
                                                   calculation=self.calculation,
                                                   costs=self.costs)
                pdf_generator = PDFGenerator(project_info=self.project_info or ProjectInfo(),
                                             entrance_data=self.project_data,
                                             should_import_rede_basica=self.project_config.should_import_rede_basica,
                                             has_sedimentation_tank=self.project_config.has_sedimentation_tank,
                                             costs=costs_calculator)
            else:
                pdf_generator = PDFGenerator(project_info=self.project_info or ProjectInfo(),
                                             entrance_data=self.project_data,
                                             should_import_rede_basica=self.project_config.should_import_rede_basica,
                                             has_sedimentation_tank=self.project_config.has_sedimentation_tank)
            self.printer_preview_dialog.load_html(pdf_generator.getPdfHtml())

    def load_project_entrance_data(self):
        self.pb_insert.setEnabled(self.project_data is None)
        self.pb_edit_data.setEnabled(self.project_data is not None)

    def load_project_config(self):
        self.pb_save_flows.clicked.connect(self.get_data_red_basica_entrance)
        if self.project_config is not None:
            self.rb_tankYes.setChecked(self.project_config.has_sedimentation_tank)
            self.rb_tankNo.setChecked(not self.project_config.has_sedimentation_tank)

            self.rb_import_yes.setChecked(self.project_config.should_import_rede_basica)
            self.rb_import_no.setChecked(not self.project_config.should_import_rede_basica)

            self.rb_areaYes.setChecked(self.project_config.should_calculate_area)
            self.rb_areaNo.setChecked(not self.project_config.should_calculate_area)

            self.rb_tankYes.setEnabled(False)
            self.rb_tankNo.setEnabled(False)
            self.rb_import_yes.setEnabled(False)
            self.rb_import_no.setEnabled(False)
            self.rb_areaYes.setEnabled(False)
            self.rb_areaNo.setEnabled(False)
            #try:
            #    self.iface.layerTreeView().currentLayerChanged.disconnect(self.current_active_layer_changed)
            #except RuntimeError:
            #    pass

        else:
            if QgsProject.instance().fileName() != '':
                self.bg_shouldImport.setExclusive(False)
                self.rb_import_yes.setChecked(False)
                self.rb_import_no.setChecked(False)
                self.rb_import_yes.setEnabled(True)
                self.rb_import_no.setEnabled(True)
                self.bg_shouldImport.setExclusive(True)
            else:
                self.bg_shouldImport.setExclusive(False)
                self.rb_import_yes.setChecked(False)
                self.rb_import_no.setChecked(True)
                self.rb_import_yes.setEnabled(False)
                self.rb_import_no.setEnabled(False)
                self.bg_shouldImport.setExclusive(True)

            self.bg_hasTank.setExclusive(False)
            self.bg_shouldCalculateArea.setExclusive(False)
            self.rb_tankYes.setChecked(False)
            self.rb_tankNo.setChecked(False)
            self.rb_areaYes.setChecked(False)
            self.rb_areaNo.setChecked(False)

            self.rb_tankYes.setEnabled(True)
            self.rb_tankNo.setEnabled(True)
            self.rb_areaYes.setEnabled(True)
            self.rb_areaNo.setEnabled(True)
            self.bg_hasTank.setExclusive(True)
            self.bg_shouldCalculateArea.setExclusive(True)
            self.iface.layerTreeView().currentLayerChanged.connect(self.current_active_layer_changed)

    def load_project_info(self):
        """Loads values from the header database in edit layout and preview."""
        if self.project_info is not None:
            self.lb_nameProject.setText(self.project_info.project_name)
            self.lb_local.setText(self.project_info.local)
            self.lb_designer.setText(self.project_info.designer)

            self.headLayout.load_project_info(self.project_info)
        else:
            project_info = ProjectInfo()
            self.lb_nameProject.setText(project_info.project_name)
            self.lb_local.setText(project_info.local)
            self.lb_designer.setText(project_info.designer)

            self.headLayout.load_project_info(project_info)

    def load_action_bar_icons(self):
        self.pb_saveAllProject.setEnabled(False)
        self.pb_saveAsAllProject.setEnabled(False)
        self.pb_export_PDF.setEnabled(ProjectDataManager.is_project_data_loaded())

    def edit_data_validation(self):
        self.edit_data_clicked()

    def load_data_validation(self):
        if self.project_data is not None:
            self.pb_validation.setEnabled(True)
            self.data_validation.reload()
        else:
            self.pb_validation.setEnabled(False)

    def editHeadProject_pb(self):
        self.screenHead.exec_()

    def save_button_clicked(self):
        super().save_button_clicked()
        self.data_validation.reload()

    def saveEditHead_pb(self):
        project_info = ProjectInfo(
            project_name=self.headLayout.le_projectName.text(),
            local=self.headLayout.le_local.text(),
            designer=self.headLayout.le_designer.text(),
            client=self.headLayout.le_client.text(),
            state=self.headLayout.le_state.text(),
            country=self.headLayout.le_country.text(),
            version=self.headLayout.le_version.text()
        )
        ProjectDataManager.save_project_info(project_info)
        self.reload()
        self.screenHead.close()

    def insert_data_pb(self):
        if not self.check_radio_buttons_ok():
            icon = QMessageBox.Warning
            self.utils.showDialog(self.tr('Inserir dados de entrada'), self.tr(
                'Todas as opções anteriores devem estar previamente preenchidas para em seguida inserir os dados.'),
                                  icon)
            return

        if self.rb_import_yes.isChecked():
            # se qualquer valor dos dados de vazão forem nulos,
            if any([x is None for x in (
                    self.flow_start, self.flow_final,
                    self.flow_domestic_start, self.flow_domestic_final,
                    self.flow_infiltration)]):
                self.utils.showDialog(self.title,
                                      self.tr('Por favor, selecione um trecho para inserirmos os dados no projeto.'),
                                      QMessageBox.Warning)
                return

        # Dimensionar tanque de sedimentacao
        if self.rb_tankYes.isChecked():
            self.rb_tankNo.setChecked(False)
            self.dock.tabWidget.setTabEnabled(2, True)
        elif self.rb_tankNo.isChecked():
            self.rb_tankYes.setChecked(False)
            self.dock.tabWidget.setTabEnabled(2, False)

        if self.rb_import_no.isChecked():
            self.screenEntrance.set_options(self.rb_tankYes.isChecked())
        else:
            from_rede_basica = FromRedeBasicaData(
                maximum_horly_sludge_flow_final=self.flow_final,
                maximum_horly_sludge_flow_initial=self.flow_start,
                average_strictly_domestic_flow_initial=self.flow_domestic_start,
                average_strictly_domestic_flow_final=self.flow_domestic_final,
                infiltration_flow=self.flow_infiltration
            )
            self.screenEntrance.set_options(self.rb_tankYes.isChecked(), from_rede_basica)
        self.screenEntrance.show_screen()

    def conclude_data_pb(self):
        """Called when all user input is done"""
        if self.rb_import_yes.isChecked():
            # se qualquer valor dos dados de vazão forem nulos,
            if any([x is None for x in (
                    self.flow_start, self.flow_final,
                    self.flow_domestic_start, self.flow_domestic_final,
                    self.flow_infiltration)]):
                self.utils.showDialog(self.title, self.tr('Por favor, selecione um trecho para inserirmos os dados no projeto.'))
                return

            QgsMessageLog.logMessage(
                f"{self.flow_start}, {self.flow_domestic_start}. {self.flow_final}, {self.flow_domestic_final}",
                "ui dock tab home")
            if self.flow_start > self.flow_domestic_start * 1.8 or self.flow_final > self.flow_domestic_final * 1.8:
                QgsMessageLog.logMessage("Avisando das vazões", "ui dock tab home")
                self.utils.showDialog(self.translate("Aviso quanto as vazões importadas"),
                                      self.translate("Notamos uma inconformidade com a vazão de esgoto sanitário "
                                                     "máxima horária. Correção automática da vazão realizada com "
                                                     "sucesso."),
                                      QMessageBox.Warning)

                if self.flow_start > self.flow_domestic_start * 1.8:
                    self.flow_start = self.flow_domestic_start * 1.8

                if self.flow_final > self.flow_domestic_final * 1.8:
                    self.flow_final = self.flow_domestic_final * 1.8

            ProjectDataManager.save_from_rede_basica_data(
                FromRedeBasicaData(
                    maximum_horly_sludge_flow_initial=self.flow_start,
                    maximum_horly_sludge_flow_final=self.flow_final,
                    average_strictly_domestic_flow_initial=self.flow_domestic_start,
                    average_strictly_domestic_flow_final=self.flow_domestic_final,
                    infiltration_flow=self.flow_infiltration,
                )
            )
            self.gb_import_red_basica.hide()



        project_data = self.screenEntrance.get_project_data()
        ProjectDataManager.save_project_data(project_data)
        self.screenEntrance.screen.close()
        icon = QMessageBox.Information
        self.utils.showDialog(self.title, self.tr('Dados processados com sucesso!'), icon)

        ProjectDataManager.save_project_config(
            ProjectConfig(
                 should_calculate_area=self.rb_areaYes.isChecked(),
                 has_sedimentation_tank=self.rb_tankYes.isChecked(),
                 should_import_rede_basica=self.rb_import_yes.isChecked(),
                 should_show_costs=False
             )
        )
        self.iface.layerTreeView().currentLayerChanged.disconnect(self.current_active_layer_changed)
        self.dock.hard_reload()

    def get_opcoes(self):
        options = [self.rb_import_yes.isChecked(),
                   self.rb_tankYes.isChecked(),
                   self.rb_areaYes.isChecked()]

        return options

    def check_radio_buttons_ok(self):
        return ((self.rb_import_yes.isChecked() or self.rb_import_no.isChecked()) and
                (self.rb_tankYes.isChecked() or self.rb_tankNo.isChecked()) and
                (self.rb_areaYes.isChecked() or self.rb_areaNo.isChecked()))

    def get_data_red_basica_entrance(self):
        # Todo: implementar atribuição dos valores de entrada coletados do redbasica
        if self.flow_initial != None:
            n_entrance_flow_initial = self.flow_initial
            n_entrance_flow_final = self.flow_final
            print(n_entrance_flow_initial, n_entrance_flow_final)
