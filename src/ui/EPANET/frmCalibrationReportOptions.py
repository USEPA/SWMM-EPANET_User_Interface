import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.calibration as pcali
from ui.help import HelpHandler
from ui.EPANET.frmCalibrationReportOptionsDesigner import Ui_frmCalibrationReportOptions
from ui.EPANET.frmCalibrationReport import frmCalibrationReport


class frmCalibrationReportOptions(QtGui.QMainWindow, Ui_frmCalibrationReportOptions):

    def __init__(self, main_form, project, output):
        QtGui.QMainWindow.__init__(self, main_form)
        self.loaded = False
        self.helper = HelpHandler(self)
        self.help_topic = "epanet/src/src/Crea0079.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), \
                               self.comboBox_selChanged)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL("itemClicked(QListWidgetItem *)"), \
                               self.listWidget_clicked)
        self.project = project
        self.output = output
        # limit what shows up in the combo box to only those with calibration data
        self.comboBox.addItems(['Demand','Head','Pressure','Quality','Flow','Velocity'])
        self._main_form = main_form
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        #self.listWidget.setItemSelected(self.listWidget.item(0),True)
        self.currentECaliType = None
        self.selected_nodes = []
        self.selected_pipes = []
        self.isFlow = None
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

    def listWidget_clicked(self, item):
        if not self.loaded:
            return
        #w = QtGui.QWidget()
        #QtGui.QMessageBox.information(w, "Message", "clicked")
        if self.currentECaliType == pcali.ECalibrationType.DEMAND or \
           self.currentECaliType == pcali.ECalibrationType.HEAD or \
           self.currentECaliType == pcali.ECalibrationType.QUALITY or \
           self.currentECaliType == pcali.ECalibrationType.PRESSURE:
            # save selected nodes
            del self.selected_nodes[:]
            for sitm in self.listWidget.selectedItems():
                self.selected_nodes.append(sitm.text())
            #self.selected_nodes.append(self.listWidget.selectedItems())
            self.select_cali_data(self.currentECaliType, self.selected_nodes)
        else:
            # save selected pipes
            del self.selected_pipes[:]
            for sitm in self.listWidget.selectedItems():
                self.selected_pipes.append(sitm.text())
            #self.selected_pipes.append(self.listWidget.selectedItems())
            self.select_cali_data(self.currentECaliType, self.selected_pipes)

    def select_cali_data(self, aECaliType, aSelectedIDs):
        if self.calibrations is None:
            return
        for lcali in self.calibrations.value:
            if lcali.etype == aECaliType:
                for ldsid in lcali.hobjects:
                    if ldsid in aSelectedIDs:
                        lcali.hobjects[ldsid].is_selected = True
                    else:
                        lcali.hobjects[ldsid].is_selected = False

    def comboBox_selChanged(self):
        #if not self.loaded:
        #    return
        lselText = self.comboBox.currentText().upper()
        lcali = self.calibrations.find_item(lselText)
        if lselText in pcali.ECalibrationType.DEMAND.name:
            self.currentECaliType = pcali.ECalibrationType.DEMAND
            self.isFlow = False
        elif lselText in pcali.ECalibrationType.HEAD.name:
            self.currentECaliType = pcali.ECalibrationType.HEAD
            self.isFlow = False
        elif lselText in pcali.ECalibrationType.PRESSURE.name:
            self.currentECaliType = pcali.ECalibrationType.PRESSURE
            self.isFlow = False
        elif lselText in pcali.ECalibrationType.QUALITY.name:
            self.currentECaliType = pcali.ECalibrationType.QUALITY
            self.isFlow = False
        elif lselText in pcali.ECalibrationType.FLOW.name:
            self.currentECaliType = pcali.ECalibrationType.FLOW
            self.isFlow = True
        elif lselText in pcali.ECalibrationType.VELOCITY.name:
            self.currentECaliType = pcali.ECalibrationType.VELOCITY
            self.isFlow = True

        self.set_items(lcali)
        pass

    def set_items(self, aCali):
        self.listWidget.clear()
        #aCali = pcali.Calibration('') #debug only
        if aCali.is_flow:
            self.gbxMeasured.setTitle('Measured in Links:')
            if aCali is not None:
                for i in range(0, len(self.project.pipes.value)):
                    if self.project.pipes.value[i].name in aCali.hobjects:
                        self.listWidget.addItem(self.project.pipes.value[i].name)
        else:
            self.gbxMeasured.setTitle('Measured at Nodes:')
            if aCali is not None:
                for i in range(0, len(self.project.junctions.value)):
                    if self.project.junctions.value[i].name in aCali.hobjects:
                        self.listWidget.addItem(self.project.junctions.value[i].name)

    def cmdOK_Clicked(self):
        #selected_name = ''
        #for column_item in self.listWidget.selectedItems():
        #    selected_name = str(column_item.text())
        selected_name = self.selected_nodes
        if self.isFlow:
            selected_name = self.selected_pipes

        if len(selected_name) > 0:
            self._frmCalibrationReport = frmCalibrationReport(self._main_form,
                                                              self.project,
                                                              self.output,
                                                              self.currentECaliType)
            self._frmCalibrationReport.show()
            self.close()

    def cmdCancel_Clicked(self):
        self.close()
