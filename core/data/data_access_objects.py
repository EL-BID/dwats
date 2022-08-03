"""
/***************************************************************************
 In this module resides the data access objects of our project.

 The readEntry and writeEntry methods are used to directly access the QGIS project
 data.
 ***************************************************************************/
"""
from typing import List, Tuple
from qgis.core import QgsProject
from abc import abstractmethod, ABC


class DAO(ABC):
    """Classe base dos nossos objetos de acesso de dados. Toda DAO terá os métodos set/is_done, além de um escopo
    obrigatório para podermos adicionar informações ao projeto.

    Evite chamar essas classes de acesso de dados diretamente no código, para evitar dependências indesejadas. Ao invés
    disso, utilize o serviço em data_manager.py para acessar os métodos nesse módulo."""

    KEY_DONE = "done"

    proj: QgsProject = QgsProject.instance()

    @property
    @classmethod
    @abstractmethod
    def SCOPE(cls):
        """Constante do escopo utilizado para inserir informações no projeto QGIS."""
        return NotImplementedError

    # Flag utilizada para determinar se os dados de certo DAO já foi setado
    # verificamos isso para saber se o projeto tem as informações que queremos
    @classmethod
    def is_done(cls):
        return cls.proj.readBoolEntry(cls.SCOPE, cls.KEY_DONE, False)

    @classmethod
    def set_done(cls, done=True):
        return cls.proj.writeEntryBool(cls.SCOPE, cls.KEY_DONE, done)


class ProjectInfoDAO(DAO):
    """Classe de acessos de dados para as informações de cabeçalho do projeto"""
    SCOPE = "SanibidProjectInfoScope"
    KEY_PROJECT_NAME = "project_name"
    KEY_LOCAL = "local"
    KEY_DESIGNER = "designer"
    KEY_CLIENT = "client"
    KEY_STATE = "state"
    KEY_COUNTRY = "country"
    KEY_VERSION = "version"

    @classmethod
    def get_project_name(cls) -> Tuple[str, bool]:
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_PROJECT_NAME, None)

    @classmethod
    def get_local(cls) -> Tuple[str, bool]:
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_LOCAL, None)

    @classmethod
    def get_designer(cls) -> Tuple[str, bool]:
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_DESIGNER, None)

    @classmethod
    def get_client(cls) -> Tuple[str, bool]:
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_CLIENT, None)

    @classmethod
    def get_state(cls) -> Tuple[str, bool]:
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_STATE, None)

    @classmethod
    def get_country(cls) -> Tuple[str, bool]:
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_COUNTRY, None)

    @classmethod
    def get_version(cls) -> Tuple[str, bool]:
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_VERSION, None)

    @classmethod
    def set_project_name(cls, project_name: str) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_PROJECT_NAME, project_name)

    @classmethod
    def set_local(cls, local: str) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_LOCAL, local)

    @classmethod
    def set_designer(cls, designer: str) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_DESIGNER, designer)

    @classmethod
    def set_client(cls, client: str) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_CLIENT, client)

    @classmethod
    def set_state(cls, state: str) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_STATE, state)

    @classmethod
    def set_country(cls, country: str) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_COUNTRY, country)

    @classmethod
    def set_version(cls, version: str) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_VERSION, version)


class ProjectConfigDAO(DAO):
    """Classe de acesso de dados para as configurações do projeto, como se é de tanque de sedimentação ou etc."""
    SCOPE = "SanibidProjectConfigScope"
    KEY_SHOULD_IMPORT_REDE_BASICA = "should_import_rede_basica"
    KEY_HAS_SEDIMENTATION_TANK = "has_sedimentation_tank"
    KEY_SHOULD_CALCULATE_AREA = "should_calculate_area"
    KEY_SHOULD_SHOW_COSTS = "should_show_costs"

    @classmethod
    def get_should_import_rede_basica(cls) -> Tuple[bool, bool]:
        return cls.proj.readBoolEntry(cls.SCOPE, cls.KEY_SHOULD_IMPORT_REDE_BASICA)

    @classmethod
    def get_has_sedimentation_tank(cls) -> Tuple[bool, bool]:
        return cls.proj.readBoolEntry(cls.SCOPE, cls.KEY_HAS_SEDIMENTATION_TANK)

    @classmethod
    def get_should_calculate_area(cls) -> Tuple[bool, bool]:
        return cls.proj.readBoolEntry(cls.SCOPE, cls.KEY_SHOULD_CALCULATE_AREA)

    @classmethod
    def get_should_show_costs(cls) -> Tuple[bool, bool]:
        return cls.proj.readBoolEntry(cls.SCOPE, cls.KEY_SHOULD_SHOW_COSTS)

    @classmethod
    def set_should_import_rede_basica(cls, should_import_rede_basica: bool) -> bool:
        return cls.proj.writeEntryBool(cls.SCOPE, cls.KEY_SHOULD_IMPORT_REDE_BASICA, should_import_rede_basica)

    @classmethod
    def set_has_sedimentation_tank(cls, has_sedimentation_tank: bool) -> bool:
        return cls.proj.writeEntryBool(cls.SCOPE, cls.KEY_HAS_SEDIMENTATION_TANK, has_sedimentation_tank)

    @classmethod
    def set_should_calculate_area(cls, should_calculate_area: bool) -> bool:
        return cls.proj.writeEntryBool(cls.SCOPE, cls.KEY_SHOULD_CALCULATE_AREA, should_calculate_area)

    @classmethod
    def set_should_show_costs(cls, should_show_costs: bool):
        return cls.proj.writeEntryBool(cls.SCOPE, cls.KEY_SHOULD_SHOW_COSTS, should_show_costs)


