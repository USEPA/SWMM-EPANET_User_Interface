import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ui.help import HelpHandler
from ui.SWMM.frmScatterPlotDesigner import Ui_frmScatterPlot
from ui.help import HelpHandler
from core.graph import SWMM as graphSWMM

class frmScatterPlot(QMainWindow, Ui_frmScatterPlot):

    def __init__(self, main_form):
        QMainWindow.__init__(self, main_form)
        self._main_form = main_form
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/scatterplotdialog.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.cboStart.currentIndexChanged.connect(self.cboStart_currentIndexChanged)
        self.cboEnd.currentIndexChanged.connect(self.cboEnd_currentIndexChanged)
        self.cboXCat.currentIndexChanged.connect(self.cboXCat_currentIndexChanged)
        self.cboYCat.currentIndexChanged.connect(self.cboYCat_currentIndexChanged)

        if (main_form.program_settings.value("Geometry/" + "frmScatterPlot_geometry") and
                main_form.program_settings.value("Geometry/" + "frmScatterPlot_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmScatterPlot_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmScatterPlot_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboStart.clear()
        if project and self.output:
            for time_index in range(0, self.output.num_periods):
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

    def cboObjectType_currentIndexChanged(self, cboObjectType, lst_names, cboVariable):
        items = self.output.get_items(cboObjectType.currentText())

        lst_names.clear()
        for item in items:
            lst_names.addItem(item)

        cboVariable.clear()
        if items:
            for item in items.values():
                for attribute in item.attributes:
                    cboVariable.addItem(attribute.name)
                break  # Only need variables from first item

    def cmdOK_Clicked(self):
        if not self.lstX.currentItem():
            QMessageBox.information(None, "Scatter Plot",
                                    "X variable not set.",
                                          QMessageBox.Ok)
        elif not self.lstY.currentItem():
            QMessageBox.information(None, "Scatter Plot",
                                    "Y variable not set.",
                                          QMessageBox.Ok)
        else:
            start_index = self.cboStart.currentIndex()
            end_index = self.cboEnd.currentIndex()
            num_steps = end_index - start_index + 1
            title = "Scatter Plot " + self.cboStart.currentText() + ' - ' + self.cboEnd.currentText()
            object_type_label_x = self.cboXCat.currentText()
            object_name_x = self.lstX.currentItem().text()
            attribute_name_x = self.cboVarX.currentText()
            object_type_label_y = self.cboYCat.currentText()
            object_name_y = self.lstY.currentItem().text()
            attribute_name_y = self.cboVarY.currentText()
            graphSWMM.plot_scatter(self.output, title,
                                   object_type_label_x, object_name_x, attribute_name_x,
                                   object_type_label_y, object_name_y, attribute_name_y, start_index, num_steps)

        self._main_form.program_settings.setValue("Geometry/" + "frmScatterPlot_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmScatterPlot_state", self.saveState())

    def cmdCancel_Clicked(self):
        self._main_form.program_settings.setValue("Geometry/" + "frmScatterPlot_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmScatterPlot_state", self.saveState())
        self.close()
