import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
import core.epanet.options.backdrop
from ui.EPANET.frmMapBackdropOptionsDesigner import Ui_frmMapBackdropOptions
import ui.convenience


class frmMapBackdropOptions(QMainWindow, Ui_frmMapBackdropOptions):

    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Map_Dime.htm"
        self.setupUi(self)
        ui.convenience.set_combo_items(core.epanet.options.backdrop.BackdropUnits, self.cboMapUnits)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

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
        ui.convenience.set_combo(self.cboMapUnits, backdrop_options.units)
        self.txtMapFile.setText(str(project.options.map))

    def cmdOK_Clicked(self):
        backdrop_options = self._main_form.project.backdrop
        backdrop_options.file = self.txtBackdropFile.text()
        backdrop_options.offset = (self.txtBackdropX.text(), self.txtBackdropY.text())
        backdrop_options.dimensions = (self.txtLLX.text(), self.txtLLY.text(), self.txtURX.text(), self.txtURY.text())
        backdrop_options.units = core.epanet.options.backdrop.BackdropUnits[self.cboMapUnits.currentText()]
        self._main_form.project.options.map = self.txtMapFile.text()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
