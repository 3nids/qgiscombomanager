from PyQt4.QtCore import SIGNAL, QObject, QVariant
from qgis.core import QgsVectorLayer

from layercombo import VectorLayerCombo


class FieldCombo():
    def __init__(self, widget, vectorLayerCombo, initField="", fieldType=None):
        if not isinstance(vectorLayerCombo, VectorLayerCombo):
            raise NameError("You must provide a VectorLayerCombo.")
        self.widget = widget
        self.layerCombo = vectorLayerCombo
        self.initField = initField
        self.fieldType = fieldType
        QObject.connect(self.layerCombo.widget, SIGNAL("currentIndexChanged(int)"), self.__layerChanged)
        self.layer = None
        self.__layerChanged()

    def __layerChanged(self):
        if type(self.layer) == QgsVectorLayer:
            QObject.disconnect(self.layer, SIGNAL("attributeAdded(int)"),   self.__layerChanged)
            QObject.disconnect(self.layer, SIGNAL("attributeDeleted(int)"), self.__layerChanged)
        if hasattr(self.initField, '__call__'):
            initField = self.initField()
        else:
            initField = self.initField
        self.widget.clear()
        self.widget.addItem("")
        self.layer = self.layerCombo.getLayer()
        if self.layer is None:
            return
        QObject.connect(self.layer, SIGNAL("attributeAdded(int)"),   self.__layerChanged)
        QObject.connect(self.layer, SIGNAL("attributeDeleted(int)"), self.__layerChanged)
        i = 0
        for idx, field in enumerate(self.layer.pendingFields()):
            i += 1
            fieldAlias = self.layer.attributeDisplayName(idx)
            try:
                fieldName = field.name()
            except:  # qgis <1.9
                fieldName = self.layer.pendingFields()[idx].name()
            self.widget.addItem(fieldAlias, fieldName)
            if not self.__isFieldValid(idx):
                j = self.widget.model().index(i, 0)
                self.widget.model().setData(j, QVariant(0), Qt.UserRole-1)
                continue
            if fieldName == initField:
                self.widget.setCurrentIndex(i)

    def __isFieldValid(self, idx):
        if self.fieldType is None:
            return True
        return self.layer.dataProvider().fields()[idx].type() == self.fieldType

    def isValid(self):
        idx = self.getFieldIndex()
        if idx == -1:
            return False
        return self.__isFieldValid(idx)

    def getFieldAlias(self):
        i = self.widget.currentIndex()
        if i == 0:
            return ""
        return self.widget.currentText()

    def getFieldName(self):
        i = self.widget.currentIndex()
        if i == 0:
            return ""
        return self.widget.itemData(i).toString()

    def getFieldIndex(self):
        i = self.widget.currentIndex()
        if i == 0:
            return None
        return self.layer.fieldNameIndex(self.getFieldName())
