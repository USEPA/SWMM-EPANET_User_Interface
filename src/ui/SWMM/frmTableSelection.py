import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmTableSelectionDesigner import Ui_frmTableSelection
from ui.SWMM.frmGenericListOutput import frmGenericListOutput
from ui.help import HelpHandler
import Externals.swmm.outputapi.SMOutputWrapper as SMO


class frmTableSelection(QtGui.QMainWindow, Ui_frmTableSelection):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/controlrules.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

        # self.set_from(parent.project)
        self._main_form = main_form
        self.cboObject.currentIndexChanged.connect(self.cboObject_currentIndexChanged)
        self.cboObject.setCurrentIndex(0)
        self.lstNodes.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.lstVariables.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboStart.clear()
        if project and self.output:
            self.cboTime.addItems(["Elapsed Time", "Date/Time"])
            self.cboObject.addItems(["Subcatchments", "Nodes", "Links"])
            for time_index in range(0, self.output.numPeriods):
                time_string = self.output.get_time_string(time_index)
                self.cboStart.addItem(time_string)
                self.cboEnd.addItem(time_string)
            self.cboStart.setCurrentIndex(0)
            self.cboEnd.setCurrentIndex(self.cboEnd.count() - 1)
            self.cboObject.setCurrentIndex(0)

    def cmdOK_Clicked(self):
        start_index = self.cboStart.currentIndex()
        end_index = self.cboEnd.currentIndex()
        num_steps = end_index - start_index + 1

        num_columns = 0
        headers = []
        headers.append('Date')
        for location in self.lstNodes.selectedIndexes():
            selected_location = str(location.data())
            for variable in self.lstVariables.selectedIndexes():
                selected_variable = str(variable.data())
                # for each selected location, for each selected variable
                x_values, x_units = self._get_values(self.lblNodes.text(),
                                                     location,
                                                     variable,
                                                     start_index, num_steps)
                headers.append(variable & ' at ' & self.lblNodes.text() & ' ' & location)
                num_columns += 1

        local_data = ['2012-01-23','2012-01-24','2012-01-25','2012-01-29','2012-01-30',3.0,4.1,5.0,2.3,3.1]
        headers = ['Date', 'Depth']

        self._frmOutputTable = frmGenericListOutput(self._main_form, "SWMM Table Output")
        self._frmOutputTable.set_data(num_steps, num_columns, headers, local_data)
        self._frmOutputTable.show()

        self.close()

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

    def cmdCancel_Clicked(self):
        self.close()

    def cboObject_currentIndexChanged(self, newIndex):
        if newIndex == 0: # subcatchments
            self.lblNodes.setText("Subcatchments")
            items = self.output.subcatchment_ids
            variables = SMO.SMO_subcatchAttributeNames
        elif newIndex == 1: # nodes
            self.lblNodes.setText("Nodes")
            items = self.output.node_ids
            variables = SMO.SMO_nodeAttributeNames
        elif newIndex == 2: # links
            self.lblNodes.setText("Links")
            items = self.output.link_ids
            variables = SMO.SMO_linkAttributeNames

        self.lstNodes.clear()
        for item in items:
            self.lstNodes.addItem(item)

        self.lstVariables.clear()
        for variable in variables:
            self.lstVariables.addItem(variable)

