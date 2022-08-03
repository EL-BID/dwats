from dataclasses import dataclass

#from ...gui.ui_entrance_data import EntranceDataUI


@dataclass
class ProjectData:
    relSolidSedimentableDQO = 0.4
    velAscendingFlowMax = 1.1
    coefProductionSolid = 0.2
    concentrationMethaneBiogas = 0.75  # 75% é o valor
    functionPotentialCH4 = 0.6
    factorCorrectMethaneMCF = 0.8

    initial_population: int = 0
    final_population: int = 0
    max_flow_hour_start_plan: float = 0
    max_flow_hour_final_plan: float = 0
    avg_flow_strictly_domestic_start_plan: float = 0
    avg_flow_strictly_domestic_final_plan: float = 0
    final_infiltration_flow: float = 0

    consWater: float = 0
    concentrationDQOEntrance: float = 0
    concentrationDBOEntrance: float = 0
    depthOutRac: float = 0
    numCompartRac: int = 0
    widthShafts: float = 0
    tempOperReactor: float = 0
    tdh: float = 0
    intervalTimeRemovalSludge: int = 0
    widthTank: float = 0
    depthTank: float = 0
    k1CoefDayMaxConsume: float = 0
    k2CoefDayMaxConsume: float = 0
    coefReturn: float = 0
    tempDigestSludge: float = 0
    #should_import_rede_basica = None


    def getCoefProductionSolid(self):
        return self.coefProductionSolid

    def getConcentrationMethaneBiogas(self):
        return self.concentrationMethaneBiogas

    def getFunctionPotentialCH4(self):
        return self.functionPotentialCH4

    def getFactorCorrectMethaneMCF(self):
        return self.factorCorrectMethaneMCF

    def getInitialPopulation(self):
        return self.initial_population

    def getFinalPopulation(self):
        return self.final_population

    def getConsWater(self):
        return self.consWater

    def getConcentrationDQOEntrance(self):
        return self.concentrationDQOEntrance

    def getConcentrationDBOEntrance(self):
        return self.concentrationDBOEntrance

    def getDepthOutRac(self):
        return self.depthOutRac

    def getNumCompartRAC(self):
        return self.numCompartRac

    def getWidthShafts(self):
        return self.widthShafts

    def getTempOperReactor(self):
        return self.tempOperReactor

    def getTdh(self):
        return self.tdh

    def getIntervalTimeRemovalSludge(self):
        return self.intervalTimeRemovalSludge

    def getWidthTank(self):
        return self.widthTank

    def getDepthTank(self):
        return self.depthTank

    def getK1CoefDayMaxConsume(self):
        return self.k1CoefDayMaxConsume

    def getK2CoefDayMaxConsume(self):
        return self.k2CoefDayMaxConsume

    def getCoefReturn(self):
        return self.coefReturn

    def getRelSolidSedimentableDQO(self):
        return self.relSolidSedimentableDQO

    def getTempDigestSludge(self):
        return self.tempDigestSludge

    def getVelAscendingFlowMax(self):
        return self.velAscendingFlowMax

    def setCoefProductionSolid(self, coefProductionSolid):
        self.coefProductionSolid = coefProductionSolid

    def setConcentrationMethaneBiogas(self, concentrationMethaneBiogas):
        self.concentrationMethaneBiogas = concentrationMethaneBiogas

    def setFunctionPotentialCH4(self, functionPotentialCH4):
        self.functionPotentialCH4 = functionPotentialCH4

    def setFactorCorrectMethaneMCF(self, factorCorrectMethaneMCF):
        self.factorCorrectMethaneMCF = factorCorrectMethaneMCF

    def setInitialPopulation(self, population):
        self.initial_population = population

    def setConsWater(self, consWater):
        self.consWater = consWater

    def setConcentrationDQOEntrance(self, concentrationDQOEntrance):
        self.concentrationDQOEntrance = concentrationDQOEntrance

    def setConcentrationDBOEntrance(self, concentrationDBOEntrance):
        self.concentrationDBOEntrance = concentrationDBOEntrance

    def setDepthOutRac(self, depthOutRac):
        self.depthOutRac = depthOutRac

    def setNumCompartRac(self, numCompartRac):
        self.numCompartRac = numCompartRac

    def setWidthShafts(self, widthShafts):
        self.widthShafts = widthShafts

    def setTempOperReactor(self, tempOperReactor):
        self.tempOperReactor = tempOperReactor

    def setTdh(self, tdh):
        self.tdh = tdh

    def setIntervalTimeRemovalSludge(self, intervalTimeRemovalSludge):
        self.intervalTimeRemovalSludge = intervalTimeRemovalSludge

    def setWidthTank(self, widthTank):
        self.widthTank = widthTank

    def setDepthTank(self, depthTank):
        self.depthTank = depthTank

    def setK1CoefDayMaxConsume(self, k1CoefDayMaxConsume):
        self.k1CoefDayMaxConsume = k1CoefDayMaxConsume

    def setK2CoefDayMaxConsume(self, k2CoefDayMaxConsume):
        self.k2CoefDayMaxConsume = k2CoefDayMaxConsume

    def setCoefReturn(self, coefReturn):
        self.coefReturn = coefReturn

    def setRelSolidSedimentableDQO(self, relSolidSedimentableDQO):
        self.relSolidSedimentableDQO = relSolidSedimentableDQO

    def setTempDigestSludge(self, tempDigestSludge):
        self.tempDigestSludge = tempDigestSludge

    def setVelAscendingFlowMax(self, velAscendingFlowMax):
        self.velAscendingFlowMax = velAscendingFlowMax

    def restartEntranceData(self):
        self.setInitialPopulation(0)
        self.final_population = 0
        self.setConsWater(0)
        self.setConcentrationDQOEntrance(0)
        self.setConcentrationDBOEntrance(0)
        self.setDepthOutRac(0)
        self.setNumCompartRac(0)
        self.setWidthShafts(0)
        self.setTempOperReactor(0)
        self.setTdh(0)
        self.setIntervalTimeRemovalSludge(0)
        self.setWidthTank(0)
        self.setDepthTank(0)
        self.setK1CoefDayMaxConsume(1.2)
        self.setK2CoefDayMaxConsume(1.5)
        self.setCoefReturn(0.8)
        self.setTempDigestSludge(20)
        self.max_flow_hour_start_plan = 0
        self.max_flow_hour_final_plan = 0
        self.avg_flow_strictly_domestic_start_plan = 0
        self.avg_flow_strictly_domestic_final_plan = 0
        self.final_infiltration_flow = 0
