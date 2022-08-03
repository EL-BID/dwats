import math
from operator import itemgetter

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox
from qgis.core import QgsGeometry, QgsPointXY, QgsWkbTypes
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand

from .draw_shadow import DrawShadowRaster


# from .utils import tryfloat


def isLayerVisible(iface, layer):
    vl = iface.layerTreeView().layerTreeModel().rootGroup().findLayer(layer)
    return vl.itemVisibilityChecked()


def setLayerVisible(iface, layer, visible):
    vl = iface.layerTreeView().layerTreeModel().rootGroup().findLayer(layer)
    vl.setItemVisibilityChecked(visible)


class MoveDrawRaster(QgsMapToolEmitPoint):
    """docstring for MoveDrawRaster"""

    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rasterShadow = DrawShadowRaster(self.canvas)
        self.rubberBandDisplacement = QgsRubberBand(
            self.canvas, QgsWkbTypes.LineGeometry
        )
        self.rubberBandDisplacement.setColor(Qt.red)
        self.rubberBandDisplacement.setWidth(2)
        self.rubberBandExtent = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.rubberBandExtent.setColor(Qt.red)
        self.rubberBandExtent.setWidth(2)
        self.isLayerVisible = True
        self.reset()

    def setLayer(self, layer):
        self.layer = layer

    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBandDisplacement.reset(QgsWkbTypes.LineGeometry)
        self.rubberBandExtent.reset(QgsWkbTypes.LineGeometry)
        self.rasterShadow.reset()
        self.layer = None

    def canvasPressEvent(self, e):  # captura click sobre a camada
        self.startPoint = self.toMapCoordinates(e.pos())
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.originalCenter = self.layer.center
        # this tool do the displacement itself TODO update so it is done by
        # transformed coordinates + new center)
        self.originalCornerPoints = self.layer.transformedCornerCoordinates(
            *self.layer.transformParameters()
        )
        self.isLayerVisible = isLayerVisible(self.iface, self.layer)
        setLayerVisible(self.iface, self.layer, False)
        self.showDisplacement(self.startPoint, self.endPoint)
        self.layer.history.append({"action": "move", "center": self.layer.center})

    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = False
        self.rubberBandDisplacement.reset(QgsWkbTypes.LineGeometry)
        self.rubberBandExtent.reset(QgsWkbTypes.LineGeometry)
        self.rasterShadow.reset()
        x = self.originalCenter.x() + self.endPoint.x() - self.startPoint.x()
        y = self.originalCenter.y() + self.endPoint.y() - self.startPoint.y()
        self.layer.setCenter(QgsPointXY(x, y))
        setLayerVisible(self.iface, self.layer, self.isLayerVisible)
        self.layer.repaint()
        self.layer.commitTransformParameters()

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return

        self.endPoint = self.toMapCoordinates(e.pos())
        self.showDisplacement(self.startPoint, self.endPoint)

    def showDisplacement(self, startPoint, endPoint):
        self.rubberBandDisplacement.reset(QgsWkbTypes.LineGeometry)
        point1 = QgsPointXY(startPoint.x(), startPoint.y())
        point2 = QgsPointXY(endPoint.x(), endPoint.y())
        self.rubberBandDisplacement.addPoint(point1, False)
        self.rubberBandDisplacement.addPoint(point2, True)  # true to update canvas
        self.rubberBandDisplacement.show()

        self.rubberBandExtent.reset(QgsWkbTypes.LineGeometry)
        for point in self.originalCornerPoints:
            self._addDisplacementToPoint(self.rubberBandExtent, point, False)
        # for closing
        self._addDisplacementToPoint(
            self.rubberBandExtent, self.originalCornerPoints[0], True
        )
        self.rubberBandExtent.show()
        self.rasterShadow.reset(self.layer)
        self.rasterShadow.setDeltaDisplacement(
            self.endPoint.x() - self.startPoint.x(),
            self.endPoint.y() - self.startPoint.y(),
            True,
        )
        self.rasterShadow.show()

    def _addDisplacementToPoint(self, rubberBand, point, doUpdate):
        x = point.x() + self.endPoint.x() - self.startPoint.x()
        y = point.y() + self.endPoint.y() - self.startPoint.y()
        self.rubberBandExtent.addPoint(QgsPointXY(x, y), doUpdate)


