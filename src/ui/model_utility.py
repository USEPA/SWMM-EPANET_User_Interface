from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from enum import Enum

class SWMMTreeObjects(object):
    ObjRoot = ['Title/Notes','Options','Climatology', 'Hydrology', \
               'Hydraulics','Quality','Curves', 'Time Series', 'Time Patterns', 'Map Labels']
    ObjOptions = ['General','Dates','Time Steps','Dynamic Wave','Interface Files','Reporting','Map/Backdrop']
    ObjClimatology = ['Temperature','Evaporation','Wind Speed','Snow Melt','Areal Depletion',\
                      'Adjustment']
    ObjHydrology = ['Rain Gages','Subcatchments','Aquifers','Snow Packs','Unit Hydrographs', \
                    'LID Controls']
    ObjHydraulics = ['Nodes','Links','Transects','Controls']
    ObjQuality = ['Pollutants','Land Uses']
    ObjCurves = ['Control Curves','Diversion Curves','Pump Curves','Rating Curves','Shape Curves', \
                 'Storage Curves','Tidal Curves']

    ObjNodes = ['Junctions','Outfalls','Dividers','Storage Units']
    ObjLinks = ['Conduits','Pumps','Orifices','Weirs','Outlets']

class EPANETTreeObjects(object):
    ObjRoot = ['Title/Notes','Options','Junctions', 'Reservoirs', \
               'Tanks','Pipes', 'Pumps', 'Valves', 'Labels', 'Patterns', 'Curves', 'Controls']
    ObjOptions=['Hydraulics','Quality','Reactions','Times','Energy','Report','Map/Backdrop']
    ObjControls = ['Simple','Rule-Based']

class ObjectTreeView(QTreeWidget):
    def __init__(self, parent=None, **kwargs):
        super(ObjectTreeView, self).__init__(parent)
        self.model = kwargs['model'] #either SWMM or EPANET
        self.treeItems = None
        #self.setEditTriggers(QAbstractItemView.EditKeyPressed | QAbstractItemView.SelectedClicked)
        #self.setExpandsOnDoubleClick(False)
        #QtCore.QObject.connect(self, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem, int)'), self.edit_options)
        #self.itemDoubleClicked.connect(self.edit_options)
        if self.model == 'SWMM':
            self.treeItems = SWMMTreeObjects()
            self.setupUISWMM()
        elif self.model == 'EPANET':
            self.treeItems = EPANETTreeObjects()
            self.setupUIEPANET()

    def setupUIEPANET(self):
        self.setHeaderHidden(True)
        #self.addItems(self.invisibleRootItem())
        self.setColumnCount(1)
        #self.itemChanged.connect(self.handleChanged)
        for tnode in self.treeItems.ObjRoot:
            itm = self.addParent(self, 0, tnode, tnode)
            if tnode == 'Options':
                for cnode in self.treeItems.ObjOptions:
                    citm = self.addChild(itm,0, cnode, cnode)
            elif tnode == 'Controls':
                for cnode in self.treeItems.ObjControls:
                    citm = self.addChild(itm,0, cnode, cnode)

    def setupUISWMM(self):
        self.setHeaderHidden(True)
        #self.addItems(self.invisibleRootItem())
        self.setColumnCount(1)
        #self.itemChanged.connect(self.handleChanged)
        for tnode in self.treeItems.ObjRoot:
            itm = self.addParent(self, 0, tnode, tnode)
            if tnode == 'Options':
                for cnode in self.treeItems.ObjOptions:
                    citm = self.addChild(itm,0, cnode, cnode)
            elif tnode == 'Climatology':
                for cnode in self.treeItems.ObjClimatology:
                    citm = self.addChild(itm,0, cnode, cnode)
            elif tnode == 'Hydrology':
                for cnode in self.treeItems.ObjHydrology:
                    citm = self.addChild(itm,0, cnode, cnode)
            elif tnode == 'Hydraulics':
                for cnode in self.treeItems.ObjHydraulics:
                    citm = self.addChild(itm,0, cnode, cnode)
                    if cnode=='Nodes':
                        for cnode1 in self.treeItems.ObjNodes:
                            citm1 = self.addChild(citm,0, cnode1, cnode1)
                    elif cnode=='Links':
                        for cnode1 in self.treeItems.ObjLinks:
                            citm1 = self.addChild(citm,0, cnode1, cnode1)
            elif tnode == 'Quality':
                for cnode in self.treeItems.ObjQuality:
                    citm = self.addChild(itm,0, cnode, cnode)
            elif tnode == 'Curves':
                for cnode in self.treeItems.ObjCurves:
                    citm = self.addChild(itm,0, cnode, cnode)

    def addParent(self, parent, column, title, data):
        itm = QtGui.QTreeWidgetItem(parent, [title])
        itm.setData(column, QtCore.Qt.UserRole, data)
        itm.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        itm.setExpanded(True)
        return itm

    def addChild(self, parent, column, title, data):
        itm = QtGui.QTreeWidgetItem(parent, [title])
        itm.setData(column, QtCore.Qt.UserRole, data)
        return itm

    def edit_options(self, itm, column):
        pass

class ObjectListView(QListWidget):
    def __init__(self, parent=None, **kwargs):
        super(ObjectListView, self).__init__(parent)
        self.model = kwargs['model']
        self.ObjRoot = kwargs['ObjRoot']
        self.ObjType = kwargs['ObjType']
        self.ObjList = kwargs['ObjList']
        self.setupUI()

    def set_model(self, model):
        self.model = model
    def set_root(self, root):
        self.ObjRoot = root
    def set_type(self, type):
        self.ObjType = type
    def set_list(self, objList):
        self.ObjList = objList

    def setupUI(self):
        if self.ObjRoot == '':
            return
        for obj in self.ObjList:
            self.addItem(obj)
        pass

class StatusMonitor0(QtGui.QDialog):
    def __init__(self, cmd, args, parent=None, **kwargs):
        super(StatusMonitor0, self).__init__(parent)
        self.cmd = cmd
        self.args = args
        self.keepGoing = True
        self.prog = kwargs['model']

        layout = QVBoxLayout()
        self.output = QtGui.QTextEdit()
        self.butt = QPushButton('Close')
        self.setupConnections()
        self.setWindowTitle('Running ' + self.prog)
        layout.addWidget(self.output)
        layout.addWidget(self.butt)
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)
        self.butt.clicked.connect(self.close)

    def setupConnections(self):
        self.worker = Worker(self.cmd, self.args)
        self.worker.finished.connect(self.end_worker)
        self.worker.sendOutput.connect(self.showOutput)

    @QtCore.pyqtSlot(QString)
    def showOutput(self, output):
        self.output.append(output)

    def end_worker(self):
        self.worker.process.kill()
        del self.worker

    def closeEvent(self,event):
        event.accept()

class Worker(QtCore.QObject):
    sendOutput = QtCore.pyqtSignal(QString)
    finished = QtCore.pyqtSignal()
    def __init__(self, cmd, args):
        super(Worker, self).__init__()
        self.cmd = cmd
        self.args = args
        self.process = QtCore.QProcess()
        self.setupProcess()

    def setupProcess(self):
        self.process.readyReadStandardOutput.connect(self.readStdOutput)
        self.process.start(self.cmd, self.args)
        self.finished.emit()

    @QtCore.pyqtSlot()
    def readStdOutput(self):
        output = QString(self.process.readAllStandardOutput())
        self.sendOutput.emit(output)
