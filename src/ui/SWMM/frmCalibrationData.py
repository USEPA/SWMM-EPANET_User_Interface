import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from ui.SWMM.frmCalibrationDataDesigner import Ui_frmCalibrationData


class frmCalibrationData(QMainWindow, Ui_frmCalibrationData):

    def __init__(self, main_form):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/registeringcalibrationdata.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.toolButton.clicked.connect(self.toolButton_Clicked)
        # need to load table with selected file names
        self._main_form = main_form

    def toolButton_Clicked(self):
        file_name, ftype = QFileDialog.getOpenFileName(self, "Select a Calibration File", '',
                                                      "Data files (*.DAT);;All files (*.*)")
        if file_name:
            self.tableWidget.setItem(self.tableWidget.currentRow()-1,1,QTableWidgetItem(QLineEdit(file_name).text()))

    def cmdOK_Clicked(self):
        # need to store selected file names
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
