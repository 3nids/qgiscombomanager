## Quick start

[QGIS](http://www.qgis.org) Combo Manager is a python module to easily manage a combo box with
a layer list and eventually relate it with one or several combos with
list of corresponding fields.

The field combos are filled with the names of columns of the currently
selected layer in the layer combo.

In your plugin, create first a _LayerCombo_:

```python
self.LayerComboManager = VectorLayerCombo(iface.legendInterface(), self.layerComboWidget)
```


Then, associates some _FieldCombo_:

```python
self.myFieldComboManager = FieldCombo(self.myFieldComboManager, self.LayerComboManager)
```


The managers (layer or field) must be saved as a class property (self.something), so the variable is not
getting out of scope in python.

The classes offers some convenience methods: _getLayer()_, for layer combos, and _getFieldName()_, _getFieldAlias()_, _getFieldIndex()_ for field combos.

## Installing the module

To use this module you can easily copy the files and put them in your project.
A more elegant way is to use git submodule. Hence, you can keep up with latest improvements. In you plugin directory, do

```
git submodule add git://github.com/3nids/qgiscombomanager.git
```

Then, import the needed classes:

```python
from qgiscombomanager import LayerCombo, RasterLayerCombo, VectorLayerCombo, FieldCombo
```

## Layer Combos

A combo box can be assigned to list the layers. Three classes are available:
* _LayerCombo_
* _VectorLayerCombo_
* _RasterLayerCombo_

```python
LayerCombo(legendInterface, widget, initLayer="", options={}, layerType=None)
```

_VectorLayerCombo_ and _RasterLayerCombo_ are convenient classes which are calling the main LayerCombo class with the same parameters and specifying the _layerType_.

* **legendInterface**: give the legendInterface (used to display layers in the same way as in the legend)
* **widget**: the QComboBox widget
* **initLayer**: the initally selected layer ID or a lambda function returning the ID (it could look for a value in settings)
* **options**: a dictionnary of options: {"opt1": val1, "opt2": val2, etc.}. Options are listed hereunder (default values are first listed).

**Options**
* **groupLayers**: False/True. Groups layers in combobox according to the legend interface groups
* **hasGeometry***: None/True/False. Restrains the possible selection of layers to layers having or not geometry (None = all).
* **geomType***: None/QGis.Point/QGis.Line/QGis.Polygon. Restrains the possible selection of layers to a certain [type of geometry](http://qgis.org/api/classQGis.html#a09947eb19394302eeeed44d3e81dd74b). (None = all)
* **dataProvider**: None/postgres/etc. Filters the layers based on the data provider name (None = all).
* **finishInit**: True/False. If False, the combo box will not be initiated (filled with layers). this might useful if you want the manager to be returned before it is filled with layers.

*used for vector layer combos


## Field combos

A combo box can be assigned to list the fields related to a given VectorLayerCombo.

```python
FieldCombo(widget, vectorLayerCombo, initField="", fieldType=None)
```

* **widget**: the qcombobox widget
* **vectorLayerCombo**: the combobox defining the vector layer
* **initField**: the initially selected field name or a lambda function returning the name (it could look for a value in settings)
* **fieldType**: restrain the possible selection to a certain type of field (see [QGIS doc](http://qgis.org/api/classQgsField.html#a00409d57dc65d6155c6d08085ea6c324) or [Qt doc](http://developer.qt.nokia.com/doc/qt-4.8/qmetatype.html#Type-enum)).

## Band combos

A combo box can be assigned to list the bands related to agin RasterLayerCombo.

```python
BandCombo(widget, rasterLayerCombo, initBand=None)
```

* **widget**: the qcombobox widget
* **rasterLayerCombo**: the combobox defining the raster layer
* **initBand**: the initially selected band (integer) or a lambda function returning it (it could look for a value in settings)
