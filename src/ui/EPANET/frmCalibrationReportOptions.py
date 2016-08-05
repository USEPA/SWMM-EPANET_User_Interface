import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.help import HelpHandler
from ui.EPANET.frmCalibrationReportOptionsDesigner import Ui_frmCalibrationReportOptions
from ui.EPANET.frmCalibrationReport import frmCalibrationReport


class frmCalibrationReportOptions(QtGui.QMainWindow, Ui_frmCalibrationReportOptions):

    def __init__(self, main_form, project):
        QtGui.QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "epanet/src/src/Crea0079.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.project = project
        # limit what shows up in the combo box to only those with calibration data
        self.comboBox.addItems(['Demand','Head','Pressure','Quality','Flow','Velocity'])
        # this list needs to contain all nodes that have calibration data, just poplating with all junctions for now.
        for i in range(0, len(self.project.junctions.value)):
            self.listWidget.addItem(self.project.junctions.value[i].name)
        self._main_form = main_form
        self.listWidget.setItemSelected(self.listWidget.item(0),True)

    def cmdOK_Clicked(self):
        selected_name = ''
        for column_item in self.listWidget.selectedItems():
                selected_name = str(column_item.text())
        if selected_name:
          self._frmCalibrationReport = frmCalibrationReport(self._main_form, self.comboBox.currentText(), selected_name)
          self._frmCalibrationReport.show()
          self.close()

    def cmdCancel_Clicked(self):
        self.close()
