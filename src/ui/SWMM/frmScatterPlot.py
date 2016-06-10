import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmScatterPlotDesigner import Ui_frmScatterPlot
from ui.help import HelpHandler
from core.graph import SWMM as graphSWMM

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
                    if self.output.subcatchments:
                        cboObjectType.addItem("Subcatchment")
                    if self.output.nodes:
                        cboObjectType.addItem("Node")
                    if self.output.links:
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
        items = self.output.get_items(cboObjectType.currentText())

        lst_ids.clear()
        for item in items:
            lst_ids.addItem(item.id)

        cboVariable.clear()
        if items:
            for variable in items[0].AttributeNames:
                cboVariable.addItem(variable)

    def cmdOK_Clicked(self):
        if not self.lstX.currentItem():
            QtGui.QMessageBox.information(None, "Scatter Plot",
                                    "X variable not set.",
                                          QtGui.QMessageBox.Ok)
        elif not self.lstY.currentItem():
            QtGui.QMessageBox.information(None, "Scatter Plot",
                                    "Y variable not set.",
                                          QtGui.QMessageBox.Ok)
        else:
            start_index = self.cboStart.currentIndex()
            end_index = self.cboEnd.currentIndex()
            num_steps = end_index - start_index + 1
            title = "Scatter Plot " + self.cboStart.currentText() + ' - ' + self.cboEnd.currentText()
            object_type_label_x = self.cboXCat.currentText()
            object_id_x = self.lstX.currentItem().text()
            attribute_name_x = self.cboVarX.currentText()
            object_type_label_y = self.cboYCat.currentText()
            object_id_y = self.lstY.currentItem().text()
            attribute_name_y = self.cboVarY.currentText()
            graphSWMM.plot_scatter(self.output, title,
                                   object_type_label_x, object_id_x, attribute_name_x,
                                   object_type_label_y, object_id_y, attribute_name_y, start_index, num_steps)

    def cmdCancel_Clicked(self):
        self.close()
