import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QComboBox, QTableWidgetItem
from core.swmm.hydraulics.link import Weir
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from core.swmm.hydraulics.link import CrossSection
from core.swmm.hydraulics.link import CrossSectionShape


class frmWeirs(frmGenericPropertyEditor):

    SECTION_NAME = "[WEIRS]"
    SECTION_TYPE = Weir

    def __init__(self, main_form, edit_these, new_item):
        self.help_topic = "swmm/src/src/weirproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        self.project_section = self.project.weirs
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
            # for can surcharge, show true/false
            combobox = QComboBox()
            combobox.addItem('True')
            combobox.addItem('False')
            combobox.setCurrentIndex(1)
            if len(edit_these) > 0:
                if edit_these[column].can_surcharge == 'True' or edit_these[column].can_surcharge == True:
                    combobox.setCurrentIndex(0)
            self.tblGeneric.setCellWidget(14, column, combobox)
            self.set_cross_section_cells(column)

        self.installEventFilter(self)

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.set_cross_section_cells(self.refresh_column)
                self.refresh_column = -1
        return False

    def set_cross_section_cells(self, column):
        xsection = None
        link_id = self.tblGeneric.item(0,column).text()
        if len(self.project.xsections.value) > 0:
            for value in self.project.xsections.value:
                if value.link == link_id:
                    self.tblGeneric.setItem(6, column, QTableWidgetItem(value.geometry1))
                    self.tblGeneric.setItem(7, column, QTableWidgetItem(value.geometry2))
                    self.tblGeneric.setItem(8, column, QTableWidgetItem(value.geometry3))
                    xsection = value
                    break
        else:
            if self._main_form and self._main_form.project_settings and \
                    self._main_form.project_settings.xsection:
                value = self._main_form.project_settings.xsection
                self.tblGeneric.setItem(6, column, QTableWidgetItem(value.geometry1))
                self.tblGeneric.setItem(7, column, QTableWidgetItem(value.geometry2))
                self.tblGeneric.setItem(8, column, QTableWidgetItem(value.geometry3))

        if not xsection:
            # create new xsection
            xsection = CrossSection()
            if self._main_form and self._main_form.project_settings and \
                    self._main_form.project_settings.xsection:
                value = self._main_form.project_settings.apply_default_attributes(xsection)
                xsection.link = link_id
                if self._main_form.project:
                    self._main_form.project.xsections.value.append(xsection)

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        # also need to apply xsection parameters
        for column in range(0, self.tblGeneric.columnCount()):
            for value in self.project.xsections.value:
                if value.link == str(self.tblGeneric.item(0, column).text()):
                    Type =self.tblGeneric.cellWidget(5, 0).currentText()
                    if Type == 'ROADWAY' or Type == 'SIDEFLOW' or Type == 'TRANSVERSE':
                        value.shape = CrossSectionShape.RECT_OPEN
                    elif Type == 'TRAPEZOIDAL':
                        value.shape = CrossSectionShape.TRAPEZOIDAL
                    elif Type == 'V_NOTCH':
                        value.shape = CrossSectionShape.TRIANGULAR
                    value.geometry1 = str(self.tblGeneric.item(6, column).text())
                    value.geometry2 = str(self.tblGeneric.item(7, column).text())
                    value.geometry3 = str(self.tblGeneric.item(8, column).text())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
