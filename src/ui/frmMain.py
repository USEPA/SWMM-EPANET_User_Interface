import os, sys
os.environ['QT_API'] = 'pyqt'
import sip
for typ in ["QString","QVariant", "QDate", "QDateTime", "QTextStream", "QTime", "QUrl"]:
    sip.setapi(typ, 2)
from cStringIO import StringIO
if sys.version_info >= (3,):
    unicode = str
# from embed_ipython_new import EmbedIPython
from threading import Lock
from PyQt4.Qsci import QsciScintilla

#from ui.ui_utility import EmbedMap
# from ui.ui_utility import *
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.help import HelpHandler
from ui.model_utility import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from frmMainDesigner import Ui_frmMain
#from IPython import embed
#from RestrictedPython import compile_restricted
#import py_compile
import imp
import traceback
from core.indexed_list import IndexedList
from core.project_base import ProjectBase
from core.coordinate import Coordinate, Link, Polygon

INSTALL_DIR = os.path.abspath(os.path.dirname('__file__'))
INIT_MODULE = "__init__"
MAX_RECENT_FILES = 8

class frmMain(QtGui.QMainWindow, Ui_frmMain):

    signalTimeChanged = QtCore.pyqtSignal()

    def __init__(self, q_application):
        QtGui.QMainWindow.__init__(self, None)
        self.crs = None
        self.project_settings = None
        self.no_items = True
        self.setupUi(self)
        self.q_application = q_application
        try:
            print("QsciScintilla.SC_TYPE_STRING:")
            print(str(QsciScintilla.SC_TYPE_STRING))
        except Exception as exQsci:
            print str(exQsci)
        self._forms = []
        self._editor_form = None
        """List of editor windows used during this session, kept here so they are not automatically closed."""

        # Make sure all required properties have already been set by subclass
        for prop_name in ["model", "project_type", "project"]:
            if not hasattr(self, prop_name):
                # set these here just so auto-completion recognizes them as fields of this class
                self.model = "Not Set"
                self.project_type = ProjectBase
                self.project = None
                raise Exception(prop_name + " must be set by subclass before calling frmMain.__init__")
        self.obj_tree = None
        self.obj_list = None
        self.obj_view_model = QStandardItemModel()
        self.plugins = self.get_plugins()
        self.recent_projects = self.create_recent_menus(self.menuFile, self.open_recent_project)
        self.add_recent_project(None)  # Populate the recent script menus, not adding one
        self.recent_scripts = self.create_recent_menus(self.menuScripting, self.run_recent_script)
        self.add_recent_script(None)  # Populate the recent script menus, not adding one
        self.populate_plugins_menu()
        self.time_widget.setVisible(False)
        self.actionStdNewProjectMenu.triggered.connect(self.new_project)
        self.actionStdNewProject.triggered.connect(self.new_project)
        self.actionStdOpenProjMenu.triggered.connect(self.open_project)
        self.actionStdOpenProj.triggered.connect(self.open_project)
        self.actionStdExit.triggered.connect(self.action_exit)
        self.actionEditScript.triggered.connect(self.edit_script)
        self.actionRun_Script.triggered.connect(self.script_browse_and_run)
        self.actionStdSave.triggered.connect(self.save_project)
        self.actionStdSaveMenu.triggered.connect(self.save_project)
        self.actionStdSave_As.triggered.connect(self.save_project_as)
        self.actionStdRun_Simulation.triggered.connect(self.run_simulation)
        self.actionRun_SimulationMenu.triggered.connect(self.run_simulation)
        self.actionStdProjCalibration_Data.triggered.connect(self.calibration_data)
        # self.tabProjMap.currentChanged.connect(self.tabProjMapChanged)
        self.actionStdPrint.triggered.connect(self.saveMapAsImage)
        self.actionSave_Map_As_Image.triggered.connect(self.saveMapAsImage)
        self.actionStdImportMap.triggered.connect(self.import_from_gis)
        self.actionStdExportMap.triggered.connect(self.export_to_gis)
        self.actionToolbarShowMap.triggered.connect(
            lambda: self.toggle_toolbar('map,' + str(self.actionToolbarShowMap.isChecked())))
        self.actionToolbarShowObject.triggered.connect(
            lambda: self.toggle_toolbar('object,' + str(self.actionToolbarShowObject.isChecked())))
        self.actionToolbarShowStandard.triggered.connect(
            lambda: self.toggle_toolbar('standard,' + str(self.actionToolbarShowStandard.isChecked())))
        self.actionStdMapBackLoad.triggered.connect(self.map_addraster)
        self.actionStdMapBackUnload.triggered.connect(self.unloadBasemap)
        self.actionStdMapBackAlign.triggered.connect(lambda: self.setMenuMapTool('pan'))
        self.actionAdd_Vector.triggered.connect(self.map_addvector)
        self.actionAdd_Raster.triggered.connect(self.map_addraster)
        # self.actionGroup_Obj = QActionGroup(self)
        self.cbAutoLength.currentIndexChanged.connect(self.cbAutoLength_currentIndexChanged)
        self.auto_length = (self.cbAutoLength.currentIndex == 1)

        self.setAcceptDrops(True)
        self.tree_section = ''

        # Map attributes will be set below if possible or will remain None to indicate map is not present.
        self.canvas = None
        self.map_widget = None
        self.selecting = Lock()
        try:
            # TODO: make sure this works on all platforms, both in dev environment and in our installed packages
            orig_path = os.environ["Path"]
            print("Original Path = " + orig_path)
            search_paths = []
            if os.environ.has_key("QGIS_PREFIX_PATH"):
                search_paths.append(os.environ.get("QGIS_PREFIX_PATH"))
            if os.environ.has_key("QGIS_HOME"):
                search_paths.append(os.environ.get("QGIS_HOME"))
            dirname = INSTALL_DIR
            package_dir = INSTALL_DIR + "\\dist\\" + self.model + "-UI"
            if os.path.isdir(package_dir):
                dirname = package_dir
                os.environ["QT_PLUGIN_PATH"] = dirname + "\\plugins"
            while dirname:
                search_paths.append(dirname)
                search_paths.append(os.path.join(dirname, "qgis"))
                updir = os.path.dirname(dirname)
                if not updir or updir == dirname:
                    break
                dirname = updir
            search_paths.extend([r"C:\OSGeo4W64\apps\qgis",
                                 r"C:\OSGeo4W\apps\qgis",
                                 r"/usr",
                                 r"/Applications/QGIS.app/Contents/MacOS"])
            for qgis_home in search_paths:
                try:
                    print("Search " + qgis_home)
                    if os.path.isdir(qgis_home):
                        updir = os.path.dirname(qgis_home)
                        updir2 = os.path.dirname(updir)
                        os.environ["QGIS"] = qgis_home
                        os.environ["QGIS_PREFIX_PATH"] = qgis_home
                        path = orig_path
                        for add_path in [os.path.join(updir2, "bin"),
                                         os.path.join(qgis_home, "bin"),
                                         os.path.join(updir, r"/Python27/Scripts"),
                                         qgis_home]:
                            if os.path.isdir(add_path):
                                path = add_path + ';' + path
                        os.environ["Path"] = path
                        print("Try path = " + os.environ["Path"])
                        from qgis.core import QgsApplication
                        from qgis.gui import QgsMapCanvas
                        from map_tools import EmbedMap
                        QgsApplication.setPrefixPath(qgis_home, True)
                        QgsApplication.initQgis()
                        self.canvas = QgsMapCanvas(self, 'mapCanvas')
                        self.canvas.setMouseTracking(True)
                        self.map_widget = EmbedMap(session=self, canvas=self.canvas, main_form=self)
                        self.map_win = self.map.addSubWindow(self.map_widget, QtCore.Qt.Widget)
                        if self.map_win:
                            self.map_win.setWindowTitle('Study Area Map')
                            self.map_win.showMaximized()
                            # self.map_win.map_unit_names = [transl8("frmMain", units, None)
                            #                                for units in self.map_win.map_unit_names]
                            self.actionPan.triggered.connect(self.setQgsMapTool)
                            self.actionMapSelectObj.triggered.connect(self.setQgsMapTool)
                            self.actionStdSelect_Object.triggered.connect(self.setQgsMapToolSelect)
                            self.actionMapSelectVertices.triggered.connect(self.setQgsMapTool)
                            self.actionStdSelect_Vertex.triggered.connect(self.setQgsMapToolSelectVertex)
                            self.actionZoom_in.triggered.connect(self.setQgsMapTool)
                            self.actionZoom_out.triggered.connect(self.setQgsMapTool)
                            self.actionZoom_full.triggered.connect(self.zoomfull)
                            self.actionMapMeasure.triggered.connect(self.setQgsMapTool)
                            self.actionAdd_Feature.triggered.connect(self.map_addfeature)
                            self.actionMapOption.triggered.connect(self.map_addfeature)

                            self.actionStdMapPan.triggered.connect(lambda: self.setMenuMapTool('pan'))
                            self.actionStdMapZoomIn.triggered.connect(lambda: self.setMenuMapTool('zoomin'))
                            self.actionStdMapZoomOut.triggered.connect(lambda: self.setMenuMapTool('zoomout'))
                            self.actionStdMapFullExtent.triggered.connect(lambda: self.setMenuMapTool('fullextent'))

                            from qgis.gui import QgsLayerTreeView
                            from qgis.core import QgsLayerTreeModel
                            from qgis.core import QgsProject
                            from qgis.gui import QgsLayerTreeMapCanvasBridge
                            self.gis_layer_root = QgsProject.instance().layerTreeRoot()
                            self.gis_layer_model = QgsLayerTreeModel(self.gis_layer_root)
                            self.gis_layer_model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
                            self.gis_layer_model.setFlag(QgsLayerTreeModel.AllowLegendChangeState)
                            self.gis_layer_model.setFlag(QgsLayerTreeModel.AllowSymbologyChangeState)
                            self.gis_layer_model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
                            self.gis_layer_tree = QgsLayerTreeView()
                            self.gis_layer_tree.setModel(self.gis_layer_model)
                            self.gis_layer_bridge = QgsLayerTreeMapCanvasBridge(self.gis_layer_root, self.canvas, self.tabGIS)
                            mlayout = QVBoxLayout(self.tabGIS)
                            mlayout.setContentsMargins(0, 0, 0, 0)
                            mlayout.addWidget(self.gis_layer_tree)
                            self.tabGIS.setLayout(mlayout)

                            print("Found QGIS in " + qgis_home)
                            break  # Success, done looking for a qgis_home
                except Exception as e1:
                    msg = "Did not load QGIS from " + qgis_home + " (" + str(e1) + ")\n" # + str(traceback.print_exc())
                    print(msg)
                    # QMessageBox.information(None, "Error Initializing Map", msg, QMessageBox.Ok)
        except Exception as eImport:
            self.canvas = None
            print str(eImport) + str(traceback.print_exc())
        if not self.canvas:
            self.map_widget = None
            print("QGIS libraries not found, Not creating map\n")
            # QMessageBox.information(None, "QGIS libraries not found", "Not creating map\n" + str(eImport), QMessageBox.Ok)

        self.add_point_tools = [[self.actionObjAddGage, "raingages"],
                                [self.actionObjAddJunc, "junctions"],
                                [self.actionObjAddLabel, "labels"],
                                [self.actionObjAddOutfall, "outfalls"],
                                [self.actionObjAddDivider, "dividers"],
                                [self.actionObjAddStorage, "storage"],
                                [self.actionObjAddStorage, "reservoirs"],
                                [self.actionObjAddTank, "tanks"]]

        self.add_link_tools = [[self.actionObjAddConduit, "conduits"],
                               [self.actionObjAddConduit, "pipes"],
                               [self.actionObjAddOrifice, "orifices"],
                               [self.actionObjAddOutlet, "outlets"],
                               [self.actionObjAddPump, "pumps"],
                               [self.actionObjAddValve, "valves"],
                               [self.actionObjAddWeir, "weirs"]]

        self.add_polygon_tools = [[self.actionObjAddSub, "subcatchments"]]

        # First pass through all possible tools, hide and remove the ones this model does not use
        for tools in [self.add_point_tools, self.add_link_tools, self.add_polygon_tools]:
            tool_index = 0
            while tool_index < len(tools):
                tool = tools[tool_index]
                act, name = tool
                if self.canvas and hasattr(self.project, name):
                    tool_index += 1
                else:
                    act.setVisible(False)
                    tools.remove(tool)

        # Second pass through only tools that will be used, show them and connect them to setQgsMapTool
        for tools in [self.add_point_tools, self.add_link_tools, self.add_polygon_tools]:
            for act, name in tools:
                act.setVisible(True)
                act.triggered.connect(self.setQgsMapTool)

        self.time_index = 0
        self.horizontalTimeSlider.valueChanged.connect(self.currentTimeChanged)

        self.onLoad()
        self.undo_stack = QUndoStack(self)
        # self.undo_view = QUndoView(self.undo_stack)

        self.action_undo = QtGui.QAction(self)
        self.action_undo.setObjectName("actionUndo")
        self.action_undo.setText(transl8("frmMain", "Undo", None) )
        self.action_undo.setToolTip(transl8("frmMain", "Undo the most recent edit", None))
        self.action_undo.setShortcut(QKeySequence("Ctrl+Z"))
        self.menuEdit.addAction(self.action_undo)
        self.action_undo.triggered.connect(self.undo)

        self.action_redo = QtGui.QAction(self)
        self.action_redo.setObjectName("actionRedo")
        self.action_redo.setText(transl8("frmMain", "Redo", None) )
        self.action_redo.setToolTip(transl8("frmMain", "Redo the most recent Undo", None) )
        self.action_redo.setShortcut(QKeySequence("Ctrl+Y"))
        self.menuEdit.addAction(self.action_redo)
        self.action_redo.triggered.connect(self.redo)

        self.actionStdImportNetwork.setVisible(False)
        self.actionStdSelect_Region.setEnabled(False)
        self.actionStdSelect_All.setEnabled(False)
        self.actionAdd_Feature.setCheckable(True)
        self.actionAdd_Feature.setVisible(False)
        self.actionMapFindObj.setVisible(False)
        self.actionMapQuery.setVisible(False)
        self.menuTools.setVisible(False)
        self.menuWindow.setVisible(False)
        self.actionStdPage_Setup.setVisible(False)
        self.actionStdPrint_Preview.setVisible(False)
        self.actionStdPrint.setVisible(False)
        self.actionStdCopy_To.setVisible(False)
        self.actionStdGroup_Edit.setVisible(False)

    def loadBasemap(self):
        pass
    def unloadBasemap(self):
        pass
    def alignBasemap(self):
        pass

    def cbAutoLength_currentIndexChanged(self):
        self.auto_length = (self.cbAutoLength.currentIndex() == 1)

    def import_from_gis(self):
        import import_export

        file_filter = "GeoJSON (*.json);;" \
                      "Shapefile (*.shp);;" \
                      "Comma-separated text (*.csv);;" \
                      "All files (*.*)"
        directory = self.program_settings.value("GISPath", os.path.dirname(self.project.file_name))

        file_name = QtGui.QFileDialog.getOpenFileName(self, "Select GIS file to import",
                                                      directory, file_filter)
        if file_name:
            path_only, file_only = os.path.split(file_name)
            if path_only != directory:  # Save path as default for next import/export operation
                self.program_settings.setValue("GISPath", path_only)
                self.program_settings.sync()

            import_export.import_from_gis(self, file_name)

    def export_to_gis(self):
        import import_export

        file_filter = "GeoJSON (*.json);;" \
                      "Shapefile (*.shp);;" \
                      "Comma-separated text (*.csv);;" \
                      "All files (*.*)"
        directory = self.program_settings.value("GISPath", os.path.dirname(self.project.file_name))

        file_name = QtGui.QFileDialog.getSaveFileName(self, "Export to GIS",
                                                      directory, file_filter)
        if file_name:
            path_only, file_only = os.path.split(file_name)
            if path_only != directory:  # Save path as default for next import/export operation
                self.program_settings.setValue("GISPath", path_only)
                self.program_settings.sync()

            import_export.export_to_gis(self, file_name)

    # def tabProjMapChanged(self, index):
    #     if index == 1:
    #         self.time_widget.setVisible(True)
    #     else:
    #         self.time_widget.setVisible(False)

    def saveMapAsImage(self):
        directory = self.program_settings.value("ProjectDir", "")
        file_name = QtGui.QFileDialog.getSaveFileName(self, "Save Map As...", directory,
                                                            "PNG Files (*.png);;All files (*.*)")
        if file_name:
            self.canvas.saveAsImage(file_name)

    def undo(self):
        self.undo_stack.undo()

    def redo(self):
        self.undo_stack.redo()

    class _AddItem(QtGui.QUndoCommand):
        """Private class that adds an item to the model and the map. Accessed via add_item method."""
        def __init__(self, session, item):
            QtGui.QUndoCommand.__init__(self, "Add " + str(item))
            self.session = session
            self.item = item
            self.added_id = None
            self.added_centroid_id = None
            self.centroid_layer = None
            self.isSubLink = False
            self.isSub2Sub = 0 #False
            section_field_name = session.section_types[type(item)]
            if not hasattr(session.project, section_field_name):
                raise Exception("Section not found in project: " + section_field_name)
            self.section = getattr(session.project, section_field_name)
            self.layer = self.session.model_layers.layer_by_name(section_field_name)
            #if isinstance(self.item, Polygon):
            #    self.centroid_layer = self.session.model_layers.layer_by_name("subcentroids")

        def redo(self):
            self.isSubLink = False
            self.isSub2Sub = 0 #False
            self.inlet_sub = None
            self.outlet_sub = None
            self.inlet_sub_id = ""
            self.outlet_sub_id = ""
            if isinstance(self.item, Link):
                if 'subcentroid' in self.item.inlet_node: #not self.item.inlet_node in self.session.project.all_nodes():
                    self.centroid_layer = self.session.model_layers.layer_by_name("subcentroids")
                    for cf in self.centroid_layer.getFeatures():
                        if cf["name"] == self.item.inlet_node:
                            self.inlet_sub_id = cf["sub_modelid"]
                            s = self.session.project.subcatchments.find_item(self.inlet_sub_id)
                            if s is not None:
                                self.inlet_sub = s.centroid
                            break

                    #for s in self.session.project.subcatchments.value:
                    #    if s.name == self.item.inlet_node:
                    #        self.inlet_sub_id = s.name
                    #        self.inlet_sub = s.centroid
                    #        break
                    self.isSubLink = True

                if 'subcentroid' in self.item.outlet_node: #not self.item.outlet_node in self.session.project.all_nodes():
                    self.centroid_layer = self.session.model_layers.layer_by_name("subcentroids")
                    for cf in self.centroid_layer.getFeatures():
                        if cf["name"] == self.item.outlet_node:
                            self.outlet_sub_id = cf["sub_modelid"]
                            s = self.session.project.subcatchments.find_item(self.outlet_sub_id)
                            if s is not None:
                                self.outlet_sub = s.centroid
                            break
                    #for s in self.session.project.subcatchments.value:
                    #    if s.name == self.item.outlet_node:
                    #        self.outlet_sub_id = s.name
                    #        self.outlet_sub = s.centroid
                    #        break
                    self.isSubLink = True

                if self.inlet_sub is not None and self.outlet_sub is not None:
                    self.isSub2Sub = 1 #True

            if self.isSubLink:
                #swap out link item and section types
                #self.layer = self.session.model_layers.layer_by_name("sublinks")
                for obj_type, lyr_name in self.session.section_types.iteritems():
                    if lyr_name == "sublinks":
                        in_node = self.item.inlet_node
                        out_node = self.item.outlet_node
                        self.item = obj_type()
                        self.item.inlet_node = in_node
                        self.item.outlet_node = out_node
                        section_field_name = self.session.section_types[type(self.item)]
                        if not hasattr(self.session.project, section_field_name):
                            raise Exception("Section not found in project: " + section_field_name)
                        self.section = getattr(self.session.project, section_field_name)
                        self.layer = self.session.model_layers.layer_by_name(section_field_name)
                        break

            if self.item.name == '' or self.item.name == 'Unnamed' or self.item.name in self.section.value:
                if self.layer and "sublink" in self.layer.name().lower():
                    self.item.name = u'sublink-' + self.item.inlet_node
                else:
                    self.item.name = self.session.new_item_name(type(self.item))
            if len(self.section.value) == 0 and not isinstance(self.section, list):
                self.section.value = IndexedList([], ['name'])
            self.section.value.append(self.item)
            if not self.isSubLink:
                # self.session.list_objects()  # Refresh the list of items on the form
                list_item = self.session.listViewObjects.addItem(self.item.name)
                self.session.listViewObjects.scrollToItem(list_item)

            if self.layer:
                self.session.map_widget.clearSelectableObjects()
                self.layer.startEditing()
                if isinstance(self.item, Coordinate):
                    added = self.layer.dataProvider().addFeatures([self.session.map_widget.point_feature_from_item(self.item)])
                elif isinstance(self.item, Link):
                    f = self.session.map_widget.line_feature_from_item(self.item,
                                                                       self.session.project.all_nodes(),
                                                                       self.inlet_sub, self.outlet_sub)
                    added = self.layer.dataProvider().addFeatures([f])
                    if added[0]:
                        #set subcatchment's outlet nodal/subcatch id
                        if self.inlet_sub and self.inlet_sub_id:
                            for s in self.session.project.subcatchments.value:
                                if s.name == self.inlet_sub_id:
                                    s.outlet = self.item.outlet_node
                                    break
                        #set sublink's attributes
                        #f.setAttributes([str(added[1][0].id()), 0.0, self.item.inlet_node, self.item.outlet_node, self.isSub2Sub])
                        #self.layer.changeAttributeValue(added[1][0].id(), 0, self.item.name)
                        #self.layer.changeAttributeValue(added[1][0].id(), 1, 0.0)
                        self.layer.changeAttributeValue(added[1][0].id(), 2, self.item.inlet_node)
                        self.layer.changeAttributeValue(added[1][0].id(), 3, self.item.outlet_node)
                        self.layer.changeAttributeValue(added[1][0].id(), 4, self.isSub2Sub)
                        self.layer.updateExtents()
                        self.layer.commitChanges()
                        self.layer.triggerRepaint()
                        self.session.map_widget.canvas.refresh()
                elif isinstance(self.item, Polygon):
                    f = self.session.map_widget.polygon_feature_from_item(self.item)
                    added = self.layer.dataProvider().addFeatures([f])
                    if added[0]:
                        pt = f.geometry().centroid().asPoint()
                        self.item.centroid.x = str(pt.x())
                        self.item.centroid.y = str(pt.y())

                        #add centroid item
                        c_item = None
                        for obj_type, lyr_name in self.session.section_types.iteritems():
                            if lyr_name == "subcentroids":
                                c_item = obj_type()
                                c_item.x = str(pt.x())
                                c_item.y = str(pt.y())
                                break
                        c_item.name = u'subcentroid-' + self.item.name #self.session.new_item_name(type(c_item))
                        c_section_field_name = self.session.section_types[type(c_item)]
                        if not hasattr(self.session.project, c_section_field_name):
                            raise Exception("Section not found in project: " + c_section_field_name)
                        c_section = getattr(self.session.project, c_section_field_name)
                        self.centroid_layer = self.session.model_layers.layer_by_name(c_section_field_name)
                        if len(c_section.value) == 0 and not isinstance(c_section, list):
                            c_section.value = IndexedList([], ['name'])
                        c_section.value.append(c_item)
                        self.centroid_layer.startEditing()
                        pf = self.session.map_widget.point_feature_from_item(self.item.centroid)
                        pf.setAttributes([c_item.name, 0.0, added[1][0].id(), self.item.name])
                        added_centroid = self.centroid_layer.dataProvider().addFeatures([pf])
                        if added_centroid[0]:
                            self.added_centroid_id = added_centroid[1][0].id()
                            self.layer.changeAttributeValue(added[1][0].id(), 2, added_centroid[1][0].id())
                            self.layer.changeAttributeValue(added[1][0].id(), 3, c_item.name)
                            self.centroid_layer.updateExtents()
                            self.centroid_layer.commitChanges()
                            self.centroid_layer.triggerRepaint()
                        else:
                            self.added_centroid_id = None
                            self.centroid_layer.rollBack()

                if added[0]:
                    self.added_id = added[1][0].id()
                    self.layer.updateExtents()
                    self.layer.commitChanges()
                    if self.session.no_items:
                        self.session.zoomfull()
                        self.session.no_items = False
                    else:
                        self.layer.triggerRepaint()
                        self.session.map_widget.canvas.refresh()
                else:
                    self.added_id = None
                    self.layer.rollBack()

        def undo(self):
            #if not "sublink" in self.layer.name().lower():
            #    self.section.value.remove(self.item)
            self.section.value.remove(self.item)
            self.session.list_objects()  # Refresh the list of items on the form
            # self.session.listViewObjects.takeItem(len(self.section.value))
            if self.added_id is not None:
                if isinstance(self.item, Link):
                    if self.isSubLink:
                        #for sub to node link, need to empty out the outlet attribute
                        # of the source sub of this soon to be deleted link
                        for s in self.session.project.subcatchments.value:
                            if s.name == self.item.inlet_node:
                                s.outlet = ""
                                break
                self.session.map_widget.clearSelectableObjects()
                self.layer.startEditing()
                self.layer.dataProvider().deleteFeatures([self.added_id])
                self.layer.commitChanges()
                self.layer.updateExtents()
                self.layer.triggerRepaint()
                self.session.map_widget.canvas.refresh()
            if self.added_centroid_id is not None:
                self.session.map_widget.clearSelectableObjects()
                self.centroid_layer.startEditing()
                self.centroid_layer.dataProvider().deleteFeatures([self.added_centroid_id])
                self.centroid_layer.commitChanges()
                self.centroid_layer.updateExtents()
                self.centroid_layer.triggerRepaint()
                self.session.map_widget.canvas.refresh()

    def add_item(self, new_item):
        self.undo_stack.push(self._AddItem(self, new_item))

    class _DeleteItem(QtGui.QUndoCommand):
        """Private class that removes an item from the model and the map. Accessed via delete_item method."""
        def __init__(self, session, item):
            QtGui.QUndoCommand.__init__(self, "Delete " + str(item))
            self.session = session
            self.item = item
            section_field_name = session.section_types[type(item)]
            if hasattr(session.project, section_field_name):
                self.section = getattr(session.project, section_field_name)
            else:
                raise Exception("Section not found in project: " + section_field_name)
            self.layer = self.session.model_layers.layer_by_name(section_field_name)

        def redo(self):
            self.item_index = self.section.value.index(self.item)
            self.section.value.remove(self.item)
            self.session.list_objects()  # Refresh the list of items on the form
            if self.layer:
                self.session.map_widget.clearSelectableObjects()
                self.delete_feature = self.session.map_widget.find_feature(self.layer, self.item.name)
                if self.delete_feature:
                    self.layer.startEditing()
                    self.layer.dataProvider().deleteFeatures([self.delete_feature.id()])
                    self.layer.commitChanges()
                    self.layer.updateExtents()
                    self.layer.triggerRepaint()
                    self.session.map_widget.canvas.refresh()
                    try:
                        self.session.setQgsMapTool()
                    except:
                        pass

        def undo(self):
            self.section.value.insert(self.item_index, self.item)
            self.session.list_objects()  # Refresh the list of items on the form
            if self.layer and self.delete_feature:
                self.session.map_widget.clearSelectableObjects()
                self.layer.startEditing()
                self.layer.dataProvider().addFeatures([self.delete_feature])
                self.layer.commitChanges()
                self.layer.updateExtents()
                self.layer.triggerRepaint()
                self.session.map_widget.canvas.refresh()
                try:
                    self.session.setQgsMapTool()
                except:
                    pass

    def delete_item(self, item):
        self.undo_stack.push(self._DeleteItem(self, item))

    class _MoveSelectedItems(QtGui.QUndoCommand):
        """Private class that removes an item from the model and the map. Accessed via delete_item method."""
        def __init__(self, session, layer, dx, dy):
            QtGui.QUndoCommand.__init__(self, "Move " + str(dx) + ", " + str(dy))
            self.session = session
            self.layer = layer
            self.dx = dx
            self.dy = dy
            self.map_features = [feature for feature in layer.selectedFeatures()]
            self.moved_links = []
            self.selectSubAndCentroid()

        def selectSubAndCentroid(self):
            if "centroid" in self.layer.name().lower():
                layer_subcatchments = self.session.model_layers.layer_by_name("subcatchments")
                layer_subcatchments.removeSelection()
                sel_sub_ids = []
                for f in self.layer.selectedFeatures():
                    sel_sub_ids.append(f['sub_mapid'])
                layer_subcatchments.setSelectedFeatures(sel_sub_ids)
                self.map_features.extend(layer_subcatchments.selectedFeatures())
                pass
            elif "subcatchment" in self.layer.name().lower():
                layer_subcentroids = self.session.model_layers.layer_by_name("subcentroids")
                layer_subcentroids.removeSelection()
                sel_cent_ids = []
                for f in self.layer.selectedFeatures():
                    sel_cent_ids.append(f['c_mapid'])
                layer_subcentroids.setSelectedFeatures(sel_cent_ids)
                self.map_features.extend(layer_subcentroids.selectedFeatures())

            pass

        def redo(self):
            self.move(False)

        def undo(self):
            self.move(True)

        def move(self, undo):
            from qgis.core import QgsGeometry, QGis, QgsPoint
            try:
                self.layer.startEditing()
                all_nodes = self.session.project.all_nodes()
                all_links = self.session.project.all_links()
                if hasattr(self.session.project, "subcatchments"):
                    all_nodes.extend(self.session.project.find_section("subcentroids").value)
                    all_links.extend(self.session.project.find_section("sublinks").value)
                moved_coordinates = IndexedList([], ['name'])
                for section_field_name in ["labels", "raingages"]:
                    if hasattr(self.session.project, section_field_name):
                        all_nodes.extend(getattr(self.session.project, section_field_name).value)
                if undo:
                    dx = -self.dx
                    dy = -self.dy
                else:
                    dx = self.dx
                    dy = self.dy
                    self.moved_links = []
                for feature in self.map_features:
                    name = feature.attributes()[0]
                    geometry = feature.geometry()
                    if geometry.wkbType() == QGis.WKBPoint:
                        point = geometry.asPoint()
                        if undo:
                            new_point = point
                        else:
                            new_point = QgsPoint(point.x() + dx, point.y() + dy)
                        if "subcatchment" in self.layer.name().lower():
                            layer_subcentroids = self.session.model_layers.layer_by_name("subcentroids")
                            layer_subcentroids.startEditing()
                            layer_subcentroids.changeGeometry(feature.id(), QgsGeometry.fromPoint(new_point))
                            layer_subcentroids.commitChanges()
                            layer_subcentroids.updateExtents()
                            layer_subcentroids.triggerRepaint()
                        else:
                            self.layer.changeGeometry(feature.id(), QgsGeometry.fromPoint(new_point))

                        node = all_nodes[name]
                        if node:
                            node.x = new_point.x()
                            node.y = new_point.y()
                            if not undo:
                                moved_coordinates.append(node)

                    elif geometry.wkbType() == QGis.WKBPolygon:
                        if undo:
                            new_geom = geometry
                        else:
                            new_pts = []
                            for pt in geometry.asPolygon()[0]:
                                new_pts.append(QgsPoint(pt.x() + dx, pt.y() + dy))
                            new_geom = QgsGeometry.fromPolygon([new_pts])
                        if "centroid" in self.layer.name().lower():
                            layer_subcatchments = self.session.model_layers.layer_by_name("subcatchments")
                            layer_subcatchments.startEditing()
                            layer_subcatchments.changeGeometry(feature.id(), new_geom)
                            layer_subcatchments.commitChanges()
                            layer_subcatchments.updateExtents()
                            layer_subcatchments.triggerRepaint()
                        else:
                            self.layer.changeGeometry(feature.id(), new_geom)

                    elif geometry.wkbType() == QGis.WKBLineString:
                        link = all_links[name]
                        if link:
                            for node_name in [link.inlet_node, link.outlet_node]:
                                if node_name not in moved_coordinates and node_name in all_nodes:
                                    node = all_nodes[node_name]
                                    node.x = float(node.x) + dx
                                    node.y = float(node.y) + dy
                                    section_field_name = self.session.section_types[type(node)]
                                    try:
                                        node_layer = getattr(self.session.model_layers, section_field_name)
                                        node_layer.startEditing()
                                        feature = self.session.map_widget.find_feature(node_layer, node.name)
                                        node_layer.changeGeometry(feature.id(), QgsGeometry.fromPoint(QgsPoint(node.x, node.y)))
                                        node_layer.commitChanges()
                                        node_layer.updateExtents()
                                        node_layer.triggerRepaint()
                                    except Exception as ex1:
                                        print("Skipping GIS move of node " + node_name + " for link: " + name + ": " +\
                                              str(ex1) + '\n' + str(traceback.print_exc()))
                                    moved_coordinates.append(node)
                if undo:
                    for link, link_layer, feature in self.moved_links:
                        link_layer.startEditing()
                        link_layer.changeGeometry(feature.id(), feature.geometry())
                        link_layer.commitChanges()
                        link_layer.updateExtents()
                        link_layer.triggerRepaint()
                        # TODO: undo any edits to vertices in project data structure?
                    self.moved_links = []
                else:
                    if moved_coordinates:
                        self.update_affected_links(moved_coordinates, all_links, dx, dy)

                self.layer.commitChanges()
                self.layer.updateExtents()
                self.layer.triggerRepaint()
                self.session.map_widget.canvas.refresh()
            except Exception as ex:
                print("_MoveSelectedItems: " + str(ex) + '\n' + str(traceback.print_exc()))
            try:
                self.setQgsMapTool()
            except:
                pass

        def update_affected_links(self, moved_coordinates, all_links, dx, dy):
            from qgis.core import QgsGeometry, QgsPoint
            # Update affected links when an inlet or outlet node has been edited
            for link in all_links:
                move_inlet = link.inlet_node in moved_coordinates
                move_outlet = link.outlet_node in moved_coordinates
                if move_inlet or move_outlet:
                    section_field_name = self.session.section_types[type(link)]
                    link_layer = self.session.model_layers.layer_by_name(section_field_name)
                    if link_layer:
                        feature = self.session.map_widget.find_feature(link_layer, link.name)
                        self.moved_links.append([link, link_layer, feature])

                        link_points = feature.geometry().asPolyline()
                        if move_inlet and move_outlet:
                            for vertex in link.vertices:
                                vertex.x += dx
                                vertex.y += dy
                            link_points = [QgsPoint(pt.x() + dx, pt.y() + dy) for pt in link_points]
                        elif move_inlet:
                            coord = moved_coordinates[link.inlet_node]
                            link_points[0] = QgsPoint(coord.x, coord.y)
                        else:  # move_outlet:
                            coord = moved_coordinates[link.outlet_node]
                            link_points[-1] = QgsPoint(coord.x, coord.y)
                        print("Update link " + link.name)
                        link_layer.startEditing()
                        link_layer.changeGeometry(feature.id(), QgsGeometry.fromPolyline(link_points))
                        link_layer.commitChanges()
                        link_layer.updateExtents()
                        link_layer.triggerRepaint()

    def move_selected_items(self, layer, dx, dy):
        if layer:
            self.undo_stack.push(self._MoveSelectedItems(self, layer, dx, dy))


    class _MoveVertex(QtGui.QUndoCommand):
        """Private class that removes an item from the model and the map. Accessed via delete_item method."""
        def __init__(self, session, layer, feature, point_index, from_x, from_y, to_x, to_y):
            QtGui.QUndoCommand.__init__(self, "Move Vertex " + str(point_index) +
                                        " from " + str(from_x) + ", " + str(from_y) +
                                        " to " + str(to_x) + ", " + str(to_y))
            self.session = session
            self.layer = layer
            self.subcentroids = self.session.model_layers.layer_by_name("subcentroids")
            self.sublinks = self.session.model_layers.layer_by_name("sublinks")
            self.feature = feature
            self.point_index = point_index
            self.from_x = from_x
            self.from_y = from_y
            self.to_x = to_x
            self.to_y = to_y

        def redo(self):
            self.move(False)

        def undo(self):
            self.move(True)

        def move(self, undo):
            from qgis.core import QgsGeometry, QGis, QgsPoint
            try:
                self.layer.startEditing()
                if undo:
                    x = self.from_x
                    y = self.from_y
                else:
                    x = self.to_x
                    y = self.to_y

                geometry = self.feature.geometry()
                geometry.moveVertex(x, y, self.point_index)
                self.layer.changeGeometry(self.feature.id(), geometry)
                self.layer.commitChanges()
                self.layer.updateExtents()
                self.layer.triggerRepaint()
                self.session.map_widget.canvas.refresh()

                feature_name = self.feature.attributes()[0]
                for section_field_name in self.session.section_types.values():
                    try:
                        if self.layer == self.session.model_layers.layer_by_name(section_field_name):
                            section = getattr(self.session.project, section_field_name)
                            object = section.value[feature_name]
                            vertex_index = self.point_index
                            if section_field_name != "subcatchments":
                                vertex_index -= 1
                            object.vertices[vertex_index].x = x
                            object.vertices[vertex_index].y = y
                            if hasattr(object, "centroid"):
                                new_c_g = geometry.centroid()
                                new_c = new_c_g.asPoint()
                                object.centroid.x = str(new_c.x)
                                object.centroid.y = str(new_c.y)
                                for fc in self.subcentroids.getFeatures():
                                    if fc["sub_modelid"] == feature_name:
                                        #from qgis.core import QgsMap
                                        change_map = {fc.id() : new_c_g}
                                        self.subcentroids.dataProvider().changeGeometryValues(change_map)
                                        break
                                for fl in self.sublinks.dataProvider().getFeatures():
                                    if fl["inlet"] == self.feature["c_modelid"]:
                                        if fl.geometry().wkbType() == QGis.WKBLineString:
                                            line = fl.geometry().asPolyline()
                                            new_l_g = QgsGeometry.fromPolyline([new_c, line[-1]])
                                            change_map = {fl.id() : new_l_g}
                                            self.sublinks.dataProvider().changeGeometryValues(change_map)
                                        break

                            break
                    except Exception as ex1:
                        print("Searching for object to move vertex of: " + str(ex1) + '\n' + str(traceback.print_exc()))

            except Exception as ex:
                print("_MoveVertex: " + str(ex) + '\n' + str(traceback.print_exc()))
            try:
                self.setQgsMapTool()
            except:
                pass

    def move_vertex(self, layer, feature, point_index, from_x, from_y, to_x, to_y):
        if layer:
            self.undo_stack.push(self._MoveVertex(self, layer, feature, point_index,
                                                  from_x, from_y, to_x, to_y))


    class _EditVertex(QtGui.QUndoCommand):
        """Private class that edit a sub or link vertices from the model and the map. Accessed via delete_item method."""

        def __init__(self, session, layer, feature, from_geom, to_geom):
            QtGui.QUndoCommand.__init__(self, "Change geometry")
            self.session = session
            self.layer = layer
            self.subcentroids = self.session.model_layers.layer_by_name("subcentroids")
            self.sublinks = self.session.model_layers.layer_by_name("sublinks")
            self.feature = feature
            self.from_geom = from_geom
            self.to_geom = to_geom

        def redo(self):
            self.edit(False)

        def undo(self):
            self.edit(True)

        def edit(self, undo):
            from qgis.core import QgsGeometry, QGis, QgsPoint
            try:
                #self.layer.startEditing()
                if undo:
                    geom = self.from_geom
                else:
                    geom = self.to_geom

                self.layer.changeGeometry(self.feature.id(), geom)
                #self.layer.commitChanges()
                #self.layer.updateExtents()
                #self.layer.triggerRepaint()
                self.session.map_widget.canvas.refresh()

                feature_name = self.feature.attributes()[0]
                for section_field_name in self.session.section_types.values():
                    try:
                        if self.layer == self.session.model_layers.layer_by_name(section_field_name):
                            section = getattr(self.session.project, section_field_name)
                            object = section.value[feature_name]
                            if section_field_name != "subcatchments":
                                if hasattr(object, "vertices"):
                                    del object.vertices[:]
                                    for v in geom.asPolyline():
                                        coord = Coordinate()
                                        coord.x = v.x()
                                        coord.y = v.y()
                                        object.vertices.append(coord)
                        if hasattr(object, "centroid"):
                            new_c_g = geom.centroid()
                            new_c = new_c_g.asPoint()
                            object.centroid.x = str(new_c.x)
                            object.centroid.y = str(new_c.y)
                            for fc in self.subcentroids.getFeatures():
                                if fc["sub_modelid"] == feature_name:
                                    # from qgis.core import QgsMap
                                    change_map = {fc.id(): new_c_g}
                                    self.subcentroids.dataProvider().changeGeometryValues(change_map)
                                    break
                            for fl in self.sublinks.dataProvider().getFeatures():
                                if fl["inlet"] == self.feature["c_modelid"]:
                                    if fl.geometry().wkbType() == QGis.WKBLineString:
                                        line = fl.geometry().asPolyline()
                                        new_l_g = QgsGeometry.fromPolyline([new_c, line[-1]])
                                        change_map = {fl.id(): new_l_g}
                                        self.sublinks.dataProvider().changeGeometryValues(change_map)
                                    break

                        break
                    except Exception as ex1:
                        print("Searching for object to edit vertex of: " + str(ex1) + '\n' + str(traceback.print_exc()))

            except Exception as ex:
                print("_EditVertex: " + str(ex) + '\n' + str(traceback.print_exc()))
            try:
                self.setQgsMapTool()
            except:
                pass

    def edit_vertex(self, layer, feature, from_geom, to_geom):
        if layer:
            self.undo_stack.push(self._EditVertex(self, layer, feature, from_geom, to_geom))

    def edited_name(self, edited_list):
        """Name of item was edited, need to make sure indexed_list is updated. TODO: check whether name is unique."""
        for old_name, item in edited_list:
            section_field_name = self.section_types[type(item)]
            if hasattr(self.project, section_field_name):
                section = getattr(self.project, section_field_name)
                try:
                    index = section.value.index(item)
                    section.value._index[item.name] = item
                    del section.value._index[old_name]
                except Exception as ex:
                    print("edited_name: " + str(ex) + '\n' + str(traceback.print_exc()))
            else:
                raise Exception("edited_name: Section not found in project: " + section_field_name)
        self.list_objects()
        if self.model_layers:
            self.model_layers.create_layers_from_project(self.project)
            try:
                self.setQgsMapTool()
            except:
                pass

    def new_item_name(self, item_type):
        """ Generate a name for a new item.
            Make sure name is unique within the set of items that item_type falls in
                (links, rain gages, or nodes and subcatchments)
            Search all names in the set of related items for numbers and use a number greater than any in use.
            Use the prefix for item_type from self.project_settings if specified.
        """
        section = getattr(self.project, self.section_types[item_type])
        links_groups = self.project.links_groups()
        if section in links_groups:
            unique_groups = links_groups
        elif section.SECTION_NAME.upper() in ["[RAINGAGES]", "[LABELS]"]:
            unique_groups = [section]
        else:
            unique_groups = self.project.nodes_groups()
            if hasattr(self.project, "subcatchments"):
                unique_groups.append(self.project.subcatchments)
        existing_names = []
        for section in unique_groups:
            for item in section.value:
                existing_names.append(unicode(item.name))
        prefix = u""
        number = 1
        increment = 1

        if self.project_settings:
            item_type_name = item_type.__name__
            prefix = unicode(self.project_settings.value("Labels/" + item_type_name, ""))
            try:
                increment = int(self.project_settings.value("Labels/Increment", 1))
            except:
                pass
            try:
                number = int(self.project_settings.value("Labels/" + item_type_name + "_NextID", 1))
            except:
                pass

        for name in existing_names:
            try:
                digits = filter(unicode.isdigit, name)
                if digits:
                    int_digits = int(digits)
                    if int_digits >= number:
                        number = int_digits + increment
            except Exception as ex:
                print(str(ex))

        str_number = str(number)
        new_name = prefix + str_number
        while new_name in existing_names or str_number in existing_names:
            number += increment
            str_number = str(number)
            new_name = prefix + str_number
        # Avoid making any changes to settings since this might make settings unreadable to SWMM5 interface.
        # if self.project_settings:
        #     self.project_settings.setValue("Labels/" + item_type_name + "_NextID", number + 1)
        return new_name

    def currentTimeChanged(self, slider_val):
        self.time_index = slider_val
        self.signalTimeChanged.emit()

    def setQgsMapToolSelect(self):
        self.actionMapSelectObj.setChecked(True)
        self.setQgsMapTool()

    def setQgsMapToolSelectVertex(self):
        self.actionMapSelectVertex.setChecked(True)
        self.setQgsMapTool()

    def setMenuMapTool(self, aMenuMapToolName):
        if aMenuMapToolName == 'pan':
            self.actionPan.setChecked(True)
        elif aMenuMapToolName == 'zoomin':
            self.actionZoom_in.setChecked(True)
        elif aMenuMapToolName == 'zoomout':
            self.actionZoom_out.setChecked(True)
        elif aMenuMapToolName == 'fullextent':
            self.zoomfull()
        if self.canvas:
            self.map_widget.setZoomInMode()
            self.map_widget.setZoomOutMode()
            self.map_widget.setPanMode()

    def setQgsMapTool(self):
        if self.canvas:
            from map_tools import AddPointTool, AddLinkTool, CaptureTool
            self.map_widget.setZoomInMode()
            self.map_widget.setZoomOutMode()
            self.map_widget.setPanMode()
            self.map_widget.setSelectMode()
            self.map_widget.setEditVertexMode()
            self.map_widget.setMeasureMode()
            for act, name in self.add_point_tools:
                self.map_widget.setAddObjectMode(act, name, AddPointTool)
            for act, name in self.add_link_tools:
                self.map_widget.setAddObjectMode(act, name, AddLinkTool)
            for act, name in self.add_polygon_tools:
                self.map_widget.setAddObjectMode(act, name, CaptureTool)

    def zoomfull(self):
        self.map_widget.zoomfull()

    def map_addfeature(self):
        self.map_widget.setAddFeatureMode()

    def onGeometryAdded(self):
        print 'Geometry Added'

    def onGeometryChanged(self):
        print 'Geometry Changed'

    # def mouseMoveEvent(self, event):
    #     pass
    #     x = event.x()
    #     y = event.y()
    #     if self.canvas:
    #         p = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
    #         self.btnCoord.setText('x,y: {:}, {:}'.format(p.x(), p.y()))

    # def eventFilter(self, source, event):
    #     if event.type() == QtCore.QEvent.MouseMove:
    #         if event.buttons() == QtCore.Qt.NoButton:
    #             pos = event.pos()
    #             x = pos.x()
    #             y = pos.y()
    #             if self.canvas:
    #                 p = self.map_widget.canvas.getCoordinateTransform().toMapCoordinates(x, y)
    #                 self.btnCoord.setText('x,y: %s, %s' % (p.x()), p.y())
    #         else:
    #             pass

    def map_addvector(self):
        directory = self.program_settings.value("GISDataDir", "/")
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Open Vector File...', directory,
                                                     'Shapefiles (*.shp);;All files (*.*)')
        if filename:
            try:
                self.map_widget.addVectorLayer(filename)
                path_only, file_only = os.path.split(filename)
                if path_only != directory:
                    self.program_settings.setValue("GISDataDir", path_only)
                    self.program_settings.sync()
            except Exception as ex:
                print("map_addvector error opening " + filename + ":\n" + str(ex) + '\n' + str(traceback.print_exc()))


        # from frmMapAddVector import frmMapAddVector
        # dlg = frmMapAddVector(self)
        # dlg.show()
        # result = dlg.exec_()
        # if result == 1:
        #     specs = dlg.getLayerSpecifications()
        #     filename = specs['filename']
        #     if filename.lower().endswith('.shp'):
        #         self.map_widget.addVectorLayer(filename)

    def map_addraster(self):
        directory = self.program_settings.value("GISDataDir", "/")
        filename = QtGui.QFileDialog.getOpenFileName(self, "Open Raster...", directory,
                                                     "GeoTiff files (*.tif);;Bitmap (*.bmp);;All files (*.*)")
        #filename = QtGui.QFileDialog.getOpenFileName(None, 'Specify Raster Dataset', '')
        if filename:
            try:
                self.map_widget.addRasterLayer(filename)
                path_only, file_only = os.path.split(filename)
                if path_only != directory:
                    self.program_settings.setValue("GISDataDir", path_only)
                    self.program_settings.sync()
            except Exception as ex:
                print("map_addraster error opening " + filename + ":\n" + str(ex) + '\n' + str(traceback.print_exc()))

    def on_load(self, tree_top_item_list):
        self.obj_tree = ObjectTreeView(self, tree_top_item_list)
        self.obj_tree.itemDoubleClicked.connect(self.edit_options)
        self.obj_tree.itemSelectionChanged.connect(self.list_objects)
        self.listViewObjects.doubleClicked.connect(self.edit_selected_objects)
        self.actionStdEditObject.triggered.connect(self.edit_selected_objects)
        self.listViewObjects.itemSelectionChanged.connect(self.list_selection_changed)

        self.btnObjAdd.clicked.connect(self.add_object_clicked)
        self.btnObjDelete.clicked.connect(self.delete_object_clicked)
        self.btnObjProperty.clicked.connect(self.edit_selected_objects)
        self.btnObjMoveUp.clicked.connect(self.moveup_object)
        self.btnObjMoveDown.clicked.connect(self.movedown_object)
        self.btnObjSort.clicked.connect(self.sort_object)
        self.actionStdDeleteObject.triggered.connect(self.delete_object_clicked)
        self.actionStdMapDimensions.triggered.connect(self.configMapDimensions)

        layout = QtGui.QVBoxLayout(self.tabProject)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.obj_tree)
        self.tabProject.setLayout(layout)
        self.setWindowTitle(self.model)

    def toggle_toolbar(self, eventArg):
        tbname, is_checked = eventArg.split(',')
        if tbname == 'map':
            if is_checked == 'True':
                self.toolBar_Map.setVisible(True)
            else:
                self.toolBar_Map.setVisible(False)
        elif tbname == 'object':
            if is_checked == 'True':
                self.toolBar_Object.setVisible(True)
            else:
                self.toolBar_Object.setVisible(False)
        elif tbname=='standard':
            if is_checked == 'True':
                self.toolBar_Standard.setVisible(True)
            else:
                self.toolBar_Standard.setVisible(False)
        pass

    def configMapDimensions(self):
        from frmMapDimensions import frmMapDimensions
        f = frmMapDimensions(self)
        f.show()
        result = f.exec_()
        if result:
            #from qgis.core import QgsRectangle
            #r = QgsRectangle((float)self.map_widget.coord_origin.x,
            #                 (float)self.map_widget.coord_origin.y,
            #                 (float)self.map_widget.coord_fext.x,
            #                 (float)self.map_widget.coord_fext.y)
            #self.map_widget.canvas.setExtent(r)
            pass
        pass

    def populate_plugins_menu(self):
        if self.plugins:
            menu = self.menuPlugins
            for p in self.plugins:
                lnew_action = QtGui.QAction(p['name'], menu)
                lnew_action.setCheckable(True)
                menu.addAction(lnew_action)
                lnew_action.triggered.connect(self.run_tier1_plugin)

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
                    if hasattr(lplugin, "run"):
                        lplugin.run(self)
                    elif hasattr(lplugin, "classFactory"):
                        plugin_object = lplugin.classFactory(self)
                        plugin_object.initGui()
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
            new_action.triggered.connect(self.run_plugin_custom)
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

    def edit_script(self):
        import editor
        editor.ICON_FOLDER = os.path.join(INSTALL_DIR, "icons", "editor")
        if not os.path.isdir(editor.ICON_FOLDER):
            editor.ICON_FOLDER = os.path.join(os.path.dirname(INSTALL_DIR), "icons", "editor")
        editor.MAX_RECENT_FILES = MAX_RECENT_FILES
        self._editor_form = editor.EditorWindow(parent=self, session=self)
        self._editor_form.session = self
        self._editor_form.show()
        self.add_recent_script(None)  # Populate the recent script menus, not adding one

        #try:
        #    widget = EmbedIPython(session=self, plugins=self.plugins, mainmodule=INIT_MODULE, install_dir=INSTALL_DIR)
        #    ipy_win = self.map.addSubWindow(widget, QtCore.Qt.Widget)
        #    if ipy_win:
        #        ipy_win.show()
        #except Exception as ex:
        #    print("Error opening IPython: " + str(ex) + '\n' + str(traceback.print_exc()))

    def script_browse_and_run(self):
        file_name = self.script_browse_open()
        if file_name:
            self.script_run(file_name)

    def script_browse_open(self, browse_title="Select script"):
        directory = self.program_settings.value("ScriptDir", "")
        file_name = QtGui.QFileDialog.getOpenFileName(self, browse_title, directory,
                                                      "Python Files (*.py);;All files (*.*)")
        if file_name:
            self.add_recent_script(file_name)
            path_only, file_only = os.path.split(file_name)
            if path_only != directory:
                self.program_settings.setValue("ScriptDir", path_only)
                self.program_settings.sync()

        return file_name

    def script_browse_save(self, browse_title="Save Script As..."):
        directory = self.program_settings.value("ScriptDir", "")
        file_name = QtGui.QFileDialog.getSaveFileName(self, browse_title, directory,
                                                            "Python Files (*.py);;All files (*.*)")
        if file_name:
            # Append extension if not there yet
            if not str(file_name).lower().endswith(".py"):
                file_name += ".py"
            self.add_recent_script(file_name)
            path_only, file_only = os.path.split(file_name)
            if path_only != directory:
                self.program_settings.setValue("ScriptDir", path_only)
                self.program_settings.sync()

        return file_name

    def script_run(self, file_name):
        if file_name:
            save_handle = sys.stdout
            try:
                QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                redirected_output = StringIO()
                sys.stdout = redirected_output
                session = self
                with open(file_name, 'r') as script_file:
                    exec(script_file)
                # Potential alternative way to run script, would allow running without saving
                # namespace['__file__'] = script_filename
                # if os.path.exists(script_filename):
                #     source = open(script_filename).read()
                #     code = compile(source, script_filename, 'exec')
                #     exec (code, namespace, namespace)
                QMessageBox.information(None, "Finished Running Script",
                                        file_name + "\n" + redirected_output.getvalue(), QMessageBox.Ok)
            except Exception as ex:
                QMessageBox.information(None, "Exception Running Script",
                                        file_name + '\n' + str(ex), QMessageBox.Ok)
            finally:
                QApplication.restoreOverrideCursor()
            sys.stdout = save_handle

    def run_recent_script(self):
        action = self.sender()
        if action and action.data():
            self.script_run(action.data())

    def open_recent_project(self):
        action = self.sender()
        if action and action.data():
            file_name = action.data()
            if os.path.isfile(file_name):
                self.open_project_quiet(file_name)

    def add_recent(self, file_name, settings_key):
        """ Add a recently accessed file to program settings. Used when opening and saving projects and scripts. """
        files_str = self.program_settings.value(settings_key, None)
        if files_str:
            files = files_str.split('|')
        else:
            files = []

        if files and files[0] == file_name:
            return

        if file_name:
            try:
                files.remove(file_name)
            except:
                pass

            files.insert(0, file_name)

        if files:
            del files[MAX_RECENT_FILES:]
        self.program_settings.setValue(settings_key, u'|'.join(files))
        return files

    def add_recent_project(self, file_name):
        files = self.add_recent(file_name, 'recentProjectList')
        self.update_recent(self.recent_projects, files)

    def add_recent_script(self, file_name):
        files = self.add_recent(file_name, 'recentScriptList')
        self.update_recent(self.recent_scripts, files)
        if self._editor_form:
            # try:
            self.update_recent(self._editor_form.recent_scripts, files)
            # except:
            #     self._editor_form = None

    def run_recent_script(self):
        action = self.sender()
        if action and action.data():
            self.script_run(action.data())

    def create_recent_menus(self, parent_menu, callback):
        """Create recent menus. All are invisible and have no text yet, that happens in update_recent."""
        menus = []
        parent_menu.addSeparator()
        for i in range(MAX_RECENT_FILES):
            action = QtGui.QAction(self, visible=False, triggered=callback)
            # if parent_menu is not self.menuScripting:
            #     action.setShortcut(QKeySequence("Ctrl+" + str(i+1)))
            menus.append(action)
            parent_menu.addAction(action)
        return menus

    @staticmethod
    def update_recent(recent_menu_actions, file_names):
        num_recent = 0
        if file_names:
            num_recent = min(len(file_names), MAX_RECENT_FILES)
            menu_texts = [QtCore.QFileInfo(file_name).fileName() for file_name in file_names]

        for i in range(MAX_RECENT_FILES):
            if i < num_recent:
                # text = "&%d %s" % (i + 1, QtCore.QFileInfo(file_names[i]).fileName())
                text = menu_texts[i]
                if menu_texts.count(text) > 1:
                    text = file_names[i]
                recent_menu_actions[i].setText(text)
                recent_menu_actions[i].setData(file_names[i])
                recent_menu_actions[i].setVisible(True)
            else:
                recent_menu_actions[i].setVisible(False)

        # recent_separator.setVisible((num_recent > 0))

    def make_editor_from_tree(self, search_for, tree_list, selected_items=[], new_item=None):
        edit_form = None
        # If new_item is specified, it is a new item to be edited and is only added if user presses OK.

        # First handle special cases
        section = None
        if search_for == "Pollutants":
            if self.project:
                section = self.project.pollutants
        elif search_for == "Map Labels" or search_for == "Labels":
            if self.project:
                section = self.project.labels

        if section:
            if new_item:
                edit_these = [new_item]
            else:  # add selected items to edit_these
                edit_these = []
                if not isinstance(section.value, basestring):
                    if isinstance(section.value, list):
                        for value in section.value:
                            if value.name in selected_items:
                                edit_these.append(value)
            edit_form = frmGenericPropertyEditor(self, section, edit_these, new_item, self.model + ' ' + search_for + " Editor")
        else:
            for tree_item in tree_list:
                # tree_item is a list: ["name in tree control", editor_form_type, [optional editor form arguments]]
                if search_for == tree_item[0]:  # If we found a matching tree item, return its editor
                    if len(tree_item) > 0 and tree_item[1] and not (type(tree_item[1]) is list):
                        args = [self]
                        if len(tree_item) > 2:
                            # Get arguments for editor creation from tree_item
                            # Usually this is a list, but if not, try to treat it as a single argument
                            if isinstance(tree_item[2], basestring) or not isinstance(tree_item[2], list):
                                args.append(str(tree_item[2]))
                            else:  # tree_item[2] is a list that is not a string
                                args.extend(tree_item[2])
                        args.append(selected_items)
                        args.append(new_item)
                        try:
                            edit_form = tree_item[1](*args)
                        except:  # Try without selected_items and new_item for editors that do not want them
                            args = args[0:-2]
                            edit_form = tree_item[1](*args)
                        edit_form.helper = HelpHandler(edit_form)
                        break
                    return None
                if len(tree_item) > 0 and type(tree_item[1]) is list:  # find whether there is a match in this sub-tree
                    edit_form = self.make_editor_from_tree(search_for, tree_item[1], selected_items, new_item)
                    if edit_form:
                        break
        if edit_form:
            edit_form.new_item = new_item
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

    def current_map_layer(self):
        try:
            return getattr(self.model_layers, self.section_types[self.tree_types[self.tree_section]])
        except:
            pass
        return None

    def list_selection_changed(self):
        try:
            layer = self.current_map_layer()
            self.select_named_items(layer, [str(item.data()) for item in self.listViewObjects.selectedIndexes()])
            if len(self.listViewObjects.selectedIndexes()) > 0:
                self.actionStdEditObject.setEnabled(True)
                self.actionStdDeleteObject.setEnabled(True)
            else:
                self.actionStdEditObject.setEnabled(False)
                self.actionStdDeleteObject.setEnabled(False)
        except Exception as ex:
            msg = str(ex)
            if msg and msg != "''":
                print("List selection changed, but could not select on map:\n" + msg)

    def edit_selected_objects(self):
        # Called on double click of an item in the 'bottom left' list or on the map
        if not self.project or not hasattr(self, "get_editor"):
            return
        if len(self.listViewObjects.selectedItems()) == 0:
            return
        selected = [str(item.data()) for item in self.listViewObjects.selectedIndexes()]
        self.show_edit_window(self.make_editor_from_tree(self.tree_section, self.tree_top_items, selected))

    def add_object_clicked(self):
        if self.project and self.get_editor:
            self.add_object(self.tree_section)

    def delete_object_clicked(self):
        if self.project and self.get_editor:
            selected_names = [str(item.data()) for item in self.listViewObjects.selectedIndexes()]
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Delete Object")
            msgBox.setText("Delete the following objects?")
            msgBox.setInformativeText(",".join(selected_names))
            msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            ret = msgBox.exec_()
            if ret != QMessageBox.Ok:
                return
            self.undo_stack.beginMacro("Delete selected items")  # Keep deletion as one undo action instead of one per item
            #selected_names = [str(item.data()) for item in self.listViewObjects.selectedIndexes()]
            for item_name in selected_names:
                self.delete_named_object(self.tree_section, item_name)
            self.undo_stack.endMacro()

    def moveup_object(self):
        currentRow = self.listViewObjects.currentRow()
        currentItem = self.listViewObjects.takeItem(currentRow)
        self.listViewObjects.insertItem(currentRow - 1, currentItem)

    def movedown_object(self):
        currentRow = self.listViewObjects.currentRow()
        currentItem = self.listViewObjects.takeItem(currentRow)
        self.listViewObjects.insertItem(currentRow + 1, currentItem)

    def sort_object(self):
        self.listViewObjects.sortItems()

    def select_named_items(self, layer, selected_list):
        if self.selecting.acquire(False):
            try:
                if layer:
                    try:
                        layer_name = layer.name()
                        already_selected_item = self.obj_tree.currentItem()
                        if already_selected_item is None or already_selected_item.text(0) != layer_name:
                            tree_node = self.obj_tree.find_tree_item(layer_name)
                            if tree_node:
                                self.obj_tree.setCurrentItem(tree_node)

                        if selected_list:
                            qgis_ids = [f.id() for f in layer.getFeatures() if f.attributes()[0] in selected_list]
                            layer.setSelectedFeatures(qgis_ids)

                    except Exception as ex:
                        print("Did not find layer in tree:\n" + str(ex))

                if selected_list:
                    for i in range(self.listViewObjects.count()):
                        item = self.listViewObjects.item(i)
                        if item.text() in selected_list:
                            self.listViewObjects.setItemSelected(item, True)
                            self.listViewObjects.scrollToItem(item)
                        else:
                            self.listViewObjects.setItemSelected(item, False)
                else:
                    self.listViewObjects.clearSelection()
                    self.map_widget.clearSelectableObjects()
            finally:  # Make sure lock is released even if there is an exception
                self.selecting.release()

    def confirm_discard_project(self):
        if not self.undo_stack.isClean():
            msg = QMessageBox()
            msg.setText("Discard current project?")
            msg.setWindowTitle(self.model)
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            choice = msg.exec_()
            if choice == QMessageBox.Yes:
                return True
            return False
        return True

    def new_project(self):
        self.open_project_quiet(None)

    def open_project(self):
        directory = self.program_settings.value("ProjectDir", "")
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open Project...", directory,
                                                      "Inp files (*.inp);;All files (*.*)")
        if file_name:
            self.add_recent_project(file_name)
            self.open_project_quiet(file_name)
            path_only, file_only = os.path.split(file_name)
            if path_only != directory:
                self.program_settings.setValue("ProjectDir", path_only)

    def setWaitCursor(self):
        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

    def restoreCursor(self):
        QApplication.restoreOverrideCursor()

    def open_project_quiet(self, file_name):
        if not self.confirm_discard_project():
            return
        self.map_widget.remove_all_layers()
        if hasattr(self, "project_settings"):
            del self.project_settings
        self.project_settings = None
        self.project = self.project_type()
        if file_name:
            try:
                project_reader = self.project_reader_type()
                project_reader.read_file(self.project, file_name)
                if self.map_widget:
                    projection_file_name = file_name[:-3] + "prj"
                    self.open_prj(projection_file_name)
                path_only, file_only = os.path.split(file_name)
                self.setWindowTitle(self.model + " - " + file_only)
                self.no_items = False
                ini_file_name = file_name[:-3] + "ini"
                if os.path.isfile(ini_file_name):
                    try:
                        self.project_settings = QtCore.QSettings(ini_file_name, QtCore.QSettings.IniFormat)
                        print("Read project settings from " + self.project_settings.fileName())
                    except Exception as exINI:
                        self.project_settings = None
                        print("error opening " + ini_file_name + ":\n" + str(exINI) + '\n' + str(
                            traceback.print_exc()))

            except Exception as ex:
                print("open_project_quiet error opening " + file_name + ":\n" + str(ex) + '\n' + str(traceback.print_exc()))
                self.project = ProjectBase()
                self.setWindowTitle(self.model)
        else:
            self.project.file_name = "New.inp"
            self.setWindowTitle(self.model + " - New")

    def open_prj(self, projection_file_name):
        if os.path.isfile(projection_file_name):
            try:
                from qgis.core import QgsCoordinateReferenceSystem
                with open(projection_file_name, "rt") as open_file:
                    wkt = open_file.read()
                    self.set_crs(QgsCoordinateReferenceSystem(wkt))
            except Exception as exCRS:
                print("error opening " + projection_file_name + ":\n" + str(exCRS) + '\n' + str(traceback.print_exc()))

    def set_crs(self, crs):
        self.map_widget.map_linear_unit = self.map_widget.map_unit_names[7]  # Unknown
        if crs and crs.isValid():
            self.crs = crs
            try:
                self.map_widget.map_linear_unit = self.map_widget.map_unit_names[self.crs.mapUnits()]
            except:
                pass
        else:
            self.crs = None

    def save_project(self, file_name=None):
        if not file_name:
            file_name = self.project.file_name
        project_writer = self.project_writer_type()
        project_writer.write_file(self.project, file_name)
        # Avoid making any changes to settings since this might make settings unreadable to SWMM5 interface.
        # if self.project_settings:
        #     self.project_settings.sync()
        if self.crs and self.crs.isValid():
            try:
                from qgis.core import QgsCoordinateReferenceSystem
                projection_file_name = file_name[:-3] + "prj"
                with open(projection_file_name, "wt") as save_file:
                    save_file.write(self.crs.toWkt())
            except Exception as exCRS:
                print("error saving " + projection_file_name + ":\n" + str(exCRS) + '\n' + str(traceback.print_exc()))

        self.undo_stack.setClean()
        #if self.map_widget:
        #    self.map_widget.saveVectorLayers(os.path.dirname(file_name))

    def find_external(self, lib_name):
        """ Find the specified library in program_settings, assembly path, Externals folder, or Externals/model.
            Prompt user to find library if not found.
            Save the found location in program_settings."""
        filename = self.program_settings.value("Libraries/" + lib_name, "")
        if not os.path.exists(filename):
            filename = os.path.join(self.assembly_path, lib_name)
            if not os.path.exists(filename):
                path_prefix = os.path.dirname(os.path.dirname(self.assembly_path))
                filename = os.path.join(path_prefix, "Externals", lib_name)
                if not os.path.exists(filename):
                    filename = os.path.join(path_prefix, "Externals", self.model.lower(), "model", lib_name)
                    if not os.path.exists(filename):
                        filename = QtGui.QFileDialog.getOpenFileName(self,
                                                                     'Locate ' + self.model + ' Library', '/',
                                                                     '(*{0})'.format(os.path.splitext(lib_name)[1]))
            if os.path.exists(filename):
                self.program_settings.setValue("Libraries/" + lib_name, filename)
        return filename

    def save_project_as(self):
        """ Prompt for file to save as and save project. Returns file name if saved, None on cancel or error. """
        directory = self.program_settings.value("ProjectDir", "")
        file_name = QtGui.QFileDialog.getSaveFileName(self, "Save As...", directory, "Inp files (*.inp)")
        if file_name:
            self.add_recent_project(file_name)
            path_only, file_only = os.path.split(file_name)
            try:
                self.save_project(file_name)
                self.setWindowTitle(self.model + " - " + file_only)
                if path_only != directory:
                    self.program_settings.setValue("ProjectDir", path_only)
                    self.program_settings.sync()
                return file_name
            except Exception as ex:
                print(str(ex) + '\n' + str(traceback.print_exc()))
                QMessageBox.information(self, self.model,
                                        "Error saving {0}\nin {1}\n{2}\n{2}".format(
                                            file_only, path_only,
                                            str(ex), str(traceback.print_exc())),
                                        QMessageBox.Ok)
        return None

    def dragEnterEvent(self, drag_enter_event):
        """ When user drags an item onto the form, show that the form will accept if dragging a file. """
        if drag_enter_event.mimeData().hasUrls():
            drag_enter_event.accept()
        else:
            drag_enter_event.ignore()

    def dropEvent(self, drop_event):
        """ When user drops a file onto the form:
            Open as a project if file extension is .inp,
            Open as a projection if file extension is .prj,
            Otherwise try opening as a GIS layer. """
        for url in drop_event.mimeData().urls():
            directory, filename = os.path.split(str(url.encodedPath()))
            directory = str.lstrip(str(directory), 'file:')
            # print(directory)
            if os.path.isdir(directory):
                pass  # print(' is directory')
            elif os.path.isdir(directory[1:]):
                directory = directory[1:]
            filename = str.rstrip(str(filename), '\r\n')
            print("Opening " + filename)
            full_path = os.path.join(directory, filename)
            lfilename = filename.lower()
            if lfilename.endswith('.inp'):
                self.open_project_quiet(full_path)
            elif lfilename.endswith('.prj'):
                self.open_prj(full_path)
            else:
                if not self.map_widget.add_layer_from_file(full_path):
                    QMessageBox.information(self, self.model,
                                            "Could not open dropped file '" + full_path + "'", QMessageBox.Ok)

    def action_exit(self):
        if not self.confirm_discard_project():
            return
        del self.program_settings
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

    def clear_object_listing(self):
        self.tree_section = ''
        self.listViewObjects.clear()

    def list_objects(self):
        selected_text = ''
        for item in self.obj_tree.selectedIndexes():
            selected_text = str(item.data())
        self.clear_object_listing()
        self.dockw_more.setWindowTitle('')
        if self.project is None or not selected_text:
            return
        names = self.get_object_list(selected_text)
        self.tree_section = selected_text
        if names is None:
            self.dockw_more.setEnabled(False)
        else:
            self.dockw_more.setEnabled(True)
            self.dockw_more.setWindowTitle(selected_text)
            self.listViewObjects.addItems(names)

    def onLoad(self):
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setContentsMargins(1, 2, 1, 3)
        self.listViewObjects.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        if len(self.listViewObjects.selectedIndexes()) > 0:
            self.actionStdEditObject.setEnabled(True)
            self.actionStdDeleteObject.setEnabled(True)
        else:
            self.actionStdEditObject.setEnabled(False)
            self.actionStdDeleteObject.setEnabled(False)

