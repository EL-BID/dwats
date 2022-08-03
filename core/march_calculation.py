# This Python file uses the following encoding: utf-8
from .data.data_manager import ProjectDataManager
from .data.entrance_data import ProjectData


class MarchCalculation:

    def __init__(self, data, should_import_rede_basica):
        self.data = data
        self.should_import_rede_basica = should_import_rede_basica

    # Flow calculations
    # start of plan flows
    def get_initial_average_daily_sludge_flow(self):
        if self.should_import_rede_basica:
            rede_basica = ProjectDataManager.get_from_rede_basica_data()
            return (rede_basica.infiltration_flow + rede_basica.average_strictly_domestic_flow_initial) * 86.4
        else:
            return self.strictly_domestic_avg_daily_initial_plan_flow() + self.data.final_infiltration_flow * 86.4

    def get_initial_maximum_hourly_sludge_flow(self):
        if self.should_import_rede_basica:
            rede_basica = ProjectDataManager.get_from_rede_basica_data()
            return rede_basica.maximum_horly_sludge_flow_initial * 3.6
        else:
            return self.strictly_domestic_max_initial_plan_hour_flow() + self.data.final_infiltration_flow * 3.6

    # end of plan flows
    def strictly_domestic_avg_daily_end_plan_flow(self):  # vazao media diaria
        if self.should_import_rede_basica:
            return None
        else:
            return ((self.data.getFinalPopulation() * self.data.getConsWater() * self.data.getCoefReturn()) / 1000)

    def strictly_domestic_max_end_plan_hour_flow(self):  # vazao media horaria
        if self.should_import_rede_basica:
            return None
        else:
            return (self.data.k2CoefDayMaxConsume * self.data.k1CoefDayMaxConsume *
                    (self.strictly_domestic_avg_daily_end_plan_flow() / 24.0))

    def get_final_average_daily_sludge_flow(self):
        if self.should_import_rede_basica:
            rede_basica = ProjectDataManager.get_from_rede_basica_data()
            return (rede_basica.infiltration_flow + rede_basica.average_strictly_domestic_flow_final) * 86.4
        else:
            return self.strictly_domestic_avg_daily_end_plan_flow() + self.data.final_infiltration_flow * 86.4

    def get_final_maximum_hourly_sludge_flow(self):
        if self.should_import_rede_basica:
            rede_basica = ProjectDataManager.get_from_rede_basica_data()
            return rede_basica.maximum_horly_sludge_flow_final * 3.6
        else:
            return self.strictly_domestic_max_end_plan_hour_flow() + self.data.final_infiltration_flow * 3.6

    def get_climb_speed(self):
        return (self.get_initial_maximum_hourly_sludge_flow() /
                self.getAreaOneCompartmentRAC())

    def get_hydraulic_holding_time_rac(self):
        return self.getVolumeReactor() / (self.get_initial_average_daily_sludge_flow() / 24) / 1.05

    def get_hydraulic_holding_time_sedimentation_tank(self):
        return self.getVolumeTankSedimentation() / (self.get_initial_average_daily_sludge_flow() / 24) / 1.05

    def getDailyAverageFlow(self):
        if self.should_import_rede_basica:
            return ((ProjectDataManager.get_from_rede_basica_data().average_strictly_domestic_flow_final +
                     ProjectDataManager.get_from_rede_basica_data().infiltration_flow) * 86.4)
        else:
            return (self.strictly_domestic_avg_daily_end_plan_flow() +
                    (self.data.final_infiltration_flow * 86.4))

    def max_hour_sewage_flow_end_plan(self):
        if self.should_import_rede_basica:
            return ProjectDataManager.get_from_rede_basica_data().maximum_horly_sludge_flow_final * 3.6
        else:
            return (self.strictly_domestic_max_end_plan_hour_flow() +
                    (self.data.final_infiltration_flow * 3.6))

    # start of plan
    def strictly_domestic_avg_daily_initial_plan_flow(self):
        if self.should_import_rede_basica:
            return None
        else:
            return ((self.data.initial_population * self.data.consWater * self.data.coefReturn) / 1000)

    def strictly_domestic_max_initial_plan_hour_flow(self):
        if self.should_import_rede_basica:
            return None
        else:
            return (self.data.k2CoefDayMaxConsume * self.data.k1CoefDayMaxConsume *
                    (self.strictly_domestic_avg_daily_initial_plan_flow() / 24.0))

    def avg_daily_sewage_flow_initial_plan(self):
        if self.should_import_rede_basica:
            return ((self.data.avg_flow_strictly_domestic_start_plan +
                     self.data.final_infiltration_flow) * 86.4)
        else:
            return (self.strictly_domestic_avg_daily_initial_plan_flow() +
                    (self.data.final_infiltration_flow * 86.4))

    def max_hour_sewage_flow_initial_plan(self):
        if self.should_import_rede_basica:
            return self.data.max_flow_hour_start_plan * 3.6
        else:
            return (self.strictly_domestic_max_initial_plan_hour_flow() +
                    (self.data.final_infiltration_flow * 3.6))

    # Sedimentation tank sizing all OK
    def getRelationDQO_DBOaffluent(self):  # ok
        value = self.data.getConcentrationDQOEntrance() / self.data.getConcentrationDBOEntrance()
        return value

    def getFeeRemovalDQO(self):
        value = 0
        if self.data.getTdh() < 1:
            value = self.data.getTdh() * 0.3
        elif self.data.getTdh() < 3:
            value = (self.data.getTdh() - 1) * 0.1 / 2 + 0.3
        elif self.data.getTdh() < 30:
            value = (self.data.getTdh() - 30) * 0.15 / 27 + 0.4
        else:
            value = 0.55
        return (self.data.getRelSolidSedimentableDQO() / 0.6) * value

    def getFactorRemovalDQO_DBO_Tank(self):  # tank OK
        value = 0
        if self.getFeeRemovalDQO() < 0.5:
            value = 1.06
        elif self.getFeeRemovalDQO() < 0.75:
            value = (self.getFeeRemovalDQO() - 0.75) * (self.getFeeRemovalDQO() - 0.5) * 0.065 / 0.25 + 1.06
        elif self.getFeeRemovalDQO() < 0.85:
            value = (1.125 - (self.getFeeRemovalDQO() - 0.75) * 0.1) / 0.1
        else:
            value = 1.025
        return value

    def getFeeRemovalDBO(self):
        value = self.getFactorRemovalDQO_DBO_Tank() * self.getFeeRemovalDQO()
        return value

    def getConcentrationDQOOutTank(self):  # ok
        value = (1.0 - self.getFeeRemovalDQO()) * self.data.getConcentrationDQOEntrance()
        return value

    def getConcentrationDBOOutTank(self):  # ok
        value = (1.0 - self.getFeeRemovalDBO()) * self.data.getConcentrationDBOEntrance()
        return value

    def getFeeAccumulationSludge(self):  # ok taxa = 0 if
        value = 0
        if self.data.getIntervalTimeRemovalSludge() < 36:
            value = 1 - (self.data.getIntervalTimeRemovalSludge() * 0.014)
        elif self.data.getIntervalTimeRemovalSludge() < 120:
            value = 0.5 - (self.data.getIntervalTimeRemovalSludge() - 36) * 0.002
        else:
            value = 1 / 3
        value = 0.005 * value
        return value

    def getLengthTankSedimentation(self):
        value = 0
        if self.getFeeRemovalDBO() > 0:
            if ((self.getFeeAccumulationSludge() * (self.data.getConcentrationDBOEntrance() -
                                                    self.getConcentrationDBOOutTank()) / 1000 * 30 * self.getDailyAverageFlow() *
                 self.data.getIntervalTimeRemovalSludge() + self.max_hour_sewage_flow_end_plan()
                 * self.data.getTdh()) < (2 * self.max_hour_sewage_flow_end_plan() * self.data.getTdh())):
                value = 2 * self.data.getTdh() * self.max_hour_sewage_flow_end_plan()
            else:
                value = (self.getFeeAccumulationSludge() * (
                        self.data.getConcentrationDBOEntrance() - self.getConcentrationDBOOutTank())
                         / 1000 * 30 * self.data.getIntervalTimeRemovalSludge() *
                         self.getDailyAverageFlow()
                         + (self.max_hour_sewage_flow_end_plan() * self.data.getTdh()))
        else:
            value = 0
        value = value / self.data.getWidthTank() / self.data.getDepthTank()
        return value

    def getVolumeTankSedimentation(self):
        value = (self.getLengthTankSedimentation() * self.data.getDepthTank()
                 * self.data.getWidthTank())
        return value

    # Sizing the Anaerobic Compartment Reactor
    def getAreaOneCompartmentRAC(self):
        value = self.max_hour_sewage_flow_end_plan() / self.data.getVelAscendingFlowMax()
        return value

    def getLengthCompartmentRAC(self):
        value = self.data.getDepthOutRac() * 0.5
        return value

    def getWidthMinCompartmentRAC(self):
        value = self.getAreaOneCompartmentRAC() / self.getLengthCompartmentRAC()
        return value

    def getWidthAdoptedCompartmentRAC(self):
        value = round(self.getWidthMinCompartmentRAC() + 0.05, 1)
        return value

    def getCorrectionVelocityAscensionFlow(self):  # correcao velocidade fluxo ascencional
        value = (self.max_hour_sewage_flow_end_plan() / self.getLengthCompartmentRAC() /
                 self.getWidthAdoptedCompartmentRAC())
        return value

    def getVolumeReactor(self):
        value = ((self.data.getWidthShafts() + self.getLengthCompartmentRAC()) * self.data.getNumCompartRAC()
                 * self.data.getDepthOutRac() * self.getWidthAdoptedCompartmentRAC())
        return value

    def getTimeHydraulicDetentionTotalRAC(self):
        value = self.getVolumeReactor() / (self.getDailyAverageFlow() / 24) / 1.05
        return value

    def getOrganicLoadAppliedVolumetricDBO(self):  # CargaOrganicaVolumetricaAplicadaDBO
        value = (self.getConcentrationDBOOutTank() * self.max_hour_sewage_flow_end_plan() * 24 /
                 self.getVolumeReactor() / 1000)
        return value

    def getRemovalFactorDQOLoadFunctionF_overload(self):
        value = 0
        if self.getOrganicLoadAppliedVolumetricDBO() < 8:
            value = 1
        elif self.getOrganicLoadAppliedVolumetricDBO() < 15:
            value = 1 - (self.getOrganicLoadAppliedVolumetricDBO() - 8) * 0.18 / 7
        else:
            value = 0.82 - (self.getOrganicLoadAppliedVolumetricDBO() - 15) * 0.9 / 5
        return value

    def getRemovalFactorDQOForceFunctionSludge(self):
        value = 0
        if self.getConcentrationDQOOutTank() < 2000:
            value = self.getConcentrationDQOOutTank() * 0.17 / 2000 + 0.87
        elif self.getConcentrationDQOOutTank() < 3000:
            value = (self.getConcentrationDQOOutTank() - 2000) * 0.02 / 1000 + 1.04
        else:
            value = 1.06
        return value

    def getFactorRemovalDQOFunctionTemperature(self):
        value = 0
        if self.data.getTempDigestSludge() < 20:
            value = (self.data.getTempDigestSludge() - 10) * 0.39 / 20 + 0.47
        elif self.data.getTempDigestSludge() < 25:
            value = (self.data.getTempDigestSludge() - 20) * 0.14 / 5 + 0.86
        elif self.data.getTempDigestSludge() < 30:
            value = (self.data.getTempDigestSludge() - 25) * 0.08 / 5 + 1
        else:
            value = 1.1
        return value

    def getFactorRemovalDQOFunctionTDH(self):
        value = 0
        if self.getTimeHydraulicDetentionTotalRAC() < 5:
            value = self.getTimeHydraulicDetentionTotalRAC() * 0.51 / 5
        elif self.getTimeHydraulicDetentionTotalRAC() < 10:
            value = (self.getTimeHydraulicDetentionTotalRAC() - 5) * 0.31 / 5 + 0.51
        elif self.getTimeHydraulicDetentionTotalRAC() < 20:
            value = (self.getTimeHydraulicDetentionTotalRAC() - 10) * 0.13 / 10 + 0.82
        else:
            value = 0.95
        return value

    def getFactorRemovalTheoreticalDQO(self):
        value = (self.getFactorRemovalDQOFunctionTDH() * self.getFactorRemovalDQOFunctionTemperature()
                 * self.getRemovalFactorDQOForceFunctionSludge() * self.getRemovalFactorDQOLoadFunctionF_overload())
        return value

    def getFeeRemovalDQO_RAC(self):
        factor = (self.getRemovalFactorDQOLoadFunctionF_overload() *
                  self.getRemovalFactorDQOForceFunctionSludge() *
                  self.getFactorRemovalDQOFunctionTemperature() *
                  self.getFactorRemovalDQOFunctionTDH())
        if self.data.getNumCompartRAC() < 7:
            value = factor * (self.data.getNumCompartRAC() * 0.04 + 0.82)
        else:
            value = factor * 0.98
        return value

    def getConcentrationDQOEffluentFinal(self):
        value = self.getConcentrationDQOOutTank() * (1 - self.getFeeRemovalDQO_RAC())
        return value

    def getEfficiencyRemovalTotalDQOProcess(self):
        value = 1 - self.getConcentrationDQOEffluentFinal() / self.data.getConcentrationDQOEntrance()
        return value

    def getFactorRemovalDQO_DBO_RAC(self):  # RAC
        value = 0
        if self.getFeeRemovalDQO_RAC() < 0.5:
            value = 1.06
        elif self.getFeeRemovalDQO_RAC() < 0.75:
            value = (self.getFeeRemovalDQO_RAC() - 0.75) * (self.getFeeRemovalDQO_RAC() - 0.5) * 0.065 / 0.25 + 1.06
        elif self.getFeeRemovalDQO_RAC() < 0.85:
            value = 1.125 - (self.getFeeRemovalDQO_RAC() - 0.75) * 0.1 / 0.1
        else:
            value = 1.025
        return value

    def getFeeRemovalDBO_RAC(self):
        value = self.getFactorRemovalDQO_DBO_RAC() * self.getFeeRemovalDQO_RAC()
        return value

    def getConcentrationDBOEffluentFinal(self):
        value = self.getConcentrationDBOOutTank() * (1 - self.getFeeRemovalDBO_RAC())
        return value

    def getEfficiencyRemovalTotalDBOProcess(self):
        value = 1 - self.getConcentrationDBOEffluentFinal() / self.data.getConcentrationDBOEntrance()
        return value

    # Estimate of biogas production
    def getLoadDQOConvertedMethane(self):
        value = (self.getDailyAverageFlow() * (
                (self.data.getConcentrationDQOEntrance() / 1000) - (self.getConcentrationDQOEffluentFinal() / 1000))
                 - self.data.getCoefProductionSolid() * self.getDailyAverageFlow() * (
                         self.data.getConcentrationDQOEntrance() / 1000))
        return value

    def getFactorCorrectionTempOperationReactor(self):
        value = 779.92 / (273 + self.data.getTempOperReactor())
        return value

    def getDailyFlowMethane(self):
        value = self.getLoadDQOConvertedMethane() / self.getFactorCorrectionTempOperationReactor()
        return value

    def getDailyFlowBiogas(self):
        value = self.getDailyFlowMethane() / self.data.getConcentrationMethaneBiogas()
        return value

    # Estimation of the generation of greenhouse gases
    def getLoadOrganic(self):
        value = (((self.data.getConcentrationDBOEntrance() - self.getConcentrationDBOEffluentFinal()) / 1000) *
                 self.getDailyAverageFlow())
        return value

    def getEmissionMethaneDaily(self):
        value = self.getLoadOrganic() * self.data.getFunctionPotentialCH4() * self.data.getFactorCorrectMethaneMCF()
        return value

    def getEmissionGasCarbonicEquivalentDaily(self):
        value = self.getEmissionMethaneDaily() * 25
        return value

    # Areas Calculation - BUFFER
    def getAreaSedimentationTank(self):
        value = (self.getLengthTankSedimentation() + (2 * 0.2)) * self.data.getWidthTank()
        return value

    def getAreaCompartmentRAC(self):
        value = (
                        self.getLengthCompartmentRAC() + self.data.getWidthShafts() + 0.2) * self.getWidthAdoptedCompartmentRAC()
        return value

    def getAreaTotalRAC(self):
        value = self.getAreaCompartmentRAC() * self.data.getNumCompartRAC()
        return value

    def getAreaUtilTotal(self):
        value = self.getAreaSedimentationTank() + self.getAreaTotalRAC()
        return value

    def getConstructedAreaTotal(self):
        value = 3 * self.getAreaUtilTotal()
        return value
