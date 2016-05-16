import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
from ui.EPANET.frmTableDesigner import Ui_frmTable
from ui.EPANET.frmGenericListOutput import frmGenericListOutput


class frmTable(QtGui.QMainWindow, Ui_frmTable):

    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(parent.project)   # do after init to set control type CONTROLS or RULES
        self._parent = parent
        # self.set_from(parent.project)

    # def set_from(self, project):
        # section = core.epanet.project.Control()
        # section = project.find_section(control_type)
        # self.txtControls.setPlainText(str(section.get_text()))

    def cmdOK_Clicked(self):
        # section = self._parent.project.find_section(self.control_type)
        # section.set_text(str(self.txtControls.toPlainText()))

        num_columns = 2
        num_rows = 5
        local_data = ['2012-01-23','2012-01-24','2012-01-25','2012-01-29','2012-01-30',3.0,4.1,5.0,2.3,3.1]
        headers = ['Date','Depth']

        self._frmOutputTable = frmGenericListOutput(self.parent(),"EPANET Table Output")
        self._frmOutputTable.set_data(num_rows,num_columns,headers,local_data)
        self._frmOutputTable.show()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
