from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QMessageBox
from ui.frmMapDimensionsDesigner import Ui_frmMapDimensionsDesigner

class frmMapDimensions(QDialog):
    def __init__(self, main_form=None, *args):
        QDialog.__init__(self)
        self.ui = Ui_frmMapDimensionsDesigner()
        self.ui.setupUi(self)
        self.session = main_form
        self.icon = main_form.windowIcon()
        self.map_widget = self.session.map_widget
        self.options = None
        if args is not None and len(args) > 0:
            self.options = args[0]
        self.ui.rdoUnitDegrees.toggled.connect(self.changeLinearMapUnit)
        self.ui.rdoUnitNone.toggled.connect(self.changeLinearMapUnit)
        self.ui.rdoUnitFeet.toggled.connect(self.changeLinearMapUnit)
        self.ui.rdoUnitMeters.toggled.connect(self.changeLinearMapUnit)
        self.ui.txtLLx.textChanged.connect(lambda:self.checkCoords(self.ui.txtLLx.text()))
        self.ui.txtLLy.textChanged.connect(lambda:self.checkCoords(self.ui.txtLLy.text()))
        self.ui.txtURx.textChanged.connect(lambda:self.checkCoords(self.ui.txtURx.text()))
        self.ui.txtURy.textChanged.connect(lambda:self.checkCoords(self.ui.txtURy.text()))
        self.ui.btnAutoSize.clicked.connect(self.autoSetMapDimensions)
        self.ui.buttonBox.accepted.connect(self.setExtent)
        self.setupOptions()

    def autoSetMapDimensions(self):
        # Determines map dimensions based on range of vertices' coordinates
        MAXDEGDIGITS = 4 # Max.decimal digits for lat - long degrees pass
        sigDigit = 2
        if self.ui.rdoUnitDegrees.isChecked():
            sigDigit = MAXDEGDIGITS
        self.display_layers_extent()

    def setExtent(self):
        if self.session is None:
            return
        if self.map_widget is None:
            return
        val1, is_val_good1 = self.floatTryParse(self.ui.txtLLx.text())
        val2, is_val_good2 = self.floatTryParse(self.ui.txtLLy.text())
        val3, is_val_good3 = self.floatTryParse(self.ui.txtURx.text())
        val4, is_val_good4 = self.floatTryParse(self.ui.txtURy.text())

        if is_val_good1 and is_val_good2 and is_val_good3 and is_val_good4:
            if val1 == val3 or val2 == val4:
                #MSG_ILLEGAL_MAP_LIMITS
                #LLXEdit.SetFocus
                return
            else:
                self.map_widget.coord_origin.x = val1
                self.map_widget.coord_origin.y = val2
                self.map_widget.coord_fext.x = val3
                self.map_widget.coord_fext.y = val4
                if self.session.project is not None:
                    if self.session.project.map is not None:
                        self.session.project.map.dimensions = (val1, val2, val3, val4)
                        self.session.map_widget.set_extent_by_corners(self.session.project.map.dimensions)
                if self.session.project is not None:
                    if self.session.project.backdrop is not None:
                        self.session.project.backdrop.dimensions = (self.ui.txtLLx.text(), self.ui.txtLLy.text(), self.ui.txtURx.text(), self.ui.txtURy.text())
                        if self.ui.rdoUnitFeet.isChecked():
                            if not isinstance(self.session.project.backdrop.units, str):
                                self.session.project.backdrop.units = self.session.project.backdrop.units.FEET
                            else:
                                self.session.project.backdrop.units = "FEET"
                        elif self.ui.rdoUnitMeters.isChecked():
                            if not isinstance(self.session.project.backdrop.units, str):
                                self.session.project.backdrop.units = self.session.project.backdrop.units.METERS
                            else:
                                self.session.project.backdrop.units = "METERS"
                        elif self.ui.rdoUnitDegrees.isChecked():
                            if not isinstance(self.session.project.backdrop.units, str):
                                self.session.project.backdrop.units = self.session.project.backdrop.units.DEGREES
                            else:
                                self.session.project.backdrop.units = "DEGREES"
                        else:
                            if not isinstance(self.session.project.backdrop.units, str):
                                self.session.project.backdrop.units = self.session.project.backdrop.units.NONE
                            else:
                                self.session.project.backdrop.units = ""
        pass

    def setupOptions(self):
        if self.session is None:
            return
        if self.map_widget is None:
            return

        model_dim = self.session.project.backdrop.dimensions
        if model_dim and model_dim[0] and model_dim[1] and model_dim[2] and model_dim[3]:
            #self.ui.txtLLx.setText('{:.3f}'.format(self._main_form.map_widget.coord_origin.x))
            #self.ui.txtLLy.setText('{:.3f}'.format(self._main_form.map_widget.coord_origin.y))
            #self.ui.txtURx.setText('{:.3f}'.format(self._main_form.map_widget.coord_fext.x))
            #self.ui.txtURy.setText('{:.3f}'.format(self._main_form.map_widget.coord_fext.x))
            self.ui.txtLLx.setText(str(model_dim[0]))
            self.ui.txtLLy.setText(str(model_dim[1]))
            self.ui.txtURx.setText(str(model_dim[2]))
            self.ui.txtURy.setText(str(model_dim[3]))
        else:
            self.display_layers_extent()

        if not isinstance(self.session.project.backdrop.units, str):
            units = self.session.project.backdrop.units.name
        else:
            units = self.session.project.backdrop.units.upper()

        if units == "FEET":  # feet
            self.ui.rdoUnitFeet.setChecked(True)
        elif units == "METERS":  # meters
            self.ui.rdoUnitMeters.setChecked(True)
        elif units == "DEGREES":  # degrees
            self.ui.rdoUnitDegrees.setChecked(True)
        else:
            self.ui.rdoUnitNone.setChecked(True)

        self.setWindowIcon(self.icon)

    def display_layers_extent(self):
        if self.session.model_layers:
            llx = 0
            lly = 0
            urx = 10000
            ury = 10000
            layers = []
            for mlyr in self.session.model_layers.all_layers:
                lyr_name = mlyr.name()
                if lyr_name and \
                        (lyr_name.lower().startswith("label") or
                             lyr_name.lower().startswith("subcentroid") or
                             lyr_name.lower().startswith("sublink")):
                    continue
                layers.append(mlyr)
            r = self.session.map_widget.get_extent(layers)
            llx = r.xMinimum()
            lly = r.yMinimum()
            urx = r.xMaximum()
            ury = r.yMaximum()
            self.ui.txtLLx.setText(str(llx))
            self.ui.txtLLy.setText(str(lly))
            self.ui.txtURx.setText(str(urx))
            self.ui.txtURy.setText(str(ury))

    def floatTryParse(self, value):
        try:
            return float(value), True
        except ValueError:
            return value, False

    def changeLinearMapUnit(self):
        if self.session is None:
            return
        if self.map_widget is None:
            return
        if self.ui.rdoUnitDegrees.isChecked():
            self.map_widget.map_linear_unit = self.map_widget.map_unit_names[6]  # Degrees
        elif self.ui.rdoUnitMeters.isChecked():
            self.map_widget.map_linear_unit = self.map_widget.map_unit_names[0]  # Meters
        elif self.ui.rdoUnitNone.isChecked():
            self.map_widget.map_linear_unit = self.map_widget.map_unit_names[7]  # Unknown
        elif self.ui.rdoUnitFeet.isChecked():
            self.map_widget.map_linear_unit = self.map_widget.map_unit_names[2]  # Feet

        if self.session.project is not None:
            if self.session.project.map is not None:
                self.session.project.map.setMapUnits(
                    self.session.map_widget.map_linear_unit
                )
        return

    def checkCoords(self, avalue):
        if len(avalue) ==0:
            return
        if len(avalue) == 1 and avalue[0] == '-':
            return
        val, value_is_good = self.floatTryParse(avalue)
        if not value_is_good:
            msg = QMessageBox()
            msg.setWindowTitle('Map Dimension')
            msg.setText('Coordinate value is not valid numeric value.')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            del msg
        pass

    def coordsInGoodFormat(self):
        val1, is_val_good1 = self.floatTryParse(self.ui.txtLLx.text())
        val2, is_val_good2 = self.floatTryParse(self.ui.txtLLy.text())
        val3, is_val_good3 = self.floatTryParse(self.ui.txtURx.text())
        val4, is_val_good4 = self.floatTryParse(self.ui.txtURy.text())
        if is_val_good1 and is_val_good2 and is_val_good3 and is_val_good4:
            if val1 == val3 or val2 == val4:
                #MSG_ILLEGAL_MAP_LIMITS
                #LLXEdit.SetFocus
                return False
            else:
                return True
        else:
            return False


