from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog
from frmMapAddVectorDesigner import Ui_frmAddVectorLayer

class frmMapAddVector(QDialog):
    def __init__(self, main_form=None, *args):
        self._main_form = main_form
        QDialog.__init__(self)
        self.ui = Ui_frmAddVectorLayer()
        self.ui.setupUi(self)
        self.specs = {}
        self.ui.cboEncoding.addItem("System")
        self.ui.cboEncoding.addItem("UTF-8")
        self.ui.cboEncoding.currentIndexChanged.connect(self.cboEncoding_currentIndexChanged)
        self.ui.btnBrowse.clicked.connect(self.btnBrowse_Clicked)
        #QtCore.QObject.connect(self.ui.btnBox, QtCore.SIGNAL("clicked(QAbstractButton)"), self.btnBox_Clicked)
        self.ui.btnBox.accepted.connect(self.btnBox_Accepted)
        self.ui.btnBox.rejected.connect(self.btnBox_Rejected)

    def cboEncoding_currentIndexChanged(self):
        pass

    def btnBrowse_Clicked(self):
        filename, ftype = QFileDialog.getOpenFileName(None, 'Specify Vector Dataset', '/', 'Shapefiles (*.shp)')
        self.ui.txtDataset.setText(filename)
        self.specs['filename'] = filename

    def btnBox_Clicked(self, btn):
        if len(self.ui.txtDataset.text().strip()) == 0:
            QMessageBox.information(None, "Add Vector Layer",  "Need to specify a data file", QMessageBox.Ok)
            pass

    def btnBox_Accepted(self):
        filename = self.ui.txtDataset.text.strip()
        if len(filename) == 0:
            QMessageBox.information(None, "Add Vector Layer",  "Need to specify a data file", QMessageBox.Ok)
            return ''
        else:
            return filename

    def btnBox_Rejected(self):
        return ''

    def getLayerSpecifications(self):
        self.specs['filename'] = self.ui.txtDataset.text().strip()
        #self.specs.add['datatype'] = ''
        #self.specs.add['dataencoding'] = ''
        return self.specs
