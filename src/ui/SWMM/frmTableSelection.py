import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmTableSelectionDesigner import Ui_frmTableSelection
from ui.SWMM.frmGenericListOutput import frmGenericListOutput
from ui.help import HelpHandler


class frmTableSelection(QtGui.QMainWindow, Ui_frmTableSelection):

    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.help_topic = "swmm/src/src/controlrules.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

        # self.set_from(parent.project)
        self._parent = parent

    # def set_from(self, project):
        # section = core.epanet.project.Control()
        # section = project.find_section("CONTROLS")
        # self.txtControls.setPlainText(str(section.get_text()))

    def cmdOK_Clicked(self):
        num_columns = 2
        num_rows = 5
        local_data = ['2012-01-23','2012-01-24','2012-01-25','2012-01-29','2012-01-30',3.0,4.1,5.0,2.3,3.1]
        headers = ['Date','Depth']

        self._frmOutputTable = frmGenericListOutput(self.parent(),"SWMM Table Output")
        self._frmOutputTable.set_data(num_rows,num_columns,headers,local_data)
        self._frmOutputTable.show()

        self.close()

    def cmdCancel_Clicked(self):
        self.close()
