import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
import core.epanet.options.backdrop
from enum import Enum
from ui.EPANET.frmMapBackdropOptionsDesigner import Ui_frmMapBackdropOptions


class frmMapBackdropOptions(QtGui.QMainWindow, Ui_frmMapBackdropOptions):

    def __init__(self, parent=None):
        # TODO: Move this and same version from frmHydraulicsOptions to a shared location
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        frmMapBackdropOptions.set_combo_items(core.epanet.options.backdrop.BackdropUnits, self.cboMapUnits)
        self.cboMapUnits.addItems(("FEET", "METERS", "DEGREES", "NONE"))
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.epanet.options.backdrop.BackdropOptions()
        backdrop_options = project.backdrop
        self.txtBackdropFile.setText(str(backdrop_options.file))
        self.txtBackdropX.setText(str(backdrop_options.offset[0]))
        self.txtBackdropY.setText(str(backdrop_options.offset[1]))
        self.txtLLX.setText(str(backdrop_options.dimensions[0]))
        self.txtLLY.setText(str(backdrop_options.dimensions[1]))
        self.txtURX.setText(str(backdrop_options.dimensions[2]))
        self.txtURY.setText(str(backdrop_options.dimensions[3]))
        frmMapBackdropOptions.set_combo(self.cboMapUnits, backdrop_options.units)
        section = project.find_section("OPTIONS")
        self.txtMapFile.setText(str(project.options.map))

    def cmdOK_Clicked(self):
        backdrop_options = self._parent.project.backdrop
        backdrop_options.file = self.txtBackdropFile.text()
        backdrop_options.offset = (float(self.txtBackdropX.text()), float(self.txtBackdropY.text()))
        backdrop_options.dimensions = (self.txtLLX.text(), self.txtLLY.text(), self.txtURX.text(), self.txtURY.text())
        backdrop_options.units = core.epanet.options.backdrop.BackdropUnits[self.cboMapUnits.currentText()]
        options = self._parent.project.options
        options.map = self.txtMapFile.text()
        with open(self._parent.project.file_name + ".BackdropOk.txt", 'w') as writer:
            writer.writelines(self._parent.project.get_text())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
