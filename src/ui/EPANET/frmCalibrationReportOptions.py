import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.calibration as pcali
from ui.help import HelpHandler
from ui.EPANET.frmCalibrationReportOptionsDesigner import Ui_frmCalibrationReportOptions
from ui.EPANET.frmCalibrationReport import frmCalibrationReport


class frmCalibrationReportOptions(QtGui.QMainWindow, Ui_frmCalibrationReportOptions):

    def __init__(self, main_form, project):
        QtGui.QMainWindow.__init__(self, main_form)
        self.loaded = False
        self.helper = HelpHandler(self)
        self.help_topic = "epanet/src/src/Crea0079.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), \
                               self.comboBox_selChanged)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL("itemSelectionChanged(QString)"), \
                               self.listWidget_selChanged)
        self.project = project
        # limit what shows up in the combo box to only those with calibration data
        self.comboBox.addItems(['Demand','Head','Pressure','Quality','Flow','Velocity'])
        self._main_form = main_form
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        #self.listWidget.setItemSelected(self.listWidget.item(0),True)
        self.currentECaliType = None
        self.selected_nodes = []
        self.selected_pipes = []
        self.set_from(project)
        self.loaded = True

    def set_from(self, aproj):
        self.project = aproj
        self.current_calitype = None
        self.calibrations = self.project.calibrations
        for lcali in self.calibrations.value:
            #lcali = pcali.Calibration() #debug only
            if len(lcali.filename) > 0 and \
               lcali.status == pcali.ECalibrationFileStatus.ReadToCompletion:
                self.comboBox.setCurrentIndex(lcali.etype.value - 1)
                break
        pass

    def listWidget_selChanged(self):
        if not self.loaded:
            return
        if self.currentECaliType == pcali.ECalibrationType.DEMAND or \
           self.currentECaliType == pcali.ECalibrationType.HEAD or \
           self.currentECaliType == pcali.ECalibrationType.QUALITY or \
           self.currentECaliType == pcali.ECalibrationType.PRESSURE:
            # save selected nodes
            del self.selected_nodes[:]
            self.selected_nodes.append(self.listWidget.selectedItems())
        else:
            # save selected pipes
            del self.selected_pipes[:]
            self.selected_pipes.append(self.listWidget.selectedItems())

    def comboBox_selChanged(self):
        #if not self.loaded:
        #    return
        lselText = self.comboBox.currentText().upper()
        if lselText in pcali.ECalibrationType.DEMAND.name:
            self.currentECaliType = pcali.ECalibrationType.DEMAND
            self.set_items(False)
        elif lselText in pcali.ECalibrationType.HEAD.name:
            self.currentECaliType = pcali.ECalibrationType.HEAD
            self.set_items(False)
        elif lselText in pcali.ECalibrationType.PRESSURE.name:
            self.currentECaliType = pcali.ECalibrationType.PRESSURE
            self.set_items(False)
        elif lselText in pcali.ECalibrationType.QUALITY.name:
            self.currentECaliType = pcali.ECalibrationType.QUALITY
            self.set_items(False)
        elif lselText in pcali.ECalibrationType.FLOW.name:
            self.currentECaliType = pcali.ECalibrationType.FLOW
            self.set_items(True)
        elif lselText in pcali.ECalibrationType.VELOCITY.name:
            self.currentECaliType = pcali.ECalibrationType.VELOCITY
            self.set_items(True)
        pass

    def set_items(self, is_flow):
        self.listWidget.clear()
        # this list needs to contain all nodes that have calibration data, just poplating with all junctions for now.
        if is_flow:
            for i in range(0, len(self.project.pipes.value)):
                self.listWidget.addItem(self.project.pipes.value[i].name)
        else:
            for i in range(0, len(self.project.junctions.value)):
                self.listWidget.addItem(self.project.junctions.value[i].name)

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
