from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow
from ui.help import HelpHandler
from frmFindDesigner import Ui_frmFind


class frmFind(QMainWindow, Ui_frmFind):

    def __init__(self, session, project):
        QMainWindow.__init__(self, session)
        self.helper = HelpHandler(self)
        self.help_topic = "epanet/src/src/Finding_.htm"
        self.setupUi(self)
        self.session = session
        self.project = project
        self.rbnNode.setChecked(True)
        self.gbxAdjacent.setTitle("Adjacent Links")
        self.rbnNode.clicked.connect(self.rbn_Clicked)
        self.rbnLink.clicked.connect(self.rbn_Clicked)
        self.rbnSources.clicked.connect(self.rbn_Clicked)
        self.cmdFind.clicked.connect(self.cmdFind_Clicked)
        # self.lstAdjacent.clicked.connect(self.lstAdjacent_Clicked)
        self.lstAdjacent.currentItemChanged.connect(self.lstAdjacent_Clicked)
        self.lstAdjacent.itemSelectionChanged.connect(self.lstAdjacent_Clicked)

    def rbn_Clicked(self):
        if self.rbnNode.isChecked():
            self.txtID.setText("")
            self.lstAdjacent.clear()
            self.txtID.setEnabled(True)
            self.gbxAdjacent.setTitle("Adjacent Links")
        elif self.rbnLink.isChecked():
            self.txtID.setText("")
            self.lstAdjacent.clear()
            self.txtID.setEnabled(True)
            self.gbxAdjacent.setTitle("Adjacent Nodes")
        elif self.rbnSources.isChecked():
            self.txtID.setText("")
            self.lstAdjacent.clear()
            self.txtID.setEnabled(False)
            self.gbxAdjacent.setTitle("Source Nodes")

    def cmdFind_Clicked(self):
        TXT_NO_SUCH_OBJECT = 'There is no such object on the map'
        TXT_NO_SOURCE_NODES = 'There are no WQ source nodes.'
        TXT_LINK_NOT_ON_MAP = 'Link exists but is not on the map.'
        TXT_NODE_NOT_ON_MAP = 'Node exists but is not on the map.'

        # Search database for specified node/link ID
        # and save object type and index if found
        s = self.txtID.text()
        self.lstAdjacent.clear()
        found = False
        otype = ''
        self.session.map_widget.clearSelectableObjects()
        if self.rbnSources.isChecked():
            for node in self.project.sources.value:
                self.lstAdjacent.addItem(node.name)
                found = True
                otype = 'Sources'
        if self.rbnNode.isChecked():
            for node in self.project.junctions.value:
                if node.name == s:
                    found = True
                    otype = 'Junctions'
            for node in self.project.reservoirs.value:
                if node.name == s:
                    found = True
                    otype = 'Reservoirs'
            for node in self.project.tanks.value:
                if node.name == s:
                    found = True
                    otype = 'Tanks'
            if found:
                for link in self.project.pipes.value:
                    if link.inlet_node == s or link.outlet_node == s:
                        self.lstAdjacent.addItem(link.name)
                for link in self.project.pumps.value:
                    if link.inlet_node == s or link.outlet_node == s:
                        self.lstAdjacent.addItem(link.name)
                for link in self.project.valves.value:
                    if link.inlet_node == s or link.outlet_node == s:
                        self.lstAdjacent.addItem(link.name)
        if self.rbnLink.isChecked():
            for link in self.project.pipes.value:
                if link.name == s:
                    found = True
                    otype = 'Pipes'
                    self.lstAdjacent.addItem(link.inlet_node)
                    self.lstAdjacent.addItem(link.outlet_node)
            for link in self.project.pumps.value:
                if link.name == s:
                    found = True
                    otype = 'Pumps'
                    self.lstAdjacent.addItem(link.inlet_node)
                    self.lstAdjacent.addItem(link.outlet_node)
            for link in self.project.valves.value:
                if link.name == s:
                    found = True
                    otype = 'Valves'
                    self.lstAdjacent.addItem(link.inlet_node)
                    self.lstAdjacent.addItem(link.outlet_node)
        if found:
            if self.rbnLink.isChecked() or self.rbnNode.isChecked():
                # highlight and zoom to this object
                # select in tree diagram
                self.HighlightAndSelect(s, otype)
        if not found:
            if self.rbnSources.isChecked():
                QMessageBox.information(self, self.session.model, TXT_NO_SOURCE_NODES, QMessageBox.Ok)
            else:
                QMessageBox.information(self, self.session.model, TXT_NO_SUCH_OBJECT, QMessageBox.Ok)

    def lstAdjacent_Clicked(self):
        # highlight and zoom to this object
        # select in tree diagram
        s = self.lstAdjacent.currentItem().text()
        # figure out what type this adjacent thing is
        otype = ''
        if self.rbnSources.isChecked():
            otype = 'Sources'
        elif self.rbnNode.isChecked():
            for link in self.project.pipes.value:
                if link.name == s:
                    otype = 'Pipes'
            for link in self.project.pumps.value:
                if link.name == s:
                    otype = 'Pumps'
            for link in self.project.valves.value:
                if link.name == s:
                    otype = 'Valves'
        elif self.rbnLink.isChecked():
            for node in self.project.junctions.value:
                if node.name == s:
                    otype = 'Junctions'
            for node in self.project.reservoirs.value:
                if node.name == s:
                    otype = 'Reservoirs'
            for node in self.project.tanks.value:
                if node.name == s:
                    otype = 'Tanks'
        self.session.map_widget.clearSelectableObjects()
        self.HighlightAndSelect(s,otype)

    def HighlightAndSelect(self, s, type):
        # highlight and zoom to this object
        # select in tree diagram
        slist = []
        slist.append(s)
        layer = self.session.set_current_map_layer(type)
        self.session.select_named_items(layer, slist)
