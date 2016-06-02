from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox
from frmMapAddVectorDesigner import Ui_frmAddVectorLayer

class frmMapAddVector(QtGui.QDialog):
    def __init__(self, main_form=None, *args):
        self._main_form = main_form
        QtGui.QDialog.__init__(self)
        self.ui = Ui_frmAddVectorLayer()
        self.ui.setupUi(self)
        self.specs = {}
        self.ui.cboEncoding.addItem("System")
        self.ui.cboEncoding.addItem("UTF-8")
        QtCore.QObject.connect(self.ui.cboEncoding,
                               QtCore.SIGNAL("currentIndexChanged(QString)"),
                               self.cboEncoding_currentIndexChanged)
        QtCore.QObject.connect(self.ui.btnBrowse, QtCore.SIGNAL("clicked()"), self.btnBrowse_Clicked)
        #QtCore.QObject.connect(self.ui.btnBox, QtCore.SIGNAL("clicked(QAbstractButton)"), self.btnBox_Clicked)
        QtCore.QObject.connect(self.ui.btnBox, QtCore.SIGNAL("accepted()"), self.btnBox_Accepted)
        QtCore.QObject.connect(self.ui.btnBox, QtCore.SIGNAL("rejected()"), self.btnBox_Rejected)

    def cboEncoding_currentIndexChanged(self):
        pass

    def btnBrowse_Clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Specify Vector Dataset', '/', 'Shapefiles (*.shp)')
        self.ui.txtDataset.text = filename
        self.ui.txtDataset.setText(filename)
        self.specs['filename'] = filename

    def btnBox_Clicked(self, btn):
        choice = ""
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
        #self.specs['filename'] = self.ui.txtDataset.text
        #self.specs.add['datatype'] = ''
        #self.specs.add['dataencoding'] = ''
        return self.specs
