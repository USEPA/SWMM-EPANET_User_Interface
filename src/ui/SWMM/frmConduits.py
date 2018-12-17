import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QComboBox, QTableWidgetItem
from core.swmm.hydraulics.link import Conduit
from core.swmm.hydraulics.link import CrossSection
from core.swmm.hydraulics.link import CrossSectionShape
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.text_plus_button import TextPlusButton
from ui.SWMM.frmCrossSection import frmCrossSection


class frmConduits(frmGenericPropertyEditor):

    SECTION_NAME = "[CONDUITS]"
    SECTION_TYPE = Conduit

    def __init__(self, main_form, edit_these, new_item):
        self.help_topic = "swmm/src/src/conduitproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        self.project_section = self.project.conduits
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

        frmGenericPropertyEditor.__init__(self, main_form, self.project_section, edit_these, new_item,
                                          "SWMM " + self.SECTION_TYPE.__name__ + " Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # for flapgate, show true/false
            combobox = QComboBox()
            combobox.addItem('True')
            combobox.addItem('False')
            combobox.setCurrentIndex(1)
            if len(edit_these) > 0:
                if edit_these[column].flap_gate == 'True' or edit_these[column].flap_gate == True:
                    combobox.setCurrentIndex(0)
            self.tblGeneric.setCellWidget(17, column, combobox)
            # also set special text plus button cells
            self.set_cross_section_cell(column)

        self.installEventFilter(self)

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.set_cross_section_cell(self.refresh_column)
                self.refresh_column = -1
        return False

    def set_cross_section_cell(self, column):
        # text plus button for cross section
        tb = TextPlusButton(self)
        xsection = None
        link_id = self.tblGeneric.item(0,column).text()
        if len(self.project.xsections.value) > 0:
            for value in self.project.xsections.value:
                if value.link == link_id:
                    tb.textbox.setText(value.shape.name)
                    self.tblGeneric.setItem(6, column, QTableWidgetItem(value.geometry1))
                    self.tblGeneric.setItem(18, column, QTableWidgetItem(value.culvert_code))
                    xsection = value
                    break
        else:
            if self._main_form and self._main_form.project_settings and \
                    self._main_form.project_settings.xsection:
                value = self._main_form.project_settings.xsection
                tb.textbox.setText(value.shape.name)
                self.tblGeneric.setItem(6, column, QTableWidgetItem(value.geometry1))
                self.tblGeneric.setItem(18, column, QTableWidgetItem(value.culvert_code))

        if not xsection:
            # create new xsection
            xsection = CrossSection()
            if self._main_form and self._main_form.project_settings and \
                    self._main_form.project_settings.xsection:
                self._main_form.project_settings.apply_default_attributes(xsection)
                tb.textbox.setText(xsection.shape.name)
                self.tblGeneric.setItem(6, column, QTableWidgetItem(xsection.geometry1))
                self.tblGeneric.setItem(18, column, QTableWidgetItem(xsection.culvert_code))
                xsection.link = link_id
                if self._main_form.project:
                    self._main_form.project.xsections.value.append(xsection)

        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.show_cross_section(column))
        self.tblGeneric.setCellWidget(5, column, tb)

    def show_cross_section(self, column):
        def local_show():
            editor = frmCrossSection(self._main_form)
            editor.set_link(self.project, str(self.tblGeneric.item(0, column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        # also need to apply xsection parameters
        for column in range(0, self.tblGeneric.columnCount()):
            for value in self.project.xsections.value:
                if value.link == str(self.tblGeneric.item(0,column).text()):
                    value.geometry1 = str(self.tblGeneric.item(6, column).text())
                    value.culvert_code = str(self.tblGeneric.item(18, column).text())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
