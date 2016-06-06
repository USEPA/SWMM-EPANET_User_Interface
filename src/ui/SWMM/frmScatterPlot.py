import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import matplotlib.pyplot as plt
import core.swmm.project
from ui.SWMM.frmScatterPlotDesigner import Ui_frmScatterPlot
from ui.help import HelpHandler
import Externals.swmm.outputapi.SMOutputWrapper as SMO


class frmScatterPlot(QtGui.QMainWindow, Ui_frmScatterPlot):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self._main_form = main_form
        # self.help_topic = "swmm/src/src/controlrules.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.cboStart.currentIndexChanged.connect(self.cboStart_currentIndexChanged)
        self.cboEnd.currentIndexChanged.connect(self.cboEnd_currentIndexChanged)
        self.cboXCat.currentIndexChanged.connect(self.cboXCat_currentIndexChanged)
        self.cboYCat.currentIndexChanged.connect(self.cboYCat_currentIndexChanged)

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboStart.clear()
        if project and self.output:
            for time_index in range(0, self.output.numPeriods):
                time_string = self.output.get_time_string(time_index)
                self.cboStart.addItem(time_string)
                self.cboEnd.addItem(time_string)
            self.cboStart.setCurrentIndex(0)
            self.cboEnd.setCurrentIndex(self.cboEnd.count() - 1)
            for cboObjectType in (self.cboXCat, self.cboYCat):
                cboObjectType.clear()
                if self.project and self.output:
                    if self.output.subcatchment_ids:
                        cboObjectType.addItem("Subcatchment")
                    if self.output.node_ids:
                        cboObjectType.addItem("Node")
                    if self.output.link_ids:
                        cboObjectType.addItem("Link")
                    if cboObjectType.count() > 0:
                        cboObjectType.setCurrentIndex(0)

    def cboStart_currentIndexChanged(self):
        if self.cboEnd.currentIndex() < self.cboStart.currentIndex():
            self.cboEnd.setCurrentIndex(self.cboStart.currentIndex())

    def cboEnd_currentIndexChanged(self):
        if self.cboEnd.currentIndex() < self.cboStart.currentIndex():
            self.cboStart.setCurrentIndex(self.cboEnd.currentIndex())

    def cboXCat_currentIndexChanged(self):
        self.cboObjectType_currentIndexChanged(self.cboXCat, self.lstX, self.cboVarX)

    def cboYCat_currentIndexChanged(self):
        self.cboObjectType_currentIndexChanged(self.cboYCat, self.lstY, self.cboVarY)

    def cboObjectType_currentIndexChanged(self, cboObjectType, lst_ids, cboVariable):

        if cboObjectType.currentText() == "Subcatchment":
            items = self.output.subcatchment_ids
            variables = SMO.SMO_subcatchAttributeNames
        elif cboObjectType.currentText() == "Node":
            items = self.output.node_ids
            variables = SMO.SMO_nodeAttributeNames
        elif cboObjectType.currentText() == "Link":
            items = self.output.link_ids
            variables = SMO.SMO_linkAttributeNames
        else:
            items = ["None"]
            variables = ["None"]

        lst_ids.clear()
        for item in items:
            lst_ids.addItem(item)

        cboVariable.clear()
        for variable in variables:
            cboVariable.addItem(variable)

    def cmdOK_Clicked(self):
        self.plot_scatter()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def plot_scatter(self):
        fig = plt.figure()
        start_index = self.cboStart.currentIndex()
        end_index = self.cboEnd.currentIndex()
        num_steps = end_index - start_index + 1
        # if num_steps < self.output.numPeriods:
        title = "Scatter Plot " + self.cboStart.currentText() + ' - ' + self.cboEnd.currentText()
        fig.canvas.set_window_title(title)
        plt.title(title)

        x_values, x_units = self._get_values(self.cboXCat.currentText(),
                                           self.lstX.currentItem().text(),
                                           self.cboVarX.currentText(),
                                           start_index, num_steps)

        y_values, y_units = self._get_values(self.cboYCat.currentText(),
                                           self.lstY.currentItem().text(),
                                           self.cboVarY.currentText(),
                                           start_index, num_steps)

        plt.scatter(x_values, y_values, s=15, alpha=0.5)

        if x_units:
            x_units = ' (' + x_units + ')'

        if y_units:
            y_units = ' (' + y_units + ')'

        plt.xlabel(self.cboXCat.currentText() + ' ' +
                   self.lstX.currentItem().text() + ' ' +
                   self.cboVarX.currentText() + x_units)
        plt.ylabel(self.cboYCat.currentText() + ' ' +
                   self.lstY.currentItem().text() + ' ' +
                   self.cboVarY.currentText() + y_units)

        plt.grid(True)
        plt.show()

    def _get_values(self, object_type, object_id, variable, start_index, num_steps):
        if object_type == "Node":
            item_index = self.output.get_NodeIndex(object_id)
            attribute_index = SMO.SMO_nodeAttributes[SMO.SMO_nodeAttributeNames.index(variable)]
            units = SMO.SMO_nodeAttributeUnits[attribute_index][self.output.unit_system]
            return self.output.get_NodeSeries(item_index, attribute_index, start_index, num_steps), units
        elif object_type == "Link":
            item_index = self.output.get_LinkIndex(object_id)
            attribute_index = SMO.SMO_linkAttributes[SMO.SMO_linkAttributeNames.index(variable)]
            units = SMO.SMO_linkAttributeUnits[attribute_index][self.output.unit_system]
            return self.output.get_LinkSeries(item_index, attribute_index, start_index, num_steps), units
        elif object_type == "Subcatchment":
            item_index = self.output.get_SubcatchmentIndex(object_id)
            attribute_index = SMO.SMO_subcatchAttributes[SMO.SMO_subcatchAttributeNames.index(variable)]
            units = SMO.SMO_subcatchAttributeUnits[attribute_index][self.output.unit_system]
            return self.output.get_SubcatchmentSeries(item_index, attribute_index, start_index, num_steps), units
        elif object_type == "System":
            attribute_index = SMO.SMO_systemAttributes[SMO.SMO_systemAttributeNames.index(variable)]
            units = SMO.SMO_systemAttributeUnits[attribute_index][self.output.unit_system]
            return self.output.get_SystemSeries(attribute_index, start_index, num_steps), units