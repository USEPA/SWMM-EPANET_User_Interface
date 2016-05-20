import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import matplotlib.pyplot as plt
import core.epanet.project
from ui.model_utility import transl8
from ui.EPANET.frmGraphDesigner import Ui_frmGraph
from Externals.epanet.outputapi.ENOutputWrapper import *


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
        self.lstToGraph.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self._parent = parent

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboTime.clear()
        if self.output:
            for time_index in range(0, self.output.numPeriods - 1):
                self.cboTime.addItem(self.time_string(time_index))

    def rbnNodes_Clicked(self):
        if self.rbnNodes.isChecked():
            self.gbxToGraph.setTitle(transl8("frmGraph", "Nodes to Graph", None))
            self.cboParameter.clear()
            self.cboParameter.addItems(ENR_NodeAttributeNames)
            self.lstToGraph.clear()
            # for index in range(0, self.output.nodeCount - 1):
            #     self.lstToGraph.addItem(str(self.output.get_NodeID(index)))
            for nodes in (self.project.junctions, self.project.reservoirs, self.project.tanks):
                for node in nodes.value:
                    if self.output.get_NodeIndex(node.id) > -1:
                        self.lstToGraph.addItem(str(node.id))

    def rbnLinks_Clicked(self):
        if self.rbnLinks.isChecked():
            self.gbxToGraph.setTitle(transl8("frmGraph", "Links to Graph", None))
            self.cboParameter.clear()
            self.cboParameter.addItems(ENR_LinkAttributeNames)
            self.lstToGraph.clear()
            # for index in range(0, self.output.linkCount - 1):
            #     self.lstToGraph.addItem(str(self.output.get_LinkID(index)))
            for links in (self.project.pipes, self.project.pumps, self.project.valves):
                for link in links.value:
                    if self.output.get_LinkIndex(link.id) > -1:
                        self.lstToGraph.addItem(link.id)

    def cmdOK_Clicked(self):
        # section = self._parent.project.find_section(self.control_type)
        # section.set_text(str(self.txtControls.toPlainText()))

        import matplotlib.pyplot as plt1
        # plt1.plot([1,2,3,4])
        # plt1.ylabel('some numbers')
        # plt1.show()

        import numpy as np
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        # days, impressions = np.loadtxt("page-impressions.csv", unpack=True,
        # converters={ 0: mdates.strpdate2num('%Y-%m-%d')})

        if self.rbnTime.isChecked():
            if self.rbnNodes.isChecked():
                self.plot_time(self.output.get_NodeIndex,
                               self.output.get_NodeValue,
                               ENR_NodeAttributes[self.cboParameter.currentIndex()],
                               self.cboParameter.currentText())
            if self.rbnLinks.isChecked():
                self.plot_time(self.output.get_LinkIndex,
                               self.output.get_LinkValue,
                               ENR_LinkAttributes[self.cboParameter.currentIndex()],
                               self.cboParameter.currentText())

        if self.rbnProfile.isChecked():
            if self.rbnNodes.isChecked():
                self.plot_profile(self.output.get_NodeIndex,
                                  self.output.get_NodeValue,
                                  ENR_NodeAttributes[self.cboParameter.currentIndex()],
                                  self.cboParameter.currentText(),
                                  self.cboTime.currentIndex())

            if self.rbnLinks.isChecked():
                self.plot_profile(self.output.get_LinkIndex,
                                  self.output.get_LinkValue,
                                  ENR_LinkAttributes[self.cboParameter.currentIndex()],
                                  self.cboParameter.currentText(),
                                  self.cboTime.currentIndex())

                    # for node_item in [self.lstToGraph.item(i) for i in range(self.lstToGraph.count())]:
                # parameter_label = self.cboParameter.currentText()
                # parameter_code = self.cboParameter.currentIndex()
                # for list_item in self.lstToGraph.selectedItems():
                #     id = str(list_item.text())
                #     output_index = self.output.get_NodeIndex(id)
                #     x_values = []
                #     y_values = []
                #     for period in range(0, self.output.numPeriods - 1):
                #         x_values.append(period * self.output.reportStep / 3600)  # translate period into number of hours
                #         y_values.append(self.output.get_NodeValue(output_index, period, parameter_code))
                #
                #     plt.plot(x_values, y_values, label="Node " + id)
                # plt.title("Time Series Plot")
                # plt.ylabel(parameter_label)
                # plt.grid(True)
                # plt.show()



        # days = ['2012-01-23','2012-01-24','2012-01-25','2012-01-29','2012-01-30']
        # y_values = [3.0,4.1,5.0,2.3,3.1]
        # mdates.strpdate2num('%Y-%m-%d')
        # days_num = [mdates.strpdate2num.__call__(mdates.strpdate2num('%Y-%m-%d'), days[0]),
        #             mdates.strpdate2num.__call__(mdates.strpdate2num('%Y-%m-%d'), days[1]),
        #             mdates.strpdate2num.__call__(mdates.strpdate2num('%Y-%m-%d'), days[2]),
        #             mdates.strpdate2num.__call__(mdates.strpdate2num('%Y-%m-%d'), days[3]),
        #             mdates.strpdate2num.__call__(mdates.strpdate2num('%Y-%m-%d'), days[4])]
        #
        # plt.plot_date(x=days_num, y=y_values, fmt="r-")
        # plt.title("Example time series plot")
        # plt.ylabel("Flow")
        # plt.grid(True)
        # plt.show()

        self.close()

    def plot_time(self, get_index, get_value, parameter_code, parameter_label):
        fig = plt.figure()
        title = "Time Series Plot of " + parameter_label
        fig.canvas.set_window_title(title)
        plt.title(title)
        x_values = []
        for time_index in range(0, self.output.numPeriods - 1):
            x_values.append(time_index * self.output.reportStep / 3600)  # translate period into number of hours

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
        title = "Profile Plot of " + parameter_label + " at " + self.time_string(time_index)
        fig.canvas.set_window_title(title)
        plt.title(title)
        x_values = []
        y_values = []
        min_y = 999.9

        x = 0
        for list_item in self.lstToGraph.selectedItems():
            x += 1
            x_values.append(x)
            id = str(list_item.text())
            output_index = get_index(id)
            y = get_value(output_index, time_index, parameter_code)
            if min_y == 999.9 or y < min_y:
                min_y = y
            y_values.append(y)
            plt.annotate(
                id,
                xy=(x, y), xytext=(0, 20),
                textcoords='offset points', ha='center', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
            #, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        plt.fill_between(x_values, y_values, min_y)

        # fig.suptitle("Time Series Plot")
        plt.ylabel(parameter_label)
        plt.xlabel("Index")
        plt.grid(True)
        plt.show()

    def time_string(self, time_index):
        hours = int(time_index * self.output.reportStep / 3600)
        minutes = int(time_index * self.output.reportStep / 600 - (hours * 60))
        return '{:02d}:{:02d}'.format(hours, minutes)

    def cmdCancel_Clicked(self):
        self.close()
