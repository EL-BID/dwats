from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt, QLocale
from qgis.PyQt.QtGui import QIcon, QPixmap, QFont
from qgis.PyQt.QtWidgets import (QAction, QLabel,  QDialog, QApplication, 
    QFileDialog, QDialogButtonBox, QTableWidgetItem, QTableWidget, QTextBrowser, 
    QMessageBox, QWidget, QAbstractItemView, QStyledItemDelegate, QScrollArea, 
    QTabWidget, QFormLayout, QHBoxLayout, QRadioButton, QVBoxLayout, QFrame, 
    QButtonGroup, QPushButton, QGridLayout, QStackedLayout, QSpinBox,
    QDoubleSpinBox, QGroupBox)
from ..utils.utils import Utils
from ..gui.ui_files_dialog import FileDialogUI
import os.path
import sys
import re


class NewProjectUI():

	screen = QDialog()
	utils = Utils()
	gl_Layout = QGridLayout()
	deleteAll = False
	pb_save = QPushButton()
	pb_discard = QPushButton()
	save = FileDialogUI()
	titleBid = ''
	titleScreen = ''
	dataDict = False
	typeFile = False

	def dialogNewProject(self, insertData, saveFileJson, titleBid, titleScreen='', dataDict=False, typeFile=False):
		if insertData == False and saveFileJson == False:
			icon = QMessageBox.Information
			self.utils.showDialog(titleBid, self.utils.tr('NewProject', 'Novo projeto disponível, preencher dados ao lado para iniciar!'), icon)
			#self.deleteAll = False
			#return self.deleteAll
		elif insertData == True and saveFileJson == False:
			self.titleBid = titleBid
			self.titleScreen = titleScreen
			self.dataDict= dataDict
			self.typeFile = typeFile
			self.pb_save.setFixedSize(100, 25)
			self.pb_save.setText('Salvar')
			self.pb_discard.setFixedSize(100, 25)
			self.pb_discard.setText(self.utils.tr('NewProject', 'Descartar'))
			self.gl_Layout.addWidget(QLabel(self.utils.tr('NewProject', 'Existe um projeto em andamento, deseja:')), 0, 0, 1, 2)
			self.gl_Layout.addWidget(self.pb_save, 1, 0)
			self.gl_Layout.addWidget(self.pb_discard, 1, 1)
			self.screen.setLayout(self.gl_Layout)
			self.screen.setGeometry(470, 220, 350, 110)
			self.screen.setWindowTitle(self.titleBid + self.titleScreen)
			self.screen.exec_()
			#perguntar se quer salvar
			#pass
		#elif insertData == True and saveFileJson == True:
		#	self.deleteAll = True
		#	return self.deleteAll
	
		