class ModelLayers:
    """
    This is a base class for creating and managing the map layers that are directly linked to model elements.
    Model-specific inheritors contain the model-specific set of layers.
    """
    def __init__(self, map_widget):
        self.map_widget = map_widget
        self.nodes_layers = []
        self.links_layers = []
        self.all_layers = []
        self.map_widget.remove_all_layers()

    def create_layers_from_project(self, project):
        # First remove old ModelLayers already on the map
        self.map_widget.remove_all_layers()
        self.project = project

    def all_node_features(self):
        features = []
        for layer in self.nodes_layers:
            if layer and layer.isValid():
                for feature in layer.getFeatures():
                    features.append(feature)
        return features

    def all_link_features(self):
        features = []
        for layer in self.links_layers:
            if layer and layer.isValid():
                for feature in layer.getFeatures():
                    features.append(feature)
        return features

    def layer_by_name(self, layer_name):
        try:
            return getattr(self, layer_name)
        except:
            return None


def print_process_id():
    print 'Process ID is:', os.getpid()

if __name__ == '__main__':
    application = QtGui.QApplication(sys.argv)
    QMessageBox.information(None, "frmMain",
                            "Run ui/EPANET/frmMainEPANET or ui/SWMM/frmMainSWMM instead of frmMain.",
                            QMessageBox.Ok)
