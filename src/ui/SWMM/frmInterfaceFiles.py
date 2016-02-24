import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.options.files
from ui.SWMM.frmInterfaceFilesDesigner import Ui_frmInterfaceFiles


class frmInterfaceFiles(QtGui.QMainWindow, Ui_frmInterfaceFiles):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.swmm.options.files.Files()
        section = project.files
        self.txtUseRainfall.setText(str(section.use_rainfall))
        self.txtSaveRainfall.setText(str(section.save_rainfall))
        self.txtUseRunoff.setText(str(section.use_runoff))
        self.txtSaveRunoff.setText(str(section.save_runoff))
        self.txtUseHotstart.setText(str(section.use_hotstart))
        self.txtSaveHotstart.setText(str(section.save_hotstart))
        self.txtUseRDII.setText(str(section.use_rdii))
        self.txtSaveRDII.setText(str(section.save_rdii))
        self.txtUseInflows.setText(str(section.use_inflows))
        self.txtSaveOutflows.setText(str(section.save_outflows))

    def cmdOK_Clicked(self):
        section = self._parent.project.files
        section.use_rainfall = self.txtUseRainfall.text()
        section.save_rainfall = self.txtSaveRainfall.text()
        section.use_runoff = self.txtUseRunoff.text()
        section.save_runoff = self.txtSaveRunoff.text()
        section.use_hotstart = self.txtUseHotstart.text()
        section.save_hotstart = self.txtSaveHotstart.text()
        section.use_rdii = self.txtUseRDII.text()
        section.save_rdii = self.txtSaveRDII.text()
        section.use_inflows = self.txtUseInflows.text()
        section.save_outflows = self.txtSaveOutflows.text()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()