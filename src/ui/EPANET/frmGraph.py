import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAbstractItemView
import matplotlib.pyplot as plt
from core.epanet.reports import Reports
from ui.convenience import all_list_items, selected_list_items
from ui.model_utility import transl8
from ui.EPANET.frmGraphDesigner import Ui_frmGraph
from Externals.epanet.outputapi.ENOutputWrapper import OutputObject, ENR_node_type, ENR_link_type
from core.graph import EPANET as graphEPANET

class frmGraph(QMainWindow, Ui_frmGraph):

    def __init__(self, main_form):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Graph_Se.htm"
        self.setupUi(self)
        self.cmdAdd.setVisible(True)
        self.cmdDelete.setVisible(True)
        self.cmdUp.setVisible(True)
        self.cmdDown.setVisible(True)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.rbnNodes.clicked.connect(self.rbnNodes_Clicked)
        self.rbnLinks.clicked.connect(self.rbnLinks_Clicked)
        self.rbnTime.clicked.connect(self.rbnTime_Clicked)
        self.rbnProfile.clicked.connect(self.rbnProfile_Clicked)
        self.rbnContour.clicked.connect(self.rbnContour_Clicked)
        self.rbnFrequency.clicked.connect(self.rbnFrequency_Clicked)
        self.rbnSystem.clicked.connect(self.rbnSystem_Clicked)

        self.cboTime.currentIndexChanged.connect(self.cboTime_currentIndexChanged)

        self.cmdAdd.clicked.connect(self.add_element)
        self.cmdDelete.clicked.connect(self.delete_element)
        self.cmdUp.clicked.connect(self.moveup_element)
        self.cmdDown.clicked.connect(self.movedown_element)

        self.lstToGraph.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.lstToGraph.itemSelectionChanged.connect(self.select_on_map)
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
            self.rbnTime.setChecked(True)
            self.rbnNodes.setChecked(True)
            self.rbnTime_Clicked()
            self.rbnNodes_Clicked()
            self.add_element()

    def rbnNodes_Clicked(self):
        if self.rbnNodes.isChecked():
            self.gbxToGraph.setTitle(transl8("frmGraph", "Nodes to Graph", None))
            self.cboParameter.clear()
            attr_list = []
            for att in ENR_node_type.Attributes:
                if att.name == "Quality":
                    if self.project.options.quality.quality.value == 2: # 'chemical'
                        attr_list.append("Chemical")
                        # units = attribute.units(self.output.unit_system)
                    elif self.project.options.quality.quality.value == 3: # 'Age'
                        attr_list.append("Age")
                        # units = "hours"
                    elif self.project.options.quality.quality.value == 4:  # 'Trace'
                        attr_list.append("Trace " + self.project.options.quality.trace_node)
                        # units = "percent"
                else:
                    attr_list.append(att.name)

            self.cboParameter.addItems(attr_list)
            self.lstToGraph.clear()
            self.list_items = self.output.nodes
            self.add_element()
            # self.lstToGraph.addItems(self.list_items.keys())

    def rbnLinks_Clicked(self):
        if self.rbnLinks.isChecked():
            self.gbxToGraph.setTitle(transl8("frmGraph", "Links to Graph", None))
            self.cboParameter.clear()

            attr_list = []
            for att in ENR_link_type.Attributes:
                if att.name == "Quality":
                    if self.project.options.quality.quality.value == 2: # 'chemical'
                        attr_list.append("Chemical")
                        # units = attribute.units(self.output.unit_system)
                    elif self.project.options.quality.quality.value == 3: # 'Age'
                        attr_list.append("Age")
                        # units = "hours"
                    elif self.project.options.quality.quality.value == 4:  # 'Trace'
                        attr_list.append("Trace " + self.project.options.quality.trace_node)
                        # units = "percent"
                else:
                    attr_list.append(att.name)

            self.cboParameter.addItems(attr_list)
            self.lstToGraph.clear()
            self.list_items = self.output.links
            self.add_element()
            # self.lstToGraph.addItems(self.list_items.keys())

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
        self.cboParameter.setVisible(True)
        self.cboTime.setVisible(False)
        self.lstToGraph.setVisible(True)

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
        self.cboParameter.setVisible(True)
        self.cboTime.setVisible(True)
        self.lstToGraph.setVisible(True)
        if self.rbnProfile.isChecked():
            self.rbnNodes.setChecked(True)
            self.rbnNodes_Clicked()

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
        self.cboParameter.setVisible(True)
        self.cboTime.setVisible(True)
        self.lstToGraph.setVisible(False)

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
        self.cboParameter.setVisible(True)
        self.cboTime.setVisible(True)
        self.lstToGraph.setVisible(False)

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
        self.cboParameter.setVisible(False)
        self.cboTime.setVisible(False)
        self.lstToGraph.setVisible(False)

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


    def add_element(self):
        layers = None
        if self.rbnNodes.isChecked():
            layers = self._main_form.model_layers.nodes_layers
        elif self.rbnLinks.isChecked():
            layers = self._main_form.model_layers.links_layers
        if layers is None:
            return
        selected_prev = []
        for ind in range(0, self.lstToGraph.count()):
            selected_prev.append(self.lstToGraph.item(ind).text())
        selected_new = []
        for layer in layers:
            # from qgis.core import QgsVectorLayer()
            # layer = QgsVectorLayer()
            for f in layer.getSelectedFeatures():
                if not f['name'] in selected_new:
                    selected_new.append(f['name'])

        for n in selected_new:
            if not n in selected_prev:
                selected_prev.append(n)

        if len(selected_prev) > 0:
            self.lstToGraph.clear()
            self.lstToGraph.addItems(selected_prev)

    def delete_element(self):
        all = []
        selected = []
        for ind in range(0, self.lstToGraph.count()):
            itm = self.lstToGraph.item(ind)
            all.append(itm.text())
            if itm.isSelected():
                selected.append(itm.text())

        if len(selected) > 0:
            for s in selected:
                all.remove(s)
            self.lstToGraph.clear()
            self.lstToGraph.addItems(all)

    def moveup_element(self):
        current_row = self.lstToGraph.currentRow()
        if current_row - 1 >= 0:
            current_itm = self.lstToGraph.takeItem(current_row)
            self.lstToGraph.insertItem(current_row - 1, current_itm)
            self.lstToGraph.setCurrentRow(current_row - 1)
            current_itm.setSelected(True)

    def movedown_element(self):
        current_row = self.lstToGraph.currentRow()
        if current_row + 1 < self.lstToGraph.count():
            current_itm = self.lstToGraph.takeItem(current_row)
            self.lstToGraph.insertItem(current_row + 1, current_itm)
            self.lstToGraph.setCurrentRow(current_row + 1)
            current_itm.setSelected(True)

    def cmdOK_Clicked(self):
        if self.rbnTime.isChecked() or self.rbnProfile.isChecked():
            if self.lstToGraph.count() == 0 or len(self.selected_items()) == 0:
                QMessageBox.information(None, self._main_form.model, "Need to select model elements for graphing.", QMessageBox.Ok)
                return
        parameter_label = self.cboParameter.currentText()
        lqual_name = ""
        lqual_unit = ""
        if parameter_label.startswith("Chemical") or \
            parameter_label.startswith("Age") or \
            parameter_label.startswith("Trace"):
            lqual_name = parameter_label
            if lqual_name.startswith("Age"):
                lqual_unit = "hours"
            elif lqual_name.startswith("Trace"):
                lqual_unit = "percent"
            parameter_label = "Quality"

        if self.rbnNodes.isChecked():
            attribute = ENR_node_type.get_attribute_by_name(parameter_label)
        else:
            attribute = ENR_link_type.get_attribute_by_name(parameter_label)

        time_index = self.cboTime.currentIndex()

        if self.rbnTime.isChecked():  # TODO: use get_series instead of get_value if it is more efficient
            graphEPANET.plot_time(self.output, attribute, self.selected_items(), lqual_name, lqual_unit)

        if self.rbnSystem.isChecked():
            ljuncs = []
            lreserv = []
            for node_j in self.project.junctions.value:
                ljuncs.append(node_j.name)
            for node_res in self.project.reservoirs.value:
                lreserv.append(node_res.name)
            graphEPANET.plot_system_flow(self.output, ljuncs, lreserv)

        if time_index < 0 and (self.rbnProfile.isChecked() or self.rbnFrequency.isChecked()):
            QMessageBox.information(None, self._main_form.model,
                                    "There is no time step currently selected.",
                                    QMessageBox.Ok)
        else:
            if self.rbnProfile.isChecked():
                items = self.selected_items()
                if len(items) < 2:  # if fewer than two items were selected, use all items
                    items = self.list_items.values()
                self.plot_profile(attribute, time_index, items, lqual_name, lqual_unit)
            if self.rbnFrequency.isChecked():
                graphEPANET.plot_freq(self.output, attribute, time_index, self.list_items.values(), lqual_name, lqual_unit)

    def selected_items(self):
        names = selected_list_items(self.lstToGraph)
        items = []
        for name in names:
            items.append(self.list_items[name])
        return items

    def plot_profile(self, attribute, time_index, items, aname="", aunit=""):
        fig = plt.figure()
        if self.rbnNodes.isChecked():
            x_values = self.report.node_distances(items)
        else:
            x_values = range(0, len(items))
        self.time_linked_graphs.append([graphEPANET.update_profile, self.output, items, x_values,
                                        attribute, fig.number, time_index])
        graphEPANET.update_profile(self.output, items, x_values,
                                   attribute, fig.number, time_index, aname, aunit)

    def cmdCancel_Clicked(self):
        self.close()
