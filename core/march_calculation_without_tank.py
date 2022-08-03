from .march_calculation import MarchCalculation
from .data.entrance_data import ProjectData


class MarchCalculationWithoutTank(MarchCalculation):
    def __init__(self, data, should_import_rede_basica):
        super().__init__(data, should_import_rede_basica)
        self.marchCalculation = MarchCalculation(data, should_import_rede_basica)
        self.data = data

    def getOrganicLoadAppliedVolumetricDBO(self):
        return ((self.data.getConcentrationDBOEntrance() *
                 self.marchCalculation.strictly_domestic_max_end_plan_hour_flow()
                 * 24) / self.data.getVolumeReactor() / 1000)

    def getRemovalFactorDQOForceFunctionSludge(self):
        if self.data.getConcentrationDQOEntrance() < 2000:
            return (self.data.getConcentrationDQOEntrance() * 0.17) / 2000 + 0.87
        if self.data.getConcentrationDQOEntrance() < 3000:
            return (self.data.getConcentrationDQOEntrance() - 2000) * 0.02 / 1000 + 1.04
        return 1.06

    def getConcentrationDQOEffluentFinal(self):
        return self.data.getConcentrationDQOEntrance() * (1 - self.getFeeRemovalDQO_RAC())

    def getConcentrationDBOEffluentFinal(self):
        return self.data.getConcentrationDBOEntrance() * (1 - self.getFeeRemovalDBO_RAC())

    def getAreaTotalRAC(self):
        return ((self.marchCalculation.getAreaCompartmentRAC() * self.data.getNumCompartRAC()) +
                (0.2 * self.getWidthAdoptedCompartmentRAC()))

    def getConstructedAreaTotal(self):
        return (3 * self.getAreaUtilTotal())

    def getAreaUtilTotal(self):
        return self.getAreaTotalRAC()

    # ------- Common data for both calculation march --------
    def get_initial_average_daily_sludge_flow(self):
        return self.marchCalculation.get_initial_average_daily_sludge_flow()

    def get_initial_maximum_hourly_sludge_flow(self):
        return self.marchCalculation.get_initial_maximum_hourly_sludge_flow()

    def get_climb_speed(self):
        return self.marchCalculation.get_climb_speed()

    def get_hydraulic_holding_time_rac(self):
        return self.marchCalculation.get_hydraulic_holding_time_rac()

    def getRacArea(self):
        return self.marchCalculation.getAreaOneCompartmentRAC()

    def getLengthCompartmentRAC(self):
        return self.marchCalculation.getLengthCompartmentRAC()

    def getWidthMinCompartmentRAC(self):
        return self.marchCalculation.getWidthMinCompartmentRAC()

    def getWidthAdoptedCompartmentRAC(self):
        return self.marchCalculation.getWidthAdoptedCompartmentRAC()

    def getCorrectionVelocityAscensionFlow(self):
        return self.marchCalculation.getCorrectionVelocityAscensionFlow()

    def getVolumeReactor(self):
        return self.marchCalculation.getVolumeReactor()

    def getTimeHydraulicDetentionTotalRAC(self):
        return self.marchCalculation.getTimeHydraulicDetentionTotalRAC()

    def getRemovalFactorDQOLoadFunctionF_overload(self):
        return self.marchCalculation.getRemovalFactorDQOLoadFunctionF_overload()

    def getFactorRemovalDQOFunctionTemperature(self):
        return self.marchCalculation.getFactorRemovalDQOFunctionTemperature()

    def getFactorRemovalDQOFunctionTDH(self):
        return self.marchCalculation.getFactorRemovalDQOFunctionTDH()

    def getFactorRemovalTheoreticalDQO(self):
        return self.marchCalculation.getFactorRemovalTheoreticalDQO()

    def getFeeRemovalDQO_RAC(self):
        return self.marchCalculation.getFeeRemovalDQO_RAC()

    def getEfficiencyRemovalTotalDQOProcess(self):
        return self.marchCalculation.getEfficiencyRemovalTotalDQOProcess()

    def getFactorRemovalDQO_DBO_RAC(self):
        return self.marchCalculation.getFactorRemovalDQO_DBO_RAC()

    def getFeeRemovalDBO_RAC(self):
        return self.marchCalculation.getFeeRemovalDBO_RAC()

    def getEfficiencyRemovalTotalDBOProcess(self):
        return self.marchCalculation.getEfficiencyRemovalTotalDBOProcess()

    def getLoadDQOConvertedMethane(self):
        return self.marchCalculation.getLoadDQOConvertedMethane()

    def getFactorCorrectionTempOperationReactor(self):
        return self.marchCalculation.getFactorCorrectionTempOperationReactor()

    def getDailyFlowMethane(self):
        return self.marchCalculation.getDailyFlowMethane()

    def getDailyFlowBiogas(self):
        return self.marchCalculation.getDailyFlowBiogas()

    def getLoadOrganic(self):
        return self.marchCalculation.getLoadOrganic()

    def getEmissionMethaneDaily(self):
        return self.marchCalculation.getEmissionMethaneDaily()

    def getEmissionGasCarbonicEquivalentDaily(self):
        return self.marchCalculation.getEmissionGasCarbonicEquivalentDaily()

    def getAreaCompartmentRAC(self):
        return self.marchCalculation.getAreaCompartmentRAC()

    def getDailyAverageFlow(self):
        return self.marchCalculation.getDailyAverageFlow()
