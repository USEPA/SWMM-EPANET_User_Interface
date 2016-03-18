import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
import ui.convenience
from core.swmm.patterns import PatternType
from ui.SWMM.frmGenericPropertyEditorDesigner import Ui_frmGenericPropertyEditor


class cBox( QtGui.QComboBox ):
    def __init__( self, *args, **kwargs ):
        super( cBox, self ).__init__( *args, **kwargs)


class frmGenericPropertyEditor(QtGui.QMainWindow, Ui_frmGenericPropertyEditor):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # self.cboType.clear()
        # ui.convenience.set_combo_items(core.swmm.patterns.PatternType, self.cboType)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.tblGeneric.currentCellChanged.connect(self.tblGeneric_currentCellChanged)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        self.tblGeneric.setColumnCount(1)
        self.tblGeneric.setRowCount(4)
        self.tblGeneric.setVerticalHeaderLabels(("Aquifer Name","Porosity","Wilting Point","Upper Evap. Pattern"))

        led = QtGui.QLineEdit("New Name")
        self.tblGeneric.setItem(-1,1,QtGui.QTableWidgetItem(led.text()))

        led = QtGui.QLineEdit(str("0.5"))
        self.tblGeneric.setItem(0,1,QtGui.QTableWidgetItem(led.text()))

        led = QtGui.QLineEdit(str("0.15"))
        self.tblGeneric.setItem(1,1,QtGui.QTableWidgetItem(led.text()))

        combobox = QtGui.QComboBox()
        combobox.addItem('one')
        combobox.addItem('two')
        self.tblGeneric.setCellWidget(3, 0, combobox)

    def cmdOK_Clicked(self):
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def tblGeneric_currentCellChanged(self):
        row = self.tblGeneric.currentRow()
        col = self.tblGeneric.currentColumn()
        if row == 0:
            self.lblNotes.setText("Text for row 0")
        elif row == 1:
            self.lblNotes.setText("Text for row 1")
        elif row == 2:
            self.lblNotes.setText("Text for row 2")
        elif row == 3:
            self.lblNotes.setText("Text for row 3")