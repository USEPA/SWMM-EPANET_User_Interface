import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
import core.epanet.options.backdrop
from ui.EPANET.frmMapBackdropOptionsDesigner import Ui_frmMapBackdropOptions


class frmMapBackdropOptions(QtGui.QMainWindow, Ui_frmMapBackdropOptions):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # TODO: function that populates combo box from Enum
        self.cboMapUnits.addItems(("FEET", "METERS", "DEGREES", "NONE"))
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.epanet.options.backdrop.BackdropOptions()
        section = project.find_section("BACKDROP")
        self.txtBackdropFile.setText(str(section.file))
        self.txtBackdropX.setText(str(section.offset_x))
        self.txtBackdropY.setText(str(section.offset_y))
        self.txtLLX.setText(str(section.dimensions(0)))
        self.txtLLY.setText(str(section.dimensions(1)))
        self.txtURX.setText(str(section.dimensions(2)))
        self.txtURY.setText(str(section.dimensions(3)))
        self.cboMapUnits = section.units
        section = project.find_section("OPTIONS")
        self.txtMapFile.setText(str(section.mapfile))

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("BACKDROP")
        section.file = self.txtBackdropFile.text()
        section.offset_x = self.txtBackdropX.text()
        section.offset_y = self.txtBackdropY.text()
        section.dimensions = (self.txtLLX.text(), self.txtLLY.text(), self.txtURX.text(), self.txtURY.text())
        section.units = self.cboMapUnits
        section = self._parent.project.find_section("OPTIONS")
        section.mapfile = self.txtMapFile.Text()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
