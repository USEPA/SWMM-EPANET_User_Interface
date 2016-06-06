import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmTimeSeriesSelectionDesigner import Ui_frmTimeSeriesSelection
from ui.help import HelpHandler
import Externals.swmm.outputapi.SMOutputWrapper as SMO


class frmTimeSeriesSelection(QtGui.QMainWindow, Ui_frmTimeSeriesSelection):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/controlrules.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.cboObjectType.currentIndexChanged.connect(self.cboObjectType_currentIndexChanged)

        self._main_form = main_form

    def set_from(self, project, output, listener):
        self.project = project
        self.output = output
        self.listener = listener
        self.cboObjectType.clear()
        if project and self.output:
            if self.output.subcatchment_ids:
                self.cboObjectType.addItem("Subcatchment")
            if self.output.node_ids:
                self.cboObjectType.addItem("Node")
            if self.output.link_ids:
                self.cboObjectType.addItem("Link")
            self.cboObjectType.addItem("System")
            self.cboObjectType.setCurrentIndex(0)

    def cboObjectType_currentIndexChanged(self):
        has_objects = True
        if self.cboObjectType.currentText() == "Subcatchment":
            variables = SMO.SMO_subcatchAttributeNames  #subcatchment_ids
        elif self.cboObjectType.currentText() == "Node":
            variables = SMO.SMO_nodeAttributeNames  # node_ids
        elif self.cboObjectType.currentText() == "Link":
            variables = SMO.SMO_linkAttributeNames  # link_ids
        elif self.cboObjectType.currentText() == "System":
            variables = SMO.SMO_systemAttributeNames
            has_objects = False
        else:
            variables = ["None"]
            has_objects = False

        self.cboVariable.clear()
        for item in variables:
            self.cboVariable.addItem(item)

        self.lblSpecify.setEnabled(has_objects)
        self.txtObject.setVisible(has_objects)
        if has_objects:
            self.lblSpecify.setText(self.cboObjectType.currentText() + " Name")
        else:
            self.lblSpecify.setText(self.cboObjectType.currentText() + " does not need a name")

    def cmdOK_Clicked(self):
        if self.rbnRight.isChecked():
            axis = "Right"
        else:
            axis = "Left"

        self.listener(self.cboObjectType.currentText(), self.txtObject.text(),
                      self.cboVariable.currentText(), axis, self.txtLegend.text())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
