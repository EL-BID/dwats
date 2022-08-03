from PyQt5.QtCore import QCoreApplication

from .data.data_manager import ProjectDataManager
from .data.entrance_data import ProjectData
from .march_calculation import MarchCalculation


class DataValidation:
    def translate(self, msg, disambiguation=None, n=-1):
        return QCoreApplication.translate(DataValidation.__name__, msg, disambiguation, n)

    def get_march_calculation(self):
        return MarchCalculation(ProjectDataManager.get_project_data(),
                                ProjectDataManager.get_project_config().should_import_rede_basica)

    def validation_dimensions_ts(self):
        """
        Validates if 2 < W/L < 4, where W and L is the sedimentation tank width and length, respectively

        Returns a tuple with True if it's valid, and the validation rule explanation
        Retorna uma tupla com True ou False para se válido ou não e, texto com regra de validação.
        """
        str_rule = self.translate('Relação comprimento/largura recomendada: 2<C/L<4. '
                                  'Para ajuste, verifique: largura do tanque de sedimentação ou '
                                  'altura útil do tanque de sedimentação.')
        march_calculation = self.get_march_calculation()
        if (ProjectDataManager.get_project_data().getWidthTank() * 2.0 >= march_calculation.getLengthTankSedimentation()
            and ProjectDataManager.get_project_data().getWidthTank()) * 4.0 \
                <= march_calculation.getLengthTankSedimentation():
            return True, str_rule
        else:
            return False, str_rule

    def validation_climb_speed(self):
        """
        Validates the climb speed
        """
        str_rule = self.translate('A velocidade ascensional de fluxo no início de plano excede o valor máximo '
                                  'recomendado. Para ajuste, verifique: altura útil do reator anaeróbio e comprimento '
                                  'do compartimento do reator anaeróbio. ')
        march_calculation = self.get_march_calculation()
        climb_speed = march_calculation.get_climb_speed()
        data = ProjectDataManager.get_project_data()
        return climb_speed <= data.velAscendingFlowMax, str_rule

    def validation_hydraulic_holding_time_rac(self):
        str_rule = self.translate('O tempo de detenção hidráulica para o reator anaeróbio deve ser menor ou igual a '
                                  '36 horas. Para ajuste, verifique: altura útil do RAC, '
                                  'número de compartimentos do RAC, largura dos shafts. ')
        return self.get_march_calculation().get_hydraulic_holding_time_rac() <= 36, str_rule
        pass

    def validation_hydraulic_holding_time_sedimentation_tank(self):
        str_rule = self.translate('O tempo de detenção hidráulica para o tanque de sedimentação deve ser '
                                  'menor ou igual a 24 horas. Para ajuste, verifique: largura ou altura útil do '
                                  'tanque de sedimentação.')
        return self.get_march_calculation().get_hydraulic_holding_time_sedimentation_tank() <= 24, str_rule

