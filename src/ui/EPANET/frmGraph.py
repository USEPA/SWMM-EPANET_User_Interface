import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import matplotlib.pyplot as plt
import core.epanet.project
from core.epanet.reports import Reports
from ui.model_utility import transl8
from ui.EPANET.frmGraphDesigner import Ui_frmGraph
from Externals.epanet.outputapi.ENOutputWrapper import *
from Externals.epanet.outputapi.outputapi import ENR_demand, ENR_head, ENR_pressure, ENR_quality

class frmGraph(QtGui.QMainWindow, Ui_frmGraph):

    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
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
        self._parent = parent
        self.time_linked_graphs = []

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.report = Reports(project, output)
        self.cboTime.clear()
        if project and self.output:
            for time_index in range(0, self.output.numPeriods - 1):
                self.cboTime.addItem(self.report.get_time_string(time_index))
            self.rbnNodes.setChecked(True)
            self.rbnNodes_Clicked()

    def rbnNodes_Clicked(self):
        if self.rbnNodes.isChecked():
            self.gbxToGraph.setTitle(transl8("frmGraph", "Nodes to Graph", None))
            self.cboParameter.clear()
            self.cboParameter.addItems(ENR_NodeAttributeNames)
            self.lstToGraph.clear()
            # for index in range(0, self.output.nodeCount - 1):
            #     self.lstToGraph.addItem(str(self.output.get_NodeID(index)))
            for node_id in self.report.all_node_ids():
                self.lstToGraph.addItem(node_id)

    def rbnLinks_Clicked(self):
        if self.rbnLinks.isChecked():
            self.gbxToGraph.setTitle(transl8("frmGraph", "Links to Graph", None))
            self.cboParameter.clear()
            self.cboParameter.addItems(ENR_LinkAttributeNames)
            self.lstToGraph.clear()
            self.lstToGraph.addItems(self.report.all_link_ids())

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
        for graph in self.time_linked_graphs:
            graph[-1] = time_index
            graph[0](*graph[1:])

    def cmdOK_Clicked(self):
        if self.rbnNodes.isChecked():
            get_index = self.output.get_NodeIndex
            get_value = self.output.get_NodeValue
            parameter_code = ENR_NodeAttributes[self.cboParameter.currentIndex()]
        else:
            get_index = self.output.get_LinkIndex
            get_value = self.output.get_LinkValue
            parameter_code = ENR_NodeAttributes[self.cboParameter.currentIndex()]

        parameter_label = self.cboParameter.currentText()
        time_index = self.cboTime.currentIndex()

        if self.rbnTime.isChecked():
            self.plot_time(get_index, get_value, parameter_code, parameter_label)

        if self.rbnProfile.isChecked():
            self.plot_profile(get_index, get_value, parameter_code, parameter_label, time_index)

        if self.rbnFrequency.isChecked():
            self.plot_freq(get_index, get_value, parameter_code, parameter_label, time_index)

        if self.rbnSystem.isChecked():
            self.plot_system_flow()

        # self.close()

    def plot_time(self, get_index, get_value, parameter_code, parameter_label):
        fig = plt.figure()
        title = "Time Series Plot of " + parameter_label
        fig.canvas.set_window_title(title)
        plt.title(title)
        x_values = []
        for time_index in range(0, self.output.numPeriods - 1):
            x_values.append(self.report.elapsed_hours_at_index(time_index))

        for list_item in self.lstToGraph.selectedItems():
            id = str(list_item.text())
            output_index = get_index(id)
            y_values = []
            for time_index in range(0, self.output.numPeriods - 1):
                y_values.append(get_value(output_index, time_index, parameter_code))
            plt.plot(x_values, y_values, label=id)

        # fig.suptitle("Time Series Plot")
        plt.ylabel(parameter_label)
        plt.xlabel("Time (hours)")
        plt.grid(True)
        plt.legend()
        plt.show()

    def plot_profile(self, get_index, get_value, parameter_code, parameter_label, time_index):
        fig = plt.figure()
        graph_ids = []
        for list_item in self.lstToGraph.selectedItems():
            graph_ids.append(str(list_item.text()))
        if not graph_ids:
            graph_ids = self.report.all_node_ids()

        if self.rbnNodes.isChecked():
            x_values = self.report.node_distances(graph_ids)
        else:
            x_values = range(0, len(graph_ids))

        self.time_linked_graphs.append(
            [self.update_profile, graph_ids, x_values, get_index, get_value, parameter_code, parameter_label, fig.number, time_index])
        self.update_profile(graph_ids, x_values, get_index, get_value, parameter_code, parameter_label, fig.number, time_index)

    def update_profile(self, graph_ids, x_values, get_index, get_value, parameter_code, parameter_label, fig_number, time_index):
        fig = plt.figure(fig_number)
        fig.clear()
        title = "Profile Plot of " + parameter_label + " at " + self.report.get_time_string(time_index)
        fig.canvas.set_window_title(title)
        plt.title(title)
        y_values = []
        min_y = 999.9


        for (graph_id, x_value) in zip(graph_ids, x_values):
            output_index = get_index(graph_id)
            y = get_value(output_index, time_index, parameter_code)
            if min_y == 999.9 or y < min_y:
                min_y = y
            y_values.append(y)
            plt.annotate(
                graph_id,
                xy=(x_value, y), xytext=(0, 20),
                textcoords='offset points', ha='center', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
            #, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        plt.fill_between(x_values, y_values, min_y)

        plt.ylabel(parameter_label)
        plt.xlabel("Index")
        plt.grid(True)
        plt.show()

    def plot_freq(self, get_index, get_value, parameter_code, parameter_label, time_index):
        fig = plt.figure()
        title = "Distribution of " + parameter_label + " at " + self.report.get_time_string(time_index)
        fig.canvas.set_window_title(title)
        plt.title(title)
        items = self.lstToGraph.selectedItems()
        count = len(items)
        percent = []
        values = []
        index = 0
        for list_item in items:
            percent.append(index * 100 / count)
            index += 1
            id = str(list_item.text())
            output_index = get_index(id)
            values.append(get_value(output_index, time_index, parameter_code))

        values.sort()
        # Cumulative distributions:
        plt.plot(values, percent)  # From 0 to the number of data points-1
        # plt.step(values[::-1], np.arange(len(values)))  # From the number of data points-1 to 0

        plt.ylabel("Percent Less Than")
        plt.xlabel(parameter_label)
        plt.grid(True)
        plt.show()

    def plot_system_flow(self):
        fig = plt.figure()
        title = "System Flow Balance"
        fig.canvas.set_window_title(title)
        plt.title(title)
        x_values = []
        produced = []
        consumed = []
        for time_index in range(0, self.output.numPeriods - 1):
            x_values.append(self.report.elapsed_hours_at_index(time_index))
            produced.append(0)
            consumed.append(0)

        for node_index in range(0, self.output.nodeCount - 1):
            node_flows = self.output.get_NodeSeries(node_index, ENR_demand)
            for time_index in range(0, self.output.numPeriods - 1):
                flow = node_flows[time_index]
                if flow > 0:
                    consumed[time_index] += flow
                else:
                    produced[time_index] -= flow

        plt.plot(x_values, consumed, label="Consumed")
        plt.plot(x_values, produced, label="Produced")

        # fig.suptitle("Time Series Plot")
        plt.ylabel("Flow")
        plt.xlabel("Time (hours)")
        plt.grid(True)
        plt.legend()
        plt.show()

    #  Rstart        : Longint;              //Start of reporting period (sec) = output.reportStart
    #  Rstep         : Longint;              //Interval between reporting (sec) = output.reportStep
    #  PRODUCED = 0;
    #  CONSUMED = 1;
    # // Refreshes the display of a system flow plot.
    # //---------------------------------------------
    # var
    #   j, k       : Integer;
    #   n, n1, n2  : Integer;
    #   dt         : Single;
    #   x          : Single;
    #   sysflow    : Array[PRODUCED..CONSUMED] of Double;
    # begin
    # //Determine number of points to plot
    #   n1 := 0;
    #   n2 := Nperiods - 1;
    #   n  := n2 - n1 + 1;
    #   dt := Rstep/3600.;
    #
    # //Fill in system flow time series
    #   for k := PRODUCED to CONSUMED do
    #   begin
    #     Chart1.Series[k].Clear;
    #     Chart1.Series[k].Active := False;
    #   end;
    #   x := (Rstart + n1*Rstep)/3600;
    #   for j := 0 to n-1 do
    #   begin
    #     GetSysFlow(j,sysflow);
    #     for k := PRODUCED to CONSUMED do
    #       Chart1.Series[k].AddXY(x, sysflow[k], '', clTeeColor);
    #     x := x + dt;
    #   end;
    #   for k := PRODUCED to CONSUMED do Chart1.Series[k].Active := True;

    # procedure TGraphForm.GetSysFlow(const Period: Integer;
    #   var SysFlow: array of Double);
    # //--------------------------------------------------------------
    # // Sums up flow produced and consumed in network in time Period.
    # //--------------------------------------------------------------
    # var
    #   i,j,k: Integer;
    #   aNode: TNode;
    #   Z  : PSingleArray;
    # begin
    # // Allocate scratch array to hold nodal demands
    #   for i := PRODUCED to CONSUMED do SysFlow[i] := 0;
    #   GetMem(Z, Nnodes*SizeOf(Single));
    #   try
    #
    #   // Retrieve nodal demands from output file for time Period
    #     k := NodeVariable[DEMAND].SourceIndex[JUNCS];
    #     GetNodeValues(k,Period,Z);
    #
    #   // Update total consumption/production depending on sign of demand
    #     for i := JUNCS to RESERVS do
    #     begin
    #       for j := 0 to Network.Lists[i].Count-1 do
    #       begin
    #         aNode := Node(i,j);
    #         k := aNode.Zindex;
    #         if k >= 0 then
    #         begin
    #           if Z[k] > 0 then SysFlow[CONSUMED] := SysFlow[CONSUMED] + Z[k]
    #           else SysFlow[PRODUCED] := SysFlow[PRODUCED] - Z[k];
    #         end;
    #       end;
    #     end;
    #   finally
    #     FreeMem(Z, Nnodes*SizeOf(Single));

    def cmdCancel_Clicked(self):
        self.close()
