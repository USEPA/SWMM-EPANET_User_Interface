import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.epanet.hydraulics.node import Reservoir
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from ui.EPANET.frmSourcesQuality import frmSourcesQuality


class frmReservior(frmGenericPropertyEditor):

    SECTION_NAME = "[RESERVOIRS]"
    SECTION_TYPE = Reservoir

    def __init__(self, session, edit_these, new_item):
        self.help_topic = "epanet/src/src/Rese0029.htm"
        self.session = session
        self.project = session.project
        self.refresh_column = -1
        self.project_section = self.project.reservoirs
        if self.project_section and \
                isinstance(self.project_section.value, list) and \
                len(self.project_section.value) > 0 and \
                isinstance(self.project_section.value[0], self.SECTION_TYPE):

            if edit_these:  # Edit only specified item(s) in section
                if isinstance(edit_these[0], basestring):  # Translate list from names to objects
                    edit_names = edit_these
                    edit_objects = [item for item in self.project_section.value if item.name in edit_these]
                    edit_these = edit_objects

            else:  # Edit all items in section
                edit_these = []
                edit_these.extend(self.project_section.value)

        frmGenericPropertyEditor.__init__(self, session, session.project.reservoirs,
                                          edit_these, new_item, "EPANET Reservoir Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # for pattern, show available patterns
            pattern_list = self.project.patterns.value
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in pattern_list:
                combobox.addItem(value.name)
                if edit_these[column].head_pattern_name == value.name:
                    selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(6, column, combobox)
            # set coordinates
            # coordinate_section = self.project.find_section("COORDINATES")
            # if coordinate_section.value[edit_these[column].name]:
            #     value = coordinate_section.value[edit_these[column].name].x
            #     self.tblGeneric.setItem(1, column, QtGui.QTableWidgetItem(value))
            #     value = coordinate_section.value[edit_these[column].name].y
            #     self.tblGeneric.setItem(2, column, QtGui.QTableWidgetItem(value))
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
        name = str(self.tblGeneric.item(0, column).text())
        try:
            source = self.project_section.value[name]
            tb.textbox.setText(str(source.baseline_strength))
        except:
            pass
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
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
