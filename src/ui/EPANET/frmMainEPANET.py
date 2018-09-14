import os, sys
os.environ['QT_API'] = 'pyqt'
import sip
for typ in ["QString","QVariant", "QDate", "QDateTime", "QTextStream", "QTime", "QUrl"]:
    sip.setapi(typ, 2)
import traceback
import webbrowser
from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog, QAction
from PyQt5.QtCore import QObject, QSettings
from threading import Lock, Thread
from time import sleep


from ui.model_utility import QString, from_utf8, transl8, process_events
from ui.help import HelpHandler
from ui.frmMain import frmMain, ModelLayers
from ui.EPANET.frmEnergyOptions import frmEnergyOptions
from ui.EPANET.frmHydraulicsOptions import frmHydraulicsOptions
from ui.EPANET.frmMapBackdropOptions import frmMapBackdropOptions
from ui.EPANET.frmQualityOptions import frmQualityOptions
from ui.EPANET.frmReactionsOptions import frmReactionsOptions
from ui.EPANET.frmReportOptions import frmReportOptions
from ui.EPANET.frmTimesOptions import frmTimesOptions
from ui.EPANET.frmTitle import frmTitle

from ui.EPANET.frmAbout import frmAbout
from ui.EPANET.frmSummary import frmSummary
from ui.EPANET.frmControls import frmControls
from ui.EPANET.frmJunction import frmJunction
from ui.EPANET.frmReservoir import frmReservior
from ui.EPANET.frmTank import frmTank
from ui.EPANET.frmPipe import frmPipe
from ui.EPANET.frmPump import frmPump
from ui.EPANET.frmValve import frmValve
from ui.EPANET.frmCurveEditor import frmCurveEditor
from ui.EPANET.frmPatternEditor import frmPatternEditor
from ui.EPANET.frmSourcesQuality import frmSourcesQuality
from ui.EPANET.frmDemands import frmDemands
from ui.EPANET.frmGraph import frmGraph
from ui.EPANET.frmTable import frmTable
from ui.EPANET.frmEnergyReport import frmEnergyReport
from ui.EPANET.frmCalibrationData import frmCalibrationData
from ui.EPANET.frmCalibrationReportOptions import frmCalibrationReportOptions
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor

from core.epanet.epanet_project import EpanetProject as Project
from core.epanet.inp_reader_project import ProjectReader
from core.epanet.inp_writer_project import ProjectWriter
from core.epanet.hydraulics.node import Junction
from core.epanet.hydraulics.node import Reservoir
from core.epanet.hydraulics.node import Tank
from core.epanet.hydraulics.link import Pipe
from core.epanet.hydraulics.link import Pump
from core.epanet.hydraulics.link import Valve
from core.epanet.labels import Label

from core.epanet.patterns import Pattern
from core.epanet.curves import Curve

import core.epanet.reports as reports
from core.epanet.options.quality import QualityAnalysisType
from Externals.epanet.model.epanet2 import ENepanet
from Externals.epanet.outputapi import ENOutputWrapper
from ui.EPANET.frmRunEPANET import frmRunEPANET

import Externals.epanet.outputapi.ENOutputWrapper as ENO
import ui.convenience
from ui.EPANET.inifile import DefaultsEPANET


