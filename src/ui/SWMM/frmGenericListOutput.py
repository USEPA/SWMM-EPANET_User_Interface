import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from ui.frmGenericPropertyEditorDesigner import Ui_frmGenericPropertyEditor


class frmGenericListOutput(QtGui.QMainWindow, Ui_frmGenericPropertyEditor):
    def __init__(self, parent, title):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.fraNotes.setVisible(False)
        self.cmdOK.setVisible(False)
        self.cmdCancel.setText('Close')

    def set_data(self, nrows, ncols, headers, data):
        counter = -1
        self.tblGeneric.setRowCount(nrows)
        self.tblGeneric.setColumnCount(ncols)
        self.tblGeneric.setHorizontalHeaderLabels(headers)
        self.tblGeneric.verticalHeader().setVisible(False)
        for col in range(ncols):
            for row in range(nrows):
                counter += 1
                led = QtGui.QLineEdit(str(data[counter]))
                item = QtGui.QTableWidgetItem(led.text())
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tblGeneric.setItem(row,col,item)

    def cmdCancel_Clicked(self):
        self.close()

