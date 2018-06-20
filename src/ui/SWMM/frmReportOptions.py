import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView
import core.swmm.options.report
from ui.SWMM.frmReportOptionsDesigner import Ui_frmReportOptions


class frmReportOptions(QMainWindow, Ui_frmReportOptions):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/reportingoptionsdialog.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.cmdNodeAll.clicked.connect(self.cmdNodeAll_Clicked)
        self.cmdNodeNone.clicked.connect(self.cmdNodeNone_Clicked)
        self.cmdLinksAll.clicked.connect(self.cmdLinksAll_Clicked)
        self.cmdLinksNone.clicked.connect(self.cmdLinksNone_Clicked)
        self.cmdSubcatchmentsAll.clicked.connect(self.cmdSubcatchmentsAll_Clicked)
        self.cmdSubcatchmentsNone.clicked.connect(self.cmdSubcatchmentsNone_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

    def set_from(self, project):
        # section = core.swmm.options.report.Report()
        section = project.find_section("REPORT")
        self.cbxContinuity.setChecked(section.continuity)
        self.cbxControls.setChecked(section.controls)
        self.cbxFlow.setChecked(section.flow_stats)
        self.cbxInput.setChecked(section.input)
        # add nodes to list 1
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget.clear()
        counter = -1
        for node_group in project.nodes_groups():
            if node_group and node_group.value:
                for node in node_group.value:
                    self.listWidget.addItem(node.name)
                    counter += 1
                    if node.name in section.nodes:
                        self.listWidget.item(counter).setSelected(True)
        if section.nodes[0] == 'ALL':
            self.listWidget.selectAll()
        # add links to list 2
        self.listWidget_2.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_2.clear()
        counter = -1
        for link in project.all_links():
            self.listWidget_2.addItem(link.name)
            counter += 1
            if link.name in section.links:
                self.listWidget_2.item(counter).setSelected(True)
        if section.links[0] == 'ALL':
            self.listWidget_2.selectAll()
        # add subcatchments to list 3
        self.listWidget_3.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_3.clear()
        counter = -1
        for subcatchment in project.subcatchments.value:
            self.listWidget_3.addItem(subcatchment.name)
            counter += 1
            if subcatchment.name in section.subcatchments:
                self.listWidget_3.item(counter).setSelected(True)
        if section.subcatchments[0] == 'ALL':
            self.listWidget_3.selectAll()

    def cmdOK_Clicked(self):
        section = self._main_form.project.find_section("REPORT")
        section.continuity = self.cbxContinuity.isChecked()
        section.controls = self.cbxControls.isChecked()
        section.flow_stats = self.cbxFlow.isChecked()
        section.input = self.cbxInput.isChecked()
        # if none selected NONE, ALL, or list
        if self.listWidget.selectedItems().__len__() == self.listWidget.count():
            section.nodes = ['ALL']
        elif self.listWidget.selectedItems().__len__() == 0:
            section.nodes = ['NONE']
        else:
            section.nodes = []
            for item in self.listWidget.selectedItems():
                section.nodes.append(str(item.text()))
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cmdNodeAll_Clicked(self):
        self.listWidget.selectAll()

    def cmdNodeNone_Clicked(self):
        self.listWidget.clearSelection()

    def cmdLinksAll_Clicked(self):
        self.listWidget_2.selectAll()

    def cmdLinksNone_Clicked(self):
        self.listWidget_2.clearSelection()

    def cmdSubcatchmentsAll_Clicked(self):
        self.listWidget_3.selectAll()

    def cmdSubcatchmentsNone_Clicked(self):
        self.listWidget_3.clearSelection()