class RotateRasterMapTool(QgsMapToolEmitPoint):
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        QgsMapToolEmitPoint.__init__(self, self.canvas)

        self.rasterShadow = DrawShadowRaster(self.canvas)

        self.rubberBandExtent = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.rubberBandExtent.setColor(Qt.red)
        self.rubberBandExtent.setWidth(1)

        # In case of rotation around pressed point (ctrl)
        # Use rubberBand for displaying an horizontal line.
        self.rubberBandDisplacement = QgsRubberBand(
            self.canvas, QgsWkbTypes.LineGeometry
        )
        self.rubberBandDisplacement.setColor(Qt.red)
        self.rubberBandDisplacement.setWidth(1)

        self.reset()

    def setLayer(self, layer):
        self.layer = layer

    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBandExtent.reset(QgsWkbTypes.LineGeometry)
        self.rubberBandDisplacement.reset(QgsWkbTypes.LineGeometry)
        self.rasterShadow.reset()
        self.layer = None

    def canvasPressEvent(self, e):
        self.startY = e.pos().y()
        self.endY = self.startY
        self.isEmittingPoint = True
        self.height = self.canvas.height()

        modifiers = QApplication.keyboardModifiers()
        self.isRotationAroundPoint = bool(modifiers & Qt.ControlModifier)
        self.startPoint = self.toMapCoordinates(e.pos())
        self.endPoint = self.startPoint

        self.isLayerVisible = isLayerVisible(self.iface, self.layer)
        setLayerVisible(self.iface, self.layer, False)

        rotation = self.computeRotation()
        self.showRotation(rotation)

        self.layer.history.append(
            {
                "action": "rotation",
                "rotation": self.layer.rotation,
                "center": self.layer.center,
            }
        )  # rotation set

    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = False

        self.rubberBandExtent.reset(QgsWkbTypes.LineGeometry)
        self.rubberBandDisplacement.reset(QgsWkbTypes.LineGeometry)
        self.rasterShadow.reset()

        rotation = self.computeRotation()
        if self.isRotationAroundPoint:
            self.layer.moveCenterFromPointRotate(self.startPoint, rotation, 1, 1)
        val = self.layer.rotation + rotation

        self.layer.setRotation(val)

        setLayerVisible(self.iface, self.layer, self.isLayerVisible)
        self.layer.repaint()

        self.layer.commitTransformParameters()

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return

        self.endY = e.pos().y()
        rotation = self.computeRotation()
        self.showRotation(rotation)

        self.endPoint = self.toMapCoordinates(e.pos())

    def computeRotation(self):
        if self.isRotationAroundPoint:
            dX = self.endPoint.x() - self.startPoint.x()
            dY = self.endPoint.y() - self.startPoint.y()
            return math.degrees(math.atan2(-dY, dX))
        else:
            dY = self.endY - self.startY
            return 90.0 * dY / self.height

    def showRotation(self, rotation):
        if self.isRotationAroundPoint:
            cornerPoints = self.layer.transformedCornerCoordinatesFromPoint(
                self.startPoint, rotation, 1, 1
            )

            self.rasterShadow.reset(self.layer)
            self.rasterShadow.setDeltaRotationFromPoint(rotation, self.startPoint, True)
            self.rasterShadow.show()

            self.rubberBandDisplacement.reset(QgsWkbTypes.LineGeometry)
            point0 = QgsPointXY(self.startPoint.x() + 10, self.startPoint.y())
            point1 = QgsPointXY(self.startPoint.x(), self.startPoint.y())
            point2 = QgsPointXY(self.endPoint.x(), self.endPoint.y())
            self.rubberBandDisplacement.addPoint(point0, False)
            self.rubberBandDisplacement.addPoint(point1, False)
            self.rubberBandDisplacement.addPoint(point2, True)  # true to update canvas
            self.rubberBandDisplacement.show()
        else:
            center, originalRotation, xScale, yScale = self.layer.transformParameters()
            newRotation = rotation + originalRotation
            cornerPoints = self.layer.transformedCornerCoordinates(
                center, newRotation, xScale, yScale
            )

            self.rasterShadow.reset(self.layer)
            self.rasterShadow.setDeltaRotation(rotation, True)
            self.rasterShadow.show()

        self.rubberBandExtent.reset(QgsWkbTypes.LineGeometry)
        for point in cornerPoints:
            self.rubberBandExtent.addPoint(point, False)
        # for closing
        self.rubberBandExtent.addPoint(cornerPoints[0], True)
        self.rubberBandExtent.show()
