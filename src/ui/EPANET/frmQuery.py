from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow
from ui.help import HelpHandler
from ui.frmQueryDesigner import Ui_frmQuery
import Externals.epanet.outputapi.ENOutputWrapper as ENO
from core.epanet.hydraulics.node import Junction
from core.epanet.hydraulics.node import Reservoir
from core.epanet.hydraulics.node import Tank
from core.epanet.hydraulics.link import Pipe
from core.epanet.hydraulics.link import Pump
from core.epanet.hydraulics.link import Valve


class frmQuery(QMainWindow, Ui_frmQuery):

    def __init__(self, session, project):
        QMainWindow.__init__(self, session)
        self.helper = HelpHandler(self)
        self.help_topic = "epanet/src/src/Submitti.htm"
        self.setupUi(self)
        self.session = session
        self.project = project

        self.cboFind.currentIndexChanged.connect(self.cboFind_Changed)
        self.cmdSubmit.clicked.connect(self.cmdSubmit_Clicked)

        self.cboFind.addItem('Find Nodes with')
        self.cboFind.addItem('Find Links with')

        self.cboAbove.addItem('Below')
        self.cboAbove.addItem('Equal To')
        self.cboAbove.addItem('Above')

        self.selected_objects = {}

    def cboFind_Changed(self):
        # Changes list of map display variables to choose
        # from when user switches between Node & Link query.
        self.cboProperty.clear()
        if self.cboFind.currentIndex() == 0:
            self.cboProperty.addItems(['Elevation','Base Demand','Initial Quality'])
            if self.session.output:
                object_type = ENO.ENR_node_type
                if object_type:
                    attribute_names = [attribute.name for attribute in object_type.Attributes]
                    for item in attribute_names:
                        self.cboProperty.addItem(item)
        else:
            self.cboProperty.addItems(['Length','Diameter','Roughness','Bulk Coeff.','Wall Coeff.'])
            if self.session.output:
                object_type = ENO.ENR_link_type
                if object_type:
                    attribute_names = [attribute.name for attribute in object_type.Attributes]
                    for item in attribute_names:
                        if item == "Setting" or item == "Status":
                            pass
                        else:
                            self.cboProperty.addItem(item)

    def identify_selected_model_objects(self, otype, ids):
        self.selected_objects.clear()
        model_objects = None
        if otype.startswith("node"):
            model_objects = self.project.nodes_groups()
        elif otype.startswith("link"):
            model_objects = self.project.links_groups()
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
        val = float(self.txtNum.text())
        selected_attribute = self.cboProperty.currentText()
        setting_index = self.cboProperty.currentIndex()
        slist = []

        count = 0
        if self.cboFind.currentIndex() == 0:
            otype = "nodes"
            attribute = None
            if setting_index < 3:
                meta_item = Junction.metadata.meta_item_of_label(selected_attribute)
                attribute = meta_item.attribute
                if attribute:  # Found an attribute of the node class to color by
                    for item in self.project.all_nodes():
                        value = float(getattr(item, attribute, 0))
                        if self.cboAbove.currentIndex() == 0:
                            # below
                            if value < val:
                                count += 1
                                slist.append(item.name)
                        elif self.cboAbove.currentIndex() == 1:
                            # equal to
                            if value == val:
                                count += 1
                                slist.append(item.name)
                        elif self.cboAbove.currentIndex() == 2:
                            # above
                            if value > val:
                                count += 1
                                slist.append(item.name)
            elif self.session.output:  # Look for attribute to color by in the output
                attribute = ENO.ENR_node_type.get_attribute_by_name(selected_attribute)
                if attribute:
                    values = ENO.ENR_node_type.get_attribute_for_all_at_time(self.session.output, attribute, self.session.time_index)
                    index = 1 # output arrays are zero-based, but value starts at index 1
                    for node in self.session.output.nodes.values():
                        value = values[index]
                        index += 1
                        if self.cboAbove.currentIndex() == 0:
                            # below
                            if value < val:
                                count += 1
                                slist.append(node.name)
                        elif self.cboAbove.currentIndex() == 1:
                            # equal to
                            if value == val:
                                count += 1
                                slist.append(node.name)
                        elif self.cboAbove.currentIndex() == 2:
                            # above
                            if value > val:
                                count += 1
                                slist.append(node.name)
        else:
            otype = 'links'
            attribute = None
            if setting_index < 5:
                meta_item = Pipe.metadata.meta_item_of_label(selected_attribute)
                attribute = meta_item.attribute
                if attribute:  # Found an attribute of the pipe class to color by
                    for link in self.project.all_links():
                        value = float(getattr(link, attribute, 0))
                        if self.cboAbove.currentIndex() == 0:
                            # below
                            if value < val:
                                count += 1
                                slist.append(link.name)
                        elif self.cboAbove.currentIndex() == 1:
                            # equal to
                            if value == val:
                                count += 1
                                slist.append(link.name)
                        elif self.cboAbove.currentIndex() == 2:
                            # above
                            if value > val:
                                count += 1
                                slist.append(link.name)
            elif self.session.output:  # Look for attribute to color by in the output
                attribute = ENO.ENR_link_type.get_attribute_by_name(selected_attribute)
                if attribute:
                    values = ENO.ENR_link_type.get_attribute_for_all_at_time(self.session.output, attribute, self.session.time_index)
                    index = 1
                    for link in self.session.output.links.values():
                        value = values[index]
                        index += 1
                        if self.cboAbove.currentIndex() == 0:
                            # below
                            if value < val:
                                count += 1
                                slist.append(link.name)
                        elif self.cboAbove.currentIndex() == 1:
                            # equal to
                            if value == val:
                                count += 1
                                slist.append(link.name)
                        elif self.cboAbove.currentIndex() == 2:
                            # above
                            if value > val:
                                count += 1
                                slist.append(link.name)

        self.identify_selected_model_objects(otype, slist)

        # Display number of items matching the query
        self.txtSummary.setText(str(count) + ' items found')

        self.session.map_widget.clearSelectableObjects()
        if len(self.selected_objects) == 1:
            layer = self.session.model_layers.find_layer_by_name(self.selected_objects.keys()[0])
            if layer:
                self.session.select_named_items(layer, slist)
        else:
            self.session.clear_section_selection()
            self.session.clear_object_listing()
            self.session.map_widget.select_model_objects_by_ids(self.selected_objects)
