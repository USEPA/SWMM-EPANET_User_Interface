from PyQt4 import QtCore, QtGui
from frmMapDimensionsDesigner import Ui_frmMapDimensionsDesigner

class frmMapDimensions(QtGui.QDialog):
    def __init__(self, main_form=None, *args):
        self._main_form = main_form
        QtGui.QDialog.__init__(self)
        self.ui = Ui_frmMapDimensionsDesigner()
        self.ui.setupUi(self)
        self.options = None
        if args is not None and len(args) > 0:
            self.options = args[0]
        self.ui.rdoUnitDegrees.toggled.connect(self.changeLinearMapUnit)
        self.ui.rdoUnitNone.toggled.connect(self.changeLinearMapUnit)
        self.ui.rdoUnitFeet.toggled.connect(self.changeLinearMapUnit)
        self.ui.rdoUnitMeters.toggled.connect(self.changeLinearMapUnit)
        self.setupOptions()

    def setupOptions(self):
        if self._main_form is None:
            return
        if self._main_form.map_widget is None:
            return
        lu = self._main_form.map_widget.mapLinearUnit
        if lu == 'none':
            self.ui.rdoUnitNone.setChecked(True)
        elif lu == 'feet':
            self.ui.rdoUnitFeet.setChecked(True)
        elif lu == 'meters':
            self.ui.rdoUnitMeters.setChecked(True)
        elif lu == 'degrees':
            self.ui.rdoUnitDegrees.setChecked(True)

    def changeLinearMapUnit(self):
        if self._main_form is None:
            return
        if self._main_form.map_widget is None:
            return
        if self.ui.rdoUnitDegrees.isChecked():
            self._main_form.map_widget.mapLinearUnit = 'degrees'
        elif self.ui.rdoUnitMeters.isChecked():
            self._main_form.map_widget.mapLinearUnit = 'meters'
        elif self.ui.rdoUnitNone.isChecked():
            self._main_form.map_widget.mapLinearUnit = 'none'
        elif self.ui.rdoUnitFeet.isChecked():
            self._main_form.map_widget.mapLinearUnit = 'feet'
        return