class frmMainEPANET(frmMain):
    """Main form for EPANET user interface, based on frmMain which is shared with SWMM."""

    # Variables used to populate the tree control
    # Each item is a list: label plus either editing form for this section or a child list.
    # Special cases may just have a label and no editing form or children.
    # *_items are a lists of items in a section
    tree_options_Hydraulics = ["Hydraulics", frmHydraulicsOptions]
    tree_options_Quality = ["Quality", frmQualityOptions]
    tree_options_Reactions = ["Reactions", frmReactionsOptions]
    tree_options_Times = ["Times", frmTimesOptions]
    tree_options_Energy = ["Energy", frmEnergyOptions]
    tree_options_Report = ["Report", frmReportOptions]
    tree_options_MapBackdrop = ["Map/Backdrop", frmMapBackdropOptions]
    tree_options_items = [tree_options_Hydraulics,
                          tree_options_Quality,
                          tree_options_Reactions,
                          tree_options_Times,
                          tree_options_Energy,
                          tree_options_Report,
                          tree_options_MapBackdrop]

    tree_controls_Simple = ["Simple", frmControls, ["EPANET Simple Controls", "CONTROLS"]]
    tree_controls_RuleBased = ["Rule-Based", frmControls, ["EPANET Rule-Based Controls", "RULES"]]
    tree_controls_items = [tree_controls_Simple,
                           tree_controls_RuleBased]

    tree_TitleNotes = ["Title/Notes", frmTitle]
    tree_Options = ["Options", tree_options_items]
    tree_Junctions = ["Junctions", frmJunction]
    tree_Reservoirs = ["Reservoirs", frmReservior]
    tree_Tanks = ["Tanks", frmTank]
    tree_Pipes = ["Pipes", frmPipe]
    tree_Pumps = ["Pumps", frmPump]
    tree_Valves = ["Valves", frmValve]
    tree_Labels = ["Labels", None]
    tree_Patterns = ["Patterns", frmPatternEditor]
    tree_Curves = ["Curves", frmCurveEditor]
    tree_Controls = ["Controls", tree_controls_items]
    tree_top_items = [tree_TitleNotes,
                      tree_Options,
                      tree_Junctions,
                      tree_Reservoirs,
                      tree_Tanks,
                      tree_Pipes,
                      tree_Pumps,
                      tree_Valves,
                      tree_Labels,
                      tree_Patterns,
                      tree_Curves,
                      tree_Controls]
    tree_nodes_items = [
        tree_Junctions,
        tree_Reservoirs,
        tree_Tanks]

    def __init__(self, q_application):
        self.model = "EPANET"
        self.program_settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "EPA", self.model)
        print("Read program settings from " + self.program_settings.fileName())
        self.model_path = ''  # Set this only if needed later when running model
        self.output = None    # Set this when model output is available
        self.status_suffix = "_status.txt"
        self.status_file_name = ''  # Set this when model status is available
        self.output_filename = ''   # Set this when model output is available
        self.project_type = Project  # Use the model-specific Project as defined in core.epanet.project
        self.project_reader_type = ProjectReader
        self.project_writer_type = ProjectWriter
        self.project = Project()
        self.assembly_path = os.path.dirname(os.path.abspath(__file__))
        frmMain.__init__(self, q_application)
        self.on_load(tree_top_item_list=self.tree_top_items)
        self.project_settings = DefaultsEPANET("", self.project)
        self.tree_types = {
            self.tree_Patterns[0]: Pattern,
            self.tree_Curves[0]: Curve,
            self.tree_Junctions[0]: Junction,
            self.tree_Reservoirs[0]: Reservoir,
            self.tree_Tanks[0]: Tank,
            self.tree_Pipes[0]: Pipe,
            self.tree_Pumps[0]: Pump,
            self.tree_Valves[0]: Valve,
            self.tree_Labels[0]: Label
        }

        self.section_types = {
            Pattern: "patterns",
            Curve: "curves",
            Junction: "junctions",
            Reservoir: "reservoirs",
            Tank: "tanks",
            Pipe: "pipes",
            Pump: "pumps",
            Valve: "valves",
            Label: "labels"
        }

        if self.map_widget:  # initialize empty model map layers, ready to have model elements added
            self.model_layers = ModelLayersEPANET(self.map_widget)

        HelpHandler.init_class(os.path.join(self.assembly_path, "epanet.qhc"))
        self.help_topic = ""  # TODO: specify topic to open when Help key is pressed on main form
        self.helper = HelpHandler(self)

        self.actionTranslate_Coordinates = QAction(self)
        self.actionTranslate_Coordinates.setObjectName(from_utf8("actionTranslate_CoordinatesMenu"))
        self.actionTranslate_Coordinates.setText(transl8("frmMain", "Translate Coordinates", None))
        self.actionTranslate_Coordinates.setToolTip(transl8("frmMain", "Change model objects coordinates", None))
        self.menuView.addAction(self.actionTranslate_Coordinates)
        #QObject.connect(self.actionTranslate_Coordinates, QtCore.SIGNAL('triggered()'), lambda: self.open_translate_coord_dialog(None, None))
        self.actionTranslate_Coordinates.triggered.connect(lambda: self.open_translate_coord_dialog(None, None))

        self.actionStdProjSummary.triggered.connect(self.show_summary)
        self.actionStdProjSimulation_Options.triggered.connect(self.edit_simulation_options)
        self.menuProject.removeAction(self.actionStdProjDetails)  # remove menus that are SWMM-specific
        self.menuTools.removeAction(self.actionStdConfigTools)
        self.menuTools.removeAction(self.actionStdProgPrefer)
        self.menuTools.deleteLater()
        self.menuObjects.deleteLater()
        self.toolBar_Standard.removeAction(self.actionProjTableStatistics)

        self.actionStatus_ReportMenu = QAction(self)
        self.actionStatus_ReportMenu.setObjectName(from_utf8("actionStatus_ReportMenu"))
        self.actionStatus_ReportMenu.setText(transl8("frmMain", "Status", None))
        self.actionStatus_ReportMenu.setToolTip(transl8("frmMain", "Display Simulation Status", None))
        self.menuReport.addAction(self.actionStatus_ReportMenu)
        self.actionStatus_ReportMenu.triggered.connect(self.report_status)
        self.actionProjStatus.triggered.connect(self.report_status)

        self.actionEnergy_ReportMenu = QAction(self)
        self.actionEnergy_ReportMenu.setObjectName(from_utf8("actionEnergy_ReportMenu"))
        self.actionEnergy_ReportMenu.setText(transl8("frmMain", "Energy", None))
        self.actionEnergy_ReportMenu.setToolTip(transl8("frmMain", "Display Simulation Energy", None))
        self.menuReport.addAction(self.actionEnergy_ReportMenu)
        self.actionEnergy_ReportMenu.triggered.connect(self.report_energy)

        self.actionCalibration_ReportMenu = QAction(self)
        self.actionCalibration_ReportMenu.setObjectName(from_utf8("actionCalibration_ReportMenu"))
        self.actionCalibration_ReportMenu.setText(transl8("frmMain", "Calibration", None))
        self.actionCalibration_ReportMenu.setToolTip(transl8("frmMain", "Display Simulation Calibration", None))
        self.menuReport.addAction(self.actionCalibration_ReportMenu)
        self.actionCalibration_ReportMenu.triggered.connect(self.report_calibration)

        self.actionReaction_ReportMenu = QAction(self)
        self.actionReaction_ReportMenu.setObjectName(from_utf8("actionReaction_ReportMenu"))
        self.actionReaction_ReportMenu.setText(transl8("frmMain", "Reaction", None))
        self.actionReaction_ReportMenu.setToolTip(transl8("frmMain", "Display Simulation Reaction", None))
        self.menuReport.addAction(self.actionReaction_ReportMenu)
        self.actionReaction_ReportMenu.triggered.connect(self.report_reaction)

        self.actionFull_ReportMenu = QAction(self)
        self.actionFull_ReportMenu.setObjectName(from_utf8("actionFull_ReportMenu"))
        self.actionFull_ReportMenu.setText(transl8("frmMain", "Full...", None))
        self.actionFull_ReportMenu.setToolTip(transl8("frmMain", "Save full report as text file", None))
        self.menuReport.addAction(self.actionFull_ReportMenu)
        self.actionFull_ReportMenu.triggered.connect(self.report_full)

        self.actionGraph_ReportMenu = QAction(self)
        self.actionGraph_ReportMenu.setObjectName(from_utf8("actionGraph_ReportMenu"))
        self.actionGraph_ReportMenu.setText(transl8("frmMain", "Graph...", None))
        self.actionGraph_ReportMenu.setToolTip(transl8("frmMain", "Display graph selection options", None))
        self.menuReport.addAction(self.actionGraph_ReportMenu)
        self.actionGraph_ReportMenu.triggered.connect(self.report_graph)
        self.actionProjPlotTimeseries.triggered.connect(self.report_graph)
        self.actionProjPlotScatter.triggered.connect(self.report_graph)
        self.actionProjPlotProfile.setVisible(False)

        self.actionTable_ReportMenu = QAction(self)
        self.actionTable_ReportMenu.setObjectName(from_utf8("actionTable_ReportMenu"))
        self.actionTable_ReportMenu.setText(transl8("frmMain", "Table...", None))
        self.actionTable_ReportMenu.setToolTip(transl8("frmMain", "Display table selection options", None))
        self.menuReport.addAction(self.actionTable_ReportMenu)
        self.actionTable_ReportMenu.triggered.connect(self.report_table)
        self.actionProjTableTimeseries.triggered.connect(self.report_table)

        self.actionStdMapQuery.triggered.connect(self.map_query)
        self.actionStdMapFind.triggered.connect(self.map_finder)

        self.Help_Topics_Menu = QAction(self)
        self.Help_Topics_Menu.setObjectName(from_utf8("Help_Topics_Menu"))
        self.Help_Topics_Menu.setText(transl8("frmMain", "Help Topics", None))
        self.Help_Topics_Menu.setToolTip(transl8("frmMain", "Display Help Topics", None))
        self.menuHelp.addAction(self.Help_Topics_Menu)
        self.Help_Topics_Menu.triggered.connect(self.help_topics)

        self.Help_About_Menu = QAction(self)
        self.Help_About_Menu.setObjectName(from_utf8("Help_About_Menu"))
        self.Help_About_Menu.setText(transl8("frmMain", "About", None))
        self.Help_About_Menu.setToolTip(transl8("frmMain", "About EPANET", None))
        self.menuHelp.addAction(self.Help_About_Menu)
        self.Help_About_Menu.triggered.connect(self.help_about)

        self.cbFlowUnits.clear()
        self.cbFlowUnits.addItems(['Flow Units: CFS','Flow Units: GPM','Flow Units: MGD','Flow Units: IMGD',
                                   'Flow Units: AFD','Flow Units: LPS','Flow Units: LPM','Flow Units: MLD',
                                   'Flow Units: CMH','Flow Units: CMD'])
        self.cbFlowUnits.currentIndexChanged.connect(self.cbFlowUnits_currentIndexChanged)
        self.cbOffset.setVisible(False)

        self.cboDate.setVisible(False)
        self.lblDate.setVisible(False)
        self.sbETime.setVisible(False)
        self.txtETime.setVisible(False)
        self.lblETime.setVisible(False)

        if self.map_widget:
            self.map_widget.applyLegend()
            self.map_widget.LegendDock.setVisible(False)
            self.cboMapSubcatchments.setVisible(False)
            self.lblMapSubcatchments.setVisible(False)
            self.set_thematic_controls()
            self.cboMapNodes.currentIndexChanged.connect(self.update_thematic_map)
            self.cboMapLinks.currentIndexChanged.connect(self.update_thematic_map)
            self.signalTimeChanged.connect(self.update_thematic_map_time)
            # self.signalTimeChanged.connect(self.update_time_display)

    def set_thematic_controls(self):
        self.allow_thematic_update = False
        self.cboMapNodes.clear()
        self.cboMapNodes.addItems(['None','Elevation','Base Demand','Initial Quality'])
        self.cboMapLinks.clear()
        self.cboMapLinks.addItems(['None','Length','Diameter','Roughness','Bulk Coeff.','Wall Coeff.'])
        if self.output:
            # Add object type labels to map combos if there are any of each type in output
            object_type = ENO.ENR_node_type
            if object_type:
                attribute_names = [attribute.name for attribute in object_type.Attributes]
                for item in attribute_names:
                    self.cboMapNodes.addItem(item)
            object_type = ENO.ENR_link_type
            if object_type:
                attribute_names = [attribute.name for attribute in object_type.Attributes]
                for item in attribute_names:
                    if item == "Status" or item == "Setting":
                        continue
                    self.cboMapLinks.addItem(item)
            self.horizontalTimeSlider.setMaximum(self.output.num_periods - 1)

        self.allow_thematic_update = True
        self.update_thematic_map()

    def update_thematic_map(self):
        if not self.allow_thematic_update or not self.map_widget:
            return

        enable_time_widget = False

        if self.model_layers.nodes_layers:
            selected_attribute = self.cboMapNodes.currentText()
            attribute = None
            setting_index = self.cboMapNodes.currentIndex()
            if setting_index < 4:
                meta_item = Junction.metadata.meta_item_of_label(selected_attribute)
                attribute = meta_item.attribute
            color_by = {}
            self.thematic_node_min = None
            self.thematic_node_max = None
            if attribute:  # Found an attribute of the node class to color by
                for item in self.project.all_nodes():
                    value = float(getattr(item, attribute, 0))
                    color_by[item.name] = value
                    if self.thematic_node_min is None or value < self.thematic_node_min:
                        self.thematic_node_min = value
                    if self.thematic_node_max is None or value > self.thematic_node_max:
                        self.thematic_node_max = value

            elif self.output:  # Look for attribute to color by in the output
                attribute = ENO.ENR_node_type.get_attribute_by_name(selected_attribute)
                if attribute:
                    enable_time_widget = True
                    # find min and max values over entire run
                    # ToDo: this needs to be sped up!!!
                    for time_increment in range(0, self.output.num_periods-1):
                        values = ENO.ENR_node_type.get_attribute_for_all_at_time(self.output, attribute,  time_increment)
                        for value in values:
                            if self.thematic_node_min is None or value < self.thematic_node_min:
                                self.thematic_node_min = value
                            if self.thematic_node_max is None or value > self.thematic_node_max:
                                self.thematic_node_max = value
                    values = ENO.ENR_node_type.get_attribute_for_all_at_time(self.output, attribute, self.time_index)
                    index = 1
                    for node in self.output.nodes.values():
                        color_by[node.name] = values[index]
                        index += 1

            # for layer in self.model_layers.nodes_layers:
            #     if layer.isValid():
            #         if color_by:
            #             self.map_widget.applyGraduatedSymbologyStandardMode(layer, color_by,
            #                                                                 self.thematic_node_min,
            #                                                                 self.thematic_node_max)
            #         else:
            #             self.map_widget.set_default_point_renderer(layer)
            #         layer.triggerRepaint()

        if self.model_layers.links_layers:
            selected_attribute = self.cboMapLinks.currentText()
            attribute = None
            setting_index = self.cboMapLinks.currentIndex()
            if setting_index < 6:
                meta_item = Pipe.metadata.meta_item_of_label(selected_attribute)
                attribute = meta_item.attribute
            color_by = {}
            self.thematic_link_min = None
            self.thematic_link_max = None
            if attribute:  # Found an attribute of the pipe class to color by
                for link in self.project.all_links():
                    try:
                        if attribute == 'max_depth':
                            pass
                            # for value in self.project.xsections.value:
                            #     if value.link == conduit.name:
                            #         color_by[conduit.name] = float(value.geometry1)
                        else:
                            color_by[link.name] = float(getattr(link, attribute, 0))
                        if self.thematic_link_min is None or color_by[link.name] < self.thematic_link_min:
                            self.thematic_link_min = color_by[link.name]
                        if self.thematic_link_max is None or color_by[link.name] > self.thematic_link_max:
                            self.thematic_link_max = color_by[link.name]
                    except Exception as exLinkAtt:
                        print("update_thematic_map: link attribute: " + link.name + ': ' + str(exLinkAtt))

            elif self.output:  # Look for attribute to color by in the output
                attribute = ENO.ENR_link_type.get_attribute_by_name(selected_attribute)
                if attribute:
                    enable_time_widget = True
                    # find min and max values over entire run
                    for time_increment in range(0, self.output.num_periods-1):
                        values = ENO.ENR_link_type.get_attribute_for_all_at_time(self.output, attribute,  time_increment)
                        for value in values:
                            if self.thematic_link_min is None or value < self.thematic_link_min:
                                self.thematic_link_min = value
                            if self.thematic_link_max is None or value > self.thematic_link_max:
                                self.thematic_link_max = value
                    values = ENO.ENR_link_type.get_attribute_for_all_at_time(self.output, attribute, self.time_index)
                    index = 0
                    for link in self.output.links.values():
                        color_by[link.name] = values[index]
                        index += 1
            # for layer in self.model_layers.links_layers:
            #     if layer.isValid():
            #         if color_by:
            #             self.map_widget.applyGraduatedSymbologyStandardMode(layer, color_by,
            #                                                                 self.thematic_link_min,
            #                                                                 self.thematic_link_max)
            #         else:
            #             self.map_widget.set_default_line_renderer(layer)
            #         layer.triggerRepaint()
        self.time_widget.setVisible(enable_time_widget)
        if enable_time_widget:
            self.update_thematic_map_time()

    def update_thematic_map_time(self):
        """
            Update thematic map for the current self.time_index.
            Depends on update_thematic_map having been called since last change to thematic map options.
        """
        try:
            if not self.allow_thematic_update or not self.map_widget:
                return

            if self.model_layers.nodes_layers:
                selected_attribute = self.cboMapNodes.currentText()
                setting_index = self.cboMapNodes.currentIndex()
                color_by = {}
                if setting_index >= 4 and self.output:  # Look for attribute to color by in the output
                    attribute = ENO.ENR_node_type.get_attribute_by_name(selected_attribute)
                    if attribute:
                        values = ENO.ENR_node_type.get_attribute_for_all_at_time(self.output, attribute, self.time_index)
                        # index = 1
                        for node in self.output.nodes.values():
                            color_by[node.name] = values[node.index]
                            # index += 1

                for layer in self.model_layers.nodes_layers:
                    if layer.isValid():
                        do_label = self.map_widget.do_label(layer)
                        if color_by:
                            if layer.id() in self.map_widget.layer_styles and \
                                self.map_widget.validatedGraduatedSymbol(None, self.map_widget.layer_styles[layer.id()]):
                                self.map_widget.applyGraduatedSymbologyStandardMode(layer, color_by,
                                                                                    self.thematic_node_min,
                                                                                    self.thematic_node_max,
                                                            self.map_widget.layer_styles[layer.id()],
                                                                                    True, None, do_label)
                            else:
                                self.map_widget.applyGraduatedSymbologyStandardMode(layer, color_by,
                                                                                self.thematic_node_min,
                                                                                self.thematic_node_max,
                                                                                    None, True, None, do_label)
                            self.annotate_layername(selected_attribute, "node", layer)
                        else:
                            if len(self.project.all_nodes()) > 300:
                                do_label = False
                            self.map_widget.set_default_point_renderer(layer, None, 3.5, do_label)
                        layer.triggerRepaint()

            if self.model_layers.links_layers:
                selected_attribute = self.cboMapLinks.currentText()
                setting_index = self.cboMapLinks.currentIndex()
                color_by = {}
                if setting_index >= 6 and self.output:  # Look for attribute to color by in the output
                    attribute = ENO.ENR_link_type.get_attribute_by_name(selected_attribute)
                    if attribute:
                        values = ENO.ENR_link_type.get_attribute_for_all_at_time(self.output, attribute, self.time_index)
                        # index = 1
                        for link in self.output.links.values():
                            color_by[link.name] = values[link.index]
                            # index += 1

                color_by_flow = None
                if selected_attribute and selected_attribute.lower() == "flow":
                    color_by_flow = color_by
                elif self.chkDisplayFlowDir.isChecked():
                    color_by_flow = {}
                    selected_attribute = "Flow"
                    attribute = ENO.ENR_link_type.get_attribute_by_name(selected_attribute)
                    if attribute:
                        values = ENO.ENR_link_type.get_attribute_for_all_at_time(self.output, attribute, self.time_index)
                        # index = 1
                        for link in self.output.links.values():
                            color_by_flow[link.name] = values[link.index]
                            # index += 1

                for layer in self.model_layers.links_layers:
                    if layer.isValid():
                        do_label = self.map_widget.do_label(layer)
                        if len(self.project.all_links()) > 300:
                            do_label = False

                        if color_by:
                            if layer.id() in self.map_widget.layer_styles and \
                                self.map_widget.validatedGraduatedSymbol(None,self.map_widget.layer_styles[layer.id()]):
                                self.map_widget.applyGraduatedSymbologyStandardMode(layer, color_by,
                                                                                    self.thematic_link_min,
                                                                                    self.thematic_link_max,
                                                                             self.map_widget.layer_styles[layer.id()],
                                                                                    self.chkDisplayFlowDir.isChecked(),
                                                                                    color_by_flow, do_label)
                            else:
                                self.map_widget.applyGraduatedSymbologyStandardMode(layer, color_by,
                                                                                self.thematic_link_min,
                                                                                self.thematic_link_max,
                                                                                    None,
                                                                                    self.chkDisplayFlowDir.isChecked(),
                                                                                    color_by_flow, do_label)
                            self.annotate_layername(selected_attribute, "link", layer)
                        else:
                            self.map_widget.set_default_line_renderer(layer, do_label)
                        layer.triggerRepaint()
            if self.cboTime.count() > 0:
                if self.time_index >=0 and self.time_index < self.cboTime.count():
                    # self.cboTime.disconnect(self.cboTime, "currentIndexChanged()",
                    #                         self.update_thematic_map_time)
                    self.cboTime.setCurrentIndex(self.time_index)
                    # self.cboTime.connect(self.cboTime, "currentIndexChanged()",
                    #                         self.update_thematic_map_time)
        except Exception as exBig:
            print("Exception in update_thematic_map_time: " + str(exBig))

    def annotate_layername(self, selected_attribute, obj_type, layer):
        """
        Append attribute and its unit to layer name in legend
        Args:
            selected_attribute: node/link attribute name
            obj_type: either 'node' or 'link'
            layer: map layer to be applied with graduated symbols
        Returns: None
        """
        unit_text = ""
        if obj_type == "node":
            if selected_attribute in self.output.nodes_units:
                unit_text = self.output.nodes_units[selected_attribute]
            else:
                if selected_attribute == "Elevation":
                    if self.output.unit_system:
                        unit_text = "m"
                    else:
                        unit_text = "ft"
                elif selected_attribute == "Base Demand":
                    unit_text = self.output.links_units["Flow"]
                elif selected_attribute == "Initial Quality":
                    unit_text = self.output.links_units["Quality"]
        elif obj_type == "link":
            if selected_attribute in self.output.links_units:
                unit_text = self.output.links_units[selected_attribute]
            else:
                if selected_attribute == "Length":
                    if self.output.unit_system:
                        unit_text = "m"
                    else:
                        unit_text = "ft"
                elif selected_attribute == "Diameter":
                    if self.output.unit_system:
                        unit_text = "m"
                    else:
                        unit_text = "in"

        layer_name = layer.name()
        if " [" in layer_name:
            layer_name = layer_name[0:layer_name.index(" [")]
        if unit_text:
            layer.setName(layer_name + " [" + selected_attribute + ", " + unit_text + "]")
        else:
            layer.setName(layer_name + " [" + selected_attribute + "]")

    def animate_e(self):
        if self.output:
            for self.time_index in range(1, self.output.num_periods):
                self.horizontalTimeSlider.setSliderPosition(self.time_index)
                sleep(2)

    def animate_e_step(self, i):
        if self.output:
            if i >= 0 and i <= self.output.num_periods:
                self.horizontalTimeSlider.setSliderPosition(i)

    def cboMap_currentIndexChanged(self):
        pass

    def cbFlowUnits_currentIndexChanged(self):
        import core.epanet.options.hydraulics
        self.project.options.hydraulics.flow_units = core.epanet.options.hydraulics.FlowUnits[self.cbFlowUnits.currentText()[12:]]
        self.project.metric = self.project.options.hydraulics.flow_units in core.epanet.options.hydraulics.flow_units_metric

    def report_status(self):
        print ("report_status")
        if not os.path.isfile(self.status_file_name):
            prefix, extension = os.path.splitext(self.project.file_name)
            if os.path.isfile(prefix + self.status_suffix):
                self.status_file_name = prefix + self.status_suffix
        if os.path.isfile(self.status_file_name):
            webbrowser.open_new_tab(self.status_file_name)
        else:
            QMessageBox.information(None, self.model,
                                    "Model status not found.\n"
                                    "Run the model to generate model status.",
                                    QMessageBox.Ok)

    def report_energy(self):
        if self.output:
            self._frmEnergyReport = frmEnergyReport(self)
            self._frmEnergyReport.set_data(self.project, self.output)
            self._frmEnergyReport.show()
        else:
            QMessageBox.information(None, self.model,
                                    "Model output not found.\n"
                                    "Run the model to generate output.",
                                    QMessageBox.Ok)

    def report_calibration(self):
        if self.output:
            self._frmCalibrationReportOptions = frmCalibrationReportOptions(self,
                                                                            self.project,
                                                                            self.output)
            self._frmCalibrationReportOptions.show()
        else:
            QMessageBox.information(None, self.model,
                                    "Model output not found.\n"
                                    "Run the model to generate output.",
                                    QMessageBox.Ok)

    def report_reaction(self):
        self.reaction_report()
        pass

    def report_full(self):
        if self.output:
            directory = os.path.dirname(self.project.file_name)
            report_file_name, ftype = QFileDialog.getSaveFileName(self, "Save Full Report As...", directory, "Text files (*.txt)")
            if report_file_name:
                try:
                    reporter = reports.Reports(self.project, self.output)
                    reporter.write_report(report_file_name)
                    webbrowser.open_new_tab(report_file_name)
                except Exception as e1:
                    msg = str(e1) + '\n' + str(traceback.print_exc())
                    print(msg)
                    QMessageBox.information(None, self.model,
                                            "Error writing report to \n" + report_file_name + '\n' + msg,
                                            QMessageBox.Ok)

        else:
            QMessageBox.information(None, self.model,
                                    "There is no model output currently open.\n"
                                    "Model output is automatically opened after model is run.",
                                    QMessageBox.Ok)

    def report_graph(self):
        if self.output:
            self._frmGraph = frmGraph(self)
            self._frmGraph.set_from(self.project, self.output)
            self._frmGraph.show()
        else:
            QMessageBox.information(None, self.model,
                                    "Model output not found.\n"
                                    "Run the model to generate output.",
                                    QMessageBox.Ok)

    def report_table(self):
        if self.output:
            self._frmTable = frmTable(self)
            self._frmTable.set_from(self.project, self.output)
            self._frmTable.show()
        else:
            QMessageBox.information(None, self.model,
                                    "Model output not found.\n"
                                    "Run the model to generate output.",
                                    QMessageBox.Ok)

    def reaction_report(self):
        # Reaction Report'

        if self.output:
            # Find conversion factor to kilograms/day
            ucf = 1.0e6/24
            quality_options = self.project.options.quality
            if quality_options.quality != QualityAnalysisType.NONE:
                if 'ug' in str(quality_options.mass_units):
                    ucf = 1.0e9/24

                # Get average reaction rates from output file
                bulk, wall, tank, source = self.output.get_reaction_summary()
                bulk /= ucf
                wall /= ucf
                tank /= ucf
                source /= ucf

                if bulk > 0 or wall > 0 or tank > 0 or source > 0:
                    footer_text = "Inflow Rate = " + format(source,'0.1f')
                else:
                    footer_text = 'No reactions occurred'

                import matplotlib.pyplot as plt

                labels = "%10.1f Tanks" % tank, "%10.1f Bulk" % bulk, "%10.1f Wall" % wall
                sum_reaction = bulk + wall + tank
                size_bulk = bulk / sum_reaction
                size_wall = wall / sum_reaction
                size_tank = tank / sum_reaction
                sizes = [size_tank, size_bulk, size_wall]
                colors = ['green', 'blue', 'red']
                explode = (0, 0, 0)

                plt.figure("Reaction Report")

                plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                        autopct='%1.2f%%', shadow=True, startangle=180)

                plt.axis('equal')
                plt.suptitle("Average Reaction Rates (kg/day)", fontsize=16)
                plt.text(0.9,-0.9,footer_text)

                plt.show()
            else:
                QMessageBox.information(None, self.model,
                                    "No water quality analysis is specified.\n"
                                    "See Options --> Quality.",
                                    QMessageBox.Ok)
        else:
            QMessageBox.information(None, self.model,
                                    "Model output not found.\n"
                                    "Run the model to generate output.",
                                    QMessageBox.Ok)

    def calibration_data(self):
        self._frmCalibrationData = frmCalibrationData(self)
        self._frmCalibrationData.show()
        pass

    def edit_defaults(self):
        directory = self.program_settings.value("ProjectDir", "")
        from ui.EPANET.frmDefaultsEditor import frmDefaultsEditor
        fd = frmDefaultsEditor(self, self.project, self.project_settings)
        fd.show()

    def map_query(self):
        from ui.EPANET.frmQuery import frmQuery
        frmQ = frmQuery(self, self.project)
        frmQ.show()

    def map_finder(self):
        from ui.EPANET.frmFind import frmFind
        frmF = frmFind(self, self.project)
        frmF.show()

    def map_overview(self):
        layerset = []
        layerset.append(self.model_layers.pipes.id())
        layerset.append(self.model_layers.pumps.id())
        layerset.append(self.model_layers.valves.id())
        self.map_widget.create_overview(layerset)
        pass

    def edit_simulation_options(self):
        self.show_edit_window(self.get_editor('Hydraulics'))

    def get_editor(self, edit_name):
        frm = None
        # First handle special cases where forms need more than simply being created

        # the following items will respond to a click on a node form, not the tree diagram
        if edit_name == 'Labels':
            edit_these = []
            new_item = None
            if self.project and self.project.labels:
                if not isinstance(self.project.labels.value, str):
                    if isinstance(self.project.labels.value, list):
                        edit_these.extend(self.project.labels.value)
                if len(edit_these) == 0:
                    new_item = Label()
                    new_item.name = "NewLabel"
                    edit_these.append(new_item)
                    self.project.labels.value = edit_these
                else:
                    self.new_item = False
            frm = frmGenericPropertyEditor(self, self.project.labels, edit_these, new_item, "EPANET Map Label Editor")
            frm.helper = HelpHandler(frm)
            frm.help_topic = "epanet/src/src/maplabeleditordialog.htm"
        elif edit_name == 'Patterns' or edit_name == 'Curves':
            # in these cases the click on the tree diagram populates the lower left list, not directly to an editor
            return None
        elif edit_name == self.tree_Junctions[0] and len(self.project.junctions.value) == 0:
            return None
        elif edit_name == self.tree_Reservoirs[0] and len(self.project.reservoirs.value) == 0:
            return None
        elif edit_name == self.tree_Tanks[0] and len(self.project.tanks.value) == 0:
            return None
        elif edit_name == self.tree_Pipes[0] and len(self.project.pipes.value) == 0:
            return None
        elif edit_name == self.tree_Pumps[0] and len(self.project.pumps.value) == 0:
            return None
        elif edit_name == self.tree_Valves[0] and len(self.project.valves.value) == 0:
            return None
        elif edit_name == self.tree_Labels[0] and len(self.project.labels.value) == 0:
            return None
        else:  # General-purpose case finds most editors from tree information
            frm = self.make_editor_from_tree(edit_name, self.tree_top_items)
        return frm

    def get_editor_with_selected_items(self, edit_name, selected_items):
        return self.make_editor_from_tree(edit_name, self.tree_top_items, selected_items)

    def get_object_list(self, category):
        section = self.project.find_section(category)
        if category == 'Quality' or category == 'Controls' or category == 'Reactions':
            return None
        if section and isinstance(section.value, list):
            return [item.name for item in section.value]
        else:
            return None

    def move_object_in_list(self, category, item_name, old_index, new_index):
        section = self.project.find_section(category)
        if section and isinstance(section.value, list):
            item = section.value[item_name]
            section.value.remove(section.value[old_index])
            section.value.insert(new_index, item)

    def sort_objects_in_list(self, category):
        section = self.project.find_section(category)
        if section and isinstance(section.value, list):
            section.value.sort(key=lambda x: x.name)

    def add_object(self, tree_text):
        item_type = self.tree_types[tree_text]
        new_item = item_type()
        new_item.name = self.new_item_name(item_type)
        if self.project_settings:
            self.project_settings.apply_default_attributes(new_item)
        self.show_edit_window(self.make_editor_from_tree(self.tree_section, self.tree_top_items, [], new_item))

    def delete_named_object(self, tree_text, item_name):
        item_type = self.tree_types[tree_text]
        section_field_name = self.section_types[item_type]

        if hasattr(self.project, section_field_name):
            section = getattr(self.project, section_field_name)
        else:
            raise Exception("Section not found in project: " + section_field_name)
        item = section.value[item_name]
        self.delete_item(item)

    def run_simulation(self):
        # self.open_output()
        # return

        # Find input file to run
        # TODO: decide whether to automatically save to temp location as previous version did.
        use_existing = self.project and self.project.file_name
        if use_existing:
            filename, file_extension = os.path.splitext(self.project.file_name)
            ts = QtCore.QTime.currentTime().toString().replace(":", "_")
            if not os.path.exists(self.project.file_name_temporary):
                self.project.file_name_temporary = filename + "_trial_" + ts + file_extension
            self.save_project(self.project.file_name_temporary)
        elif self.project.all_nodes():
            # unsaved changes to a new project have been made, prompt to save
            if self.save_project_as():
                use_existing = True
            else:
                return None
        else:
            self.open_project()

        inp_file_name = ''
        if self.project:
            inp_file_name = self.project.file_name_temporary

        if os.path.exists(inp_file_name):
            current_directory = os.getcwd()
            if not os.path.exists(self.model_path):
                if 'darwin' in sys.platform:
                    lib_name = 'libepanet.dylib.dylib'
                elif 'win' in sys.platform:
                    lib_name = 'epanet2_amd64.dll'
                else:  # Linux
                    lib_name = 'libepanet2_amd64.so'
                self.model_path = self.find_external(lib_name)
            if os.path.exists(self.model_path):
                try:
                    prefix, extension = os.path.splitext(inp_file_name)
                    self.status_file_name = prefix + self.status_suffix
                    self.output_filename = prefix + '.out'
                    working_dir = os.path.abspath(os.path.dirname(inp_file_name))
                    if os.path.isdir(working_dir):
                        print("Changing into directory containing input file: " + working_dir)
                        os.chdir(working_dir)
                    else:
                        try:
                            import tempfile
                            working_dir = tempfile.gettempdir()
                            print("Changing into temporary directory: " + working_dir)
                            os.chdir(working_dir)
                        except Exception as err_temp:
                            print("Could not change into temporary directory: " + str(err_temp))

                    if self.output:
                        self.output.close()
                        self.output = None
                    model_api = ENepanet(inp_file_name, self.status_file_name, self.output_filename, self.model_path)
                    frmRun = frmRunEPANET(model_api, self.project, self)
                    self._forms.append(frmRun)
                    frmRun.Execute()
                    # self.report_status()
                    if frmRun.run_err_msg:
                        # raise Exception(frmRun.run_err_msg)
                        return

                    try:
                        self.output = ENOutputWrapper.OutputObject(self.output_filename)
                        self.output.build_units_dictionary()
                        self.set_thematic_controls()
                        self.labelStartTime.setText('0:00')
                        if self.output:
                            time_labels = []
                            self.cboTime.clear()
                            for i in range(1, self.output.num_periods):
                                time_labels.append(self.output.get_time_string(i))
                            self.cboTime.addItems(time_labels)
                            # self.cboTime.currentIndexChanged.connect(self.update_thematic_map)
                        self.labelEndTime.setText(self.project.times.duration)
                        return
                    except Exception as e1:
                        print(str(e1) + '\n' + str(traceback.print_exc()))
                        QMessageBox.information(None, self.model,
                                                "Error opening model output:\n {0}\n{1}\n{2}".format(
                                                    self.output_filename, str(e1), str(traceback.print_exc())),
                                                QMessageBox.Ok)
                except Exception as e1:
                    print(str(e1) + '\n' + str(traceback.print_exc()))
                    QMessageBox.information(None, self.model,
                                            "Model library:\n {0}\n{1}\n{2}".format(
                                                self.model_path, str(e1), str(traceback.print_exc())),
                                            QMessageBox.Ok)
                finally:
                    try:
                        os.chdir(current_directory)
                        if model_api and model_api.isOpen():
                            model_api.ENclose()
                    except:
                        pass
                    return

            # # Could not run with library, try running with executable
            # # Run executable with StatusMonitor0
            # args = []
            # self.modelenv1 = 'EXE_EPANET'
            # program = os.environ[self.modelenv1]
            #
            # exe_name = "epanet2d.exe"
            # exe_path = os.path.join(self.assembly_path, exe_name)
            # if not os.path.exists(exe_path):
            #     pp = os.path.dirname(os.path.dirname(self.assembly_path))
            #     exe_path = os.path.join(pp, "Externals", exe_name)
            # if not os.path.exists(exe_path):
            #     exe_path = QFileDialog.getOpenFileName(self, 'Locate EPANET Executable', '/',
            #                                              'exe files (*.exe)')
            # if os.path.exists(exe_path):
            #     os.environ[self.modelenv1] = exe_path
            # else:
            #     os.environ[self.modelenv1] = ''
            #
            # if not os.path.exists(program):
            #     QMessageBox.information(None, "EPANET", "EPANET Executable not found", QMessageBox.Ok)
            #     return -1
            #
            # args.append(file_name)
            # args.append(prefix + '.txt')
            # args.append(prefix + '.out')
            # status = model_utility.StatusMonitor0(program, args, self, model='EPANET')
            # status.show()
            # os.chdir(current_directory)
        else:
            QMessageBox.information(None, self.model, self.model + " input file not found", QMessageBox.Ok)

    def open_output(self):
        inp_file_name = ''
        if self.project:
            inp_file_name = self.project.file_name

        if os.path.exists(inp_file_name):
            current_directory = os.getcwd()
            if not os.path.exists(self.model_path):
                if 'darwin' in sys.platform:
                    lib_name = 'libepanet.dylib.dylib'
                elif 'win' in sys.platform:
                    lib_name = 'epanet2_amd64.dll'
                else:  # Linux
                    lib_name = 'libepanet2_amd64.so'
                self.model_path = self.find_external(lib_name)
            if os.path.exists(self.model_path):
                try:
                    prefix, extension = os.path.splitext(inp_file_name)
                    self.status_file_name = prefix + self.status_suffix
                    self.output_filename = prefix + '.out'
                    working_dir = os.path.abspath(os.path.dirname(inp_file_name))
                    if os.path.isdir(working_dir):
                        print("Changing into directory containing input file: " + working_dir)
                        os.chdir(working_dir)
                    else:
                        try:
                            import tempfile
                            working_dir = tempfile.gettempdir()
                            print("Changing into temporary directory: " + working_dir)
                            os.chdir(working_dir)
                        except Exception as err_temp:
                            print("Could not change into temporary directory: " + str(err_temp))
                    if self.output:
                        self.output.close()
                        self.output = None
                    try:
                        if os.path.exists(self.output_filename):
                            self.output = ENOutputWrapper.OutputObject(self.output_filename)
                            self.set_thematic_controls()
                        return
                    except Exception as e1:
                        print(str(e1) + '\n' + str(traceback.print_exc()))
                        QMessageBox.information(None, self.model,
                                                "Error opening model output:\n {0}\n{1}\n{2}".format(
                                                    self.output_filename, str(e1), str(traceback.print_exc())),
                                                QMessageBox.Ok)
                except Exception as e1:
                    print(str(e1) + '\n' + str(traceback.print_exc()))
                    QMessageBox.information(None, self.model,
                                            "Error running model with library:\n {0}\n{1}\n{2}".format(
                                                self.model_path, str(e1), str(traceback.print_exc())),
                                            QMessageBox.Ok)
                finally:
                    try:
                        os.chdir(current_directory)
                    except:
                        pass
                    return
        else:
            QMessageBox.information(None, self.model, self.model + " input file not found", QMessageBox.Ok)

    def help_topics(self):
        self.helper.show_help()

    def help_about(self):
        self._frmAbout = frmAbout(self)
        self._frmAbout.show()

    def show_summary(self):
        self._frmSummary = frmSummary(self)
        self._frmSummary.show()

    def open_project_quiet(self, file_name):
        """ Set wait cursor during open to show operation is in progress.
            Open project from file_name using frmMain.open_project_quiet.
            Create model layers on map and set UI controls from opened project. """
        self.setWaitCursor()
        if file_name:
            self.setWindowTitle("Reading " + file_name)
        if self.map_widget:
            self.map_widget.setVisible(False)
        self.repaint()
        frmMain.open_project_quiet(self, file_name)
        ui.convenience.set_combo(self.cbFlowUnits, 'Flow Units: ' + self.project.options.hydraulics.flow_units.name)

        if self.time_widget:
            self.labelStartTime.setText('0:00')
            self.labelEndTime.setText(self.project.times.duration)
        if self.map_widget:
            try:
                self.model_layers.create_layers_from_project(self.project)
                self.map_widget.load_extra_layers()
                self.map_widget.zoomfull()
                self.setQgsMapTool()  # Reset any active tool that still has state from old project
            except Exception as ex:
                print(str(ex) + '\n' + str(traceback.print_exc()))
            self.map_widget.setVisible(True)
        self.restoreCursor()


