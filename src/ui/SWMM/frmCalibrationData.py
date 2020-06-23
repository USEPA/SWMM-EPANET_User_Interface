import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from ui.SWMM.frmCalibrationDataDesigner import Ui_frmCalibrationData


class frmCalibrationData(QMainWindow, Ui_frmCalibrationData):

    def __init__(self, main_form, defaults):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/registeringcalibrationdata.htm"
        self.defaults = defaults
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.toolButton.clicked.connect(self.toolButton_Clicked)

        file_name = self.defaults.config.value("Calibration/File1")
        if file_name:
            self.tableWidget.setItem(0, 0, QTableWidgetItem(QLineEdit(file_name).text()))
        file_name = self.defaults.config.value("Calibration/File2")
        if file_name:
            self.tableWidget.setItem(1, 0, QTableWidgetItem(QLineEdit(file_name).text()))
        file_name = self.defaults.config.value("Calibration/File3")
        if file_name:
            self.tableWidget.setItem(2, 0, QTableWidgetItem(QLineEdit(file_name).text()))
        file_name = self.defaults.config.value("Calibration/File4")
        if file_name:
            self.tableWidget.setItem(3, 0, QTableWidgetItem(QLineEdit(file_name).text()))
        file_name = self.defaults.config.value("Calibration/File5")
        if file_name:
            self.tableWidget.setItem(4, 0, QTableWidgetItem(QLineEdit(file_name).text()))
        file_name = self.defaults.config.value("Calibration/File6")
        if file_name:
            self.tableWidget.setItem(5, 0, QTableWidgetItem(QLineEdit(file_name).text()))
        file_name = self.defaults.config.value("Calibration/File7")
        if file_name:
            self.tableWidget.setItem(6, 0, QTableWidgetItem(QLineEdit(file_name).text()))
        file_name = self.defaults.config.value("Calibration/File8")
        if file_name:
            self.tableWidget.setItem(7, 0, QTableWidgetItem(QLineEdit(file_name).text()))
        file_name = self.defaults.config.value("Calibration/File9")
        if file_name:
            self.tableWidget.setItem(8, 0, QTableWidgetItem(QLineEdit(file_name).text()))
        file_name = self.defaults.config.value("Calibration/File10")
        if file_name:
            self.tableWidget.setItem(9, 0, QTableWidgetItem(QLineEdit(file_name).text()))
        file_name = self.defaults.config.value("Calibration/File11")
        if file_name:
            self.tableWidget.setItem(10, 0, QTableWidgetItem(QLineEdit(file_name).text()))
        file_name = self.defaults.config.value("Calibration/File12")
        if file_name:
            self.tableWidget.setItem(11, 0, QTableWidgetItem(QLineEdit(file_name).text()))

        self._main_form = main_form

        if (main_form.program_settings.value("Geometry/" + "frmCalibrationData_geometry") and
                main_form.program_settings.value("Geometry/" + "frmCalibrationData_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmCalibrationData_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmCalibrationData_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def toolButton_Clicked(self):
        file_name, ftype = QFileDialog.getOpenFileName(self, "Select a Calibration File", '',
                                                      "Data files (*.DAT);;All files (*.*)")
        if file_name:
            self.tableWidget.setItem(self.tableWidget.currentRow()-1,1,QTableWidgetItem(QLineEdit(file_name).text()))

    def cmdOK_Clicked(self):
        # need to store selected file names
        item = self.tableWidget.item(0, 0)
        if item:
            self.defaults.config.setValue("Calibration/File1", item.text())
        else:
            self.defaults.config.setValue("Calibration/File1", '')

        item = self.tableWidget.item(1, 0)
        if item:
            self.defaults.config.setValue("Calibration/File2", item.text())
        else:
            self.defaults.config.setValue("Calibration/File2", '')

        item = self.tableWidget.item(2, 0)
        if item:
            self.defaults.config.setValue("Calibration/File3", item.text())
        else:
            self.defaults.config.setValue("Calibration/File3", '')

        item = self.tableWidget.item(3, 0)
        if item:
            self.defaults.config.setValue("Calibration/File4", item.text())
        else:
            self.defaults.config.setValue("Calibration/File4", '')

        item = self.tableWidget.item(4, 0)
        if item:
            self.defaults.config.setValue("Calibration/File5", item.text())
        else:
            self.defaults.config.setValue("Calibration/File5", '')

        item = self.tableWidget.item(5, 0)
        if item:
            self.defaults.config.setValue("Calibration/File6", item.text())
        else:
            self.defaults.config.setValue("Calibration/File6", '')

        item = self.tableWidget.item(6, 0)
        if item:
            self.defaults.config.setValue("Calibration/File7", item.text())
        else:
            self.defaults.config.setValue("Calibration/File7", '')

        item = self.tableWidget.item(7, 0)
        if item:
            self.defaults.config.setValue("Calibration/File8", item.text())
        else:
            self.defaults.config.setValue("Calibration/File8", '')

        item = self.tableWidget.item(8, 0)
        if item:
            self.defaults.config.setValue("Calibration/File9", item.text())
        else:
            self.defaults.config.setValue("Calibration/File9", '')

        item = self.tableWidget.item(9, 0)
        if item:
            self.defaults.config.setValue("Calibration/File10", item.text())
        else:
            self.defaults.config.setValue("Calibration/File10", '')

        item = self.tableWidget.item(10, 0)
        if item:
            self.defaults.config.setValue("Calibration/File11", item.text())
        else:
            self.defaults.config.setValue("Calibration/File11", '')

        item = self.tableWidget.item(11, 0)
        if item:
            self.defaults.config.setValue("Calibration/File12", item.text())
        else:
            self.defaults.config.setValue("Calibration/File12", '')

        self._main_form.program_settings.setValue("Geometry/" + "frmCalibrationData_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmCalibrationData_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
