from PyQt4 import QtCore, QtGui
from frmOptionsDesigner import Ui_diagOptions
import pymsgbox

class frmOptions(QtGui.QDialog):
    def __init__(self, parent=None, *args):
        self.parent = parent
        QtGui.QDialog.__init__(self)
        self.ui = Ui_diagOptions()
        self.ui.setupUi(self)
        self.options = args[0]
        #QtCore.QObject.connect(self.ui.btnBox, QtCore.SIGNAL("rejected()"), self.btnBox_Rejected)
        self.ui.tableOptions.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.ui.tableOptions.itemChanged.connect(self.itemChanged)
        self.setupOptions()

    def setupOptions(self):
        p = self.add_root('Options', 'Value')
        self.add_child(p, 'Accuracy',self.options.accuracy)
        self.add_child(p, 'frequency', self.options.check_frequency)
        self.add_child(p, 'damp limit', self.options.damp_limit)
        #self.add_child(p, 'pattern', self.options.default_pattern)
        self.add_child(p, 'multiplier', self.options.demand_multiplier)
        self.add_child(p, 'exponent', self.options.emitter_exponent)

    def add_root(self, name, data):
        itm = QtGui.QTreeWidgetItem(self.ui.tableOptions, [name])
        itm.setFirstColumnSpanned(False)
        itm.setText(0, name)
        itm.setText(1, data)
        #itm.setData(0, QtCore.Qt.UserRole, name)
        #itm.setData(1, QtCore.Qt.UserRole, data)
        #self.ui.tableOptions.addTopLevelItem(itm)
        return itm

    def add_child(self, p_itm, name, data):
        itm = QtGui.QTreeWidgetItem(p_itm, [name])
        itm.setFirstColumnSpanned(False)
        itm.setText(0, name)
        itm.setText(1, str(data))
        #itm.setData(0, QtCore.Qt.UserRole, name)
        #itm.setData(1, QtCore.Qt.UserRole, data)
        p_itm.addChild(itm)

    def itemChanged(self, itm, column):
        if itm.text(0) == 'Accuracy':self.options.accuracy = float(itm.text(1))
        elif itm.text(0) == 'frequency': self.options.check_frequency= float(itm.text(1))
        elif itm.text(0) == 'damp limit': self.options.damp_limit= float(itm.text(1))
        elif itm.text(0) == 'pattern': self.options.default_pattern= itm.text(1)
        elif itm.text(0) == 'multiplier': self.options.demand_multiplier= float(itm.text(1))
        elif itm.text(0) == 'exponent': self.options.emitter_exponent= float(itm.text(1))

    def itemDoubleClicked(self, itm, column):
        tmp = itm.flags()
        if (self.isEditable(itm, column)):
            itm.setFlags(tmp | QtCore.Qt.ItemIsEditable)
        else:
            itm.setFlags(tmp ^ QtCore.Qt.ItemIsEditable)

    def isEditable(self, itm, column):
        if column == 1:
            return True
        else:
            return False

class ComboBoxOptionItem(QtGui.QComboBox):
    def __init__(self, parent=None, *args):
        self.parent = parent
        QtGui.QComboBox.__init__(parent)
        #self.item = QtGui.QTreeWidgetItem()
        #self.column = 1
        self.item = args[0] #assume passing in a QTreeWidgetItem
        self.column = args[1]
        QtCore.QObject.connect(self, QtCore.SIGNAL('currentIndexChanged(int)'), self.change_item)

    def change_item(self, int):
        self.item.setText(self.column, self.currentText())