class ProjectEntranceDataDAO(DAO):
    """Classe de acesso de dados para os dados de entrada do projeto"""
    SCOPE = "SanibidProjectEntranceDataScope"
    KEY_INITIAL_POPULATION = "initial_population"
    KEY_FINAL_POPULATION = "final_population"
    KEY_MAX_FLOW_HOUR_FINAL_PLAN = "max_flow_hour_final_plan"
    KEY_MAX_FLOW_HOUR_INITIAL_PLAN = "max_flow_hour_initial_plan"
    KEY_AVG_FLOW_STRICTLY_DOMESTIC_INITIAL_PLAN = "avg_flow_strictly_domestic_initial_plan"
    KEY_AVG_FLOW_STRICTLY_DOMESTIC_FINAL_PLAN = "avg_flow_strictly_domestic_final_plan"
    KEY_FINAL_INFITRATION_FLOW = "final_infiltration_flow"
    KEY_CONS_WATER = "cons_water"
    KEY_CONCENTRATION_DQO_ENTRANCE = "concentrationDQOEntrance"
    KEY_CONCENTRATION_DBO_ENTRANCE = "concentrationDBOEntrance"
    KEY_DEPTH_OUT_RAC = "depthOutRac"
    KEY_NUM_COMPART_RAC = "numCompartRac"
    KEY_WIDTH_SHAFTS = "widthShafts"
    KEY_TEMP_OPER_REACTOR = "tempOperReactor"
    KEY_TDH = "tdh"
    KEY_INTERVAL_TIME_REMOVAL_SLUDGE = "intervalTimeRemovalSludge"
    KEY_WIDTH_TANK = "widthTank"
    KEY_DEPTH_TANK = "depthTank"
    KEY_K1_COEF_DAY_MAX_CONSUME = "k1CoefDayMaxConsume"
    KEY_K2_COEF_DAY_MAX_CONSUME = "k2CoefDayMaxConsume"
    KEY_COEF_RETURN = "coefReturn"
    KEY_TEMP_DIGEST_SLUDGE = "tempDigestSludge"
    #KEY_FINAL_MAX_HOURLY_SLUDGE_FLOW = "final_max_daily_sludge_flow"
    #KEY_INITIAL_MAX_HOURLY_SLUDGE_FLOW = "initial_max_daily_sludge_flow"

    #@classmethod
    #def get_final_max_hourly_sludge_flow(cls):
    #    return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_FINAL_MAX_HOURLY_SLUDGE_FLOW)

    #@classmethod
    #def get_initial_max_hourly_sludge_flow(cls):
    #    return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_INITIAL_MAX_HOURLY_SLUDGE_FLOW)

    @classmethod
    def get_initial_population(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_INITIAL_POPULATION)

    @classmethod
    def get_final_population(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_FINAL_POPULATION)

    @classmethod
    def get_final_infiltration_flow(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_FINAL_INFITRATION_FLOW)

    @classmethod
    def get_max_flow_hour_final_plan(cls) -> Tuple[float, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_MAX_FLOW_HOUR_FINAL_PLAN)

    @classmethod
    def get_max_flow_hour_initial_plan(cls) -> Tuple[float, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_MAX_FLOW_HOUR_INITIAL_PLAN)

    @classmethod
    def get_avg_flow_strictly_domestic_initial_plan(cls) -> Tuple[float, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_AVG_FLOW_STRICTLY_DOMESTIC_INITIAL_PLAN)

    @classmethod
    def get_avg_flow_strictly_domestic_final_plan(cls) -> Tuple[float, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_AVG_FLOW_STRICTLY_DOMESTIC_FINAL_PLAN)

    @classmethod
    def get_cons_water(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_CONS_WATER)

    @classmethod
    def get_concentration_dqo_entrance(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_CONCENTRATION_DQO_ENTRANCE)

    @classmethod
    def get_concentration_dbo_entrance(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_CONCENTRATION_DBO_ENTRANCE)

    @classmethod
    def get_depth_out_rac(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_DEPTH_OUT_RAC)

    @classmethod
    def get_num_compart_rac(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_NUM_COMPART_RAC)

    @classmethod
    def get_width_shafts(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_WIDTH_SHAFTS)

    @classmethod
    def get_temp_oper_reactor(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_TEMP_OPER_REACTOR)

    @classmethod
    def get_tdh(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_TDH)

    @classmethod
    def get_interval_time_removal_sludge(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_INTERVAL_TIME_REMOVAL_SLUDGE)

    @classmethod
    def get_width_tank(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_WIDTH_TANK)

    @classmethod
    def get_depth_tank(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_DEPTH_TANK)

    @classmethod
    def get_k1_coef_day_max_consume(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_K1_COEF_DAY_MAX_CONSUME)

    @classmethod
    def get_k2_coef_day_max_consume(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_K2_COEF_DAY_MAX_CONSUME)

    @classmethod
    def get_coef_return(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_COEF_RETURN)

    @classmethod
    def get_temp_digest_sludge(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_TEMP_DIGEST_SLUDGE)

    @classmethod
    def set_initial_population(cls, value: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_INITIAL_POPULATION, value)

    #@classmethod
    #def set_final_max_daily_sludge_flow(cls, final_max_daily_sludge_flow: float):
    #    return cls.proj.writeEntryDouble(
    #        cls.SCOPE, cls.KEY_FINAL_MAX_HOURLY_SLUDGE_FLOW, final_max_daily_sludge_flow)

    #@classmethod
    #def set_initial_max_daily_sludge_flow(cls, initial_max_daily_sludge_flow: float):
    #    return cls.proj.writeEntryDouble(
    #        cls.SCOPE, cls.KEY_INITIAL_MAX_HOURLY_SLUDGE_FLOW, initial_max_daily_sludge_flow)

    @classmethod
    def set_final_population(cls, value: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_FINAL_POPULATION, value)

    @classmethod
    def set_final_infiltration_flow(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_FINAL_INFITRATION_FLOW, value)

    @classmethod
    def set_max_flow_hour_final_plan(cls, value: float) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_MAX_FLOW_HOUR_FINAL_PLAN, value)

    @classmethod
    def set_max_flow_hour_initial_plan(cls, value: float) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_MAX_FLOW_HOUR_INITIAL_PLAN, value)

    @classmethod
    def set_avg_flow_strictly_domestic_initial_plan(cls, value: float) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_AVG_FLOW_STRICTLY_DOMESTIC_INITIAL_PLAN, value)

    @classmethod
    def set_avg_flow_strictly_domestic_final_plan(cls, value: float) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_AVG_FLOW_STRICTLY_DOMESTIC_FINAL_PLAN, value)

    @classmethod
    def set_cons_water(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_CONS_WATER, value)

    @classmethod
    def set_concentration_dqo_entrance(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_CONCENTRATION_DQO_ENTRANCE, value)

    @classmethod
    def set_concentration_dbo_entrance(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_CONCENTRATION_DBO_ENTRANCE, value)

    @classmethod
    def set_depth_out_rac(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_DEPTH_OUT_RAC, value)

    @classmethod
    def set_num_compart_rac(cls, value: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_NUM_COMPART_RAC, value)

    @classmethod
    def set_width_shafts(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_WIDTH_SHAFTS, value)

    @classmethod
    def set_temp_oper_reactor(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_TEMP_OPER_REACTOR, value)

    @classmethod
    def set_tdh(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_TDH, value)

    @classmethod
    def set_interval_time_removal_sludge(cls, value: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_INTERVAL_TIME_REMOVAL_SLUDGE, value)

    @classmethod
    def set_width_tank(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_WIDTH_TANK, value)

    @classmethod
    def set_depth_tank(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_DEPTH_TANK, value)

    @classmethod
    def set_k1_coef_day_max_consume(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_K1_COEF_DAY_MAX_CONSUME, value)

    @classmethod
    def set_k2_coef_day_max_consume(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_K2_COEF_DAY_MAX_CONSUME, value)

    @classmethod
    def set_coef_return(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_COEF_RETURN, value)

    @classmethod
    def set_temp_digest_sludge(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_TEMP_DIGEST_SLUDGE, value)


