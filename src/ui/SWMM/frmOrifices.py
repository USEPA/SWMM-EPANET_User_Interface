import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydraulics.link import Orifice
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.text_plus_button import TextPlusButton
from ui.SWMM.frmCrossSection import frmCrossSection


class frmOrifices(frmGenericPropertyEditor):

    SECTION_NAME = "[ORIFICES]"
    SECTION_TYPE = Orifice

    def __init__(self, main_form):
        self.help_topic = "swmm/src/src/orificeproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        edit_these = []
        project_section = self.project.find_section(self.SECTION_NAME)
        if project_section and\
                isinstance(project_section.value, list) and\
                len(project_section.value) > 0 and\
                isinstance(project_section.value[0], self.SECTION_TYPE):
                    edit_these.extend(project_section.value)

        frmGenericPropertyEditor.__init__(self, main_form, edit_these, "SWMM " + self.SECTION_TYPE.__name__ + " Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # for flapgate, show true/false
            combobox = QtGui.QComboBox()
            combobox.addItem('True')
            combobox.addItem('False')
            if edit_these[column].flap_gate == 'True':
                combobox.setCurrentIndex(0)
            else:
                combobox.setCurrentIndex(1)
            self.tblGeneric.setCellWidget(11, column, combobox)
            # set cross section cell
            combobox = QtGui.QComboBox()
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
                    self.tblGeneric.setItem(7, column, QtGui.QTableWidgetItem(value.geometry1))
                    self.tblGeneric.setItem(8, column, QtGui.QTableWidgetItem(value.geometry2))
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
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
