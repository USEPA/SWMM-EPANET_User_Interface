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
        self.set_from(main_form.project)
        self._main_form = main_form

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
        section.file = self.txtBackdropFile.text()
        section.dimensions = (float(self.txtLLXBack.text()), float(self.txtLLYBack.text()),
                              float(self.txtURXBack.text()), float(self.txtURYBack.text()))

        section = self._main_form.project.map
        if self.rbnNone.isChecked():
            section.units = MapUnits.NONE
        if self.rbnDegrees.isChecked():
            section.units =  MapUnits.DEGREES
        if self.rbnFeet.isChecked():
            section.units = MapUnits.FEET
        if self.rbnMeters.isChecked():
            section.units = MapUnits.METERS
        section.dimensions = (float(self.txtLLXMap.text()), float(self.txtLLYMap.text()),
                              float(self.txtURXMap.text()), float(self.txtURYMap.text()))
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
