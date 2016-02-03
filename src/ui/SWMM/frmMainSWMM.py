import os

os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
from src.ui.embed_ipython_new import EmbedIPython
#from src.ui.ui_utility import EmbedMap
from src.ui.ui_utility import *
from src.ui.model_utility import *
from PyQt4 import QtCore, QtGui
from src.ui.frmMain import frmMain
#from IPython import embed
#from RestrictedPython import compile_restricted
#import py_compile
import pymsgbox
import imp
from qgis.core import *
from qgis.gui import *
from src.core.coordinates import *
from src.core.inputfile import *
from src.core.epanet.project import *
from src.core.epanet.title import *
from src.core.epanet.curves import *
from src.core.epanet.labels import *
from src.core.epanet.patterns import *
from src.core.epanet.vertex import *
from src.core.epanet.options import *
from src.core.epanet.hydraulics import *

class frmMainSWMM(frmMain):
    def __init__(self, parent=None, *args):
        frmMain.__init__(self, parent)
        QtCore.QObject.connect(self.actionStdNewProjectMenu, QtCore.SIGNAL('triggered()'), self.std_newproj)
        QtCore.QObject.connect(self.actionStdNewProject, QtCore.SIGNAL('triggered()'), self.std_newproj)

        QtCore.QObject.connect(self.actionStdOpenProjMenu, QtCore.SIGNAL('triggered()'), self.std_openproj)
        QtCore.QObject.connect(self.actionStdOpenProj, QtCore.SIGNAL('triggered()'), self.std_openproj)
        self.model = 'SWMM'
        self.on_load(model=self.model)

    def std_newproj(self):
        pass

    def std_openproj(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Existing Project', '/', 'Inp files (*.net *.inp)')
        if len(filename) > 0:
           if os.path.splitext(filename)[1] == '.inp':
                self.model = 'SWMM'
           self.project = Project()
           try:
               self.project.read_file(filename)
               self.load_model(self.model)
           except:
               self.project = None
        pass

    def edit_options(self, itm, column):
        #pymsgbox.alert('edit options')
        mitm = itm
        if self.project == None or mitm.data(0, 0) != 'Options':
            return
        from src.ui.frmOptions import frmOptions
        dlg = frmOptions(self, self.project.options)
        dlg.show()
        result = dlg.exec_()
        if result == 1:
            pass

    def on_load(self, **kwargs):
        self.obj_tree = ObjectTreeView(model=kwargs['model'])
        self.obj_tree.itemDoubleClicked.connect(self.edit_options)
        layout = QVBoxLayout(self.tabProject)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.obj_tree)
        self.tabProject.setLayout(layout)
        self.setWindowTitle(self.model)

        self.obj_list = ObjectListView(model=kwargs['model'],ObjRoot='',ObjType='',ObjList=None)
        mlayout = self.dockw_more.layout()
        mlayout.addWidget(self.obj_list)
        self.dockw_more.setLayout(mlayout)

    def load_model(self, model):
        pass
