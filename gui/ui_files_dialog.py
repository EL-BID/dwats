from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt, QLocale
from qgis.PyQt.QtGui import QIcon, QPixmap, QFont
from qgis.PyQt.QtWidgets import (QAction, QLabel,  QDialog, QApplication, 
    QFileDialog, QDialogButtonBox, QTableWidgetItem, QTableWidget, QTextBrowser, 
    QMessageBox, QWidget, QAbstractItemView, QStyledItemDelegate, QScrollArea, 
    QTabWidget, QFormLayout, QHBoxLayout, QRadioButton, QVBoxLayout, QFrame, 
    QButtonGroup, QPushButton, QGridLayout, QStackedLayout, QSpinBox,
    QDoubleSpinBox, QGroupBox, QLineEdit)
from PyQt5.QtGui import QTextDocument
from qgis.core import QgsProject
from ..core.march_calculation import MarchCalculation
from ..utils.utils import Utils
#from .resources import *
import json
import os.path
import sys
import re


class FileDialogUI():
    """docstring for FileDialogUI"""



    typeFile = None
    titleBid = None
    titleScreen = None
    le_localFile = QLineEdit()
    filenameSave = None
    filenameOpen = None
    dataDict = None
    #statusLoadLayoutSave = 0

    def __init__(self):
        self.screenSave = QDialog()
        self.screenOpen = QDialog()
        self.sreenDialog = QDialog()
        self.utils = Utils()
        self.gl_LayoutSave = QGridLayout()
        self.gl_LayoutOpen = QGridLayout()
        self.gl_LayoutEdit = QGridLayout()
        self.pb_openDirSave = QPushButton()
        self.pb_openDirFile = QPushButton()
        self.pb_save = QPushButton()
        self.pb_openFile = QPushButton()
        self.lb_msgLocalSave = QLabel()
        self.lb_msgLocalOpen = QLabel()
        self.lb_ProjectInProgress = QLabel()

        self.pb_saveEdit = QPushButton()
        self.pb_discardEdit = QPushButton()
        self.pb_openDirSave.clicked.connect(self.selectFolderSaveFile)
        self.pb_save.clicked.connect(self.saveFile)
        self.pb_openDirFile.clicked.connect(self.selectFolderOpenFile)
        pass

    def dialogSaveFile(self, typeFile, titleBid, titleScreen, dataDict):
        self.pb_openDirSave.setFixedSize(20, 25)
        self.pb_openDirSave.setText('...')
        self.pb_save.setFixedSize(100, 25)
        self.pb_save.setText(self.utils.tr('FilesDialog', 'Salvar'))
        self.le_localFile.clear()
        self.lb_msgLocalSave.setText(self.utils.tr('FilesDialog', 'Selecione local para salvar o arquivo:'))
        self.gl_LayoutSave.addWidget(self.lb_msgLocalSave, 0, 0, 1, 2)
        self.gl_LayoutSave.addWidget(self.le_localFile, 1, 0, 1, 2)
        self.gl_LayoutSave.addWidget(self.pb_openDirSave, 1, 2)
        self.gl_LayoutSave.addWidget(self.pb_save, 2, 1, 1, 2)
        self.typeFile = typeFile
        self.titleBid = titleBid
        self.titleScreen = titleScreen
        self.dataDict = dataDict
        self.screenSave.setLayout(self.gl_LayoutSave)
        self.screenSave.setGeometry(470, 280, 350, 110)
        self.screenSave.setWindowTitle(self.titleBid + self.titleScreen)
        self.screenSave.exec_()

    def selectFolderSaveFile(self):
        self.filenameSave = QFileDialog.getSaveFileName(self.screenSave, self.utils.tr('FilesDialog', 'Salvar como'), "", self.typeFile)[0]
        self.le_localFile.setText(self.filenameSave)

    def saveFile(self):
        with open(self.filenameSave, 'w') as json_file:
            json.dump(self.dataDict, json_file, indent = 4)
        icon = QMessageBox.Information
        self.utils.showDialog(self.titleBid, self.utils.tr('FilesDialog', 'Arquivo salvo com sucesso!'), icon)
        self.screenSave.close()

    def dialogOpenFile(self, typeFile, titleBid, titleScreen, insertData=True, saveFileJson=True):
        if insertData == True and saveFileJson == False:
            self.titleBid = titleBid
            self.titleScreen = titleScreen
            self.typeFile = typeFile
            self.pb_saveEdit.setFixedSize(100, 25)
            self.pb_saveEdit.setText('Salvar')
            self.pb_discardEdit.setFixedSize(100, 25)
            self.pb_discardEdit.setText(self.utils.tr('FilesDialog', 'Descartar'))
            self.lb_ProjectInProgress.setText(self.utils.tr('FilesDialog', 'Existe um projeto em andamento, deseja:'))
            self.gl_LayoutEdit.addWidget(self.lb_ProjectInProgress, 0, 0, 1, 2)
            self.gl_LayoutEdit.addWidget(self.pb_saveEdit, 1, 0)
            self.gl_LayoutEdit.addWidget(self.pb_discardEdit, 1, 1)
            self.sreenDialog.setLayout(self.gl_LayoutEdit)
            self.sreenDialog.setGeometry(470, 220, 350, 110)
            self.sreenDialog.setWindowTitle(self.titleBid + self.titleScreen)
            self.sreenDialog.exec_()
        
        self.pb_openDirFile.setFixedSize(20, 25)
        self.pb_openDirFile.setText('...')
        self.pb_openFile.setFixedSize(100, 25)
        self.pb_openFile.setText(self.utils.tr('FilesDialog', 'Abrir'))
        self.le_localFile.clear()
        self.lb_msgLocalOpen.setText(self.utils.tr('FilesDialog', 'Abrir arquivo:'))
        self.gl_LayoutOpen.addWidget(self.lb_msgLocalOpen, 0, 0, 1, 2)
        self.gl_LayoutOpen.addWidget(self.le_localFile, 1, 0, 1, 2)
        self.gl_LayoutOpen.addWidget(self.pb_openDirFile, 1, 2)
        self.gl_LayoutOpen.addWidget(self.pb_openFile, 2, 1, 1, 2)
        self.typeFile = typeFile
        self.titleBid = titleBid
        self.titleScreen = titleScreen
        self.screenOpen.setLayout(self.gl_LayoutOpen)
        self.screenOpen.setGeometry(470, 280, 350, 110)
        self.screenOpen.setWindowTitle(self.titleBid + self.titleScreen)
        self.screenOpen.exec_()

    def selectFolderOpenFile(self):
        self.filenameOpen = QFileDialog.getOpenFileName(self.screenOpen, self.utils.tr('FilesDialog', 'Abrir'), "", self.typeFile)[0]
        self.le_localFile.setText(self.filenameOpen)

    def openFile(self):
        with open(self.filenameOpen) as json_file:
            self.dataDict = json.load(json_file)
        self.screenOpen.close()
        return self.dataDict