class ModelLayersEPANET(ModelLayers):
    """
    Create and manage the map layers that are directly linked to SWMM model elements.
    Layer names must match the text in the tree control for the corresponding model section.
    """
    def __init__(self, map_widget):
        ModelLayers.__init__(self, map_widget)
        addCoordinates = self.map_widget.addCoordinates
        addLinks = self.map_widget.addLinks
        self.junctions = addCoordinates(None, "Junctions")
        self.reservoirs = addCoordinates(None, "Reservoirs")
        self.tanks = addCoordinates(None, "Tanks")
        self.sources = addCoordinates(None, "Sources")
        self.labels = addCoordinates(None, "Labels")
        self.pumps = addLinks(None, None, "Pumps", QColor('red'), 1)
        self.valves = addLinks(None, None, "Valves", QColor('green'), 2)
        self.pipes = addLinks(None, None, "Pipes", QColor('gray'), 3)
        self.set_lists()

    def set_lists(self):
        self.nodes_layers = [self.junctions, self.reservoirs, self.tanks, self.sources]
        self.links_layers = [self.pumps, self.valves, self.pipes]
        self.all_layers = [self.labels]
        self.all_layers.extend(self.nodes_layers)
        self.all_layers.extend(self.links_layers)

    def create_layers_from_project(self, project):
        ModelLayers.create_layers_from_project(self, project)
        addCoordinates = self.map_widget.addCoordinates
        addLinks = self.map_widget.addLinks

        # Add new layers containing objects from this project
        self.junctions = addCoordinates(project.junctions.value, "Junctions")
        self.reservoirs = addCoordinates(project.reservoirs.value, "Reservoirs")
        self.tanks = addCoordinates(project.tanks.value, "Tanks")
        self.sources = addCoordinates(project.sources.value, "Sources")
        self.labels = addCoordinates(project.labels.value, "Labels")

        coordinates = project.all_nodes()
        self.pumps = addLinks(coordinates, project.pumps.value, "Pumps", QColor('red'), 1)
        self.valves = addLinks(coordinates, project.valves.value, "Valves", QColor('green'), 2)
        self.pipes = addLinks(coordinates, project.pipes.value, "Pipes", QColor('gray'), 3)
        self.set_lists()

    def find_layer_by_name(self, aname):
        if not aname:
            return None
        if aname.lower().startswith("junc"):
            return self.junctions
        elif aname.lower().startswith("pipe"):
            return self.pipes
        elif aname.lower().startswith("reser"):
            return self.reservoirs
        elif aname.lower().startswith("tank"):
            return self.tanks
        elif aname.lower().startswith("sourc"):
            return self.sources
        elif aname.lower().startswith("label"):
            return self.labels
        elif aname.lower().startswith("pump"):
            return self.pumps
        elif aname.lower().startswith("valve"):
            return self.valves
        else:
            return None

if __name__ == '__main__':
    application = QApplication(sys.argv)

    'try out internationalization'
    from ui.settings import internationalization
    lang_setting = internationalization()
    lang_setting.set_language()
    if lang_setting.ui_language != "English":
        application.installTranslator(lang_setting.ui_mTranslator)

    main_form = frmMainEPANET(application)
    main_form.show()
    sys.exit(application.exec_())
