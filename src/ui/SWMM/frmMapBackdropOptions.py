import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.options.backdrop
from ui.SWMM.frmMapBackdropOptionsDesigner import Ui_frmMapBackdropOptions


class frmMapBackdropOptions(QtGui.QMainWindow, Ui_frmMapBackdropOptions):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.swmm.options.backdrop.BackdropOptions()
        section = project.find_section("BACKDROP")
        self.txtBackdropFile.setText(str(section.file))
        self.txtLLXBack.setText(str(section.dimensions[0]))
        self.txtLLYBack.setText(str(section.dimensions[1]))
        self.txtURXBack.setText(str(section.dimensions[2]))
        self.txtURYBack.setText(str(section.dimensions[3]))
        section = project.find_section("OPTIONS")
        self.txtLLXMap.setText(str(section.dimensions[0]))
        self.txtLLYMap.setText(str(section.dimensions[1]))
        self.txtURXMap.setText(str(section.dimensions[2]))
        self.txtURYMap.setText(str(section.dimensions[3]))
        if section.units == "NONE":
            self.rbnNone.setChecked(True)
        if section.units == "DEGREES":
            self.rbnDegrees.setChecked(True)
        if section.units == "FEET":
            self.rbnFeet.setChecked(True)
        if section.units == "METERS":
            self.rbnMeters.setChecked(True)

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("BACKDROP")
        section.file = self.txtBackdropFile.text()
        section.dimensions = (self.txtLLXBack.text(), self.txtLLYBack.text(), self.txtURXBack.text(), self.txtURYBack.text())
        section = self._parent.project.find_section("OPTIONS")
        if self.rbnNone.isChecked():
            section.units = "NONE"
        if self.rbnDegrees.isChecked():
            section.units = "DEGREES"
        if self.rbnFeet.isChecked():
            section.units = "FEET"
        if self.rbnMeters.isChecked():
            section.units = "METERS"
        section.dimensions = (self.txtLLXMap.text(), self.txtLLYMap.text(), self.txtURXMap.text(), self.txtURYMap.text())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()