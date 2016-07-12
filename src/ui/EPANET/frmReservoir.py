import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.epanet.hydraulics.node import Reservoir
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from ui.EPANET.frmSourcesQuality import frmSourcesQuality


class frmReservior(frmGenericPropertyEditor):
    def __init__(self, main_form):
        self.help_topic = "epanet/src/src/reservoirproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        edit_these = []
        if self.project.reservoirs and isinstance(self.project.reservoirs.value, list):
            edit_these.extend(self.project.reservoirs.value)
        if len(edit_these) == 0:
            self.new_item = Reservoir()
            self.new_item.name = "1"
            edit_these.append(self.new_item)

        frmGenericPropertyEditor.__init__(self, main_form, edit_these, "EPANET Reservoir Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # for pattern, show available patterns
            pattern_section = self.project.find_section("PATTERNS")
            pattern_list = pattern_section.value[0:]
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in pattern_list:
                combobox.addItem(value.pattern_id)
                if edit_these[column].head_pattern_id == value.pattern_id:
                    selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(6, column, combobox)
            # also set special text plus button cells
            self.set_quality_cell(column)

        self.installEventFilter(self)

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.set_quality_cell(self.refresh_column)
                self.refresh_column = -1
        return False

    def set_quality_cell(self, column):
        # text plus button for source quality editor
        tb = TextPlusButton(self)
        section = self.project.find_section('SOURCES')
        sources_list = section.value[0:]
        for source in sources_list:
            if source.id == str(self.tblGeneric.item(0, column).text()):
                tb.textbox.setText(str(source.baseline_strength))
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_quality(column))
        self.tblGeneric.setCellWidget(8, column, tb)

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
            self.project.reservoirs.value.append(self.new_item)
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
