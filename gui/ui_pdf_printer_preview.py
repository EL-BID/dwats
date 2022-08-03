from PyQt5.QtCore import  Qt, QObject
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView, QWebPage
from qgis.core import QgsMessageLog


class CustomPage(QWebPage):
    def javaScriptConsoleMessage(self, msg, line, source):
        QgsMessageLog.logMessage(f"{source}, {line}, {msg}", "console js")


class ResolutionValues(QObject):
    def __init__(self, resolution, height):
        super().__init__()
        self.resolution = resolution
        self.height = height


class PrinterPreviewUI(QObject):
    def __init__(self):
        super().__init__()
        self.printer = QPrinter(QPrinter.HighResolution)
        self.printer.setOutputFormat(QPrinter.PdfFormat)
        self.printer.setPaperSize(QPrinter.A4)
        self.printer.setFullPage(True)

        # We use QWebView because it renders html more accurately and supports more tags.
        self.web = QWebView()
        self.web.setPage(CustomPage())
        self.__start_print_preview()

    def __start_print_preview(self):
        self.printer_preview = QPrintPreviewDialog(self.printer)
        self.printer_preview.paintRequested.connect(self.print_preview)

        # Adds minimize, maximize and close buttons in the dialog.
        self.printer_preview.setWindowFlags(
            Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowShadeButtonHint |
            Qt.WindowMaximizeButtonHint)
        self.printer_preview.setMinimumSize(1000, 1000)

    def print_pdf(self):
        # Starts the dialog maximized.
        self.__start_print_preview()
        self.printer_preview.showMaximized()
        self.printer_preview.exec_()

    def print_preview(self, printer):
        #QgsMessageLog.logMessage(f"Printing html... with html: \n{self.web.page().mainFrame().toHtml()}", "PrinterPreviewUILoad")
        self.web.print_(printer)

    def load_html(self, html):
        #QgsMessageLog.logMessage(f"Reloading html... \n{html}", "PrinterPreviewUI")
        self.web.setHtml(html)

