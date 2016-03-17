import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmInflowsDesigner import Ui_frmInflows


class frmInflows(QtGui.QMainWindow, Ui_frmInflows):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.tabInflows.currentChanged.connect(self.tabInflows_currentTabChanged)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.epanet.project.Control()
        section = project.find_section("CONTROLS")
        # self.txtControls.setPlainText(str(section.get_text()))
        self.tabInflows_currentTabChanged()

    def cmdOK_Clicked(self):
        # will need to do some validating, see dxsect.pas
        section = self._parent.project.find_section("CONTROLS")
        section.set_text(str(self.txtControls.toPlainText()))
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def tabInflows_currentTabChanged(self):

        tab_index = self.tabInflows.currentIndex()
        if tab_index == 0:
            self.lblNotes.setText("If Baseline or Time Series is left blank its value is 0. If Baseline Pattern is left blank its value is 1.0.")
        elif tab_index == 1:
            self.lblNotes.setText("If Average Value is left blank its value is 0. Any Time Pattern left blank defaults to a constant value of 1.0.")
        elif tab_index == 2:
            self.lblNotes.setText("Leave the Unit Hydrograph Group field blank to remove any RDII inflow at this node.")

        units = 1

        if units == 1:
            self.lblSewershed.setText('Sewershed Area (acres)')
        else:
            self.lblSewershed.setText('Sewershed Area (hectares)')

        # add flow units to average value lblAverage
        self.lblAverage.setText('Average Value ()')
