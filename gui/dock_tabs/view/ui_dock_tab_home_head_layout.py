from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton

from ....core.data.models import ProjectInfo


class HeadFormLayout(QGridLayout):
    """Layout class for entering Project header data"""
    def __init__(self):
        super().__init__()

        # Declarando variáveis
        self.lb_client = QLabel()
        self.le_client = QLineEdit()

        self.lb_projectName = QLabel()
        self.le_projectName = QLineEdit()

        self.lb_local = QLabel()
        self.le_local = QLineEdit()

        self.lb_state = QLabel()
        self.le_state = QLineEdit()

        self.lb_country = QLabel()
        self.le_country = QLineEdit()

        self.lb_designer = QLabel()
        self.le_designer = QLineEdit()

        #self.lb_scale = QLabel()
        #self.le_scale = QLineEdit()

        self.lb_version = QLabel()
        self.le_version = QLineEdit()

        self.pb_saveHeadProject = QPushButton()

        # Defining widget relationships and positions in the layout
        # self.screenHead.setWindowTitle(self.tr('Editar cabeçalho do projeto'))
        self.lb_client.setText(self.tr('Cliente:'))
        self.addWidget(self.lb_client, 0, 0)
        self.addWidget(self.le_client, 0, 1, 1, 3)
        self.lb_projectName.setText(self.tr('Nome do Projeto:'))
        self.addWidget(self.lb_projectName, 1, 0)  # criar var
        self.addWidget(self.le_projectName, 1, 1, 1, 3)
        self.lb_local.setText(self.tr('Local:'))
        self.addWidget(self.lb_local, 2, 0)
        self.addWidget(self.le_local, 2, 1, 1, 3)
        self.lb_state.setText(self.tr('Estado:'))
        self.addWidget(self.lb_state, 3, 0)
        self.addWidget(self.le_state, 3, 1)
        self.lb_country.setText(self.tr('País:'))
        self.addWidget(self.lb_country, 3, 2)
        self.addWidget(self.le_country, 3, 3)
        self.lb_designer.setText(self.tr('Projetista:'))
        self.addWidget(self.lb_designer, 4, 0)
        self.addWidget(self.le_designer, 4, 1, 1, 3)
        #self.lb_scale.setText(self.tr('Escala:'))
        #self.addWidget(self.lb_scale, 5, 0)
        #self.addWidget(self.le_scale, 5, 1)
        self.lb_version.setText(self.tr('Versão:'))
        self.addWidget(self.lb_version, 5, 0)
        self.addWidget(self.le_version, 5, 1)

        self.pb_saveHeadProject.setText(self.tr('Salvar'))
        self.pb_saveHeadProject.setFixedSize(100, 25)
        self.addWidget(self.pb_saveHeadProject, 6, 3)
        self.rowStretch(0)

    def set_on_save_pressed_event(self, func):
        """Adds events fired when the save button is pressed."""
        self.pb_saveHeadProject.clicked.connect(func)
        pass

    def load_project_info(self, project_info: ProjectInfo):
        """Load values from the project header into text editing variables."""
        self.le_client.setText(project_info.client)
        self.le_projectName.setText(project_info.project_name)
        self.le_local.setText(project_info.local)
        self.le_state.setText(project_info.state)
        self.le_country.setText(project_info.country)
        self.le_designer.setText(project_info.designer)
        #self.le_scale.setText(project_info.scale)
        self.le_version.setText(project_info.version)
