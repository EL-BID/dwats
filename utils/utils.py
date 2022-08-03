from PyQt5.QtCore import QMessageLogger
from qgis.core import QgsMessageLog
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt, QLocale
from qgis.PyQt.QtGui import QIcon, QPixmap, QFont
from qgis.PyQt.QtWidgets import (QAction, QLabel, QDialog, QApplication,
                                 QFileDialog, QDialogButtonBox, QTableWidgetItem, QTableWidget, QTextBrowser,
                                 QMessageBox, QWidget, QAbstractItemView, QStyledItemDelegate, QScrollArea,
                                 QTabWidget, QFormLayout, QHBoxLayout, QRadioButton, QVBoxLayout, QFrame,
                                 QButtonGroup, QPushButton, QGridLayout, QStackedLayout, QSpinBox,
                                 QDoubleSpinBox, QGroupBox)
import os.path
import sys
import re


class Utils:
    loc = QLocale()
    file = __file__

    def formatNum2Dec(self, valor):
        if isinstance(valor, int):
            valor = float(valor)
        return self.loc.toString(valor, 'f', 2)

    def formatNum1Dec(self, valor):
        if isinstance(valor, int):
            valor = float(valor)
        return self.loc.toString(valor, 'f', 1)

    @staticmethod
    def formatInteger(valor):
        return str(round(valor))

    @staticmethod
    def tr(context, msg=None, disambiguation=None, n=-1):
        return QCoreApplication.translate(context, msg, disambiguation, n)

    def formatBoldText(self):
        myFont = QFont()
        myFont.setBold(True)
        return myFont

    def formatItalicText(self):
        myFont = QFont()
        myFont.setItalic(True)
        return myFont

    def formatBoldItalicText(self):
        myFont = QFont()
        myFont.setBold(True)
        myFont.setItalic(True)
        return myFont

    def showDialog(self, title, message, information):
        msgBox = QMessageBox()
        msgBox.setIcon(information)  # Question, Warning, Critical QMessageBox.Information
        msgBox.setText(message)
        msgBox.setWindowTitle(title)
        msgBox.buttonClicked.connect(self.on_click)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            msgBox.close()

    def on_click(self):
        pass

    def get_metadata_value(self, key):
        filename = os.path.dirname(os.path.realpath(self.file)).replace('utils', '') + '/metadata.txt'
        with open(filename, "r", encoding='utf-8') as f:
            for line in f:
                if line.startswith(key):
                    return line.split("=")[1].strip()
        return None
