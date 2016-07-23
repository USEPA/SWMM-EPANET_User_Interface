import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.epanet.hydraulics.node import Tank
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from ui.EPANET.frmSourcesQuality import frmSourcesQuality


class frmTank(frmGenericPropertyEditor):
    def __init__(self, main_form):
        self.help_topic = "epanet/src/src/tankproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        edit_these = []
        if self.project.tanks and isinstance(self.project.tanks.value, list):
            edit_these.extend(self.project.tanks.value)
        if len(edit_these) == 0:
            self.new_item = Tank()
            self.new_item.name = "1"
            edit_these.append(self.new_item)
        else:
            self.new_item = False

        frmGenericPropertyEditor.__init__(self, main_form, edit_these, "EPANET Tank Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # for curve, show available curves
            curve_section = self.project.find_section("CURVES")
            curve_list = curve_section.value[0:]
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in curve_list:
                combobox.addItem(value.curve_id)
                if edit_these[column].volume_curve == value.curve_id:
                    selected_index = int(combobox.count())-1
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
            if source.id == str(self.tblGeneric.item(0, column).text()):
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
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self.project.tanks.value.append(self.new_item)
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
