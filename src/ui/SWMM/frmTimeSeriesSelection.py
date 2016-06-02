import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmTimeSeriesSelectionDesigner import Ui_frmTimeSeriesSelection
from ui.help import HelpHandler


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
        self.cboStart.clear()
        self.cboObjectType.clear()
        if project and self.output:
            if len(self.output.node_ids):
                self.cboObjectType.addItem("Subcatchment")
            if len(self.output.node_ids):
                self.cboObjectType.addItem("Node")
            if len(self.output.link_ids):
                self.cboObjectType.addItem("Link")
            if len(self.output.node_ids):
                self.cboObjectType.addItem("System")
            if self.cboObjectType.count() > 0:
                self.cboObjectType.setCurrentIndex(0)
            # self.rbnNodes.setChecked(True)
            # self.rbnNodes_Clicked()
            values = self.output.get_NodeSeries(0, 0)
            for val in values:
                print '{:7.2f}'.format(val)

    def cboObjectType_currentIndexChanged(self):
        self.cboVariable.clear()
        has_objects = True
        if self.cboObjectType.currentText() == "Subcatchment":
            items = self.output.subcatchment_ids
        elif self.cboObjectType.currentText() == "Node":
            items = self.output.node_ids
        elif self.cboObjectType.currentText() == "Link":
            items = self.output.link_ids
        elif self.cboObjectType.currentText() == "System":
            items = self.output.SysViewNames
            has_objects = False
        else:
            items = ["None"]
        for item in items:
            self.cboVariable.addItem(item)

        self.lblSpecify.setEnabled(has_objects)
        self.txtObject.setVisible(has_objects)
        if has_objects:
            self.lblSpecify.setText(self.cboObjectType.currentText() + " Name")
        else:
            self.lblSpecify.setText(self.cboObjectType.currentText() + " does not need an item name")

    def cmdOK_Clicked(self):
        self.listener(self.cboObjectType.currentText(), self.txtObject.text(),
                      self.cboVariable.currentText(), self.txtLegend.text(), self.rbnRight.isChecked())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
