from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow
from ui.help import HelpHandler
from ui.frmQueryDesigner import Ui_frmQuery
import Externals.swmm.outputapi.SMOutputWrapper as SWMMO
import core.swmm.hydraulics.node as snode
import core.swmm.hydraulics.link as slink
import core.swmm.hydrology.subcatchment as sub
import core.swmm.hydrology.lidcontrol as lid


class frmQuery(QMainWindow, Ui_frmQuery):

    def __init__(self, session, project):
        QMainWindow.__init__(self, session)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/Submitti.htm"
        self.setupUi(self)
        self.session = session
        self.project = project

        self.selected_objects = {}

        self.model_attributes = {}
        self.model_attributes["subcatchment"] = ["Area", "Width", "% Slope", "% Impervious", "% LID Usage"]
        self.model_attributes["node"] = ["Invert"]
        self.model_attributes["link"] = ["Max. Depth", "Roughness", "% Slope"]
        self.model_attributes["lid"] = ["Any LIDs", "Bio-Retention Cell", "Rain Garden", "Green Roof",
                                   "Infiltration Trench", "Permeable Pavement", "Rain Barrel",
                                   "Rooftop Disconnected", "Vegetative Swale"]
        self.model_attributes["inflow_node"] = ["Direct Inflow", "DW Inflow", "RDII Inflow", "GW Inflow"]

        self.cboFind.currentIndexChanged.connect(self.cboFind_Changed)

        self.cboFind.addItem('Find Subcatchments with')
        self.cboFind.addItem('Find Nodes with')
        self.cboFind.addItem('Find Links with')
        self.cboFind.addItem('Find Subcatchments with LID')
        self.cboFind.addItem('Find Nodes with Inflow')

        self.cboAbove.addItem('Below')
        self.cboAbove.addItem('Equal To')
        self.cboAbove.addItem('Above')

        self.cmdSubmit.clicked.connect(self.cmdSubmit_Clicked)

    def cboFind_Changed(self):
        # Changes list of map display variables to choose
        # from when user switches between Node & Link query.
        self.txtNum.setVisible(True)
        self.cboAbove.setVisible(True)
        self.cboProperty.clear()
        object_type = None
        if self.cboFind.currentIndex() == 0: #sub
            self.cboProperty.addItems(self.model_attributes["subcatchment"])
            if self.session.output:
                object_type = SWMMO.SwmmOutputSubcatchment
        elif self.cboFind.currentIndex() == 1: #node
            self.cboProperty.addItems(self.model_attributes["node"])
            if self.session.output:
                object_type = SWMMO.SwmmOutputNode
        elif self.cboFind.currentIndex() == 2: #link
            self.cboProperty.addItems(self.model_attributes["link"])
            object_type = SWMMO.SwmmOutputLink
        elif self.cboFind.currentIndex() == 3: #lid sub
            self.cboProperty.addItems(self.model_attributes["lid"])
            object_type = None
            self.txtNum.setVisible(False)
            self.cboAbove.setVisible(False)
        elif self.cboFind.currentIndex() == 4: #inflow node
            self.cboProperty.addItems(self.model_attributes["inflow_node"])
            object_type = None
            self.txtNum.setVisible(False)
            self.cboAbove.setVisible(False)
        if self.session.output:
            if object_type:
                attribute_names = [attribute.name for attribute in object_type.attributes]
                for item in attribute_names:
                    self.cboProperty.addItem(item)

    def identify_selected_model_objects(self, otype, ids):
        self.selected_objects.clear()
        model_objects = None
        if otype.startswith("node"):
            model_objects = self.project.nodes_groups()
        elif otype.startswith("link"):
            model_objects = self.project.links_groups()
        elif otype.startswith("sub"):
            model_objects = [self.project.subcatchments]

        for id in ids:
            for obj_groups in model_objects:
                model_obj = obj_groups.find_item(id)
                lsect_name = obj_groups.SECTION_NAME[1:len(obj_groups.SECTION_NAME)-1].lower()
                if model_obj:
                    if lsect_name in self.selected_objects:
                        self.selected_objects[lsect_name].append(id)
                    else:
                        self.selected_objects[lsect_name] = []
                        self.selected_objects[lsect_name].append(id)
                    break

    def cmdSubmit_Clicked(self):
        try:
            val = float(self.txtNum.text())
        except:
            val = 0.0
        selected_attribute = self.cboProperty.currentText()
        setting_index = self.cboProperty.currentIndex()
        slist = []

        count = 0
        if self.cboFind.currentIndex() == 0:
            otype = "subcatchment"
            attribute = None
            if setting_index < 5:
                if selected_attribute.startswith("% Imperv"):
                    selected_attribute = "% Imperv"
                elif selected_attribute.startswith("% LID"):
                    selected_attribute = "LID Controls"
                meta_item = sub.Subcatchment.metadata.meta_item_of_label(selected_attribute)
                attribute = meta_item.attribute
                if attribute:  # Found an attribute of the subcatchment class to color by
                    for item in self.project.subcatchments.value:
                        value = float(getattr(item, attribute, 0))
                        if self.is_selected(item.name, value, val, slist):
                            count += 1
            elif self.session.output:  # Look for attribute to color by in the output
                attribute = SWMMO.SwmmOutputSubcatchment.get_attribute_by_name(selected_attribute)
                if attribute:
                    values = SWMMO.SwmmOutputSubcatchment.get_attribute_for_all_at_time(self.session.output, attribute, self.session.time_index)
                    index = 0 # output arrays are zero-based, but value starts at index 1
                    for subcatch in self.session.output.subcatchments.values():
                        value = values[index]
                        index += 1
                        if self.is_selected(subcatch.name, value, val, slist):
                            count += 1
        elif self.cboFind.currentIndex() == 1: # Nodes
            otype = "node"
            attribute = None
            if setting_index < 2:
                if selected_attribute.startswith("Invert"):
                    selected_attribute = "Invert El."
                meta_item = snode.Junction.metadata.meta_item_of_label(selected_attribute)
                attribute = meta_item.attribute
                if attribute:  # Found an attribute of the subcatchment class to color by
                    for n in self.project.nodes_groups():
                        for item in n.value:
                            value = float(getattr(item, attribute, 0))
                            if self.is_selected(item.name, value, val, slist):
                                count += 1
            elif self.session.output:  # Look for attribute to color by in the output
                attribute = SWMMO.SwmmOutputNode.get_attribute_by_name(selected_attribute)
                if attribute:
                    values = SWMMO.SwmmOutputNode.get_attribute_for_all_at_time(self.session.output, attribute, self.session.time_index)
                    index = 0 # output arrays are zero-based, but value starts at index 1
                    for node in self.session.output.nodes.values():
                        value = values[index]
                        index += 1
                        if self.is_selected(node.name, value, val, slist):
                            count += 1
        elif self.cboFind.currentIndex() == 3: # LID
            #ToDo figure out how to search for LID's presence
            otype = "subcatchment"
            for lid in self.project.lid_usage.value:
                if lid.subcatchment_name:
                    slist.append(lid.subcatchment_name)
            pass
        elif self.cboFind.currentIndex() == 4: # nodes with inflow
            otype = "node"
            inflows = None
            if "Direct" in selected_attribute:
                inflows = self.project.inflows
            elif "DW" in selected_attribute:
                inflows = self.project.dwf
            elif "RD" in selected_attribute:
                inflows = self.project.rdii
            if inflows is not None:
                for inflow in inflows.value:
                    slist.append(inflow.node)
        else:
            otype = 'link'
            attribute = None
            if setting_index < 3:
                meta_item = slink.Conduit.metadata.meta_item_of_label(selected_attribute)
                attribute = meta_item.attribute
                for link in self.project.conduits.value:
                    if attribute:
                        value = float(getattr(link, attribute, 0))
                    else:
                        if "Slope" in selected_attribute:
                            value = link.get_slope()
                        else:
                            continue
                    if self.is_selected(link.name, value, val, slist):
                        count += 1
            elif self.session.output:  # Look for attribute to color by in the output
                attribute = SWMMO.SwmmOutputLink.get_attribute_by_name(selected_attribute)
                if attribute:
                    values = SWMMO.SwmmOutputLink.get_attribute_for_all_at_time(self.session.output, attribute, self.session.time_index)
                    index = 0
                    for link in self.session.output.links.values():
                        value = values[index]
                        index += 1
                        if self.is_selected(link.name, value, val, slist):
                            count += 1

        self.identify_selected_model_objects(otype, slist)

        # Display number of items matching the query
        self.txtSummary.setText(str(count) + ' items found')

        self.session.map_widget.clearSelectableObjects()
        if len(self.selected_objects) == 1:
            layer = self.session.model_layers.find_layer_by_name(self.selected_objects.keys()[0])
            if layer:
                self.session.select_named_items(layer, slist)
        else:
            self.session.clear_object_listing()
            self.session.map_widget.select_model_objects_by_ids(self.selected_objects)

    def is_selected(self, obj_name, output_value, target_value, slist):
        selected = False
        if self.cboAbove.currentIndex() == 0:
            # below
            if output_value < target_value:
                selected = True
                slist.append(obj_name)
        elif self.cboAbove.currentIndex() == 1:
            # equal to
            if output_value == target_value:
                selected = True
                slist.append(obj_name)
        elif self.cboAbove.currentIndex() == 2:
            # above
            if output_value > target_value:
                selected = True
                slist.append(obj_name)
        return selected
