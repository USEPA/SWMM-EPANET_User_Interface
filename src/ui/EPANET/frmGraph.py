import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from PyQt4.QtGui import QMessageBox
import matplotlib.pyplot as plt
from core.epanet.reports import Reports
from ui.convenience import all_list_items, selected_list_items
from ui.model_utility import transl8
from ui.EPANET.frmGraphDesigner import Ui_frmGraph
from Externals.epanet.outputapi.ENOutputWrapper import OutputObject, ENR_node_type, ENR_link_type
from core.graph import EPANET as graphEPANET

class frmGraph(QtGui.QMainWindow, Ui_frmGraph):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Graph_Se.htm"
        self.setupUi(self)
        self.cmdAdd.setVisible(False)
        self.cmdDelete.setVisible(False)
        self.cmdUp.setVisible(False)
        self.cmdDown.setVisible(False)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.rbnNodes, QtCore.SIGNAL("clicked()"), self.rbnNodes_Clicked)
        QtCore.QObject.connect(self.rbnLinks, QtCore.SIGNAL("clicked()"), self.rbnLinks_Clicked)

        QtCore.QObject.connect(self.rbnTime, QtCore.SIGNAL("clicked()"), self.rbnTime_Clicked)
        QtCore.QObject.connect(self.rbnProfile, QtCore.SIGNAL("clicked()"), self.rbnProfile_Clicked)
        QtCore.QObject.connect(self.rbnContour, QtCore.SIGNAL("clicked()"), self.rbnContour_Clicked)
        QtCore.QObject.connect(self.rbnFrequency, QtCore.SIGNAL("clicked()"), self.rbnFrequency_Clicked)
        QtCore.QObject.connect(self.rbnSystem, QtCore.SIGNAL("clicked()"), self.rbnSystem_Clicked)

        self.cboTime.currentIndexChanged.connect(self.cboTime_currentIndexChanged)

        self.lstToGraph.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        QtCore.QObject.connect(self.lstToGraph, QtCore.SIGNAL("itemSelectionChanged()"), self.select_on_map)
        self._main_form = main_form
        self.onObjectSelected = self._main_form.objectsSelected
        self.onObjectSelected.connect(self.set_selected_object)
        self.time_linked_graphs = []

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.report = Reports(project, output)
        self.cboTime.clear()
        if project and self.output:
            for time_index in range(0, self.output.num_periods):
                self.cboTime.addItem(self.output.get_time_string(time_index))
            self.rbnNodes.setChecked(True)
            self.rbnNodes_Clicked()

    def rbnNodes_Clicked(self):
        if self.rbnNodes.isChecked():
            self.gbxToGraph.setTitle(transl8("frmGraph", "Nodes to Graph", None))
            self.cboParameter.clear()
            self.cboParameter.addItems([att.name for att in ENR_node_type.Attributes])
            self.lstToGraph.clear()
            self.list_items = self.output.nodes
            self.lstToGraph.addItems(self.list_items.keys())

    def rbnLinks_Clicked(self):
        if self.rbnLinks.isChecked():
            self.gbxToGraph.setTitle(transl8("frmGraph", "Links to Graph", None))
            self.cboParameter.clear()
            self.cboParameter.addItems([att.name for att in ENR_link_type.Attributes])
            self.lstToGraph.clear()
            self.list_items = self.output.links
            self.lstToGraph.addItems(self.list_items.keys())

    def rbnTime_Clicked(self):
        self.cboParameter.setEnabled(True)
        self.gbxParameter.setEnabled(True)
        self.cboTime.setEnabled(False)
        self.gbxTime.setEnabled(False)
        self.gbxObject.setEnabled(True)
        self.rbnNodes.setEnabled(True)
        self.rbnLinks.setEnabled(True)
        self.gbxToGraph.setEnabled(True)
        self.lstToGraph.setEnabled(True)

    def rbnProfile_Clicked(self):
        self.cboParameter.setEnabled(True)
        self.gbxParameter.setEnabled(True)
        self.cboTime.setEnabled(True)
        self.gbxTime.setEnabled(True)
        self.gbxObject.setEnabled(False)
        # self.rbnNodes.setChecked(True)
        # self.rbnNodes.setEnabled(False)
        # self.rbnLinks.setEnabled(False)
        self.gbxToGraph.setEnabled(True)
        self.lstToGraph.setEnabled(True)

    def rbnContour_Clicked(self):
        self.cboParameter.setEnabled(True)
        self.gbxParameter.setEnabled(True)
        self.cboTime.setEnabled(True)
        self.gbxTime.setEnabled(True)
        self.gbxObject.setEnabled(False)
        self.rbnNodes.setEnabled(False)
        self.rbnLinks.setEnabled(False)
        self.gbxToGraph.setEnabled(False)
        self.lstToGraph.setEnabled(False)

    def rbnFrequency_Clicked(self):
        self.cboParameter.setEnabled(True)
        self.gbxParameter.setEnabled(True)
        self.cboTime.setEnabled(True)
        self.gbxTime.setEnabled(True)
        self.gbxObject.setEnabled(True)
        self.rbnNodes.setEnabled(True)
        self.rbnLinks.setEnabled(True)
        self.gbxToGraph.setEnabled(False)
        self.lstToGraph.setEnabled(False)

    def rbnSystem_Clicked(self):
        self.cboParameter.setEnabled(False)
        self.gbxParameter.setEnabled(False)
        self.cboTime.setEnabled(False)
        self.gbxTime.setEnabled(False)
        self.gbxObject.setEnabled(False)
        self.rbnNodes.setEnabled(False)
        self.rbnLinks.setEnabled(False)
        self.gbxToGraph.setEnabled(False)
        self.lstToGraph.setEnabled(False)

    def cboTime_currentIndexChanged(self):
        time_index = self.cboTime.currentIndex()
        if time_index >= 0:
            for graph in self.time_linked_graphs:
                graph[-1] = time_index
                graph[0](*graph[1:])

    def select_on_map(self):
        obj_lyr_group = None
        selected_items = []
        if self.rbnNodes.isChecked():
            obj_lyr_group = self._main_form.model_layers.nodes_layers
        elif self.rbnLinks.isChecked():
            obj_lyr_group = self._main_form.model_layers.links_layers
        if obj_lyr_group:
            del selected_items[:]
            for sitm in self.lstToGraph.selectedItems():
                selected_items.append(sitm.text())
            # for lyr in obj_lyr_group:
            #     self._main_form.select_named_items(lyr, selected_items)

    def set_selected_object(self, layer_name, object_ids):
        if layer_name and object_ids:
            can_select = False
            if (layer_name.lower().startswith("junction") or \
                  layer_name.lower().startswith("reserv") or \
                  layer_name.lower().startswith("tank") or \
                  layer_name.lower().startswith("source")) and \
                  self.rbnNodes.isChecked():
                can_select = True
            elif (layer_name.lower().startswith("pump") or \
                  layer_name.lower().startswith("valve") or \
                  layer_name.lower().startswith("pipe")) and \
                  self.rbnLinks.isChecked():
                can_select = True

            if can_select:
                for id in object_ids:
                    itms = self.lstToGraph.findItems(id, QtCore.Qt.MatchExactly)
                    if itms and len(itms) > 0:
                        for itm in itms:
                            itm.setSelected(True)

    def cmdOK_Clicked(self):
        parameter_label = self.cboParameter.currentText()
        if self.rbnNodes.isChecked():
            attribute = ENR_node_type.get_attribute_by_name(parameter_label)
        else:
            attribute = ENR_link_type.get_attribute_by_name(parameter_label)

        time_index = self.cboTime.currentIndex()

        if self.rbnTime.isChecked():  # TODO: use get_series instead of get_value if it is more efficient
            graphEPANET.plot_time(self.output, attribute, self.selected_items())

        if self.rbnSystem.isChecked():
            graphEPANET.plot_system_flow(self.output)

        if time_index < 0 and (self.rbnProfile.isChecked() or self.rbnFrequency.isChecked()):
            QMessageBox.information(None, self._main_form.model,
                                    "There is no time step currently selected.",
                                    QMessageBox.Ok)
        else:
            if self.rbnProfile.isChecked():
                items = self.selected_items()
                if len(items) < 2:  # if fewer than two items were selected, use all items
                    items = self.list_items.values()
                self.plot_profile(attribute, time_index, items)
            if self.rbnFrequency.isChecked():
                graphEPANET.plot_freq(self.output, attribute, time_index, self.list_items.values())

    def selected_items(self):
        names = selected_list_items(self.lstToGraph)
        items = []
        for name in names:
            items.append(self.list_items[name])
        return items

    def plot_profile(self, attribute, time_index, items):
        fig = plt.figure()
        if self.rbnNodes.isChecked():
            x_values = self.report.node_distances(items)
        else:
            x_values = range(0, len(items))
        self.time_linked_graphs.append([graphEPANET.update_profile, self.output, items, x_values,
                                        attribute, fig.number, time_index])
        graphEPANET.update_profile(self.output, items, x_values,
                                   attribute, fig.number, time_index)

    def cmdCancel_Clicked(self):
        self.close()
