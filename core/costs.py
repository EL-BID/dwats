from qgis._core import QgsMessageLog

# from .entrance_data import EntranceData
from .march_calculation import MarchCalculation
import requests
import json


class CostsCalculator:
    # common attributes for the sedimentation tank and the reactor
    topSlabThickness = 0.2
    underSlabThickness = 0.25
    thicknessSideWalls = 0.2
    frontAndEndWallThickness = 0.2
    regularizationBaseThickness = 0.1
    intermediateWallThickness = 0.2

    entrancePipeDepth = 0
    entrancePipeDiameter = 0

    # seleção de materiais
    soil = 0
    rock = 0
    concrete = 0
    masonry = 0
    final_population = 0
    entranceData = 'entranceData'
    calculation = 'calculation'

    # service values
    vlItem01 = 1.02
    vlItem02 = 14.31
    vlItem03 = 0.27
    vlItem04 = 0.16
    vlItem05 = 0.54
    vlItem06 = 0.22
    vlItem07 = 8.38
    vlItem08 = 21.07
    vlItem09 = 80.02
    vlItem10 = 8.94
    vlItem11 = 104.10
    vlItem12 = 104.10
    vlItem13 = 2.45
    vlItem14 = 8.66
    vlItem15 = 37.08
    vlItem16 = 47.84
    vlItem17 = 22.51

    def __init__(self, costs=None, entranceData=None, calculation=None, final_population=None):
        self.entranceData = entranceData
        self.calculation = calculation
        #self.final_population = final_population
        if costs is not None:
            self.costs = costs
            self.rock = costs.rock
            self.soil = costs.soil
            self.concrete = costs.concrete
            self.masonry = costs.masonry
            self.final_population = costs.final_population
            self.entrancePipeDiameter = costs.entrance_pipe_diameter
            self.entrancePipeDepth = costs.entrance_pipe_depth
            self.setVlItem01(costs.services[0])
            self.setVlItem02(costs.services[1])
            self.setVlItem03(costs.services[2])
            self.setVlItem04(costs.services[3])
            self.setVlItem05(costs.services[4])
            self.setVlItem06(costs.services[5])
            self.setVlItem07(costs.services[6])
            self.setVlItem08(costs.services[7])
            self.setVlItem09(costs.services[8])
            self.setVlItem10(costs.services[9])
            self.setVlItem11(costs.services[10])
            self.setVlItem12(costs.services[11])
            self.setVlItem13(costs.services[12])
            self.setVlItem14(costs.services[13])
            self.setVlItem15(costs.services[14])
            self.setVlItem16(costs.services[15])
            self.setVlItem17(costs.services[16])

    def loadData(self, costs, entranceData, calculation):
        self.__init__(costs, entranceData, calculation)

    def setContrete(self, value):
        self.concrete = value

    def setMasonry(self, value):
        self.masonry = value

    def setSoil(self, value):
        self.soil = value

    def setRock(self, value):
        self.rock = value

    def setEntrancePipeDepth(self, value):
        self.entrancePipeDepth = value

    def setEntrancePipeDiameter(self, value):
        self.entrancePipeDiameter = value

    # define vlr dos servicos
    def setVlItem01(self, value):
        self.vlItem01 = value

    def setVlItem02(self, value):
        self.vlItem02 = value

    def setVlItem03(self, value):
        self.vlItem03 = value

    def setVlItem04(self, value):
        self.vlItem04 = value

    def setVlItem05(self, value):
        self.vlItem05 = value

    def setVlItem06(self, value):
        self.vlItem06 = value

    def setVlItem07(self, value):
        self.vlItem07 = value

    def setVlItem08(self, value):
        self.vlItem08 = value

    def setVlItem09(self, value):
        self.vlItem09 = value

    def setVlItem10(self, value):
        self.vlItem10 = value

    def setVlItem11(self, value):
        self.vlItem11 = value

    def setVlItem12(self, value):
        self.vlItem12 = value

    def setVlItem13(self, value):
        self.vlItem13 = value

    def setVlItem14(self, value):
        self.vlItem14 = value

    def setVlItem15(self, value):
        self.vlItem15 = value

    def setVlItem16(self, value):
        self.vlItem16 = value

    def setVlItem17(self, value):
        self.vlItem17 = value

    # retorna os valores dos serviços
    def getVlItem01(self):
        return self.vlItem01

    def getVlItem02(self):
        return self.vlItem02

    def getVlItem03(self):
        return self.vlItem03

    def getVlItem04(self):
        return self.vlItem04

    def getVlItem05(self):
        return self.vlItem05

    def getVlItem06(self):
        return self.vlItem06

    def getVlItem07(self):
        return self.vlItem07

    def getVlItem08(self):
        return self.vlItem08

    def getVlItem09(self):
        return self.vlItem09

    def getVlItem10(self):
        return self.vlItem10

    def getVlItem11(self):
        return self.vlItem11

    def getVlItem12(self):
        return self.vlItem12

    def getVlItem13(self):
        return self.vlItem13

    def getVlItem14(self):
        return self.vlItem14

    def getVlItem15(self):
        return self.vlItem15

    def getVlItem16(self):
        return self.vlItem16

    def getVlItem17(self):
        return self.vlItem17

    # Dados da geometria do tanque
    def getWidthTotalTS(self):
        value = self.entranceData.getWidthTank() + (2 * self.thicknessSideWalls)
        return value

    def getDepthTS(self):  # Profundidade do tanque (altura interna)
        value = (self.entranceData.getDepthTank() + 0.15 + self.entrancePipeDepth) - self.topSlabThickness
        return value

    def getTotalDepthForExcavationTS(self):  # Profundidade total para escavação
        value = self.getDepthTS() + self.topSlabThickness + self.underSlabThickness + self.regularizationBaseThickness
        return value

    def getLengthTotalTS(self):  # Comprimento total do tanque
        value = self.calculation.getLengthTankSedimentation() + (2 * self.frontAndEndWallThickness)
        return value

    def getTopSlabAreaTS(self):  # Área laje superior
        value = self.getWidthTotalTS() * self.getLengthTotalTS()
        return value

    def getUnderSlabAreaTS(self):  # Área laje inferior
        value = (self.getLengthTotalTS() + 0.4) * (self.getWidthTotalTS() + 0.4)
        return value

    def getFrontWallAreaTS(self):  # Área parede frontal
        value = ((self.getWidthTotalTS() * self.getDepthTS()) - ((3.1415 * self.entrancePipeDiameter
                                                                  * self.entrancePipeDiameter) / 4))
        return value

    def getFinalWallAreaTS(self):  # Área parede final
        value = (self.getWidthTotalTS() * self.getDepthTS()) * 0.97
        return value

    def getSideWallAreaTS(self):
        value = (self.getDepthTS() * self.getLengthTotalTS()) * 2
        return value

    def dollarRate(self):
        # return self.cotacao['USD']['ask']
        return 5.31

    # Dados geometria do reator

    def getWidthTotalCompartimentReactor(self):
        value = self.calculation.getWidthAdoptedCompartmentRAC() + (2 * self.thicknessSideWalls)
        return value

    def getDepthCompartimentReactor(self):
        value = (self.entranceData.getDepthOutRac() + 0.15 + self.entrancePipeDepth) - self.topSlabThickness
        return value

    def getTotalDepthForExcavationReactor(self):
        value = (self.getDepthCompartimentReactor() + self.topSlabThickness + self.underSlabThickness
                 + self.regularizationBaseThickness)
        return value

    def getLengthOfEachCompartmentReactor(self):
        value = ((self.calculation.getLengthCompartmentRAC() + self.entranceData.getWidthShafts() + 0.15)
                 + (2 * self.frontAndEndWallThickness))
        return value

    def getLengthReactor(self):
        value = ((self.entranceData.getNumCompartRAC() * self.getLengthOfEachCompartmentReactor())
                 - (self.entranceData.getNumCompartRAC() - 1) * self.intermediateWallThickness)
        return value

    def getTopSlabAreaReactor(self):
        value = self.getWidthTotalCompartimentReactor() * self.getLengthReactor()
        return value

    def getUnderSlabAreaReactor(self):
        value = (self.getLengthReactor() + 0.4) * (self.getWidthTotalCompartimentReactor() + 0.4)
        return value

    def getFinalWallAreaReactor(self):
        value = (((self.getWidthTotalCompartimentReactor() * self.getDepthCompartimentReactor())
                  - (3.1415 * self.entrancePipeDiameter * self.entrancePipeDiameter) / 4))
        return value

    def getFrontWallAreaReactor(self):
        value = (self.getWidthTotalCompartimentReactor() * self.getDepthCompartimentReactor()) * 0.97
        return value

    def getSideWallAreaReactor(self):
        value = self.getDepthCompartimentReactor() * self.getLengthReactor()
        return value

    def getIntermediateWallAreaReactor(self):
        value = self.calculation.getWidthAdoptedCompartmentRAC() * self.getDepthCompartimentReactor()
        return value

    def getChicaneAreaReactor(self):
        value = (self.calculation.getWidthAdoptedCompartmentRAC() * (self.entranceData.getDepthOutRac() + 0.05)
                 * (self.entranceData.getNumCompartRAC()))
        return value

    # planilha de custos TS
    def qtdItem01TS(
            self):  # 05.02.55 - ESCAV. MECANIZ. DE VALAS - ESGOTO - EM SOLO DE 2a CAT. EXECUTADA ENTRE AS PROFUND. DE 4 A 6,00m
        value = (self.getTotalDepthForExcavationTS() * self.getUnderSlabAreaTS()) * (self.soil / 100)
        return value

    def qtdItem02TS(
            self):  # ESCAV. DE VALAS - ESGOTO - EM ROCHA BRANDA EXECUTADA ENTRE AS PROFUND. DE 4 A6,00 m, C/ USO DE ROMPEDOR PNEUMATICO
        value = (self.getTotalDepthForExcavationTS() * self.getUnderSlabAreaTS()) * (self.rock / 100)
        return value

    def qtdItem03TS(self):  # CARGA E DESCARGA DE SOLO
        value = self.qtdItem01TS() * 1.15
        return value

    def qtdItem04TS(self):  # MOVIMENTO DE TRANSPORTE DE SOLO, EM CAMINHAO BASCULANTE
        value = self.qtdItem03TS() * 30
        return value

    def qtdItem05TS(self):  # CARGA E DESCARGA DE ROCHA
        value = self.qtdItem02TS() * 1.3
        return value

    def qtdItem06TS(self):  # MOVIMENTO DE TRANSPORTE DE ROCHA, EM CAMINHAO BASCULANTE
        value = self.qtdItem05TS() * 30
        return value

    def qtdItem07TS(
            self):  # EXEC. DE ATERRO EM VALAS/POCOS/CAVAS DE FUNDACAO, C/ FORNEC. DE SOLO, INCL.  LANCAM., ESPALHAM., COMPACT. C/PLACA VIBRATORIA, SOQUETE PNEUMATICO OU  SOQUETEMANUAL - DMT=20KM
        value = (self.getUnderSlabAreaTS() - self.getTopSlabAreaTS()) * self.getTotalDepthForExcavationTS()
        return value

    def qtdItem08TS(self):  # ESCORAMENTO CONTINUO COM PRACHA METALICA C/H ACIMA DE 3,0m
        value = ((self.getWidthTotalTS() * 2) + (self.getLengthTotalTS() * 2)) * self.getTotalDepthForExcavationTS()
        return value

    def qtdItem09TS(
            self):  # CONCRETO C/ CONSUMO MIN. DE CIMENTO DE 150Kg/m3, INCL. FORNEC. DE MAT., PRODUCAO, LANC., ADENS. E CURA
        value = self.getUnderSlabAreaTS() * self.regularizationBaseThickness
        return value

    def qtdItem10TS(self):  # FORMA PLANA EM COMP. RESINADO P/ RESERV. APOIADO - E=12MM ATE 3X
        value = (((self.getTopSlabAreaTS() + self.getUnderSlabAreaTS()) * 2) +
                 ((self.getFrontWallAreaTS() + self.getFinalWallAreaTS() + self.getSideWallAreaTS()) * 2 *
                  (self.concrete / 100)))
        return value

    def qtdItem11TS(self):  # CONCRETO FCK=25MPa, INCL. FORNEC. DOS  MAT., PRODUCAO, LANC.,ADENS. E CURA (LAJES)
        value = (self.getTopSlabAreaTS() * self.topSlabThickness) + (
                    self.getUnderSlabAreaTS() * self.underSlabThickness)
        return value

    def qtdItem12TS(self):  # CONCRETO FCK=25MPa, INCL. FORNEC. DOS  MAT., PRODUCAO, LANC.,ADENS. E CURA (PAREDES)
        value = ((((self.getFrontWallAreaTS() + self.getFinalWallAreaTS()) * self.frontAndEndWallThickness)
                  + (self.getSideWallAreaTS() * self.thicknessSideWalls)) * (self.concrete / 100))
        return value

    def qtdItem13TS(self):  # ACO CA-50, INCL. FORNEC., CORTE, DOBR. E COLOCACAO NAS PECAS
        value = (self.qtdItem11TS() + self.qtdItem12TS()) * 180
        return value

    def qtdItem14TS(self):  # CIMBRAMENTO P/ RESERVATORIOS APOIADOS
        value = self.getDepthTS() * self.getTopSlabAreaTS()
        return value

    def qtdItem15TS(self):  # TAMPA CONCRETO PREMOLDADO FCK=15,0 MPA E=15 CM
        value = 0.6 * 0.6
        return value

    def qtdItem16TS(self):  # ALVENARIA DE VEDACAO C/ TIJOLO MACICO (COMUM) C/ e=20cm (MRR / RMS)
        value = ((self.getFrontWallAreaTS() + self.getFinalWallAreaTS() + self.getSideWallAreaTS())
                 * (self.masonry / 100))
        return value

    # planilha de custos TS
    def qtdItem01Reactor(
            self):  # ESCAV. MECANIZ. DE VALAS - ESGOTO - EM SOLO DE 2a CAT. EXECUTADA ENTRE AS PROFUND. DE 4 A 6,00m
        value = (self.getTotalDepthForExcavationReactor() * self.getUnderSlabAreaReactor()) * (self.soil / 100)
        return value

    def qtdItem02Reactor(
            self):  # ESCAV. DE VALAS - ESGOTO - EM ROCHA BRANDA EXECUTADA ENTRE AS PROFUND. DE 4 A6,00 m, C/ USO DE ROMPEDOR PNEUMATICO
        value = (self.getTotalDepthForExcavationReactor() * self.getUnderSlabAreaReactor()) * (self.rock / 100)
        return value

    def qtdItem03Reactor(self):  # CARGA E DESCARGA DE SOLO
        value = self.qtdItem01Reactor() * 1.15
        return value

    def qtdItem04Reactor(self):  # MOVIMENTO DE TRANSPORTE DE SOLO, EM CAMINHAO BASCULANTE
        value = self.qtdItem03Reactor() * 30
        return value

    def qtdItem05Reactor(self):  # CARGA E DESCARGA DE ROCHA
        value = self.qtdItem02Reactor() * 1.3
        return value

    def qtdItem06Reactor(self):  # MOVIMENTO DE TRANSPORTE DE ROCHA, EM CAMINHAO BASCULANTE
        value = self.qtdItem05Reactor() * 30
        return value

    def qtdItem07Reactor(
            self):  # EXEC. DE ATERRO EM VALAS/POCOS/CAVAS DE FUNDACAO, C/ FORNEC. DE SOLO, INCL.  LANCAM., ESPALHAM., COMPACT. C/PLACA VIBRATORIA, SOQUETE PNEUMATICO OU  SOQUETEMANUAL - DMT=20KM
        value = (
                            self.getUnderSlabAreaReactor() - self.getTopSlabAreaReactor()) * self.getTotalDepthForExcavationReactor()
        return value

    def qtdItem08Reactor(self):  # ESCORAMENTO CONTINUO COM PRACHA METALICA C/H ACIMA DE 3,0m
        value = ((self.getWidthTotalCompartimentReactor() * 2) + (
                    self.getLengthReactor() * 2)) * self.getTotalDepthForExcavationReactor()
        return value

    def qtdItem09Reactor(
            self):  # CONCRETO C/ CONSUMO MIN. DE CIMENTO DE 150Kg/m3, INCL. FORNEC. DE MAT., PRODUCAO, LANC., ADENS. E CURA
        value = self.getUnderSlabAreaReactor() * self.regularizationBaseThickness
        return value

    def qtdItem10Reactor(self):  # FORMA PLANA EM COMP. RESINADO P/ RESERV. APOIADO - E=12MM ATE 3X
        s = f"{self.getTopSlabAreaReactor()}, {self.getUnderSlabAreaReactor()}, {self.getFrontWallAreaReactor()}, " \
            f"{self.getFinalWallAreaReactor()}, {self.getSideWallAreaReactor()}"
        value = (((self.getTopSlabAreaReactor() + self.getUnderSlabAreaReactor()) * 2) +
                 ((
                              self.getFrontWallAreaReactor() + self.getFinalWallAreaReactor() + self.getSideWallAreaReactor()) * 2 *
                  (self.concrete / 100)))
        return value

    def qtdItem11Reactor(self):  # CONCRETO FCK=25MPa, INCL. FORNEC. DOS  MAT., PRODUCAO, LANC.,ADENS. E CURA (LAJES)
        value = (self.getTopSlabAreaReactor() * self.topSlabThickness) + (
                    self.getUnderSlabAreaReactor() * self.underSlabThickness)
        return value

    def qtdItem12Reactor(self):  # CONCRETO FCK=25MPa, INCL. FORNEC. DOS  MAT., PRODUCAO, LANC.,ADENS. E CURA (PAREDES)
        value = (((((self.getFrontWallAreaReactor() + self.getFinalWallAreaReactor()) * self.frontAndEndWallThickness)
                  + (self.getSideWallAreaReactor() * self.thicknessSideWalls))
                  + (self.getIntermediateWallAreaReactor() * self.intermediateWallThickness))
                 * (self.concrete / 100))
        return value

    def qtdItem13Reactor(self):  # ACO CA-50, INCL. FORNEC., CORTE, DOBR. E COLOCACAO NAS PECAS
        value = (self.qtdItem11Reactor() + self.qtdItem12Reactor()) * 180
        return value

    def qtdItem14Reactor(self):  # CIMBRAMENTO P/ RESERVATORIOS APOIADOS
        value = self.getDepthCompartimentReactor() * self.getTopSlabAreaReactor()
        return value

    def qtdItem15Reactor(self):  # TAMPA CONCRETO PREMOLDADO FCK=15,0 MPA E=15 CM
        value = (0.6 * 0.6) * self.entranceData.getNumCompartRAC()
        return value

    def qtdItem16Reactor(self):  # ALVENARIA DE VEDACAO C/ TIJOLO MACICO (COMUM) C/ e=20cm (MRR / RMS)
        value = ((self.getFrontWallAreaReactor() + self.getFinalWallAreaReactor() + self.getSideWallAreaReactor()
                  + self.getIntermediateWallAreaReactor()) * (self.masonry / 100))
        return value

    def qtdItem17Reactor(self):  # ALVENARIA DE VEDACAO C/ TIJOLO MACICO (COMUM) C/ e=20cm (MRR / RMS)
        value = self.getChicaneAreaReactor()
        return value

    def getTotalCostsTS(self):
        value = ((self.qtdItem01TS() * self.vlItem01) + (self.qtdItem02TS() * self.vlItem02) + (
                    self.qtdItem03TS() * self.vlItem03)
                 + (self.qtdItem04TS() * self.vlItem04) + (self.qtdItem05TS() * self.vlItem05) + (
                             self.qtdItem06TS() * self.vlItem06)
                 + (self.qtdItem07TS() * self.vlItem07) + (self.qtdItem08TS() * self.vlItem08) + (
                             self.qtdItem09TS() * self.vlItem09)
                 + (self.qtdItem10TS() * self.vlItem10) + (self.qtdItem11TS() * self.vlItem11) + (
                             self.qtdItem12TS() * self.vlItem12)
                 + (self.qtdItem13TS() * self.vlItem13) + (self.qtdItem14TS() * self.vlItem14) + (
                             self.qtdItem15TS() * self.vlItem15)
                 + (self.qtdItem16TS() * self.vlItem16))
        return value

    def getTotalCostsReactor(self):
        value = ((self.qtdItem01Reactor() * self.vlItem01) + (self.qtdItem02Reactor() * self.vlItem02) + (
                    self.qtdItem03Reactor() * self.vlItem03)
                 + (self.qtdItem04Reactor() * self.vlItem04) + (self.qtdItem05Reactor() * self.vlItem05) + (
                             self.qtdItem06Reactor() * self.vlItem06)
                 + (self.qtdItem07Reactor() * self.vlItem07) + (self.qtdItem08Reactor() * self.vlItem08) + (
                             self.qtdItem09Reactor() * self.vlItem09)
                 + (self.qtdItem10Reactor() * self.vlItem10) + (self.qtdItem11Reactor() * self.vlItem11) + (
                             self.qtdItem12Reactor() * self.vlItem12)
                 + (self.qtdItem13Reactor() * self.vlItem13) + (self.qtdItem14Reactor() * self.vlItem14) + (
                             self.qtdItem15Reactor() * self.vlItem15)
                 + (self.qtdItem16Reactor() * self.vlItem16) + (self.qtdItem17Reactor() * self.vlItem17))
        return value

    def costPerInhabitant(self, tankSedimentation, population):
        if tankSedimentation:
            return (self.getTotalCostsTS() + self.getTotalCostsReactor()) / population
        else:
            return (self.getTotalCostsReactor() / population)
