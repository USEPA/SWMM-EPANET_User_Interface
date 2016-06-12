import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmCalibrationDataDesigner import Ui_frmCalibrationData


class frmCalibrationData(QtGui.QMainWindow, Ui_frmCalibrationData):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.toolButton, QtCore.SIGNAL("clicked()"), self.toolButton_Clicked)
        # need to load table with selected file names
        self._main_form = main_form

    def toolButton_Clicked(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Select a Calibration File", '',
                                                      "Data files (*.DAT);;All files (*.*)")
        if file_name:
            self.tableWidget.setItem(self.tableWidget.currentRow()-1,1,QtGui.QTableWidgetItem(QtGui.QLineEdit(file_name).text()))

    def cmdOK_Clicked(self):
        # need to store selected file names
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
