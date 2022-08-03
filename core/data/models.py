"""
In this module resides the dataclasses of our project.
No code logic is made here, only the models to access and hold data.
The logic for data access can be found at data_access_objects
"""

from dataclasses import dataclass
from .entrance_data import ProjectData


@dataclass
class ProjectInfo:
    project_name: str = '---'
    local: str = '---'
    designer: str = '---'
    client: str = ''
    state: str = ''
    country: str = ''
    scale: str = ''
    version: str = ''


@dataclass
class ProjectConfig:
    should_import_rede_basica: bool
    has_sedimentation_tank: bool
    should_calculate_area: bool
    should_show_costs: bool


@dataclass
class Costs:
    # common attributes for the sedimentation tank and the reactor
    topSlabThickness = 0.2
    underSlabThickness = 0.25
    thicknessSideWalls = 0.2
    frontAndEndWallThickness = 0.2
    regularizationBaseThickness = 0.1  # Espessura base de regularização
    intermediateWallThickness = 0.2

    # User input data
    soil: int = 0
    rock: int = 0
    concrete: int = 0
    masonry: int = 0
    final_population: int = 0

    entrance_pipe_depth: float = 0
    entrance_pipe_diameter: float = 0

    services: list = (1.02, 14.31, 0.27, 0.16, 0.54, 0.22, 8.38, 21.07, 80.02, 8.94, 104.10, 104.10, 2.45, 8.66,
                      37.08, 47.84, 22.51)

    def __post_init__(self):
        # O valor padrão é um tuple, para evitar usar valores mutáveis como argumento
        # então garantimos a transformação do valor default para lista após o método init.
        self.services = list(self.services)


@dataclass
class FromRedeBasicaData:
    """Class used to hold data given by the rede basica plugin"""
    maximum_horly_sludge_flow_final: float = 0
    maximum_horly_sludge_flow_initial: float = 0
    average_strictly_domestic_flow_final: float = 0
    average_strictly_domestic_flow_initial: float = 0
    infiltration_flow: float = 0


@dataclass
class Project:
    info: ProjectInfo
    config: ProjectConfig
    data: ProjectData
    costs: Costs

