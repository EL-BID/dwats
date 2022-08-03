from datetime import date
from typing import Optional

import jinja2
from PyQt5.QtCore import QFile, QTextStream, QIODevice, QCoreApplication
from qgis.core import QgsMessageLog

from ..data.data_manager import ProjectDataManager
from ..data.images_manager import ImagesPathManager
from ..data_validation import DataValidation
from ...utils.utils import Utils
from ..data.models import ProjectInfo, ProjectData
from ..costs import CostsCalculator
from ..march_calculation import MarchCalculation
from ..march_calculation_without_tank import MarchCalculationWithoutTank


class PDFGenerator:
    # noinspection PyMethodMayBeStatic
    def translate(self, msg, disambiguation=None, n=-1):
        return QCoreApplication.translate(PDFGenerator.__name__, msg, disambiguation, n)

    def __init__(self,
                 project_info: ProjectInfo,
                 entrance_data: ProjectData,
                 should_import_rede_basica: bool,
                 has_sedimentation_tank: bool,
                 costs: Optional[CostsCalculator] = None):
        self.project_info = project_info
        self.project_data = entrance_data
        self.has_sedimentation_tank = has_sedimentation_tank
        self.should_import_rede_basica = should_import_rede_basica
        self.costs = costs
        self.should_render_costs = costs is not None
        self.utils = Utils()

        if has_sedimentation_tank:
            self.marchCalculation = MarchCalculation(entrance_data, self.should_import_rede_basica)
        else:
            self.marchCalculation = MarchCalculationWithoutTank(entrance_data, self.should_import_rede_basica)

    def getPdfHtml(self) -> str:
        file_path = r':/plugins/tratamientos_descentralizados/resources/pt/templates/report.html'
        file = QFile(file_path)
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            return ""
        stream = QTextStream(file)
        stream.setCodec("UTF-8")
        html = ""
        while not stream.atEnd():
            html += stream.readLine()
        file.close()

        env = jinja2.Environment(autoescape=True, loader=jinja2.BaseLoader)
        utils = Utils()

        # We insert here our custom functions that shall be used inside the jinja template.
        env.filters['formatinteger'] = utils.formatInteger
        env.filters['format1Dec'] = utils.formatNum1Dec
        env.filters['format2Dec'] = utils.formatNum2Dec
        t = env.from_string(html)

        # Choosing which march calculation shall be used
        if self.has_sedimentation_tank:
            calculation = MarchCalculation(self.project_data, self.should_import_rede_basica)
        else:
            calculation = MarchCalculationWithoutTank(self.project_data, self.should_import_rede_basica)

        # Importing data from rede basica if it exists
        from_rede_basica = None
        if self.should_import_rede_basica and ProjectDataManager.is_from_rede_basica_data_loaded():
            from_rede_basica = ProjectDataManager.get_from_rede_basica_data()

        image_manager = ImagesPathManager(n_compart=self.project_data.numCompartRac,
                                          has_sedimentation_tank=self.has_sedimentation_tank)
        imgs = image_manager.get_report_images()

        # qrc prefix is necessary for the webciew to identify local files
        img1 = "qrc" + imgs['planta_baixa']
        img2 = "qrc" + imgs['corteAA']
        img3 = "qrc" + imgs['corteBB']
        img4 = "qrc" + imgs['corteCC']

        validation = DataValidation()

        if self.costs and self.should_import_rede_basica:
            self.project_data.final_population = self.costs.final_population

        should_calculate_area = ProjectDataManager.get_project_config().should_calculate_area
        out = t.render(project_info=self.project_info,
                       has_sedimentation_tank=self.has_sedimentation_tank,
                       project_data=self.project_data, calculation=calculation,
                       from_rede_basica_data=from_rede_basica,
                       should_import_rede_basica=self.should_import_rede_basica,
                       should_calculate_area=should_calculate_area,
                       validation=validation,
                       costs=self.costs,
                       img1=img1, img2=img2, img3=img3, img4=img4)

        return out
