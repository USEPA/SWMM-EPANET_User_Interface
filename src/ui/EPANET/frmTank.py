import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QComboBox
from core.epanet.hydraulics.node import Tank
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from ui.EPANET.frmSourcesQuality import frmSourcesQuality


class frmTank(frmGenericPropertyEditor):

    SECTION_NAME = "[TANKS]"
    SECTION_TYPE = Tank

    def __init__(self, session, edit_these, new_item):
        self.help_topic = "epanet/src/src/Tank_Pro.htm"
        self.session = session
        self.project = session.project
        self.refresh_column = -1
        self.project_section = self.project.tanks
        if self.project_section and \
                isinstance(self.project_section.value, list) and \
                len(self.project_section.value) > 0 and \
                isinstance(self.project_section.value[0], self.SECTION_TYPE):

            if edit_these:  # Edit only specified item(s) in section
                if isinstance(edit_these[0], str):  # Translate list from names to objects
                    edit_names = edit_these
                    edit_objects = [item for item in self.project_section.value if item.name in edit_these]
                    edit_these = edit_objects

            else:  # Edit all items in section
                edit_these = []
                edit_these.extend(self.project_section.value)

        frmGenericPropertyEditor.__init__(self, session, session.project.tanks,
                                          edit_these, new_item, "EPANET Tank Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # for curve, show available curves
            combobox = QComboBox()
            combobox.addItem('')
            selected_index = 0
            for curve in self.project.curves.value:
                combobox.addItem(curve.name)
                if edit_these[column].volume_curve == curve.name:
                    selected_index = int(combobox.count()) - 1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(11, column, combobox)
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
            if source.name == str(self.tblGeneric.item(0, column).text()):
                tb.textbox.setText(str(source.baseline_strength))
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_quality(column))
        self.tblGeneric.setCellWidget(16, column, tb)

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
        self.session.model_layers.create_layers_from_project(self.project)
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
