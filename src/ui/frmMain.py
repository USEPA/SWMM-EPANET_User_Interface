import os, sys
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
from cStringIO import StringIO
from embed_ipython_new import EmbedIPython
#from ui.ui_utility import EmbedMap
# from ui.ui_utility import *
from ui.model_utility import *
from PyQt4 import QtCore, QtGui
from frmMainDesigner import Ui_frmMain
#from IPython import embed
#from RestrictedPython import compile_restricted
#import py_compile
import imp
import traceback
from core.inputfile import InputFile as Project

INSTALL_DIR = os.path.abspath(os.path.dirname('__file__'))
INIT_MODULE = "__init__"


class frmMain(QtGui.QMainWindow, Ui_frmMain):
    def __init__(self, q_application):
        QtGui.QMainWindow.__init__(self, None)
        self.setupUi(self)
        self.q_application = q_application
        self.layers = []
        self._forms = []
        """List of editor windows used during this session, kept here so they are not automatically closed."""
        self.model = "Not Set"
        self.project_type = Project
        self.project = None
        self.obj_tree = None
        self.obj_list = None
        self.plugins = self.get_plugins()
        self.populate_plugins_menu()
        QtCore.QObject.connect(self.actionStdNewProjectMenu, QtCore.SIGNAL('triggered()'), self.new_project)
        QtCore.QObject.connect(self.actionStdNewProject, QtCore.SIGNAL('triggered()'), self.new_project)
        QtCore.QObject.connect(self.actionStdOpenProjMenu, QtCore.SIGNAL('triggered()'), self.open_project)
        QtCore.QObject.connect(self.actionStdOpenProj, QtCore.SIGNAL('triggered()'), self.open_project)
        QtCore.QObject.connect(self.actionStdExit, QtCore.SIGNAL('triggered()'), self.action_exit)
        QtCore.QObject.connect(self.actionIPython, QtCore.SIGNAL('triggered()'), self.script_ipython)
        QtCore.QObject.connect(self.actionExec, QtCore.SIGNAL('triggered()'), self.script_exec)
        QtCore.QObject.connect(self.actionStdSave, QtCore.SIGNAL('triggered()'), self.save_project)
        QtCore.QObject.connect(self.actionStdSaveMenu, QtCore.SIGNAL('triggered()'), self.save_project)
        QtCore.QObject.connect(self.actionStdSave_As, QtCore.SIGNAL('triggered()'), self.save_project_as)
        QtCore.QObject.connect(self.actionStdRun_Simulation, QtCore.SIGNAL('triggered()'), self.run_simulation)
        QtCore.QObject.connect(self.actionRun_SimulationMenu, QtCore.SIGNAL('triggered()'), self.run_simulation)

        try:
            from qgis.core import QgsApplication
            from qgis.gui import QgsMapCanvas
            from map_tools import EmbedMap

            # TODO: make sure this works on all platforms, both in dev environment and in our installed packages
            search_paths = [os.path.join(INSTALL_DIR, "qgis"),
                            os.path.join(INSTALL_DIR, "../qgis"),
                            os.path.join(INSTALL_DIR, "../../qgis"),
                            "C:/OSGeo4W/apps/qgis/",
                            "/usr",
                            "/Applications/QGIS.app/Contents/MacOS"]
            if os.environ.has_key("QGIS_HOME"):
                search_paths.insert(0, os.environ.get("QGIS_HOME"))
            if os.environ.has_key("QGIS_PREFIX_PATH"):
                search_paths.insert(0, os.environ.get("QGIS_PREFIX_PATH"))
            try:
                for qgis_home in search_paths:
                    if os.path.isdir(qgis_home):
                        QgsApplication.setPrefixPath(qgis_home, True)
                        QgsApplication.initQgis()
                        self.canvas = QgsMapCanvas(self, 'mapCanvas')
                        self.canvas.setMouseTracking(True)
                        self.map_widget = EmbedMap(session=self, mapCanvas=self.canvas)
                        self.map_win = self.map.addSubWindow(self.map_widget, QtCore.Qt.Widget)
                        if self.map_win:
                            self.map_win.setGeometry(0, 0, 600, 400)
                            self.map_win.setWindowTitle('Study Area Map')
                            self.map_win.show()
                            QtCore.QObject.connect(self.actionAdd_Vector, QtCore.SIGNAL('triggered()'), self.map_addvector)
                            QtCore.QObject.connect(self.actionAdd_Raster, QtCore.SIGNAL('triggered()'), self.map_addraster)
                            QtCore.QObject.connect(self.actionPan, QtCore.SIGNAL('triggered()'), self.setQgsMapTool)
                            QtCore.QObject.connect(self.actionZoom_in, QtCore.SIGNAL('triggered()'), self.setQgsMapTool)
                            QtCore.QObject.connect(self.actionZoom_out, QtCore.SIGNAL('triggered()'), self.setQgsMapTool)
                            QtCore.QObject.connect(self.actionZoom_full, QtCore.SIGNAL('triggered()'), self.zoomfull)
                            QtCore.QObject.connect(self.actionAdd_Feature, QtCore.SIGNAL('triggered()'), self.map_addfeature)
                            break  # Success, done looking for a qgis_home
                else:
                    QMessageBox.information(None, "QGIS Home not found", "Not creating map", QMessageBox.Ok)
            except Exception as e1:
                msg = str(e1) + '\n' + str(traceback.print_exc())
                print(msg)
                QMessageBox.information(None, "Error Initializing Map", msg, QMessageBox.Ok)

        except Exception as eImport:
            print "QGIS libraries not found, Not creating map\n" + str(eImport)
            # QMessageBox.information(None, "QGIS libraries not found", "Not creating map\n" + str(eImport), QMessageBox.Ok)

    def setQgsMapTool(self):
        self.map_widget.setZoomInMode()
        self.map_widget.setZoomOutMode()
        self.map_widget.setPanMode()

    def map_pan(self):
        self.map_widget.setPanMode()

    def zoomfull(self):
        self.map_widget.zoomfull()

    def map_addfeature(self):
        self.map_widget.setAddFeatureMode()

    def onGeometryAdded(self):
        print 'Geometry Added'

    def mouseMoveEvent(self, event):
        pass
        x = event.x()
        y = event.y()
        p = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        self.btnCoord.setText('x,y: {:}, {:}'.format(p.x(), p.y()))

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            if event.buttons() == QtCore.Qt.NoButton:
                pos = event.pos()
                x = pos.x()
                y = pos.y()
                p = self.map_widget.canvas.getCoordinateTransform().toMapCoordinates(x, y)
                self.btnCoord.setText('x,y: %s, %s' % (p.x()), p.y())
            else:
                pass

    def map_addvector(self):
        print 'add vector'
        from frmMapAddVector import frmMapAddVector
        dlg = frmMapAddVector(self)
        dlg.show()
        result = dlg.exec_()
        if result == 1:
            specs = dlg.getLayerSpecifications()
            filename = specs['filename']
            if filename.lower().endswith('.shp'):
                self.map_widget.addVectorLayer(filename)

    def map_addraster(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Specify Raster Dataset', '/')
        if len(filename) > 0:
            self.map_widget.addRasterLayer(filename)

    def on_load(self, tree_top_item_list):
        # self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        # cleaner = QtCore.QObjectCleanupHandler()
        # cleaner.add(self.tabProjMap.layout())
        self.obj_tree = ObjectTreeView(self, tree_top_item_list)
        self.obj_tree.itemDoubleClicked.connect(self.edit_options)
        # self.tabProjMap.addTab(self.obj_tree, 'Project')
        layout = QVBoxLayout(self.tabProject)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.obj_tree)
        self.tabProject.setLayout(layout)
        self.setWindowTitle(self.model)

        self.obj_list = ObjectListView(model=self.model, ObjRoot='', ObjType='', ObjList=None)
        mlayout = self.dockw_more.layout()
        # mlayout.setContentsMargins(0, 0, 0, 0)
        mlayout.addWidget(self.obj_list)
        # layout1 = QVBoxLayout(self.dockw_more)
        self.dockw_more.setLayout(mlayout)
        # self.actionPan.setEnabled(False)

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
        plugin_folder = os.path.join(INSTALL_DIR, "plugins")
        if not os.path.exists(plugin_folder):
            plugin_folder = os.path.normpath(os.path.join(INSTALL_DIR, "../../plugins"))
        if os.path.exists(plugin_folder):
            for folder_name in os.listdir(plugin_folder):
                location = os.path.join(plugin_folder, folder_name)
                if os.path.isdir(location) and INIT_MODULE + ".py" in os.listdir(location):
                    info = imp.find_module(INIT_MODULE, [location])
                    found_plugins.append({"name": folder_name, "info": info})
        return found_plugins

    def load_plugin(self, plugin):
        try:
            return imp.load_module(INIT_MODULE, *plugin["info"])
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
        new_custom_menu = self.menubar.addMenu(plugin.plugin_name)
        new_custom_menu.menuTag = 'plugin_mainmenu_' + plugin.plugin_name
        for m in plugin.__all__:
            new_action = QtGui.QAction(m, self)
            new_action.setStatusTip(m)
            new_action.setData(plugin.plugin_name + '|' + m)
            new_action.setCheckable(False)
            # new_action.triggered.connect(self.run_plugin_custom)
            QtCore.QObject.connect(new_action, QtCore.SIGNAL('triggered()'), self.run_plugin_custom)
            new_custom_menu.addAction(new_action)

    def find_plugin_main_menu(self, plugin):
        for qm in self.menubar.children():
            if hasattr(qm, 'menuTag'):
                if qm.menuTag == 'plugin_mainmenu_' + plugin.plugin_name:
                    return qm
        return None

    def remove_plugin_menu(self, plugin):
        custom_plugin_menu = self.find_plugin_main_menu(plugin)
        if custom_plugin_menu:
            custom_plugin_menu.clear()
            menu_act = custom_plugin_menu.menuAction()
            self.menubar.removeAction(menu_act)
            menu_act.deleteLater()
            custom_plugin_menu.deleteLater()

    def run_plugin_custom(self):
        menu_text = str(self.sender().data())
        (plugin_name, method_name) = menu_text.split('|', 2)
        for plugin in self.plugins:
            if plugin['name'] == plugin_name:
                loaded_plugin = self.load_plugin(plugin)
                if loaded_plugin:
                    loaded_plugin.run(self, int(loaded_plugin.__all__[str(method_name)]))
                    return

    def script_ipython(self):
        widget = EmbedIPython(session=self, plugins=self.plugins, mainmodule=INIT_MODULE)
        ipy_win = self.map.addSubWindow(widget,QtCore.Qt.Widget)
        if ipy_win:
            ipy_win.show()

    def script_exec(self):
        gui_settings = QtCore.QSettings(self.model, "GUI")
        directory = gui_settings.value("ScriptDir", "")
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Select script to run", directory, "All files (*.*)")
        if file_name:
            path_only, file_only = os.path.split(file_name)
            if path_only != directory:
                gui_settings.setValue("ScriptDir", path_only)
                gui_settings.sync()
                del gui_settings

            save_handle = sys.stdout
            try:
                redirected_output = StringIO()
                sys.stdout = redirected_output
                session = self
                with open(file_name, 'r') as script_file:
                    exec(script_file)
                QMessageBox.information(None, "Finished Running Script",
                                        file_name + "\n" + redirected_output.getvalue(), QMessageBox.Ok)
            except Exception as ex:
                QMessageBox.information(None, "Exception Running Script",
                                        file_name + '\n' + str(ex), QMessageBox.Ok)
            sys.stdout = save_handle

    def make_editor_from_tree(self, search_for, tree_list):
        for tree_item in tree_list:
            if search_for == tree_item[0]:  # If we found a matching tree item, return its editor
                if len(tree_item) > 0 and tree_item[1] and not (type(tree_item[1]) is list):
                    args = [self]
                    if len(tree_item) > 2:
                        # We recommend this is a list, but if not, try to treat it as a single argument
                        if isinstance(tree_item[2], basestring) or not isinstance(tree_item[2], list):
                            args.append(str(tree_item[2]))
                        else:  # tree_item[2] is a list that is not a string
                            args.extend(tree_item[2])
                    return tree_item[1](*args)  # Create editor with first argument self, other args from tree_item
                return None
            if len(tree_item) > 0 and type(tree_item[1]) is list:  # find whether there is a match in this sub-tree
                edit_form = self.make_editor_from_tree(search_for, tree_item[1])
                if edit_form:
                    return edit_form

    def edit_options(self, itm, column):
        if not self.project or not self.get_editor:
            return
        edit_name = itm.data(0, 0)
        if edit_name:
            self.show_edit_window(self.get_editor(edit_name))

    def show_edit_window(self, window):
        if window:
            print "Show edit window " + str(window)
            self._forms.append(window)
            # window.destroyed.connect(lambda s, e, a: self._forms.remove(s))
            # window.destroyed = lambda s, e, a: self._forms.remove(s)
            # window.connect(window, QtCore.SIGNAL('triggered()'), self.editor_closing)
            window.show()

            # def editor_closing(self, event):
            #     print "Editor Closing: " + str(event)
            #     # self._forms.remove(event.)

    def new_project(self):
        self.project = self.project_type()
        self.setWindowTitle(self.model + " - New")
        self.project.file_name = "New.inp"

    def open_project(self):
        gui_settings = QtCore.QSettings(self.model, "GUI")
        directory = gui_settings.value("ProjectDir", "")
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open Project...", directory,
                                                      "Inp files (*.inp);;All files (*.*)")
        if file_name:
            self.project = self.project_type()
            try:
                self.project.read_file(file_name)
                path_only, file_only = os.path.split(file_name)
                self.setWindowTitle(self.model + " - " + file_only)
                if path_only != directory:
                    gui_settings.setValue("ProjectDir", path_only)
                    gui_settings.sync()
                    del gui_settings
            except:
                self.project = Project()
                self.setWindowTitle(self.model)

    def save_project(self):
        self.project.write_file(self.project.file_name)

    def save_project_as(self):
        gui_settings = QtCore.QSettings(self.model, "GUI")
        directory = gui_settings.value("ProjectDir", "")
        file_name = QtGui.QFileDialog.getSaveFileName(self, "Save As...", directory, "Inp files (*.inp)")
        if file_name:
            path_only, file_only = os.path.split(file_name)
            try:
                self.project.write_file(file_name)
                self.setWindowTitle(self.model + " - " + file_only)
                if path_only != directory:
                    gui_settings.setValue("ProjectDir", path_only)
                    gui_settings.sync()
                    del gui_settings
            except Exception as ex:
                print(str(ex) + '\n' + str(traceback.print_exc()))
                QMessageBox.information(self, self.model,
                                        "Error saving {0}\nin {1}\n{2}\n{2}".format(
                                            file_only, path_only,
                                            str(ex), str(traceback.print_exc())),
                                        QMessageBox.Ok)

    def action_exit(self):
        # TODO: check project status and prompt if there are unsaved changed
        if self.q_application:
            try:
                self.q_application.quit()
            except:
                try:
                    self.close()
                except:
                    pass

    def __unicode__(self):
        return unicode(self)


def print_process_id():
    print 'Process ID is:', os.getpid()

if __name__ == '__main__':
    application = QtGui.QApplication(sys.argv)
    QMessageBox.information(None, "frmMain",
                            "Run ui/EPANET/frmMainEPANET or ui/SWMM/frmMainSWMM instead of frmMain.",
                            QMessageBox.Ok)
