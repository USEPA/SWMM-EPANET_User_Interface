import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
import core.swmm.options.backdrop
from core.swmm.options.map import MapUnits
from ui.SWMM.frmMapBackdropOptionsDesigner import Ui_frmMapBackdropOptions


class frmMapBackdropOptions(QMainWindow, Ui_frmMapBackdropOptions):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/mapdimensionsdialog.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self._main_form = main_form
        self.set_from(main_form.project)

        if (main_form.program_settings.value("Geometry/" + "frmMapBackdropOptions_geometry") and
                main_form.program_settings.value("Geometry/" + "frmMapBackdropOptions_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmMapBackdropOptions_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmMapBackdropOptions_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_from(self, project):
        # section = core.swmm.options.backdrop.BackdropOptions()
        section = project.backdrop
        self.txtBackdropFile.setText(str(section.file))
        self.txtLLXBack.setText(str(section.dimensions[0]))
        self.txtLLYBack.setText(str(section.dimensions[1]))
        self.txtURXBack.setText(str(section.dimensions[2]))
        self.txtURYBack.setText(str(section.dimensions[3]))
        section = project.map
        self.txtLLXMap.setText(str(section.dimensions[0]))
        self.txtLLYMap.setText(str(section.dimensions[1]))
        self.txtURXMap.setText(str(section.dimensions[2]))
        self.txtURYMap.setText(str(section.dimensions[3]))

        if self._main_form.map_widget.map_linear_unit == 'Meters':
            section.units = MapUnits.METERS
        if self._main_form.map_widget.map_linear_unit == 'Unknown':
            section.units = MapUnits.NONE
        if self._main_form.map_widget.map_linear_unit == 'Degrees':
            section.units = MapUnits.DEGREES
        if self._main_form.map_widget.map_linear_unit == 'Feet':
            section.units = MapUnits.FEET

        if section.units == MapUnits.NONE:
            self.rbnNone.setChecked(True)
        if section.units == MapUnits.DEGREES:
            self.rbnDegrees.setChecked(True)
        if section.units == MapUnits.FEET:
            self.rbnFeet.setChecked(True)
        if section.units == MapUnits.METERS:
            self.rbnMeters.setChecked(True)

    def cmdOK_Clicked(self):
        section = self._main_form.project.backdrop

        orig_file = section.file
        orig_dimensions = section.dimensions

        section.file = self.txtBackdropFile.text()
        section.dimensions = (float(self.txtLLXBack.text()), float(self.txtLLYBack.text()),
                              float(self.txtURXBack.text()), float(self.txtURYBack.text()))

        if orig_file != section.file or \
            orig_dimensions != section.dimensions:
            self._main_form.mark_project_as_unsaved()

        section = self._main_form.project.map

        orig_units = section.units
        orig_dimensions = section.dimensions

        if self.rbnNone.isChecked():
            section.units = MapUnits.NONE
            self._main_form.map_widget.map_linear_unit = 'Unknown'
        if self.rbnDegrees.isChecked():
            section.units =  MapUnits.DEGREES
            self._main_form.map_widget.map_linear_unit = 'Degrees'
        if self.rbnFeet.isChecked():
            section.units = MapUnits.FEET
            self._main_form.map_widget.map_linear_unit = 'Feet'
        if self.rbnMeters.isChecked():
            section.units = MapUnits.METERS
            self._main_form.map_widget.map_linear_unit = 'Meters'
        section.dimensions = (float(self.txtLLXMap.text()), float(self.txtLLYMap.text()),
                              float(self.txtURXMap.text()), float(self.txtURYMap.text()))

        if orig_units != section.units or \
            orig_dimensions != section.dimensions:
            self._main_form.mark_project_as_unsaved()

        self._main_form.program_settings.setValue("Geometry/" + "frmMapBackdropOptions_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmMapBackdropOptions_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