class FromRedeBasicaDAO(DAO):
    SCOPE = "SanibidProjectFromRedeBasicaScope"
    KEY_MAXIMUM_HORLY_SLUDGE_FLOW_FINAL = "MAXIMUM_HORLY_SLUDGE_FLOW_FINAL"
    KEY_MAXIMUM_HORLY_SLUDGE_FLOW_INITIAL = "MAXIMUM_HORLY_SLUDGE_FLOW_INITIAL"
    KEY_AVERAGE_STRICTLY_DOMESTIC_FLOW_FINAL = "AVERAGE_STRICTLY_DOMESTIC_FLOW_FINAL"
    KEY_AVERAGE_STRICTLY_DOMESTIC_FLOW_INITIAL = "AVERAGE_STRICTLY_DOMESTIC_FLOW_INITIAL"
    KEY_INFILTRATION_FLOW = "INFILTRATION_FLOW"

    @classmethod
    def get_maximum_horly_sludge_flow_final(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_MAXIMUM_HORLY_SLUDGE_FLOW_FINAL)

    @classmethod
    def get_maximum_horly_sludge_flow_initial(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_MAXIMUM_HORLY_SLUDGE_FLOW_INITIAL)

    @classmethod
    def get_average_strictly_domestic_flow_final(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_AVERAGE_STRICTLY_DOMESTIC_FLOW_FINAL)

    @classmethod
    def get_average_strictly_domestic_flow_initial(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_AVERAGE_STRICTLY_DOMESTIC_FLOW_INITIAL)

    @classmethod
    def get_infiltration_flow(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_INFILTRATION_FLOW)

    @classmethod
    def set_maximum_horly_sludge_flow_final(cls, value) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_MAXIMUM_HORLY_SLUDGE_FLOW_FINAL, value)

    @classmethod
    def set_maximum_horly_sludge_flow_initial(cls, value) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_MAXIMUM_HORLY_SLUDGE_FLOW_INITIAL, value)

    @classmethod
    def set_average_strictly_domestic_flow_final(cls, value) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_AVERAGE_STRICTLY_DOMESTIC_FLOW_FINAL, value)

    @classmethod
    def set_average_strictly_domestic_flow_initial(cls, value) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_AVERAGE_STRICTLY_DOMESTIC_FLOW_INITIAL, value)

    @classmethod
    def set_infiltration_flow(cls, value) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_INFILTRATION_FLOW, value)


