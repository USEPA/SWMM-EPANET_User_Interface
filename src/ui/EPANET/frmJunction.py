import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.epanet.hydraulics.node import Junction
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from ui.EPANET.frmDemands import  frmDemands
from ui.EPANET.frmSourcesQuality import frmSourcesQuality


class frmJunction(frmGenericPropertyEditor):
    def __init__(self, main_form):
        self.help_topic = "epanet/src/src/junctionproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        edit_these = []
        if self.project.junctions and isinstance(self.project.junctions.value, list):
            edit_these.extend(self.project.junctions.value)
        if len(edit_these) == 0:
            self.new_item = Junction()
            self.new_item.name = "1"
            edit_these.append(self.new_item)
        else:
            self.new_item = False

        frmGenericPropertyEditor.__init__(self, main_form, edit_these, "EPANET Junction Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # for pattern, show available patterns
            pattern_section = self.project.find_section("PATTERNS")
            pattern_list = pattern_section.value[0:]
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in pattern_list:
                combobox.addItem(value.pattern_name)
                if edit_these[column].demand_pattern_name == value.pattern_name:
                    selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(7, column, combobox)
            # also set special text plus button cells
            self.set_demand_cell(column)
            self.set_quality_cell(column)

        self.installEventFilter(self)

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.set_demand_cell(self.refresh_column)
                self.set_quality_cell(self.refresh_column)
                self.refresh_column = -1
        return False

    def set_demand_cell(self, column):
        # text plus button for demand categories editor
        tb = TextPlusButton(self)
        section = self.project.find_section('DEMANDS')
        demands_list = section.value[0:]
        demand_count = 0
        for demand in demands_list:
            if demand.junction_name == str(self.tblGeneric.item(0, column).text()):
                demand_count += 1
        if demand_count == 0:
            # did not find any in demands table, so use whats in junction table
            section = self.project.find_section('JUNCTIONS')
            junctions_list = section.value[0:]
            for junction in junctions_list:
                if junction.name == str(self.tblGeneric.item(0, column).text()):
                    demand_count += 1
        tb.textbox.setText(str(demand_count))
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_demands(column))
        self.tblGeneric.setCellWidget(8, column, tb)

    def set_quality_cell(self, column):
        # text plus button for source quality editor
        tb = TextPlusButton(self)
        section = self.project.find_section('SOURCES')
        sources_list = section.value[0:]
        for source in sources_list:
            if source.name == str(self.tblGeneric.item(0, column).text()):
                tb.textbox.setText(str(source.baseline_strength))
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_quality(column))
        self.tblGeneric.setCellWidget(11, column, tb)

    def make_show_demands(self, column):
        def local_show():
            frm = frmDemands(self)
            frm.setWindowTitle('EPANET Demands for Junction ' + str(self.tblGeneric.item(0, column).text()))
            frm.set_from(self.project, str(self.tblGeneric.item(0, column).text()))
            frm.setWindowModality(QtCore.Qt.ApplicationModal)
            frm.show()
            self.refresh_column = column
        return local_show

    def make_show_quality(self, column):
        def local_show():
            frm = frmSourcesQuality(self)
            frm.setWindowTitle('EPANET Source Editor for Node ' + str(self.tblGeneric.item(0, column).text()))
            frm.set_from(self.project, str(self.tblGeneric.item(0, column).text()))
            frm.setWindowModality(QtCore.Qt.ApplicationModal)
            frm.show()
            self.refresh_column = column
        return local_show

    def cmdOK_Clicked(self):
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self.project.junctions.value.append(self.new_item)
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
