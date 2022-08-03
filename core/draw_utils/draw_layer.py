import math
import os
from qgis.PyQt.QtWidgets import QDoubleSpinBox
from PyQt5.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from PyQt5.QtCore import (
    pyqtSignal,
    qDebug,
    QFileInfo,
    QPointF,
    QRectF,
    QSettings,
    QSize,
    Qt
)
from PyQt5.QtGui import QColor, QImage, QImageReader, QPainter, QPen
from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsDataProvider,
    QgsMapLayerRenderer,
    QgsMessageLog,
    QgsPluginLayer,
    QgsPluginLayerType,
    QgsPointXY,
    QgsProject,
    QgsRasterLayer,
    QgsRectangle,
    QgsScaleCalculator,
    QgsMapUnitScale,
    QgsUnitTypes,
    QgsMapLayer
)

from ..translators.sanibid_translator import SanibidTranslator
from ...resources import *
from ..data.models import ProjectData, ProjectConfig
from ..data.data_manager import ProjectDataManager
from .draw_move_rotate_raster import MoveDrawRaster, RotateRasterMapTool
from ..march_calculation import MarchCalculation
from ..march_calculation_without_tank import MarchCalculationWithoutTank
from ...utils.utils import Utils


class SanibidDrawLayer(QgsPluginLayer):
    LAYER_TYPE = "SaniHUB_DWATS_Layer"
    transformParametersChanged = pyqtSignal(tuple)

    def __init__(self, plugin, screenExtent, title):
        QgsPluginLayer.__init__(
            self, SanibidDrawLayer.LAYER_TYPE, title
        )
        self.plugin = plugin
        self.iface = plugin.iface
        self.screenExtent = screenExtent
        self.history = []

        self.entrance_data = ProjectDataManager.get_project_data()
        self.has_sedimentation_tank = ProjectDataManager.get_project_config().has_sedimentation_tank
        self.should_import_rede_basica = ProjectDataManager.get_project_config().should_import_rede_basica
        self.calculation_area = ProjectDataManager.get_project_config().should_calculate_area

        if self.has_sedimentation_tank:
            self.marchCalculation = MarchCalculation(self.entrance_data, self.should_import_rede_basica)
        else:
            self.marchCalculation = MarchCalculationWithoutTank(self.entrance_data, self.should_import_rede_basica)

        self.filepath = self.select_img(self.entrance_data.getNumCompartRAC())

        # set custom properties
        self.setCustomProperty("title", title)
        self.setCustomProperty("filepath", self.filepath)

        self.setValid(True)

        self.setTransparency(LayerDefaultSettings.TRANSPARENCY)
        self.setBlendModeByName(LayerDefaultSettings.BLEND_MODE)

        self.center = QgsPointXY(0, 0)
        self.rotation = 0.0
        self.xScale = 1.0
        self.yScale = 1.0

        # develop here functions to read and make the needed assignments, remove this parameters from the constructor
        self.imgLength, self.imgWidth = self.measures_img_raster()

        self.rectLength = None
        self.rectWidth = None

        self.error = False
        self.initializing = False
        self.initialized = False
        self.initializeLayer(screenExtent)
        self._extent = None
        self.rectLength = None
        self.rectWidth = None

        self.provider = SanibidDrawLayerProvider(self)

    # def selectionChanged(self):
    #	pass

    def select_img(self, key):
        if self.has_sedimentation_tank:
            if self.calculation_area:
                return {
                    4: f':/plugins/tratamientos_descentralizados/images/img_layer_with_constructed_area/vista_1t-4reat_ap.png',
                    5: f':/plugins/tratamientos_descentralizados/images/img_layer_with_constructed_area/vista_1t-5reat_ap.png',
                    6: f':/plugins/tratamientos_descentralizados/images/img_layer_with_constructed_area/vista_1t-6reat_ap.png'
                }[key]
            else:
                return {
                    4: f':/plugins/tratamientos_descentralizados/images/img_layer_without_constructed_area/vista_1t-4reat.png',
                    5: f':/plugins/tratamientos_descentralizados/images/img_layer_without_constructed_area/vista_1t-5reat.png',
                    6: f':/plugins/tratamientos_descentralizados/images/img_layer_without_constructed_area/vista_1t-6reat.png'
                }[key]
        else:
            if self.calculation_area:
                return {
                    4: f':/plugins/tratamientos_descentralizados/images/img_layer_with_constructed_area/vista_st-4reat_ap.png',
                    5: f':/plugins/tratamientos_descentralizados/images/img_layer_with_constructed_area/vista_st-5reat_ap.png',
                    6: f':/plugins/tratamientos_descentralizados/images/img_layer_with_constructed_area/vista_st-6reat_ap.png'
                }[key]
            else:
                return {
                    4: f':/plugins/tratamientos_descentralizados/images/img_layer_without_constructed_area/vista_st-4reat.png',
                    5: f':/plugins/tratamientos_descentralizados/images/img_layer_without_constructed_area/vista_st-5reat.png',
                    6: f':/plugins/tratamientos_descentralizados/images/img_layer_without_constructed_area/vista_st-6reat.png'
                }[key]

    def measures_img_raster(self):
        if self.calculation_area:
            if self.has_sedimentation_tank:
                imgLength = ((self.marchCalculation.getLengthTankSedimentation() + (
                        (self.marchCalculation.getLengthCompartmentRAC()
                         + self.entrance_data.getWidthShafts()) * self.entrance_data.getNumCompartRAC()) + (
                                      self.entrance_data.getNumCompartRAC() + 1) * 0.2) + 2.0)
                imgWidth = ((
                                    self.marchCalculation.getWidthMinCompartmentRAC() + 4.0) if self.marchCalculation.getWidthMinCompartmentRAC()
                                                                                                > self.entrance_data.getWidthTank() else self.entrance_data.getWidthTank() + 4.0)
            else:
                imgLength = (((self.marchCalculation.getLengthCompartmentRAC() + self.entrance_data.getWidthShafts())
                              * self.entrance_data.getNumCompartRAC()) + (
                                     0.2 * (self.entrance_data.getNumCompartRAC() + 1)) + 2.0)
                imgWidth = (self.marchCalculation.getWidthMinCompartmentRAC() + 4.0)
        else:
            if self.has_sedimentation_tank:
                imgLength = (self.marchCalculation.getLengthTankSedimentation() + (
                        (self.marchCalculation.getLengthCompartmentRAC()
                         + self.entrance_data.getWidthShafts()) * self.entrance_data.getNumCompartRAC()) + (
                                     self.entrance_data.getNumCompartRAC() + 1) * 0.2)
                imgWidth = (
                    self.marchCalculation.getWidthMinCompartmentRAC() if self.marchCalculation.getWidthMinCompartmentRAC()
                                                                         > self.entrance_data.getWidthTank() else self.entrance_data.getWidthTank())
            else:
                imgLength = (((self.marchCalculation.getLengthCompartmentRAC() + self.entrance_data.getWidthShafts())
                              * self.entrance_data.getNumCompartRAC()) + (
                                     0.2 * (self.entrance_data.getNumCompartRAC() + 1)))
                imgWidth = self.marchCalculation.getWidthMinCompartmentRAC()
        return imgLength, imgWidth

    def initializeLayer(self, screenExtent=None):
        if self.error or self.initialized or self.initializing:
            return
        self.setCustomProperty("filepath", self.filepath)
        self.initializing = True
        QgsProject.instance().setDirty(True)
        reader = QImageReader(self.filepath)
        self.image = reader.read()
        self.initializing = False
        self.initialized = True
        self.setupCrs()
        self.setCenter(screenExtent.center())
        self.setRotation(0.0)
        self.commitTransformParameters()

    def commitTransformParameters(self):
        QgsProject.instance().setDirty(True)
        self._extent = None
        self.setCustomProperty("xScale", self.xScale)
        self.setCustomProperty("yScale", self.yScale)
        self.setCustomProperty("rotation", self.rotation)
        self.setCustomProperty("xCenter", self.center.x())
        self.setCustomProperty("yCenter", self.center.y())
        self.transformParametersChanged.emit(
            (self.xScale, self.yScale, self.rotation, self.center)
        )

    def setTransparency(self, transparency):
        self.transparency = transparency
        self.setCustomProperty("transparency", transparency)

    def setBlendModeByName(self, modeName):
        self.blendModeName = modeName
        blendMode = getattr(QPainter, "CompositionMode_" + modeName, 0)
        self.setBlendMode(blendMode)
        self.setCustomProperty("blendMode", modeName)

    def setCenter(self, center):
        self.center = center

    def setRotation(self, rotation):
        rotation = round(rotation, 3)
        if rotation < -180:
            rotation += 360
        if rotation > 180:
            rotation -= 360
        self.rotation = rotation

    def resetScale(self, sw, sh):
        self.setScale(self.imgWidth / sw, self.imgLength / sh)

    def setScale(self, xScale, yScale):
        self.xScale = xScale
        self.yScale = yScale

    def setupCrs(self):
        mapCrs = self.iface.mapCanvas().mapSettings().destinationCrs()
        self.setCrs(mapCrs)
        self.setupCrsEvents()

    def setupCrsEvents(self):
        layerId = self.id()

        def removeCrsChangeHandler(layerIds):
            if layerId in layerIds:
                try:
                    self.iface.mapCanvas().destinationCrsChanged.disconnect(
                        self.resetTransformParametersToNewCrs
                    )
                except Exception:
                    pass
                try:
                    QgsProject.instance().disconnect(removeCrsChangeHandler)
                except Exception:
                    pass

        self.iface.mapCanvas().destinationCrsChanged.connect(
            self.resetTransformParametersToNewCrs
        )  # emits signal which map CRS has been changed
        QgsProject.instance().layersRemoved.connect(removeCrsChangeHandler)

    def resetTransformParametersToNewCrs(self):
        """
		Attempts to keep the layer on the same region of the map when
		the map CRS is changed
		"""
        oldCrs = self.crs()
        newCrs = self.iface.mapCanvas().mapSettings().destinationCrs()
        self.reprojectTransformParameters(oldCrs, newCrs)
        self.commitTransformParameters()

    def reprojectTransformParameters(self, oldCrs, newCrs):
        transform = QgsCoordinateTransform(oldCrs, newCrs, QgsProject.instance())
        newCenter = transform.transform(self.center)
        newExtent = transform.transform(self.extent())

        # transform the parameters except rotation
        # TODO rotation could be better handled (maybe check rotation between
        # old and new extent)
        # but not really worth the effort ?
        self.setCrs(newCrs)
        self.setCenter(newCenter)

    # self.resetScale(newExtent.width(), newExtent.height())

    def createMapRenderer(self, rendererContext):
        return SanibidDrawLayerRenderer(self, rendererContext)

    def extent(self):
        self.initializeLayer()
        if not self.initialized:
            qDebug("Not Initialized")
            return QgsRectangle(0, 0, 1, 1)

        if self._extent:
            return self._extent

        topLeft, topRight, bottomRight, bottomLeft = self.cornerCoordinates()

        left = min(topLeft.x(), topRight.x(), bottomRight.x(), bottomLeft.x())
        right = max(topLeft.x(), topRight.x(), bottomRight.x(), bottomLeft.x())
        top = max(topLeft.y(), topRight.y(), bottomRight.y(), bottomLeft.y())
        bottom = min(topLeft.y(), topRight.y(), bottomRight.y(), bottomLeft.y())

        # recenter + create rectangle
        self._extent = QgsRectangle(left, bottom, right, top)
        return self._extent

    def cornerCoordinates(self):
        return self.transformedCornerCoordinates(
            self.center, self.rotation, self.xScale, self.yScale
        )

    def transformedCornerCoordinates(self, center, rotation, xScale, yScale):
        # scale
        topLeft = QgsPointXY(
            -1 * ((self.imgLength * xScale) / 2), ((self.imgWidth * yScale) / 2)
        )
        topRight = QgsPointXY(
            ((self.imgLength * xScale) / 2), ((self.imgWidth * yScale) / 2)
        )
        bottomLeft = QgsPointXY(
            -1 * ((self.imgLength * xScale) / 2), -1 * ((self.imgWidth * yScale) / 2)
        )
        bottomRight = QgsPointXY(
            ((self.imgLength * xScale) / 2), -1 * ((self.imgWidth * yScale) / 2)
        )
        # rotate
        # minus sign because rotation is CW in this class and Qt)
        rotationRad = -rotation * math.pi / 180
        cosRot = math.cos(rotationRad)
        sinRot = math.sin(rotationRad)

        topLeft = self._rotate(topLeft, cosRot, sinRot)
        topRight = self._rotate(topRight, cosRot, sinRot)
        bottomRight = self._rotate(bottomRight, cosRot, sinRot)
        bottomLeft = self._rotate(bottomLeft, cosRot, sinRot)

        topLeft.set(topLeft.x() + center.x(), topLeft.y() + center.y())
        topRight.set(topRight.x() + center.x(), topRight.y() + center.y())
        bottomRight.set(bottomRight.x() + center.x(), bottomRight.y() + center.y())
        bottomLeft.set(bottomLeft.x() + center.x(), bottomLeft.y() + center.y())

        return (topLeft, topRight, bottomRight, bottomLeft)

    def _rotate(self, point, cosRot, sinRot):
        return QgsPointXY(
            point.x() * cosRot - point.y() * sinRot,
            point.x() * sinRot + point.y() * cosRot,
        )

    def draw(self, renderContext):
        if renderContext.extent().isEmpty():
            qDebug("Drawing is skipped because map extent is empty.")
            return True

        self.initializeLayer()
        if not self.initialized:
            qDebug("Drawing is skipped because nothing to draw.")
            return True
        painter = renderContext.painter()
        painter.save()
        self.drawRaster(renderContext)
        painter.restore()
        return True

    def drawRaster(self, renderContext):
        painter = renderContext.painter()
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.map2pixel = renderContext.mapToPixel()

        c = QgsMapUnitScale()

        self.rectLength = self.imgLength / c.computeMapUnitsPerPixel(renderContext)
        self.rectWidth = self.imgWidth / c.computeMapUnitsPerPixel(renderContext)

        self.rect = QRectF(
            QPointF(-self.rectLength / 2.0, -self.rectWidth / 2.0),
            QPointF(self.rectLength / 2.0, self.rectWidth / 2.0),
        )
        mapCenter = self.map2pixel.transform(self.center)

        # draw the image on the map canvas
        painter.translate(QPointF(mapCenter.x(), mapCenter.y()))
        painter.rotate(self.rotation)
        painter.drawImage(self.rect, self.image)
        painter.setOpacity(1.0)
        painter.setBrush(Qt.NoBrush)
        pen = QPen()
        pen.setColor(QColor(0, 0, 0))
        pen.setWidth(0)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawRect(self.rect)

    def get_rect(self):
        return self.rect

    def rect_measures(self):
        return (self.rectLength, self.rectWidth)

    def readXml(self, node, context):
        self.readCustomProperties(node)
        self.title = self.customProperty("title", "")
        self.filepath = self.customProperty("filepath", "")
        self.xScale = float(self.customProperty("xScale", 1.0))
        self.yScale = float(self.customProperty("yScale", 1.0))
        self.rotation = float(self.customProperty("rotation", 0.0))
        xCenter = float(self.customProperty("xCenter", 0.0))
        yCenter = float(self.customProperty("yCenter", 0.0))
        self.center = QgsPointXY(xCenter, yCenter)
        self.setTransparency(
            int(self.customProperty("transparency", LayerDefaultSettings.TRANSPARENCY))
        )
        self.setBlendModeByName(
            self.customProperty("blendMode", LayerDefaultSettings.BLEND_MODE)
        )
        return True

    def writeXml(self, node, doc, context):
        element = node.toElement()
        self.writeCustomProperties(node, doc)
        element.setAttribute("type", "plugin")
        element.setAttribute("name", SanibidDrawLayer.LAYER_TYPE)
        return True

    def repaint(self):
        self.repaintRequested.emit()

    def transformParameters(self):
        return (self.center, self.rotation, self.xScale, self.yScale)

    def dataProvider(self):
        # issue with DBManager if the dataProvider of the QgsLayerPlugin
        # returns None
        return self.provider

    def transformedCornerCoordinatesFromPoint(self, startPoint, rotation, xScale, yScale):
        dX = (self.center.x() - startPoint.x()) * xScale
        dY = (self.center.y() - startPoint.y()) * yScale
        # Half width and half height in the current transformation
        hW = (self.rectLength / 2.0) * self.xScale * xScale
        hH = (self.rectWidth / 2.0) * self.yScale * yScale
        # Actual rectangle coordinates :
        pt1 = QgsPointXY(-hW, hH)
        pt2 = QgsPointXY(hW, hH)
        pt3 = QgsPointXY(hW, -hH)
        pt4 = QgsPointXY(-hW, -hH)
        # Actual rotation from the center
        # minus sign because rotation is CW in this class and Qt)
        rotationRad = -self.rotation * math.pi / 180
        cosRot = math.cos(rotationRad)
        sinRot = math.sin(rotationRad)
        pt1 = self._rotate(pt1, cosRot, sinRot)
        pt2 = self._rotate(pt2, cosRot, sinRot)
        pt3 = self._rotate(pt3, cosRot, sinRot)
        pt4 = self._rotate(pt4, cosRot, sinRot)
        # Second transformation
        # displacement of the origin
        pt1 = QgsPointXY(pt1.x() + dX, pt1.y() + dY)
        pt2 = QgsPointXY(pt2.x() + dX, pt2.y() + dY)
        pt3 = QgsPointXY(pt3.x() + dX, pt3.y() + dY)
        pt4 = QgsPointXY(pt4.x() + dX, pt4.y() + dY)
        # Rotation
        # minus sign because rotation is CW in this class and Qt)
        rotationRad = -rotation * math.pi / 180
        cosRot = math.cos(rotationRad)
        sinRot = math.sin(rotationRad)
        pt1 = self._rotate(pt1, cosRot, sinRot)
        pt2 = self._rotate(pt2, cosRot, sinRot)
        pt3 = self._rotate(pt3, cosRot, sinRot)
        pt4 = self._rotate(pt4, cosRot, sinRot)
        # translate to startPoint
        pt1 = QgsPointXY(pt1.x() + startPoint.x(), pt1.y() + startPoint.y())
        pt2 = QgsPointXY(pt2.x() + startPoint.x(), pt2.y() + startPoint.y())
        pt3 = QgsPointXY(pt3.x() + startPoint.x(), pt3.y() + startPoint.y())
        pt4 = QgsPointXY(pt4.x() + startPoint.x(), pt4.y() + startPoint.y())
        return (pt1, pt2, pt3, pt4)

    def dump(self, detail=False, bbox=None):
        pass

    def setTransformContext(self, transformContext):
        pass


class SanibidDrawLayerProvider(QgsDataProvider):
    def __init__(self, layer):
        QgsDataProvider.__init__(self, "dummyURI")

    def name(self):
        # doesn't matter
        return "SanibidDrawLayerProvider"


class LayerDefaultSettings:
    TRANSPARENCY = 30
    BLEND_MODE = "SourceOver"


class SanibidDrawLayerType(QgsPluginLayerType):
    def __init__(self, plugin, screenExtent):
        QgsPluginLayerType.__init__(self, SanibidDrawLayer.LAYER_TYPE)
        self.plugin = plugin
        self.screenExtent = screenExtent

    def createLayer(self):
        return SanibidDrawLayer(self.plugin, self.screenExtent, None)


class SanibidDrawLayerRenderer(QgsMapLayerRenderer):
    """
	Custom renderer: in QGIS3 no implementation is provided for
	QgsPluginLayers
	"""

    def __init__(self, layer, rendererContext):
        QgsMapLayerRenderer.__init__(self, layer.id())
        self.layer = layer
        self.rendererContext = rendererContext

    def render(self):
        # same implementation as for QGIS2
        return self.layer.draw(self.rendererContext)
