from PyQt5.QtWidgets import QVBoxLayout, QLabel, QGridLayout
from matplotlib.ft2font import BOLD
from qgis.PyQt.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QLocale

from .base.ui_dock_tab_base import DockTab
from ...utils.utils import Utils


class DockTabAbout(DockTab):
    def __init__(self, dock):
        super().__init__(dock)

    def tab_start_ui(self):
        version = self.utils.get_metadata_value('version')
        gridLayoutAbout = QGridLayout()
        lb_msg = QLabel(self.tr('SaniHUB DWATS'))
        lb_msg.setFont(QFont('Arial', 15, QFont.Bold))
        #lb_msg.setWordWrap(True)
        gridLayoutAbout.addWidget(lb_msg, 0, 3, Qt.AlignHCenter)
        lb_img_bid = QLabel()
        pix_bid = QPixmap(':/plugins/tratamientos_descentralizados/icons/BID.png')
        lb_img_bid.setPixmap(pix_bid.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        gridLayoutAbout.addWidget(lb_img_bid, 0, 0)
        lb_img_ufba = QLabel()
        pix_ufba = QPixmap(':/plugins/tratamientos_descentralizados/icons/UFBA.png')
        lb_img_ufba.setPixmap(pix_ufba.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        gridLayoutAbout.addWidget(lb_img_ufba, 0, 2)
        lb_img_sanihub = QLabel()
        pix_sanihub = QPixmap(':/plugins/tratamientos_descentralizados/icons/saniHub.png')
        lb_img_sanihub.setPixmap(pix_sanihub.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        gridLayoutAbout.addWidget(lb_img_sanihub, 0, 1)
        
        lb_notice = QLabel(self.tr('Software livre para projetos simplificados e descentralizados de tratamento de águas residuárias.'))
        lb_notice.setWordWrap(True)
        lb_notice.setAlignment(Qt.AlignHCenter)
        lb_notice.setFont(self.utils.formatItalicText())
        gridLayoutAbout.addWidget(lb_notice, 1, 0, 1, 0, Qt.AlignCenter)
        
        lb_version = QLabel(self.tr('SaniHUB DWATS - Versão') + ' ' + version)
        lb_version.setWordWrap(True)
        gridLayoutAbout.addWidget(lb_version, 2, 0, 1, 0)

        loc = QLocale()
        lb_local = QLabel(self.tr('Local: ' + loc.nativeCountryName() + 
                            ' - Idioma: ' + loc.name()))
        gridLayoutAbout.addWidget(lb_local, 3, 0, 1, 0)
        lb_quick_guide = QLabel()
        urlLink = "<a href=\'https://www.iadb.org/'> www.iadb.org </a>"
        lb_quick_guide.setText(self.tr('Guia Rápido disponivel em ') + urlLink)
        lb_quick_guide.setOpenExternalLinks(True)
        #gridLayoutAbout.addWidget(lb_quick_guide, 4, 0, 1, 0)

        lb_financed = QLabel()
        lb_financed.setText(self.tr('O software foi financiado por: \nA Facilidade de Investimentos para a ' 
                            'América latina (LAIF), com recursos da Comissão Europeia por meio de um programa'
                            ' da Agência Espanhola de Cooperação Internacional para o Desenvolvimento (AECID)'
                            ' e do Banco Interamericano de Desenvolvimento (BID). \nO AquaFund, um fundo de '
                            'múltiplos doadores do Banco Interamericano de Desenvolvimento para água e saneamento'
                            ' que é apoiado: pela Agência Espanhola de Cooperação Internacional para o '
                            'Desenvolvimento (AECID); pelo Ministério da Fazenda da Áustria; pela Cooperação '
                            'Suíça, através da Secretaria de Estado da Economia (SECO) e da Agência Suíça para'
                            ' a Cooperação e Desenvolvimento (COSUDE), e pela Fundação PepsiCo.'))
        lb_financed.setWordWrap(True)
        lb_financed.setFont(QFont('Arial', 8))
        lb_financed.setAlignment(Qt.AlignJustify)
        lb_financed.setMinimumHeight(220)
        gridLayoutAbout.addWidget(lb_financed, 5, 0, 1, 0)
        
        lb_bid = QLabel()
        lb_bid.setText(self.tr('Banco Interamericano de Desenvolvimento - BID'))
        lb_bid.setFont(self.utils.formatBoldText())
        lb_bid.setAlignment(Qt.AlignHCenter)
        gridLayoutAbout.addWidget(lb_bid, 6, 0, 1, 0)
        
        lb_team_bid = QLabel()
        lb_team_bid.setText('Sérgio Pérez Monforte\nAmália Palácios\nMaria Rodriguez Vera')
        lb_team_bid.setFont(QFont('Arial', 8))
        lb_team_bid.setAlignment(Qt.AlignHCenter)
        gridLayoutAbout.addWidget(lb_team_bid, 7, 0, 1, 0)

        lb_ufba = QLabel()
        lb_ufba.setText(self.tr('Universidade Federal da Bahia – UFBA'))
        lb_ufba.setFont(self.utils.formatBoldText())
        lb_ufba.setAlignment(Qt.AlignHCenter)
        gridLayoutAbout.addWidget(lb_ufba, 8, 0, 1, 0)

        lb_team_ufba = QLabel()
        lb_team_ufba.setText('João Carlos Salles Pires da Silva - ' + self.tr('Reitor') + 
                            '\nVivien Luciane Viaro – ' + self.tr('Coordenadora') + 
                            '\nLuciano Matos Queiroz\nManoel Gomes de Mendonça Neto\nRenato Lima Novais'
                            '\nRicardo Eugênio Porto Vieira\nGabriel da Silva Rangel\nDagoberto Medeiros'
                            '\nFredson Menezes Sumi\nCaio Costa Sá da Nova')
        lb_team_ufba.setFont(QFont('Arial', 8))
        lb_team_ufba.setAlignment(Qt.AlignHCenter)
        gridLayoutAbout.addWidget(lb_team_ufba, 9, 0, 1, 0)  

        lb_consultants = QLabel()                          
        lb_consultants.setText(self.tr('Consultores Ad hoc'))
        lb_consultants.setFont(self.utils.formatBoldText())
        lb_consultants.setAlignment(Qt.AlignHCenter)
        gridLayoutAbout.addWidget(lb_consultants, 10, 0, 1, 0)

        lb_team_consultants = QLabel()
        lb_team_consultants.setText('Ivan Paiva\nFlávia Rebouças\nLeonardo Nazareth'
                                    '\nMarta Fernández Gonzalez\nMartin Dell’oro\nFederico Sanches')
        lb_team_consultants.setFont(QFont('Arial', 8))
        lb_team_consultants.setAlignment(Qt.AlignHCenter)
        gridLayoutAbout.addWidget(lb_team_consultants, 11, 0, 1, 0)

        lb_licence = QLabel()
        lb_licence.setText(self.tr('O SaniHUB DWATS é licenciado sob a General Public Licence -  GNU GPLv3.'))
        lb_licence.setWordWrap(True)
        lb_licence.setFont(QFont('Arial', 8))
        lb_licence.setAlignment(Qt.AlignHCenter)
        gridLayoutAbout.addWidget(lb_licence, 12, 0, 1, 0)
        #gridLayoutAbout.setVerticalSpacing(50)

        #gridLayoutAbout.addStretch()
        self.setLayout(gridLayoutAbout)
