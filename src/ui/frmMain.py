import os, sys
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
from embed_ipython_new import EmbedIPython
from ui_utility import EmbedMap
from PyQt4 import QtCore, QtGui
from frmMainSWMMDesigner import Ui_frmMain
# import pymsgbox
import imp

CURR = os.path.abspath(os.path.dirname('__file__'))

PluginFolder = "./plugins"
MainModule = "__init__"
_plugins = []


class frmMain(QtGui.QMainWindow, Ui_frmMain):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.init_swmm()
        self.get_plugins()
        self.populatePlugins(_plugins)
        QtCore.QObject.connect(self.actionIPython, QtCore.SIGNAL('triggered()'), self.script_ipython)
        QtCore.QObject.connect(self.actionExec, QtCore.SIGNAL('triggered()'), self.script_exec)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL('triggered()'), self.action_exit)
        # map_widget = EmbedMap(session=self)
        # map_win = self.map.addSubWindow(map_widget, QtCore.Qt.Widget)
        # if map_win:
        #     map_win.setGeometry(0, 0, 600, 400)
        #     map_win.setWindowTitle('Study Area Map')
        #     map_win.show()

    def init_swmm(self):
        model = QtGui.QStandardItemModel()
        # model.setHorizontalHeaderLabels(['col1', 'col2', 'col3'])
        self.treeProject.setModel(model)
        model.appendRow(QtGui.QStandardItem("Title/Notes"))
        model.appendRow(QtGui.QStandardItem("Options"))
        model.appendRow(QtGui.QStandardItem("Climatology"))
        hydrology = QtGui.QStandardItem("Hydrology")
        hydrology.appendRow(QtGui.QStandardItem("Rain Gages"))
        hydrology.appendRow(QtGui.QStandardItem("Subcatchments"))
        hydrology.appendRow(QtGui.QStandardItem("Aquifers"))
        model.appendRow(hydrology)

    def populatePlugins(self, plugins):
        if len(plugins) > 0:
            menu = self.menuPlugins
            for p in plugins:
                """loaded = self.loadPlugin(p)
                entry = menu.addMenu(p['name'])"""
                lnew_action = QtGui.QAction(p['name'], menu)
                lnew_action.setCheckable(True)
                '''menu.addAction(QtGui.QAction(p['name'], menu, checkable=True))'''
                menu.addAction(lnew_action)
                QtCore.QObject.connect(lnew_action, QtCore.SIGNAL('triggered()'), self.run_tier1_plugin)

    def get_plugins(self):
        if not os.path.exists(PluginFolder):
            return _plugins
        possibleplugins = os.listdir(PluginFolder)
        for i in possibleplugins:
            location = os.path.join(PluginFolder, i)
            if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
                continue
            info = imp.find_module(MainModule, [location])
            _plugins.append({"name": i, "info": info})
        return _plugins

    def load_plugin(self, plugin):
        return imp.load_module(MainModule, *plugin["info"])

    def runscriptrestricted(self, src):
        lcode = 'for i in range(3):\n    print("Python is cool")'
        exec(lcode)

    def run_tier1_plugin(self):
        '''pymsgbox.alert('called here.', 'main program')'''
        for p in _plugins:
            if p['name'] == self.sender().text():
                lplugin = self.load_plugin(p)
                create_menu = False
                if hasattr(lplugin, 'plugin_create_menu'):
                    create_menu = lplugin.plugin_create_menu
                if create_menu and self.sender().isChecked():
                    self.add_plugin_menu(lplugin)
                    return
                elif create_menu and not self.sender().isChecked():
                    self.remove_plugin_menu(lplugin)
                    return
                elif hasattr(lplugin, "run"):
                    lplugin.run()
                elif hasattr(lplugin, "load"):
                    lplugin.load(self)
                return

    def add_plugin_menu(self, plugin):
        '''
        lnew_custom_menu = self.find_plugin_main_menu(plugin)
        if not lnew_custom_menu  == None:
            pass
            '''
        lnew_custom_menu = self.menubar.addMenu('P_' + plugin.plugin_name)
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
        for p in _plugins:
            if p['name'] == plugin_name:
               lp = self.load_plugin(p)
               if lp is not None:
                   lp.run(int(lp.__all__[str(method_name)]))
                   return

    def action_1(self):
        pass

    def script_ipython(self):
        widget = EmbedIPython(session=self, plugins=_plugins, mainmodule=MainModule)
        ipy_win = self.map.addSubWindow(widget,QtCore.Qt.Widget)
        if ipy_win:
            ipy_win.show()

    def script_exec(self):
        pass

    def action_exit(self):
        # TODO: check project status and prompt if there are unsaved changed
        app.quit()

def print_process_id():
    print 'Process ID is:', os.getpid()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MainApp = frmMain()
    MainApp.show()
    sys.exit(app.exec_())
