from typing import Union

from qgis.core import QgsProject
from .models import *
from .data_access_objects import *
from .entrance_data import ProjectData


class ProjectDataManager:
    """Class used to save and load the currenct project instance.

        Here we call the methods to retrieve the project data

        We use it to interface with our data access object APIS."""

    @classmethod
    def get_full_project(cls) -> Project:
        return Project(
            info=cls.get_project_info(),
            config=cls.get_project_config(),
            data=cls.get_project_data(),
            costs=cls.get_project_costs_data()
        )

    @staticmethod
    def get_project_info() -> ProjectInfo:
        return ProjectInfo(
            project_name=ProjectInfoDAO.get_project_name()[0],
            local=ProjectInfoDAO.get_local()[0],
            designer=ProjectInfoDAO.get_designer()[0],
            client=ProjectInfoDAO.get_client()[0],
            state=ProjectInfoDAO.get_state()[0],
            country=ProjectInfoDAO.get_country()[0],
            #scale=ProjectInfoDAO.get_scale()[0],
            version=ProjectInfoDAO.get_version()[0]
        )

    @staticmethod
    def get_project_config() -> ProjectConfig:
        return ProjectConfig(
            should_import_rede_basica=ProjectConfigDAO.get_should_import_rede_basica()[0],
            has_sedimentation_tank=ProjectConfigDAO.get_has_sedimentation_tank()[0],
            should_calculate_area=ProjectConfigDAO.get_should_calculate_area()[0],
            should_show_costs=ProjectConfigDAO.get_should_show_costs()[0]
        )

    @staticmethod
    def get_project_data() -> ProjectData:
        return ProjectData(
            initial_population=ProjectEntranceDataDAO.get_initial_population()[0],
            final_population=ProjectEntranceDataDAO.get_final_population()[0],
            #final_max_hourly_sludge_flow=ProjectEntranceDataDAO.get_final_max_hourly_sludge_flow()[0],
            #initial_max_hourly_sludge_flow=ProjectEntranceDataDAO.get_initial_max_hourly_sludge_flow()[0],
            final_infiltration_flow=ProjectEntranceDataDAO.get_final_infiltration_flow()[0],
            consWater=ProjectEntranceDataDAO.get_cons_water()[0],
            concentrationDQOEntrance=ProjectEntranceDataDAO.get_concentration_dqo_entrance()[0],
            concentrationDBOEntrance=ProjectEntranceDataDAO.get_concentration_dbo_entrance()[0],
            depthOutRac=ProjectEntranceDataDAO.get_depth_out_rac()[0],
            numCompartRac=ProjectEntranceDataDAO.get_num_compart_rac()[0],
            widthShafts=ProjectEntranceDataDAO.get_width_shafts()[0],
            tempOperReactor=ProjectEntranceDataDAO.get_temp_oper_reactor()[0],
            tdh=ProjectEntranceDataDAO.get_tdh()[0],
            intervalTimeRemovalSludge=ProjectEntranceDataDAO.get_interval_time_removal_sludge()[0],
            widthTank=ProjectEntranceDataDAO.get_width_tank()[0],
            depthTank=ProjectEntranceDataDAO.get_depth_tank()[0],
            k1CoefDayMaxConsume=ProjectEntranceDataDAO.get_k1_coef_day_max_consume()[0],
            k2CoefDayMaxConsume=ProjectEntranceDataDAO.get_k2_coef_day_max_consume()[0],
            coefReturn=ProjectEntranceDataDAO.get_coef_return()[0],
            tempDigestSludge=ProjectEntranceDataDAO.get_temp_digest_sludge()[0]
        )

    @staticmethod
    def get_project_costs_data() -> Costs:
        return Costs(
            soil=CostsDAO.get_soil_percentage()[0],
            rock=CostsDAO.get_rock_percentage()[0],
            concrete=CostsDAO.get_concrete_percentage()[0],
            masonry=CostsDAO.get_masonry_percentage()[0],
            final_population=CostsDAO.get_final_population()[0],

            entrance_pipe_depth=CostsDAO.get_entrance_pipe_depth()[0],
            entrance_pipe_diameter=CostsDAO.get_entrance_pipe_diameter()[0],

            services=CostsDAO.get_services()[0]
        )

    @staticmethod
    def get_from_rede_basica_data() -> FromRedeBasicaData:
        return FromRedeBasicaData(
            maximum_horly_sludge_flow_initial=FromRedeBasicaDAO.get_maximum_horly_sludge_flow_initial()[0],
            maximum_horly_sludge_flow_final=FromRedeBasicaDAO.get_maximum_horly_sludge_flow_final()[0],
            average_strictly_domestic_flow_initial=FromRedeBasicaDAO.get_average_strictly_domestic_flow_initial()[0],
            average_strictly_domestic_flow_final=FromRedeBasicaDAO.get_average_strictly_domestic_flow_final()[0],
            infiltration_flow=FromRedeBasicaDAO.get_infiltration_flow()[0],
        )

    @staticmethod
    def save_project_info(project_info: ProjectInfo) -> bool:
        success = (ProjectInfoDAO.set_project_name(project_info.project_name) and
                   ProjectInfoDAO.set_local(project_info.local) and
                   ProjectInfoDAO.set_designer(project_info.designer) and
                   ProjectInfoDAO.set_client(project_info.client) and
                   ProjectInfoDAO.set_state(project_info.state) and
                   ProjectInfoDAO.set_country(project_info.country) and
                   ProjectInfoDAO.set_version(project_info.version))
        if success:
            ProjectInfoDAO.set_done(True)
            return True

        return False

    @staticmethod
    def save_project_config(project_config: ProjectConfig):
        success = (ProjectConfigDAO.set_should_import_rede_basica(project_config.should_import_rede_basica) and
                   ProjectConfigDAO.set_has_sedimentation_tank(project_config.has_sedimentation_tank) and
                   ProjectConfigDAO.set_should_calculate_area(project_config.should_calculate_area) and
                   ProjectConfigDAO.set_should_show_costs(project_config.should_show_costs))
        if success:
            ProjectConfigDAO.set_done(True)
            return True
        return False

    @staticmethod
    def save_project_data(project_data: ProjectData):
        success = (ProjectEntranceDataDAO.set_initial_population(project_data.initial_population) and
                   ProjectEntranceDataDAO.set_final_population(project_data.final_population) and
                   ProjectEntranceDataDAO.set_final_infiltration_flow(project_data.final_infiltration_flow) and
                   ProjectEntranceDataDAO.set_cons_water(project_data.consWater) and
                   ProjectEntranceDataDAO.set_concentration_dqo_entrance(project_data.concentrationDQOEntrance) and
                   ProjectEntranceDataDAO.set_concentration_dbo_entrance(project_data.concentrationDBOEntrance) and
                   ProjectEntranceDataDAO.set_depth_out_rac(project_data.depthOutRac) and
                   ProjectEntranceDataDAO.set_num_compart_rac(project_data.numCompartRac) and
                   ProjectEntranceDataDAO.set_width_shafts(project_data.widthShafts) and
                   ProjectEntranceDataDAO.set_temp_oper_reactor(project_data.tempOperReactor) and
                   ProjectEntranceDataDAO.set_tdh(project_data.tdh) and
                   ProjectEntranceDataDAO.set_interval_time_removal_sludge(project_data.intervalTimeRemovalSludge) and
                   ProjectEntranceDataDAO.set_width_tank(project_data.widthTank) and
                   ProjectEntranceDataDAO.set_depth_tank(project_data.depthTank) and
                   ProjectEntranceDataDAO.set_k1_coef_day_max_consume(project_data.k1CoefDayMaxConsume) and
                   ProjectEntranceDataDAO.set_k2_coef_day_max_consume(project_data.k2CoefDayMaxConsume) and
                   ProjectEntranceDataDAO.set_coef_return(project_data.coefReturn) and
                   ProjectEntranceDataDAO.set_temp_digest_sludge(project_data.tempDigestSludge))#and
                   #ProjectEntranceDataDAO.set_initial_max_daily_sludge_flow(project_data.initial_max_hourly_sludge_flow) and
                   #ProjectEntranceDataDAO.set_final_max_daily_sludge_flow(project_data.final_max_hourly_sludge_flow))
        if success:
            ProjectEntranceDataDAO.set_done(True)
            return True
        return False

    @staticmethod
    def save_project_costs(project_costs: Costs):
        success = (CostsDAO.set_soil_percentage(project_costs.soil) and
                   CostsDAO.set_rock_percentage(project_costs.rock) and
                   CostsDAO.set_concrete_percentage(project_costs.concrete) and
                   CostsDAO.set_masonry_percentage(project_costs.masonry) and
                   CostsDAO.set_final_population(project_costs.final_population) and
                   CostsDAO.set_entrance_pipe_depth(project_costs.entrance_pipe_depth) and
                   CostsDAO.set_entrance_pipe_diameter(project_costs.entrance_pipe_diameter) and
                   CostsDAO.set_services(project_costs.services))

        if success:
            CostsDAO.set_done(True)
            return True
        return False

    @staticmethod
    def save_from_rede_basica_data(from_rede_basica_data: FromRedeBasicaData):
        success = (FromRedeBasicaDAO.set_maximum_horly_sludge_flow_initial(from_rede_basica_data.maximum_horly_sludge_flow_initial) and
                   FromRedeBasicaDAO.set_maximum_horly_sludge_flow_final(from_rede_basica_data.maximum_horly_sludge_flow_final) and
                   FromRedeBasicaDAO.set_average_strictly_domestic_flow_initial(from_rede_basica_data.average_strictly_domestic_flow_initial) and
                   FromRedeBasicaDAO.set_average_strictly_domestic_flow_final(from_rede_basica_data.average_strictly_domestic_flow_final) and
                   FromRedeBasicaDAO.set_infiltration_flow(from_rede_basica_data.infiltration_flow)
                   )
        if success:
            FromRedeBasicaDAO.set_done(True)
            return True

        return False

    @staticmethod
    def is_project_info_loaded() -> bool:
        return ProjectInfoDAO.is_done()[0]

    @staticmethod
    def is_project_config_loaded() -> bool:
        return ProjectConfigDAO.is_done()[0]

    @staticmethod
    def is_project_data_loaded() -> bool:
        return ProjectEntranceDataDAO.is_done()[0]

    @staticmethod
    def is_costs_loaded() -> bool:
        return CostsDAO.is_done()[0]

    @classmethod
    def is_from_rede_basica_data_loaded(cls):
        return FromRedeBasicaDAO.is_done()[0]

    @staticmethod
    def set_project_info_loaded(value) -> bool:
        return ProjectInfoDAO.set_done(value)

    @staticmethod
    def set_project_config_loaded(value) -> bool:
        return ProjectConfigDAO.set_done(value)

    @staticmethod
    def set_project_data_loaded(value) -> bool:
        return ProjectEntranceDataDAO.set_done(value)

    @staticmethod
    def set_costs_loaded(value) -> bool:
        return CostsDAO.set_done(value)


