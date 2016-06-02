import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmCalibrationDataDesigner import Ui_frmCalibrationData


class frmCalibrationData(QtGui.QMainWindow, Ui_frmCalibrationData):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(main_form.project)   # do after init to set control type CONTROLS or RULES
        self._main_form = main_form

    # def set_from(self, project, control_type):
        # section = core.epanet.project.Control()

    def cmdOK_Clicked(self):
        section = self._main_form.project.find_section(self.control_type)
        section.set_text(str(self.txtControls.toPlainText()))
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
