from PyQt5.QtCore import QCoreApplication
from qgis.PyQt.QtCore import Qt, QLocale
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import (QLabel, QWidget, QScrollArea,
                                 QTabWidget, QVBoxLayout, QFrame,
                                 QPushButton, QGridLayout, QSpinBox,
                                 QDoubleSpinBox, QGroupBox)
from qgis.core import QgsProject
from qgis.core import QgsMessageLog

from .dock_tabs.base.ui_dock_tab_base import DockTab
from .dock_tabs.ui_dock_tab_about import DockTabAbout
from .dock_tabs.ui_dock_tab_costs import DockTabCosts
from .dock_tabs.ui_dock_tab_rac import DockTabRac
from ..core.data.data_manager import ProjectDataManager
from .dock_tabs.ui_dock_tab_sedimentation_tank import DockTabSedimentationTank
from ..utils.utils import Utils
# from .resources import *
import os.path
from .dock_tabs.ui_dock_tab_home import DockTabHome
from .dock_tabs.ui_dock_tab_general import DockTabGeneral


class DockUI:
    scroll = QScrollArea()
    # tabWidget = QTabWidget()

    utils = Utils()

    def translate(self, msg, disambiguation=None, n=-1):
        return QCoreApplication.translate(DockUI.__name__, msg, disambiguation, n)

    def __init__(self, iface):
        self.tabWidget = QTabWidget()
        self.tab_home = DockTabHome(self, iface)
        self.tab_general = DockTabGeneral(self)
        self.tab_sedimentation_tank = DockTabSedimentationTank(self)
        self.tab_rac = DockTabRac(self)
        self.tab_costs = DockTabCosts(self)
        self.tab_about = DockTabAbout(self)

        self.tabWidget.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        """This method is called to reload a tab only when necessary, avoiding retrieving data unnecessarily"""
        widget: DockTab = self.tabWidget.widget(index)
        if not isinstance(widget, DockTab):
            return

        if widget.should_reload:
            QgsMessageLog.logMessage(f"Carregando aba {widget.__class__.__name__}", "on_tab_changed")
            widget.reload()
            widget.should_reload = False

    def loadDock(self):
        self.scroll.ensureVisible(50, 50)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.add_tabs()
        self.scroll.setWidget(self.tabWidget)

        self.tab_home.tab_start_ui()
        self.tab_general.tab_start_ui()
        self.tab_sedimentation_tank.tab_start_ui()
        self.tab_rac.tab_start_ui()
        self.tab_costs.tab_start_ui()
        self.tab_about.tab_start_ui()

    def add_tabs(self):
        before = self.tabWidget.currentWidget()
        self.tabWidget.clear()
        self.tabWidget.addTab(self.tab_home, self.translate('Início'))
        if ProjectDataManager.is_project_data_loaded():
            self.tabWidget.addTab(self.tab_general, self.translate('Dados gerais'))
            if ProjectDataManager.get_project_config().has_sedimentation_tank:
                self.tabWidget.addTab(self.tab_sedimentation_tank, self.translate('Tanque de sedimentação'))
            self.tabWidget.addTab(self.tab_rac, self.translate('Reator anaeróbio RAC'))
            self.tabWidget.addTab(self.tab_costs, self.translate('Custos'))
        self.tabWidget.addTab(self.tab_about, self.translate('Sobre'))
        self.tabWidget.setCurrentWidget(before)

    def reload(self):
        self.tab_home.should_reload = True
        self.tab_general.should_reload = True
        self.tab_sedimentation_tank.should_reload = True
        self.tab_rac.should_reload = True
        self.tab_costs.should_reload = True

    def hard_reload(self):
        self.add_tabs()
        self.tab_home.reload()
        self.tab_general.reload()
        self.tab_sedimentation_tank.reload()
        self.tab_rac.reload()
        self.tab_costs.reload()
