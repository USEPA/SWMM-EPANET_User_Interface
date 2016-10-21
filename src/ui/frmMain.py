import os, sys
os.environ['QT_API'] = 'pyqt'
import sip
for typ in ["QString","QVariant", "QDate", "QDateTime", "QTextStream", "QTime", "QUrl"]:
    sip.setapi(typ, 2)
from cStringIO import StringIO
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


class frmMain(QtGui.QMainWindow, Ui_frmMain):

    signalTimeChanged = QtCore.pyqtSignal()

    def __init__(self, q_application):
        QtGui.QMainWindow.__init__(self, None)
        self.setupUi(self)
        self.q_application = q_application
        try:
            print("QsciScintilla.SC_TYPE_STRING:")
            print(str(QsciScintilla.SC_TYPE_STRING))
        except Exception as exQsci:
            print str(exQsci)
        self._forms = []
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
        self.populate_plugins_menu()
        self.time_widget.setVisible(False)
        self.actionStdNewProjectMenu.triggered.connect(self.new_project)
        self.actionStdNewProject.triggered.connect(self.new_project)
        self.actionStdOpenProjMenu.triggered.connect(self.open_project)
        self.actionStdOpenProj.triggered.connect(self.open_project)
        self.actionStdExit.triggered.connect(self.action_exit)
        self.actionIPython.triggered.connect(self.script_ipython)
        self.actionExec.triggered.connect(self.script_exec)
        self.actionStdSave.triggered.connect(self.save_project)
        self.actionStdSaveMenu.triggered.connect(self.save_project)
        self.actionStdSave_As.triggered.connect(self.save_project_as)
        self.actionStdRun_Simulation.triggered.connect(self.run_simulation)
        self.actionRun_SimulationMenu.triggered.connect(self.run_simulation)
        self.actionStdProjCalibration_Data.triggered.connect(self.calibration_data)
        self.tabProjMap.currentChanged.connect(self.tabProjMapChanged)
        self.actionStdPrint.triggered.connect(self.saveMapAsImage)
        self.actionSave_Map_As_Image.triggered.connect(self.saveMapAsImage)
        self.actionGroup_Obj = QActionGroup(self)

        self.setAcceptDrops(True)
        self.tree_section = ''

        # Map attributes will be set below if possible or will remain None to indicate map is not present.
        self.canvas = None
        self.map_widget = None
        self.selecting = Lock()
        try:
            # TODO: make sure this works on all platforms, both in dev environment and in our installed packages
            orig_path = os.environ["Path"]
            search_paths = []
            if os.environ.has_key("QGIS_PREFIX_PATH"):
                search_paths.append(os.environ.get("QGIS_PREFIX_PATH"))
            if os.environ.has_key("QGIS_HOME"):
                search_paths.append(os.environ.get("QGIS_HOME"))
            dirname = INSTALL_DIR
            while dirname:
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
                    if os.path.isdir(qgis_home):
                        # os.environ["Path"] = r"C:/OSGeo4W64/apps/Python27/Scripts;C:/OSGeo4W64/apps/qgis/bin;C:/OSGeo4W64/bin;" + os.environ["Path"]
                        updir = os.path.dirname(qgis_home)
                        updir2 = os.path.dirname(updir)
                        os.environ["Path"] = os.path.join(updir, r"/Python27/Scripts;") +\
                                             os.path.join(qgis_home, "bin;") + \
                                             os.path.join(updir2, "bin;") + orig_path
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
                            self.actionAdd_Vector.triggered.connect(self.map_addvector)
                            self.actionAdd_Raster.triggered.connect(self.map_addraster)
                            self.actionPan.triggered.connect(self.setQgsMapTool)
                            self.actionMapSelectObj.triggered.connect(self.setQgsMapTool)
                            self.actionZoom_in.triggered.connect(self.setQgsMapTool)
                            self.actionZoom_out.triggered.connect(self.setQgsMapTool)
                            self.actionZoom_full.triggered.connect(self.zoomfull)
                            self.actionAdd_Feature.setCheckable(False)
                            self.actionAdd_Feature.triggered.connect(self.map_addfeature)

                            # self.actionGroup_Obj.addAction(self.actionObjAddGage)
                            # self.actionGroup_Obj.addAction(self.actionObjAddSub)
                            # self.actionGroup_Obj.addAction(self.actionObjAddConduit)
                            # self.actionGroup_Obj.addAction(self.actionObjAddDivider)
                            # self.actionGroup_Obj.addAction(self.actionObjAddJunc)
                            # self.actionGroup_Obj.addAction(self.actionObjAddLabel)
                            # self.actionGroup_Obj.addAction(self.actionObjAddOrifice)
                            # self.actionGroup_Obj.addAction(self.actionObjAddOutfall)
                            # self.actionGroup_Obj.addAction(self.actionObjAddOutlet)
                            # self.actionGroup_Obj.addAction(self.actionObjAddPump)
                            # self.actionGroup_Obj.addAction(self.actionObjAddStorage)
                            # self.actionGroup_Obj.addAction(self.actionObjAddTank)
                            # self.actionGroup_Obj.addAction(self.actionObjAddValve)
                            # self.actionGroup_Obj.addAction(self.actionObjAddWeir)
                            print("Found QGIS " + qgis_home)
                            break  # Success, done looking for a qgis_home
                except Exception as e1:
                    msg = "Did not load QGIS from " + qgis_home + ": " + str(e1) + '\n' # + str(traceback.print_exc())
                    print(msg)
                    # QMessageBox.information(None, "Error Initializing Map", msg, QMessageBox.Ok)
        except Exception as eImport:
            self.canvas = None
        if not self.canvas:
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

    def tabProjMapChanged(self, index):
        if index == 1:
            self.time_widget.setVisible(True)
        else:
            self.time_widget.setVisible(False)

    def saveMapAsImage(self):
        gui_settings = QtCore.QSettings(self.model, "GUI")
        directory = gui_settings.value("ProjectDir", "")
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
            section_field_name = session.section_types[type(item)]
            if not hasattr(session.project, section_field_name):
                raise Exception("Section not found in project: " + section_field_name)
            self.section = getattr(session.project, section_field_name)
            self.layer = self.session.model_layers.layer_by_name(section_field_name)

        def redo(self):
            if self.item.name == '' or self.item.name in self.section.value:
                self.item.name = self.session.new_item_name(type(self.item))
            if len(self.section.value) == 0 and not isinstance(self.section, list):
                self.section.value = IndexedList([], ['name'])
            self.section.value.append(self.item)
            # self.session.list_objects()  # Refresh the list of items on the form
            list_item = self.session.listViewObjects.addItem(self.item.name)
            self.session.listViewObjects.scrollToItem(list_item)
            if self.layer:
                self.session.map_widget.clearSelectableObjects()
                self.layer.startEditing()
                if isinstance(self.item, Coordinate):
                    added = self.layer.dataProvider().addFeatures([self.session.map_widget.point_feature_from_item(self.item)])
                elif isinstance(self.item, Link):
                    added = self.layer.dataProvider().addFeatures([
                        self.session.map_widget.line_feature_from_item(self.item,
                                                                       self.session.project.all_nodes())])
                elif isinstance(self.item, Polygon):
                    added = self.layer.dataProvider().addFeatures([self.session.map_widget.polygon_feature_from_item(self.item)])

                if added[0]:
                    self.added_id = added[1][0].id()
                    self.layer.updateExtents()
                    self.layer.commitChanges()
                    self.layer.triggerRepaint()
                    self.session.map_widget.canvas.refresh()
                else:
                    self.added_id = None
                    self.layer.rollBack()

        def undo(self):
            self.section.value.remove(self.item)
            self.session.list_objects()  # Refresh the list of items on the form
            # self.session.listViewObjects.takeItem(len(self.section.value))
            if self.added_id is not None:
                self.session.map_widget.clearSelectableObjects()
                self.layer.startEditing()
                self.layer.dataProvider().deleteFeatures([self.added_id])
                self.layer.commitChanges()
                self.layer.updateExtents()
                self.layer.triggerRepaint()
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
                self.session.map_widget.selectTool.build_spatial_index()
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

    def new_item_name(self, item_type):
        """ Generate a name for a new item.
            Start with a default of the number of items already in this section plus one (converted to a string).
            Next, search all sections and increase the number as needed if something already has that name. """
        section = getattr(self.project, self.section_types[item_type])
        number = len(section.value)
        found = True
        while found:
            number += 1
            new_name = str(number)
            found = False
            for obj_type, section_name in self.section_types.iteritems():
                section = getattr(self.project, section_name)
                if new_name in section.value:
                    found = True
                    break
        return str(number)

    def currentTimeChanged(self, slider_val):
        self.time_index = slider_val
        self.signalTimeChanged.emit()

    def setQgsMapTool(self):
        if self.canvas:
            from map_tools import AddPointTool, AddLinkTool, CaptureTool
            self.map_widget.setZoomInMode()
            self.map_widget.setZoomOutMode()
            self.map_widget.setPanMode()
            self.map_widget.setSelectMode()
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

    def mouseMoveEvent(self, event):
        pass
        x = event.x()
        y = event.y()
        if self.canvas:
            p = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            self.btnCoord.setText('x,y: {:}, {:}'.format(p.x(), p.y()))

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            if event.buttons() == QtCore.Qt.NoButton:
                pos = event.pos()
                x = pos.x()
                y = pos.y()
                if self.canvas:
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
        # self.obj_tree.itemClicked.connect(self.list_objects)
        self.obj_tree.itemSelectionChanged.connect(self.list_objects)
        self.listViewObjects.doubleClicked.connect(self.edit_selected_objects)
        self.listViewObjects.itemSelectionChanged.connect(self.list_selection_changed)

        self.btnObjAdd.clicked.connect(self.add_object_clicked)
        self.btnObjDelete.clicked.connect(self.delete_object_clicked)
        self.btnObjProperty.clicked.connect(self.edit_selected_objects)
        self.btnObjMoveUp.clicked.connect(self.moveup_object)
        self.btnObjMoveDown.clicked.connect(self.movedown_object)
        self.btnObjSort.clicked.connect(self.sort_object)

        # self.tabProjMap.addTab(self.obj_tree, 'Project')
        layout = QtGui.QVBoxLayout(self.tabProject)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.obj_tree)
        self.tabProject.setLayout(layout)
        self.setWindowTitle(self.model)
        '''
        self.obj_list = ObjectListView(model=self.model, ObjRoot='', ObjType='', ObjList=None)
        mlayout = self.dockw_more.layout()
        # mlayout.setContentsMargins(0, 0, 0, 0)
        mlayout.addWidget(self.obj_list)
        # layout1 = QVBoxLayout(self.dockw_more)
        self.dockw_more.setLayout(mlayout)
        # self.actionPan.setEnabled(False)
        '''

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

    def script_ipython(self):
        pass
        #widget = EmbedIPython(session=self, plugins=self.plugins, mainmodule=INIT_MODULE)
        #ipy_win = self.map.addSubWindow(widget,QtCore.Qt.Widget)
        #if ipy_win:
        #    ipy_win.show()

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
            self.undo_stack.beginMacro("Delete selected items")  # Keep deletion as one undo action instead of one per item
            selected_names = [str(item.data()) for item in self.listViewObjects.selectedIndexes()]
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

    def new_project(self):
        self.open_project_quiet(None, None, None)

    def open_project(self):
        gui_settings = QtCore.QSettings(self.model, "GUI")
        directory = gui_settings.value("ProjectDir", "")
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open Project...", directory,
                                                      "Inp files (*.inp);;All files (*.*)")
        if file_name:
            self.open_project_quiet(file_name, gui_settings, directory)

    def open_project_quiet(self, file_name, gui_settings, directory):
        self.project = self.project_type()
        if file_name:
            try:
                project_reader = self.project_reader_type()
                project_reader.read_file(self.project, file_name)
                path_only, file_only = os.path.split(file_name)
                self.setWindowTitle(self.model + " - " + file_only)
                if path_only != directory:
                    gui_settings.setValue("ProjectDir", path_only)
                    gui_settings.sync()
                    del gui_settings
            except Exception as ex:
                print("open_project_quiet error opening " + file_name + ":\n" + str(ex) + '\n' + str(traceback.print_exc()))
                self.project = ProjectBase()
                self.setWindowTitle(self.model)
        else:
            self.project.file_name = "New.inp"
            self.setWindowTitle(self.model + " - New")

    def save_project(self, file_name=None):
        if not file_name:
            file_name = self.project.file_name
        project_writer = self.project_writer_type()
        project_writer.write_file(self.project, file_name)
        if self.map_widget:
            self.map_widget.saveVectorLayers(os.path.dirname(file_name))

    def find_external(self, lib_name):
        filename = os.path.join(self.assembly_path, lib_name)
        if not os.path.exists(filename):
            pp = os.path.dirname(os.path.dirname(self.assembly_path))
            filename = os.path.join(pp, "Externals", lib_name)
        if not os.path.exists(filename):
            pp = os.path.dirname(os.path.dirname(self.assembly_path))
            filename = os.path.join(pp, "Externals", self.model.lower(), "model", lib_name)
        if not os.path.exists(filename):
            filename = QtGui.QFileDialog.getOpenFileName(self,
                                                         'Locate ' + self.model + ' Library',
                                                         '/', '(*{0})'.format(os.path.splitext(lib_name)[1]))
        return filename

    def save_project_as(self):
        gui_settings = QtCore.QSettings(self.model, "GUI")
        directory = gui_settings.value("ProjectDir", "")
        file_name = QtGui.QFileDialog.getSaveFileName(self, "Save As...", directory, "Inp files (*.inp)")
        if file_name:
            path_only, file_only = os.path.split(file_name)
            try:
                self.save_project(file_name)
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

    def dragEnterEvent(self, drag_enter_event):
        if drag_enter_event.mimeData().hasUrls():
            drag_enter_event.accept()
        else:
            drag_enter_event.ignore()

    def dropEvent(self, drop_event):
        #TODO: check project status and prompt if there are unsaved changes that would be overwritten
        for url in drop_event.mimeData().urls():
            directory, filename = os.path.split(str(url.encodedPath()))
            directory = str.lstrip(str(directory), 'file:')
            print(directory)
            if os.path.isdir(directory):
                print(' is directory')
            elif os.path.isdir(directory[1:]):
                directory = directory[1:]
            filename = str.rstrip(str(filename), '\r\n')
            print(filename)
            full_path = os.path.join(directory, filename)
            lfilename = filename.lower()
            if lfilename.endswith('.inp'):
                gui_settings = QtCore.QSettings(self.model, "GUI")
                self.open_project_quiet(full_path, gui_settings, directory)
            #TODO - check to see if QGIS can handle file type
            elif lfilename.endswith('.shp') or lfilename.endswith(".json"):
                self.map_widget.addVectorLayer(full_path)
            else:
                try:
                    self.map_widget.addRasterLayer(full_path)
                except:
                    QMessageBox.information(self, self.model,
                            "Dropped file '" + full_path + "' is not a know type of file",
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
        ids = self.get_object_list(selected_text)
        self.tree_section = selected_text
        if ids is None:
            self.dockw_more.setEnabled(False)
        else:
            self.dockw_more.setEnabled(True)
            self.dockw_more.setWindowTitle(selected_text)
            self.listViewObjects.addItems(ids)

    def onLoad(self):
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setContentsMargins(1, 2, 1, 3)
        self.listViewObjects.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)


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

    def create_layers_from_project(self, project):
        self.project = project
        # First remove old ModelLayers already on the map
        self.map_widget.remove_layers(self.all_layers)

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
