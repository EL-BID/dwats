import unittest
import sys
from ..core.data.models import *
from ..core.data.data_manager import ProjectDataManager

sys.path.append("..")


class TestProjectDataManager(unittest.TestCase):
    def test_project_info(self):
        p = ProjectInfo(
            project_name="Projeto de teste",
            local="Salvador",
            designer="Fredson",
            client="Renato",
            state="Bahia",
            country="Brasil",
            scale="1:1000",
            version="1.7"
        )

        ProjectDataManager.save_project_info(p)
        self.assertTrue(ProjectDataManager.is_project_info_loaded())
        self.assertEqual(p, ProjectDataManager.get_project_info())

    def test_project_config(self):
        p = ProjectConfig(True, False, True)
        ProjectDataManager.save_project_config(p)
        self.assertTrue(ProjectDataManager.is_project_config_loaded())
        self.assertEqual(p, ProjectDataManager.get_project_config())

    def test_project_data(self):
        p = ProjectData(
            population=800,
            consWater=100,
            concentrationDQOEntrance=633,
            concentrationDBOEntrance=333,
            depthOutRac=5,
            numCompartRac=3,
            widthShafts=0.25,
            tempOperReactor=27,
            tdh=10,
            intervalTimeRemovalSludge=9,
            widthTank=3,
            depthTank=2,
            k1CoefDayMaxConsume=4,
            k2CoefDayMaxConsume=5,
            coefReturn=2,
            tempDigestSludge=3
        )
        ProjectDataManager.save_project_data(p)
        self.assertTrue(ProjectDataManager.is_project_data_loaded())
        self.assertEqual(p, ProjectDataManager.get_project_data())

    def test_costs(self):
        l = [i + i / 10 + 2.7128128 ** (-i) for i in range(17)]

        p = Costs(
            soil=17,
            rock=100-17,
            concrete=23,
            masonry=100-23,

            entrance_pipe_depth=4,
            entrance_pipe_diameter=0.12,

            services=l
        )
        ProjectDataManager.save_project_costs(p)
        self.assertTrue(ProjectDataManager.is_costs_loaded())
        self.assertEqual(p, ProjectDataManager.get_project_costs_data())
