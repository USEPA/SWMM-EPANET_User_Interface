import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QComboBox, QTableWidgetItem
from core.swmm.hydraulics.link import Orifice
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.text_plus_button import TextPlusButton
from ui.SWMM.frmCrossSection import frmCrossSection


class frmOrifices(frmGenericPropertyEditor):

    SECTION_NAME = "[ORIFICES]"
    SECTION_TYPE = Orifice

    def __init__(self, main_form, edit_these, new_item):
        self.help_topic = "swmm/src/src/orificeproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        self.project_section = self.project.orifices
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
            self.tblGeneric.setCellWidget(11, column, combobox)
            # set cross section cell
            combobox = QComboBox()
            combobox.addItem('CIRCULAR')
            combobox.addItem('RECT_CLOSED')
            self.tblGeneric.setCellWidget(6, column, combobox)
            cross_section = self.project.find_section("XSECTIONS")
            cross_section_list = cross_section.value[0:]
            for value in cross_section_list:
                if value.link == str(self.tblGeneric.item(0,column).text()):
                    if value.link.shape == 'CIRCULAR':
                        combobox.setCurrentIndex(0)
                    elif value.link.shape == 'RECT_CLOSED':
                        combobox.setCurrentIndex(1)
                    self.tblGeneric.setItem(7, column, QTableWidgetItem(value.geometry1))
                    self.tblGeneric.setItem(8, column, QTableWidgetItem(value.geometry2))
        self.installEventFilter(self)

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.refresh_column = -1
        return False

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        # also need to apply xsection parameters
        cross_section = self.project.find_section("XSECTIONS")
        cross_section_list = cross_section.value[0:]
        for column in range(0, self.tblGeneric.columnCount()):
            for value in cross_section_list:
                if value.link == str(self.tblGeneric.item(0,column).text()):
                    value.shape = str(self.tblGeneric.item(6,column).text())
                    value.geometry1 = str(self.tblGeneric.item(7, column).text())
                    value.geometry2 = str(self.tblGeneric.item(8, column).text())
        self._main_form.list_objects()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
