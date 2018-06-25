import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QFileDialog
import core.epanet.calibration as pcali
from ui.help import HelpHandler
from ui.EPANET.frmCalibrationDataDesigner import Ui_frmCalibrationData
import os, sys

class frmCalibrationData(QMainWindow, Ui_frmCalibrationData):

    def __init__(self, main_form):
        QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "epanet/src/src/Register.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.toolButton.clicked.connect(self.toolButton_Clicked)
        # need to load table with selected file names
        self.calibrations = None
        self.set_from(main_form.project)
        self._main_form = main_form

    def set_from(self, project):
        self.model = "EPANET"
        self.calibrations = project.calibrations
        for lcali in self.calibrations.value:
            #lcali = pcali.Calibration() #debug only
            lrow = -1
            if len(lcali.filename) > 0:
                if lcali.etype == pcali.ECalibrationType.DEMAND:
                    lrow = 0
                    pass
                elif lcali.etype == pcali.ECalibrationType.HEAD:
                    lrow = 1
                    pass
                elif lcali.etype == pcali.ECalibrationType.PRESSURE:
                    lrow = 2
                    pass
                elif lcali.etype == pcali.ECalibrationType.QUALITY:
                    lrow = 3
                    pass
                elif lcali.etype == pcali.ECalibrationType.FLOW:
                    lrow = 4
                    pass
                elif lcali.etype == pcali.ECalibrationType.VELOCITY:
                    lrow = 5
                    pass

                if lrow >= 0 and lrow <= 5:
                    litem = self.tableWidget.item(lrow, 0)
                    if litem == None:
                        litem = QTableWidgetItem(lcali.filename)
                        self.tableWidget.setItem(lrow,0,litem)
                    else:
                        #litem = QTableWidgetItem(lcali.filename)
                        litem.setText(lcali.filename)

            #self.tableWidget.setItem(lrow,1,QTableWidgetItem(QLineEdit(file_name).text()))
            pass

    def toolButton_Clicked(self):
        directory = self._main_form.program_settings.value("CaliDir", "")
        file_name, ftype = QFileDialog.getOpenFileName(self, "Select a Calibration File", directory,
                                                      "Data files (*.DAT);;All files (*.*)")
        if file_name:
            #self.tableWidget.setItem(self.tableWidget.currentRow()-1,1,QTableWidgetItem(QLineEdit(file_name).text()))
            self.tableWidget.setItem(self.tableWidget.currentRow()-1,1,QTableWidgetItem(file_name))
            pass

    def cmdOK_Clicked(self):
        # need to store selected file names
        # Updates names of calibration files in database
        # with the entries in the grid control.
        if self.calibrations == None:
            return

        rowHeader = ""
        litem = None
        lcali = None
        ltype = pcali.ECalibrationType.NONE
        lis_flow = None
        for lrow in xrange(0, self.tableWidget.rowCount()):
            litem = self.tableWidget.item(lrow, 0)
            if litem == None:
                continue
            rowHeader = self.tableWidget.verticalHeaderItem(lrow).text()
            if "DEMAND" in rowHeader.upper():
                ltype = pcali.ECalibrationType.DEMAND
                lis_flow = False
            elif "HEAD" in rowHeader.upper():
                ltype = pcali.ECalibrationType.HEAD
                lis_flow = False
            elif "PRESSURE" in rowHeader.upper():
                ltype = pcali.ECalibrationType.PRESSURE
                lis_flow = False
            elif "QUALITY" in rowHeader.upper():
                ltype = pcali.ECalibrationType.QUALITY
                lis_flow = False
            elif "FLOW" in rowHeader.upper():
                ltype = pcali.ECalibrationType.FLOW
                lis_flow = True
            elif "VELOCITY" in rowHeader.upper():
                ltype = pcali.ECalibrationType.VELOCITY
                lis_flow = True

            #lcali = self.calibrations.value[ltype]
            lcali = self.calibrations.find_item(ltype.name)
            if lcali == None:
                lcali = pcali.Calibration(litem.text().strip())
                self.calibrations.value.append(lcali)
            else:
                lneed_to_read_data = False
                if litem.text().strip().upper() == lcali.filename.upper():
                    #no need to read data again
                    if lcali.status == pcali.ECalibrationFileStatus.ReadToCompletion:
                        pass
                    else:
                        lneed_to_read_data = True
                else:
                    lneed_to_read_data = True

                if lneed_to_read_data:
                    lcali.filename = litem.text().strip()
                    lcali.read_data()
            lcali.etype = ltype
            lcali.name = ltype.name
            lcali.is_flow = lis_flow

            if os.path.exists(lcali.filename):
                self._main_form.program_settings.setValue("CaliDir", os.path.dirname(lcali.filename))
                self._main_form.program_settings.sync()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
