from PyQt4.QtCore import SIGNAL, QObject

from layercombo import RasterLayerCombo


class BandCombo():
    def __init__(self, widget, rasterLayerCombo, initBand=None):
        if not isinstance(rasterLayerCombo, RasterLayerCombo):
            raise NameError("You must provide a VectorLayerCombo.")
        self.widget = widget
        self.layerCombo = rasterLayerCombo
        self.initBand = initBand
        QObject.connect(self.layerCombo.widget, SIGNAL("currentIndexChanged(int)"), self.__layerChanged)
        self.layer = None
        self.__layerChanged()

    def __layerChanged(self):
        if hasattr(self.initBand, '__call__'):
            initBand = self.initBand()
        else:
            initBand = self.initBand
        self.widget.clear()
        self.widget.addItem("")
        self.layer = self.layerCombo.getLayer()
        if self.layer is None:
            return
        for b in range(self.layer.bandCount()):
            bandName = self.layer.bandName(b)
            self.widget.addItem(bandName)
            if b == initBand:
                self.widget.setCurrentIndex(b)

    def getBand(self):
        return self.widget.currentIndex()