class CostsDAO(DAO):
    """Classe de acesso de dados para os dados necessários para o cálculo de custos"""
    SCOPE = "SanibidProjectCostsScope"
    KEY_SOIL_PERCENTAGE = "soil_percentage"
    KEY_ROCK_PERCENTAGE = "rock_percentage"
    KEY_CONCRETE_PERCENTAGE = "concrete_percentage"
    KEY_MASONRY_PERCENTAGE = "masonry_percentage"

    KEY_ENTRANCE_PIPE_DEPTH = "entrance_pipe_depth"
    KEY_ENTRANCE_PIPE_DIAMETER = "entrance_pipe_diameter"
    KEY_FINAL_POPULATION = "final_population"

    KEY_SERVICES = "services"

    @classmethod
    def get_soil_percentage(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_SOIL_PERCENTAGE)

    @classmethod
    def get_rock_percentage(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_ROCK_PERCENTAGE)

    @classmethod
    def get_concrete_percentage(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_CONCRETE_PERCENTAGE)

    @classmethod
    def get_masonry_percentage(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_MASONRY_PERCENTAGE)

    @classmethod
    def get_final_population(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_FINAL_POPULATION)

    @classmethod
    def get_entrance_pipe_depth(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_ENTRANCE_PIPE_DIAMETER)

    @classmethod
    def get_entrance_pipe_diameter(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_ENTRANCE_PIPE_DEPTH)

    @classmethod
    def get_services(cls) -> Tuple[List[float], bool]:
        # O QgsProject só salva strings, então temos que fazer essa conversão para
        # float em cada elemento.
        services, success = cls.proj.readListEntry(cls.SCOPE, cls.KEY_SERVICES, [])
        try:
            services_double = [float(x) for x in services]

            return services_double, success
        except ValueError:
            return [], False

    @classmethod
    def set_soil_percentage(cls, value: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_SOIL_PERCENTAGE, value)

    @classmethod
    def set_rock_percentage(cls, value: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_ROCK_PERCENTAGE, value)

    @classmethod
    def set_concrete_percentage(cls, value: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_CONCRETE_PERCENTAGE, value)

    @classmethod
    def set_masonry_percentage(cls, value: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_MASONRY_PERCENTAGE, value)

    @classmethod
    def set_final_population(cls, value: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_FINAL_POPULATION, value)

    @classmethod
    def set_entrance_pipe_depth(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_ENTRANCE_PIPE_DIAMETER, value)

    @classmethod
    def set_entrance_pipe_diameter(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_ENTRANCE_PIPE_DEPTH, value)

    @classmethod
    def set_services(cls, value: List[float]) -> bool:
        # O QgsProject só salva strings, então temos que garantir que só estamos inserindo números
        # em nossa lista
        if any(not isinstance(x, (float, int)) for x in value):
            return False

        services_str = [str(x) for x in value]
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_SERVICES, services_str)
