import unittest
from .test_calculations import as_int
from ..core.march_calculation import MarchCalculation
from ..core.march_calculation_without_tank import MarchCalculationWithoutTank
from ..core.data.models import ProjectData
from qgis.testing import unittest


class TestProjectDataManager(unittest.TestCase):
    def test_march_calculation_tank(self):
        data = ProjectData(
            population=1188,
            consWater=100,
            k1CoefDayMaxConsume=1.2,
            k2CoefDayMaxConsume=1.5,
            coefReturn=0.8,
            concentrationDQOEntrance=1250,
            concentrationDBOEntrance=675,
            tempDigestSludge=20,
            tdh=6,
            intervalTimeRemovalSludge=18,
            widthTank=5,
            depthTank=2.5,
            depthOutRac=2.5,
            numCompartRac=4,
            widthShafts=0.4,
            tempOperReactor=25,
        )
        calculation = MarchCalculation(data)
        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 6.8, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 85.54, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 5.2, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 239.96, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.81, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 82.35, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.88, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 675.91, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 224.1, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 74.7, 1)

        data = ProjectData(
            population=1000,
            consWater=800,
            k1CoefDayMaxConsume=1.2,
            k2CoefDayMaxConsume=1.5,
            coefReturn=0.8,
            concentrationDQOEntrance=633,
            concentrationDBOEntrance=333,
            tempDigestSludge=15,
            tdh=8,
            intervalTimeRemovalSludge=15,
            widthTank=4,
            depthTank=2,
            depthOutRac=2.5,
            numCompartRac=4,
            widthShafts=0.25,
            tempOperReactor=24,
        )
        calculation = MarchCalculation(data)
        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 96.0, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 768, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 35.0, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 271.0090813646288, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.57186559026125, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 133.00411735027149, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.6005882361853709, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 1535.968378749915, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 1870.8000000000002, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 623.6, 1)

        data = ProjectData(population=3564, consWater=234, concentrationDQOEntrance=1807, concentrationDBOEntrance=1562,
                           depthOutRac=1.6376676202744205, numCompartRac=5, widthShafts=1.6580262572090372,
                           tempOperReactor=24, tdh=10, intervalTimeRemovalSludge=24, widthTank=2.8268116964287966,
                           depthTank=1.710414934973901, k1CoefDayMaxConsume=2.032709170453779,
                           k2CoefDayMaxConsume=2.9591010775578868, coefReturn=1.0007210905874988, tempDigestSludge=33)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 865.2110282784242, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 4183.313442646018, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 232.3, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), -86.83769852024443, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 1.0480562803100413, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -106.91735550758212, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.0684490112084393, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 16714.087932619073, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 16668.277042553622, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 5556.092347517874, 1)

        data = ProjectData(population=3578, consWater=346, concentrationDQOEntrance=546, concentrationDBOEntrance=1316,
                           depthOutRac=1.0896429722120806, numCompartRac=5, widthShafts=0.800708591776311,
                           tempOperReactor=27, tdh=11, intervalTimeRemovalSludge=31, widthTank=0.942252114788306,
                           depthTank=1.7038613939861476, k1CoefDayMaxConsume=3.8800171391539497,
                           k2CoefDayMaxConsume=1.1329173956675862, coefReturn=1.8655631764217144, tempDigestSludge=29)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 5796.533372999092, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 9306.1430551222, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 705.9, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 28.33005450697911, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.948113453283921, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 42.90974346958312, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.9673938119532043, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 35283.1081746931, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 32751.36341964318, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 10917.121139881061, 1)

        data = ProjectData(population=4043, consWater=441, concentrationDQOEntrance=480, concentrationDBOEntrance=1203,
                           depthOutRac=1.9283512427409162, numCompartRac=5, widthShafts=1.264866293845293,
                           tempOperReactor=30, tdh=12, intervalTimeRemovalSludge=15, widthTank=2.915609627117955,
                           depthTank=1.5973935466440763, k1CoefDayMaxConsume=3.5474483004505952,
                           k2CoefDayMaxConsume=2.9076346071551495, coefReturn=1.1104740436866605, tempDigestSludge=34)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 4384.957067124877, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 20422.393818137167, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 802.4, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 14.544393215999959, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.9696991808000001, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 13.103634895514407, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.9891075354152, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 28270.997126807644, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 67593.91634131392, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 22531.30544710464, 1)

        data = ProjectData(population=3547, consWater=149, concentrationDQOEntrance=342, concentrationDBOEntrance=1553,
                           depthOutRac=1.3431598907596576, numCompartRac=6, widthShafts=0.846307465514738,
                           tempOperReactor=32, tdh=11, intervalTimeRemovalSludge=33, widthTank=1.1943516317710092,
                           depthTank=1.5692067085634482, k1CoefDayMaxConsume=2.8100312318932112,
                           k2CoefDayMaxConsume=3.454976421414779, coefReturn=1.25100423989879, tempDigestSludge=26)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 3139.5076740561417, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 5884.016912191842, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 362.1, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 23.6354856857641, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.930890392731684, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 77.65174253481858, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.9499988779556867, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 11705.286084999068, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 22447.30812908641, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 7482.436043028803, 1)

        data = ProjectData(population=2026, consWater=587, concentrationDQOEntrance=1495, concentrationDBOEntrance=1287,
                           depthOutRac=2.8443665740829345, numCompartRac=4, widthShafts=0.6428208518691976,
                           tempOperReactor=20, tdh=12, intervalTimeRemovalSludge=28, widthTank=1.4203944936944128,
                           depthTank=2.4066079614237914, k1CoefDayMaxConsume=3.2430135941246263,
                           k2CoefDayMaxConsume=3.787576301663816, coefReturn=1.3013864757098572, tempDigestSludge=15)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 5561.342752519952, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 19010.51976953722, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 506.4, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 582.0103488342, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.61069541884, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 462.7095189786266, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.6404743442279514, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 15308.948499735541, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 37463.58349440477, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 12487.86116480159, 1)

        data = ProjectData(population=5036, consWater=137, concentrationDQOEntrance=1937, concentrationDBOEntrance=461,
                           depthOutRac=1.0226819353648164, numCompartRac=6, widthShafts=0.4816615107616985,
                           tempOperReactor=18, tdh=10, intervalTimeRemovalSludge=29, widthTank=3.707921349717126,
                           depthTank=2.2304677661320382, k1CoefDayMaxConsume=3.3300612357871238,
                           k2CoefDayMaxConsume=1.2338875269936571, coefReturn=1.5777653365433666, tempDigestSludge=50)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 450.6805149053581, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 3727.3077022802972, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 331.4, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), -173.52279319676023, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 1.0895832695904804, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -50.896698415809894, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.110404985717592, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 6686.70669113489, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 12134.211599391698, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 4044.7371997972327, 1)

        data = ProjectData(population=3076, consWater=294, concentrationDQOEntrance=1889, concentrationDBOEntrance=1078,
                           depthOutRac=1.785863161237846, numCompartRac=4, widthShafts=1.9585031831180333,
                           tempOperReactor=25, tdh=8, intervalTimeRemovalSludge=26, widthTank=1.105149703375914,
                           depthTank=2.5638291160018483, k1CoefDayMaxConsume=2.6975146578007974,
                           k2CoefDayMaxConsume=1.385324637045372, coefReturn=0.9799718426792272, tempDigestSludge=19)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 779.2219617615217, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 2207.8591846982526, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 140.5, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 613.4272602425577, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.6752634937837174, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 316.0682022009736, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.7068012966595792, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 8102.976947946718, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 7729.51595101879, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 2576.5053170062633, 1)

        data = ProjectData(population=2572, consWater=275, concentrationDQOEntrance=807, concentrationDBOEntrance=1092,
                           depthOutRac=1.305671148233571, numCompartRac=4, widthShafts=0.3343278878306183,
                           tempOperReactor=35, tdh=8, intervalTimeRemovalSludge=23, widthTank=3.101850420879634,
                           depthTank=2.27815601211457, k1CoefDayMaxConsume=1.555466526265365,
                           k2CoefDayMaxConsume=3.97104399732474, coefReturn=1.3077273382380556, tempDigestSludge=14)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 539.0023479448462, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 3808.8596524691407, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 331.5, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 346.9400533179072, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.5700866749468312, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 438.1886970941198, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.5987282993643592, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 7256.956690557773, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 9741.972451615324, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 3247.3241505384412, 1)

        data = ProjectData(population=4516, consWater=220, concentrationDQOEntrance=1835, concentrationDBOEntrance=1161,
                           depthOutRac=1.6954083646070532, numCompartRac=6, widthShafts=0.9272809643809415,
                           tempOperReactor=20, tdh=9, intervalTimeRemovalSludge=19, widthTank=1.1271282483980964,
                           depthTank=1.59778162485358, k1CoefDayMaxConsume=3.3116446188655737,
                           k2CoefDayMaxConsume=2.9091188318423367, coefReturn=1.7146069506515427, tempDigestSludge=28)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 6834.659574983296, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 12308.571263275388, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 733.4, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), -76.8843682568038, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 1.0418988382870866, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -72.37753176775111, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.0623406819705006, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 25212.648707080232, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 49184.14009775368, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 16394.713365917894, 1)

        data = ProjectData(population=3053, consWater=534, concentrationDQOEntrance=1998, concentrationDBOEntrance=1022,
                           depthOutRac=2.5373260022181263, numCompartRac=5, widthShafts=1.3904542043467423,
                           tempOperReactor=24, tdh=7, intervalTimeRemovalSludge=28, widthTank=3.231910021785086,
                           depthTank=1.202032970499426, k1CoefDayMaxConsume=1.975038657938429,
                           k2CoefDayMaxConsume=2.707176243846868, coefReturn=1.494170027098955, tempDigestSludge=36)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 1955.6960795028456, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 7597.610172662799, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 388.9, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), -123.47710429574038, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 1.0618003525003705, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -84.51266308509167, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.0826934081067434, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 32344.892795831576, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 35644.43978678573, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 11881.479928928577, 1)

        data = ProjectData(population=1544, consWater=450, concentrationDQOEntrance=1685, concentrationDBOEntrance=673,
                           depthOutRac=1.5198489018902195, numCompartRac=5, widthShafts=0.5022737263378396,
                           tempOperReactor=24, tdh=8, intervalTimeRemovalSludge=29, widthTank=2.410199951954101,
                           depthTank=1.4642664584961904, k1CoefDayMaxConsume=2.7423325502824256,
                           k2CoefDayMaxConsume=3.915992151351603, coefReturn=1.4857381692789136, tempDigestSludge=27)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 2094.1104066207326, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 7390.481985215071, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 552.6, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 18.247027242617115, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.9891709037135803, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -6.153999578295952, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.0091441301311976, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 8413.013758684545, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 27264.72733571233, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 9088.242445237443, 1)

        data = ProjectData(population=2564, consWater=264, concentrationDQOEntrance=666, concentrationDBOEntrance=625,
                           depthOutRac=2.9400967964156286, numCompartRac=4, widthShafts=1.3741785193669922,
                           tempOperReactor=24, tdh=11, intervalTimeRemovalSludge=20, widthTank=2.202944391877314,
                           depthTank=1.4438351584423215, k1CoefDayMaxConsume=3.606146847342819,
                           k2CoefDayMaxConsume=2.7134598616814936, coefReturn=0.8178320731610715, tempDigestSludge=39)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 1561.144801632861, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 4965.515418996789, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 139.6, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 33.42142952538442, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.9498176733853086, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 19.303100678352514, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.969115038914636, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 4023.6730353228018, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 15419.678022588167, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 5139.892674196056, 1)

        data = ProjectData(population=4026, consWater=328, concentrationDQOEntrance=1678, concentrationDBOEntrance=1853,
                           depthOutRac=2.6282913685972913, numCompartRac=4, widthShafts=1.7573833660879534,
                           tempOperReactor=35, tdh=8, intervalTimeRemovalSludge=36, widthTank=4.636718948943751,
                           depthTank=1.2418884489458357, k1CoefDayMaxConsume=3.098095737710316,
                           k2CoefDayMaxConsume=3.0526736648930157, coefReturn=1.4902719636787587, tempDigestSludge=13)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 2154.783993654685, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 12407.86617479463, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 536.5, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 703.7942146178439, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.5805755574387105, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 723.23534515421, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.6096949027770049, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 26679.788044401237, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 51041.05141190577, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 17013.68380396859, 1)

        data = ProjectData(population=2556, consWater=435, concentrationDQOEntrance=1602, concentrationDBOEntrance=1023,
                           depthOutRac=2.4841536678782172, numCompartRac=5, widthShafts=1.6396543488488238,
                           tempOperReactor=31, tdh=10, intervalTimeRemovalSludge=26, widthTank=2.439448386113853,
                           depthTank=1.6083498175607345, k1CoefDayMaxConsume=3.0808189013069986,
                           k2CoefDayMaxConsume=1.1614537144560924, coefReturn=1.701770867503721, tempDigestSludge=42)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 1438.0231400409168, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 5642.064185028816, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 206.5, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), -57.58904252802692, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 1.0359482163096299, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -57.508832528620346, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.0562158675744089, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 24533.570532735634, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 20072.53936125053, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 6690.846453750177, 1)

        data = ProjectData(population=5001, consWater=333, concentrationDQOEntrance=485, concentrationDBOEntrance=1119,
                           depthOutRac=1.119261966476534, numCompartRac=6, widthShafts=1.7986003848702452,
                           tempOperReactor=25, tdh=11, intervalTimeRemovalSludge=20, widthTank=1.6552934974611808,
                           depthTank=2.4528574095363345, k1CoefDayMaxConsume=1.7076379311322354,
                           k2CoefDayMaxConsume=3.0318936827749647, coefReturn=1.8913239770199122, tempDigestSludge=35)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 3681.6364858380803, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 14948.176484386997, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 1103.8, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), -0.1559479012190414, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 1.0003215420643692, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -22.517523942101338, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.020122898965238, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 43145.03695707258, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 69112.51727139493, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 23037.505757131643, 1)

        data = ProjectData(population=4528, consWater=571, concentrationDQOEntrance=756, concentrationDBOEntrance=987,
                           depthOutRac=1.520189029228338, numCompartRac=4, widthShafts=0.541108411604734,
                           tempOperReactor=29, tdh=6, intervalTimeRemovalSludge=34, widthTank=2.1019386148677794,
                           depthTank=1.8089704747659245, k1CoefDayMaxConsume=1.2916117462837295,
                           k2CoefDayMaxConsume=3.531609635611195, coefReturn=1.6428239772683306, tempDigestSludge=48)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 2547.749560541762, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 9687.422532885366, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 965.6, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 34.14054233184005, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.954840552471111, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 25.068858627676555, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.974600953771351, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 49029.64966065534, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 33462.90041996695, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 11154.300139988984, 1)

        data = ProjectData(population=4025, consWater=256, concentrationDQOEntrance=1752, concentrationDBOEntrance=1991,
                           depthOutRac=1.1737249825910447, numCompartRac=5, widthShafts=1.6637879944346647,
                           tempOperReactor=24, tdh=6, intervalTimeRemovalSludge=20, widthTank=2.7817680421209534,
                           depthTank=1.7494981605478939, k1CoefDayMaxConsume=1.192784217681258,
                           k2CoefDayMaxConsume=3.0008733197235076, coefReturn=1.3035830361051568, tempDigestSludge=17)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 493.95762896360725, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 2403.9426409030393, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 310.4, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 600.3298294879295, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.6573459877352001, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 620.229361437802, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.6884834950086378, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 22094.826200227977, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 15535.793422448703, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 5178.597807482901, 1)

        data = ProjectData(population=1576, consWater=235, concentrationDQOEntrance=1502, concentrationDBOEntrance=1811,
                           depthOutRac=2.7647138611833695, numCompartRac=6, widthShafts=1.1739966753828914,
                           tempOperReactor=20, tdh=7, intervalTimeRemovalSludge=30, widthTank=1.8073723858773205,
                           depthTank=1.7501620350992368, k1CoefDayMaxConsume=3.5841391535306393,
                           k2CoefDayMaxConsume=2.1744827114767618, coefReturn=1.4307725585470414, tempDigestSludge=49)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 761.59904684659, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 2409.085941360626, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 113.2, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), -97.68184746627902, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 1.0650345189522497, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -155.6813988151606, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.0859643284456988, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 12505.755503839513, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 9747.994213539892, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 3249.3314045132975, 1)

        data = ProjectData(population=569, consWater=517, concentrationDQOEntrance=1690, concentrationDBOEntrance=981,
                           depthOutRac=1.5612681231617644, numCompartRac=6, widthShafts=1.512492197416073,
                           tempOperReactor=19, tdh=11, intervalTimeRemovalSludge=34, widthTank=4.770098977794596,
                           depthTank=1.4333632491237607, k1CoefDayMaxConsume=2.9756807241658256,
                           k2CoefDayMaxConsume=1.4041334581668525, coefReturn=0.8196865339862884, tempDigestSludge=36)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 135.07442051385206, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 923.5422511072464, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 48.9, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), -124.39647501307358, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 1.0736073816645406, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -92.35141574200638, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.0941400772089769, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 3105.8021727568384, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 4133.128917600444, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 1377.7096392001479, 1)

        data = ProjectData(population=4579, consWater=258, concentrationDQOEntrance=1336, concentrationDBOEntrance=1492,
                           depthOutRac=1.870646071514575, numCompartRac=5, widthShafts=0.27290277090364745,
                           tempOperReactor=18, tdh=7, intervalTimeRemovalSludge=29, widthTank=2.2966018631465577,
                           depthTank=2.3496917245629843, k1CoefDayMaxConsume=1.253017836344064,
                           k2CoefDayMaxConsume=1.234507653534001, coefReturn=1.1755387053940565, tempDigestSludge=25)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 306.96903197940514, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 1656.4989495550817, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 87.0, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 126.47410285497335, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.9053337553480738, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 112.72256213402916, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.9244486848967632, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 22985.828432147842, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 3955.447552244887, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 1318.4825174149623, 1)

        data = ProjectData(population=2086, consWater=273, concentrationDQOEntrance=1591, concentrationDBOEntrance=1542,
                           depthOutRac=2.2062121867494184, numCompartRac=6, widthShafts=1.5402128027313982,
                           tempOperReactor=20, tdh=12, intervalTimeRemovalSludge=32, widthTank=3.6716168004591196,
                           depthTank=2.66666726442876, k1CoefDayMaxConsume=3.29141817095317,
                           k2CoefDayMaxConsume=3.0345988229605614, coefReturn=1.8670147181910888, tempDigestSludge=42)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 1084.6331209874513, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 10619.621552107332, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 364.7, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), -106.3282452252801, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 1.06683107808, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -134.4228125524538, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.08717432720652, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 21388.95175264482, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 30616.728733594508, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 10205.576244531503, 1)

        data = ProjectData(population=5052, consWater=223, concentrationDQOEntrance=797, concentrationDBOEntrance=382,
                           depthOutRac=2.1940539196060067, numCompartRac=5, widthShafts=0.7273854746097748,
                           tempOperReactor=25, tdh=12, intervalTimeRemovalSludge=24, widthTank=2.7586741722409567,
                           depthTank=2.6687187286428142, k1CoefDayMaxConsume=1.959462414656947,
                           k2CoefDayMaxConsume=2.860149274422084, coefReturn=1.9751481444573147, tempDigestSludge=18)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 1693.9098961281397, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 12470.77712187608, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 430.6, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 280.15394920485755, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.6484893987392001, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 122.64136468334291, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.6789493071116678, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 6925.479346599283, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 27097.82676453501, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 9032.60892151167, 1)

        data = ProjectData(population=1099, consWater=128, concentrationDQOEntrance=498, concentrationDBOEntrance=1813,
                           depthOutRac=1.6311615370170642, numCompartRac=6, widthShafts=1.3311176393248993,
                           tempOperReactor=26, tdh=10, intervalTimeRemovalSludge=32, widthTank=2.8323411182099365,
                           depthTank=2.1494615536424497, k1CoefDayMaxConsume=1.0866731919052017,
                           k2CoefDayMaxConsume=3.9657957080592108, coefReturn=1.1334632924898673, tempDigestSludge=34)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 94.05630832844074, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 572.6155895701156, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 32.0, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), -0.6262447146479335, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 1.0012575195073252, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -38.37541986947014, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.0211668063262385, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 3542.34504324868, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 2154.295740770932, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 718.0985802569774, 1)

        data = ProjectData(population=5009, consWater=178, concentrationDQOEntrance=532, concentrationDBOEntrance=543,
                           depthOutRac=1.7177253596608366, numCompartRac=6, widthShafts=1.6776307362135068,
                           tempOperReactor=21, tdh=7, intervalTimeRemovalSludge=36, widthTank=1.1862663862823875,
                           depthTank=1.813281088300528, k1CoefDayMaxConsume=1.1117404161758164,
                           k2CoefDayMaxConsume=2.177237268767776, coefReturn=1.5316993159090218, tempDigestSludge=18)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 896.4439565858894, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 1928.2817918135866, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 145.8, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 186.47575609340157, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.6494816614785685, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 173.58872921748687, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.6803154158057332, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 6053.90971924442, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 10373.340839380702, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 3457.7802797935674, 1)

        data = ProjectData(population=1040, consWater=147, concentrationDQOEntrance=1275, concentrationDBOEntrance=463,
                           depthOutRac=1.163417854251457, numCompartRac=4, widthShafts=0.9574362539293196,
                           tempOperReactor=31, tdh=9, intervalTimeRemovalSludge=19, widthTank=2.363195337078592,
                           depthTank=2.39738745472402, k1CoefDayMaxConsume=2.1442370436541656,
                           k2CoefDayMaxConsume=3.1169496570462547, coefReturn=1.678063234799259, tempDigestSludge=48)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 226.9786417711394, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 1285.9463269619114, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 111.7, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 19.659862966319597, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.9845804996342591, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -2.04196583792263, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.004410293386442, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 1431.6352670901772, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 3943.1706386406477, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 1314.3902128802158, 1)

        data = ProjectData(population=4591, consWater=73, concentrationDQOEntrance=1254, concentrationDBOEntrance=1282,
                           depthOutRac=1.100236796632171, numCompartRac=6, widthShafts=0.4964563296411938,
                           tempOperReactor=26, tdh=8, intervalTimeRemovalSludge=28, widthTank=3.521306842327955,
                           depthTank=2.7653184562993207, k1CoefDayMaxConsume=2.1944727011841154,
                           k2CoefDayMaxConsume=2.443297658257822, coefReturn=1.1333956493623734, tempDigestSludge=37)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 139.4369818091539, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 1357.7724629663853, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 140.3, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), -61.20855125027178, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 1.0488106469300413, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -89.0237029757822, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.069441265971749, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 6249.393960011295, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 4625.326580548504, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 1541.7755268495016, 1)

        data = ProjectData(population=2580, consWater=152, concentrationDQOEntrance=344, concentrationDBOEntrance=730,
                           depthOutRac=2.0989595477160563, numCompartRac=4, widthShafts=1.0947381220819594,
                           tempOperReactor=35, tdh=11, intervalTimeRemovalSludge=27, widthTank=4.710182236165845,
                           depthTank=1.6979821681933962, k1CoefDayMaxConsume=2.213281004172849,
                           k2CoefDayMaxConsume=1.147022096815049, coefReturn=0.8327414931311128, tempDigestSludge=22)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 95.02162291493768, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 759.9644532321814, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 30.0, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 65.80816208693795, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.8086972032356454, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 87.81620349758253, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.8797038308252294, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 2516.5993964648387, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 2192.278142138561, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 730.7593807128537, 1)

        data = ProjectData(population=3019, consWater=167, concentrationDQOEntrance=667, concentrationDBOEntrance=1937,
                           depthOutRac=1.2445180503939013, numCompartRac=6, widthShafts=0.3589975732076498,
                           tempOperReactor=32, tdh=11, intervalTimeRemovalSludge=31, widthTank=3.9649803222370004,
                           depthTank=2.7598146077057035, k1CoefDayMaxConsume=3.4649600321404073,
                           k2CoefDayMaxConsume=3.4692894473729896, coefReturn=1.7936399245877839, tempDigestSludge=18)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 910.6345104547854, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 9964.718858279884, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 661.8, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), 226.6739710742477, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 0.6601589639066752, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), 598.5751899978901, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 0.6909782188962881, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 14524.128110000873, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 24908.30282333109, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 8302.76760777703, 1)

        data = ProjectData(population=4010, consWater=177, concentrationDQOEntrance=1559, concentrationDBOEntrance=1268,
                           depthOutRac=1.0404730462567309, numCompartRac=5, widthShafts=1.9974289785664046,
                           tempOperReactor=29, tdh=10, intervalTimeRemovalSludge=35, widthTank=2.4388227663044173,
                           depthTank=1.6209468372094162, k1CoefDayMaxConsume=1.7863836295170703,
                           k2CoefDayMaxConsume=1.7344271651548693, coefReturn=1.0701826872333664, tempDigestSludge=39)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 496.10785020273204, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 1961.2145702219957, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 171.4, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), -52.08381417112442, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 1.0334084760558848, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -68.02806192092658, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.0536498911048318, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 12177.899513278957, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 10619.801951027113, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 3539.9339836757044, 1)

        data = ProjectData(population=3035, consWater=296, concentrationDQOEntrance=1584, concentrationDBOEntrance=794,
                           depthOutRac=1.2897671183577186, numCompartRac=6, widthShafts=0.25831568836660584,
                           tempOperReactor=31, tdh=11, intervalTimeRemovalSludge=29, widthTank=2.858893828261956,
                           depthTank=2.2055423855589344, k1CoefDayMaxConsume=2.079463377099783,
                           k2CoefDayMaxConsume=2.735918926904216, coefReturn=1.3846117493475059, tempDigestSludge=27)

        calculation = MarchCalculation(data)

        self.assertAlmostEqual(calculation.getLengthTankSedimentation(), 1028.7999219513545, 1)
        self.assertAlmostEqual(calculation.getVolumeTankSedimentation(), 6487.006873520245, 1)
        self.assertAlmostEqual(calculation.getWidthAdoptedCompartmentRAC(), 415.7, 1)
        self.assertAlmostEqual(calculation.getConcentrationDQOEffluentFinal(), -21.10744769614514, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDQOProcess(), 1.0133254088990815, 2)
        self.assertAlmostEqual(calculation.getConcentrationDBOEffluentFinal(), -26.405688633467772, 2)
        self.assertAlmostEqual(calculation.getEfficiencyRemovalTotalDBOProcess(), 1.0332565348028562, 2)
        self.assertAlmostEqual(calculation.getEmissionGasCarbonicEquivalentDaily(), 12245.832876464612, 2)
        self.assertAlmostEqual(calculation.getConstructedAreaTotal(), 17081.918604426937, 1)
        self.assertAlmostEqual(calculation.getAreaUtilTotal(), 5693.972868142313, 1)