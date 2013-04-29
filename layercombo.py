from PyQt4.QtCore import QVariant
from qgis.core import QGis, QgsMapLayerRegistry, QgsMapLayer

########################################################################
# creates a layer combo:
#
#     widget:       the qcombobox widget
#
#     initLayer:    the initally selected layer ID or a lambda function
#                   returning the ID (it could look for a value in settings)
#
#     options:      a dictionnary of options: {"opt1": val1, "opt2": val2, etc.}
#                   possible options are listed here under (default values are first listed)
#
#     groupLayers:  False/True
#                   group layers in combobox according to the legend interface groups
#
# (1) hasGeometry:  None/True/False
#                   restrain the possible selection of layers to layers having or not geometry
#                   None = all
#
# (1) geomType:     None/QGis.Point/QGis.Line/QGis.Polygon
#                   restrain the possible selection of layers to a certain type of geometry
#                   geomType must be a GeometryType
#                   http://qgis.org/api/classQGis.html#a09947eb19394302eeeed44d3e81dd74b
#                   None = all
#
#     dataProvider: None/postgres/etc.
#                   filter the layers based on the data provider name
#                   None = all
#
#
#    finishInit:    True/False
#                   if False, the combo box will not be initiated (filled with layers)
#                   Setting this option to False is useful if you want the manager to be returned before it is filled
#                   (in case you use the manager methods in a method called by a signal from the combo)
#
# (1): used for vector layer combos
#


class LayerCombo():
    def __init__(self, legendInterface, widget, initLayer="", layerType=None, options={}):
        self.legendInterface = legendInterface
        self.widget = widget
        if hasattr(initLayer, '__call__'):
            self.initLayer = initLayer()
        else:
            self.initLayer = initLayer
        self.layerType = layerType
        # get options
        self.groupLayers = options.get("groupLayers", False)
        self.hasGeometry = options.get("hasGeometry", None)
        self.geomType = options.get("geomType", None)
        self.dataProvider = options.get("dataProvider", None)
        if self.hasGeometry not in (None, True, False):
            raise NameError("Invalid value for option hasGeometry")
        if self.geomType not in (None, QGis.Point, QGis.Line, QGis.Polygon):
            raise NameError("Invalid value for option geomType")
        if options.get("finishInit", True):
            self.finishInit()

    def finishInit(self):
        # connect signal for layers and populate combobox
        QgsMapLayerRegistry.instance().layersAdded.connect(self.canvasLayersChanged)
        if self.groupLayers:
            self.legendInterface.groupRelationsChanged.connect(self.canvasLayersChanged)
        self.canvasLayersChanged()

    def getLayer(self):
        i = self.widget.currentIndex()
        if i == 0:
            return None
        layerId = self.widget.itemData(i).toString()
        return QgsMapLayerRegistry.instance().mapLayer(layerId)

    def canvasLayersChanged(self, layerList=[]):
        self.widget.clear()
        self.widget.addItem("")
        if not self.groupLayers:
            for layer in self.legendInterface.layers():
                if not self.__checkLayer(layer):
                    continue
                self.widget.addItem(layer.name(), layer.id())
                if layer.id() == self.initLayer:
                    self.widget.setCurrentIndex(self.widget.count()-1)
        else:
            for layerGroup in self.legendInterface.groupLayerRelationship():
                groupName = layerGroup[0]
                foundParent = False
                insertPosition = self.widget.count()
                indent = 0
                for i in range(self.widget.count()):
                    lineData = self.widget.itemData(i).toList()
                    lineText = self.widget.itemText(i)
                    if len(lineData) > 0 and lineData[0] == groupName:
                        foundParent = True
                        insertPosition = i+1
                        lineData[0] = "groupTaken"
                        self.widget.setItemData(i, lineData)
                        indent = lineData[1].toInt()[0] + 1
                        break
                if not foundParent and groupName != "":
                    self.addLayerToCombo(groupName, insertPosition)
                    insertPosition += 1
                    indent += 1
                for layerid in layerGroup[1]:
                    if self.addLayerToCombo(layerid, insertPosition, indent):
                        insertPosition += 1

    def addLayerToCombo(self, layerid, position, indent=0):
        layer = QgsMapLayerRegistry.instance().mapLayer(layerid)
        preStr = "  "*2*indent
        if layer is None:  # this is a group
            # save in userdata a list ["group",indent]
            self.widget.insertItem(position, preStr+layerid, [layerid, indent])
            j = self.widget.model().index(position, 0)
            self.widget.model().setData(j, QVariant(0), Qt.UserRole - 1)
        else:
            if not self.__checkLayer(layer):
                return False
            self.widget.insertItem(position, preStr+layer.name(), layer.id())
            if layer.id() == self.initLayer:
                self.widget.setCurrentIndex(self.widget.count() - 1)
        return True

    def __checkLayer(self, layer):
        # data provider
        if self.dataProvider is not None and layer.dataProvider().name() != self.dataProvider:
            return False
        # vector layer
        if self.layerType == QgsMapLayer.VectorLayer:
            if layer.type() != QgsMapLayer.VectorLayer:
                return False
            # if wanted, filter on hasGeometry
            if self.hasGeometry is not None and layer.hasGeometryType() != self.hasGeometry:
                return False
            # if wanted, filter on the geoetry type
            if self.geomType is not None and layer.geometryType() != self.geomType:
                return False
        # raster layer
        if self.layerType == QgsMapLayer.RasterLayer:
            if layer.type() != QgsMapLayer.RasterLayer:
                return False
        return True


class VectorLayerCombo(LayerCombo):
    def __init__(self, iface, widget, initLayer="", options={}):
        LayerCombo.__init__(self, iface, widget, initLayer, QgsMapLayer.VectorLayer, options)


class RasterLayerCombo(LayerCombo):
    def __init__(self, iface, widget, initLayer="", options={}):
        LayerCombo.__init__(self, iface, widget, initLayer, QgsMapLayer.RasterLayer, options)