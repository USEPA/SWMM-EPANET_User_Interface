import os
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
import sys
from cStringIO import StringIO
from embed_ipython_new import EmbedIPython
#from ui.ui_utility import EmbedMap
from ui.ui_utility import *
from ui.model_utility import *
from PyQt4 import QtCore, QtGui
from frmMainDesigner import Ui_frmMain
#from IPython import embed
#from RestrictedPython import compile_restricted
#import py_compile
import imp
# from qgis.core import *
# from qgis.gui import *

CURR = os.path.abspath(os.path.dirname('__file__'))

MainModule = "__init__"


class frmMain(QtGui.QMainWindow, Ui_frmMain):
    def __init__(self, parent=None, *args):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.project = None
        self.obj_tree = None
        self.obj_list = None
        self.plugins = self.get_plugins()
        self.populate_plugins_menu()
        # QtCore.QObject.connect(self.actionAdd_Vector, QtCore.SIGNAL('triggered()'), self.map_addvector)
        # QtCore.QObject.connect(self.actionAdd_Raster, QtCore.SIGNAL('triggered()'), self.map_addraster)
        QtCore.QObject.connect(self.actionIPython, QtCore.SIGNAL('triggered()'), self.script_ipython)
        QtCore.QObject.connect(self.actionExec, QtCore.SIGNAL('triggered()'), self.script_exec)
        # QtCore.QObject.connect(self.actionPan, QtCore.SIGNAL('triggered()'), self.setQgsMapTool)
        # QtCore.QObject.connect(self.actionZoom_in, QtCore.SIGNAL('triggered()'), self.setQgsMapTool)
        # QtCore.QObject.connect(self.actionZoom_out, QtCore.SIGNAL('triggered()'), self.setQgsMapTool)
        # QtCore.QObject.connect(self.actionZoom_full, QtCore.SIGNAL('triggered()'), self.zoomfull)
        # QtCore.QObject.connect(self.actionAdd_Feature, QtCore.SIGNAL('triggered()'), self.map_addfeature)
        QtCore.QObject.connect(self.actionStdSave, QtCore.SIGNAL('triggered()'), self.proj_save)
        QtCore.QObject.connect(self.actionStdSaveMenu, QtCore.SIGNAL('triggered()'), self.proj_save)
        QtCore.QObject.connect(self.actionStdSave_As, QtCore.SIGNAL('triggered()'), self.proj_save_as)
        QtCore.QObject.connect(self.actionStdRun_Simulation, QtCore.SIGNAL('triggered()'), \
                               self.proj_run_simulation)
        QtCore.QObject.connect(self.actionRun_SimulationMenu, QtCore.SIGNAL('triggered()'), \
                               self.proj_run_simulation)

        self.layers = []
    #     self.canvas = QgsMapCanvas(self, 'mapCanvas')
    #     self.canvas.setMouseTracking(True)
    #     self.map_widget = EmbedMap(session=self, mapCanvas=self.canvas)
    #     self.map_win = self.map.addSubWindow(self.map_widget, QtCore.Qt.Widget)
    #     if self.map_win:
    #         self.map_win.setGeometry(0, 0, 600, 400)
    #         self.map_win.setWindowTitle('Study Area Map')
    #         self.map_win.show()
    #
    # def setQgsMapTool(self):
    #     self.map_widget.setZoomInMode()
    #     self.map_widget.setZoomOutMode()
    #     self.map_widget.setPanMode()
    #
    # def map_pan(self):
    #     self.map_widget.setPanMode()
    #
    # def zoomfull(self):
    #     self.map_widget.zoomfull()
    #
    # def map_addfeature(self):
    #     self.map_widget.setAddFeatureMode()
    #
    # def onGeometryAdded(self):
    #     pymsgbox.alert('A new feature is added.')
    #
    # def showCoords(self, event):
    #     pass
    #
    # def mouseMoveEvent(self, event):
    #     pass
    #     x = event.x()
    #     y = event.y()
    #     p = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
    #     self.btnCoord.setText('x,y: {:}, {:}'.format(p.x(), p.y()))
    #
    # def eventFilter(self, source, event):
    #     if event.type() == QtCore.QEvent.MouseMove:
    #         if event.buttons() == QtCore.Qt.NoButton:
    #             pos = event.pos()
    #             x = pos.x()
    #             y = pos.y()
    #             p = self.map_widget.canvas.getCoordinateTransform().toMapCoordinates(x, y)
    #             self.btnCoord.setText('x,y: %s, %s' % (p.x()), p.y())
    #         else:
    #             pass
    #
    # def map_addvector(self):
    #     #pymsgbox.alert('add vector')
    #     from frmMapAddVector import frmMapAddVector
    #     dlg = frmMapAddVector(self)
    #     dlg.show()
    #     result = dlg.exec_()
    #     if result == 1:
    #         specs = dlg.getLayerSpecifications()
    #         filename = specs['filename']
    #         if filename.lower().endswith('.shp'):
    #             self.map_widget.addVectorLayer(filename)
    #
    # def map_addraster(self):
    #     filename = QtGui.QFileDialog.getOpenFileName(None, 'Specify Raster Dataset', '/')
    #     if len(filename) > 0:
    #         self.map_widget.addRasterLayer(filename)

    def populate_plugins_menu(self):
        if self.plugins:
            menu = self.menuPlugins
            for p in self.plugins:
                lnew_action = QtGui.QAction(p['name'], menu)
                lnew_action.setCheckable(True)
                menu.addAction(lnew_action)
                QtCore.QObject.connect(lnew_action, QtCore.SIGNAL('triggered()'), self.run_tier1_plugin)

    def get_plugins(self):
        found_plugins = []
        plugin_folder = os.path.join(CURR, "plugins")
        if not os.path.exists(plugin_folder):
            plugin_folder = os.path.normpath(os.path.join(CURR, "../../plugins"))
        if os.path.exists(plugin_folder):
            for folder_name in os.listdir(plugin_folder):
                location = os.path.join(plugin_folder, folder_name)
                if os.path.isdir(location) and MainModule + ".py" in os.listdir(location):
                    info = imp.find_module(MainModule, [location])
                    found_plugins.append({"name": folder_name, "info": info})
        return found_plugins

    def load_plugin(self, plugin):
        try:
            return imp.load_module(MainModule, *plugin["info"])
        except Exception as ex:
            QMessageBox.information(None, "Exception Loading Plugin", plugin['name'] + '\n' + str(ex), QMessageBox.Ok)
            return None

    def run_tier1_plugin(self):
        # pymsgbox.alert('called here.', 'main program')
        for p in self.plugins:
            if p['name'] == self.sender().text():
                lplugin = self.load_plugin(p)
                if lplugin:
                    create_menu = False
                    if hasattr(lplugin, 'plugin_create_menu'):
                        create_menu = lplugin.plugin_create_menu
                    if create_menu and self.sender().isChecked():
                        self.add_plugin_menu(lplugin)
                        return
                    elif create_menu and not self.sender().isChecked():
                        self.remove_plugin_menu(lplugin)
                        return
                    lplugin.run(self)
                return

    def add_plugin_menu(self, plugin):
        '''
        lnew_custom_menu = self.find_plugin_main_menu(plugin)
        if not lnew_custom_menu  == None:
            pass
            '''
        lnew_custom_menu = self.menubar.addMenu(plugin.plugin_name)
        lnew_custom_menu.menuTag = 'plugin_mainmenu_' + plugin.plugin_name
        Action1=QtGui.QAction('Menu 1 0',self)
        Action1.setVisible(False)
        Action1.triggered.connect(self.action_1)
        lnew_custom_menu.addAction(Action1)
        '''
        self.menuPluginCustom = QtGui.QMenu(self.menubar)
        self.menuPluginCustom.setObjectName("menu" + plugin.plugin_name)
        '''
        for m in plugin.__all__:
            lnewAction = QtGui.QAction(m, self)
            lnewAction.setStatusTip(m)
            lnewAction.setData(plugin.plugin_name + '|' + m)
            lnewAction.setCheckable(False)
            QtCore.QObject.connect(lnewAction, QtCore.SIGNAL('triggered()'), self.run_plugin_custom)
            lnew_custom_menu.addAction(lnewAction)

    def find_plugin_main_menu(self, plugin):
        lfound = False
        for qm in self.menubar.children():
            if hasattr(qm, 'menuTag'):
                if qm.menuTag == 'plugin_mainmenu_' + plugin.plugin_name:
                    return qm
        if not lfound:
            return None

    def remove_plugin_menu(self, plugin):
        lcustom_pluginmenu = self.find_plugin_main_menu(plugin)
        if lcustom_pluginmenu  == None:
            pass
        else:
            lcustom_pluginmenu.clear()
            menu_act = lcustom_pluginmenu.menuAction()
            self.menubar.removeAction(menu_act)
            menu_act.deleteLater()
            lcustom_pluginmenu.deleteLater()
            '''
            lplugins2remove = []
            for a in lcustom_pluginmenu.actions():
                lplugins2remove.append(a)
            for p in lplugins2remove:
                lcustom_pluginmenu.removeAction(p)
            for p in self.menubar.actions():
                lstop = 'stop here'
            '''

    def run_plugin_custom(self):
        ltxt = str(self.sender().data())
        (plugin_name, method_name) = ltxt.split('|', 2)
        for p in self.plugins:
            if p['name'] == plugin_name:
                lp = self.load_plugin(p)
                if lp:
                    lp.run(self, int(lp.__all__[str(method_name)]))
                    return

    def action_1(self):
        pass

    def script_ipython(self):
        widget = EmbedIPython(session=self, plugins=self.plugins, mainmodule=MainModule)
        ipy_win = self.map.addSubWindow(widget,QtCore.Qt.Widget)
        if ipy_win:
            ipy_win.show()

    def script_exec(self):
            file_name = QtGui.QFileDialog.getOpenFileName(self, "Select script to run", None, "All files (*.*)")
            if file_name:
                save_handle = sys.stdout
                try:
                    redirected_output = StringIO()
                    sys.stdout = redirected_output
                    session = self
                    with open(file_name, 'r') as myfile:
                        exec(myfile)
                    QMessageBox.information(None, "Finished Running Script",
                                            file_name + "\n" + redirected_output.getvalue(), QMessageBox.Ok)
                except Exception as ex:
                    QMessageBox.information(None, "Exception Running Script",
                                            file_name + '\n' + str(ex), QMessageBox.Ok)
                sys.stdout = save_handle

    def __unicode__(self):
        return unicode(self)


def print_process_id():
    print 'Process ID is:', os.getpid()
