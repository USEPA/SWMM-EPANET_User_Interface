import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QComboBox
from core.swmm.hydraulics.link import Pump
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.text_plus_button import TextPlusButton
from core.swmm.curves import CurveType


class frmPumps(frmGenericPropertyEditor):

    SECTION_NAME = "[PUMPS]"
    SECTION_TYPE = Pump

    def __init__(self, main_form, edit_these, new_item):
        self.help_topic = "swmm/src/src/pumpproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        self.project_section = self.project.pumps
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
            # for curves, show available curves
            curves_section = self.project.find_section("CURVES")
            curves_list = curves_section.value[0:]
            combobox = QComboBox()
            combobox.addItem('*')
            selected_index = 0
            for curve in curves_list:
                if curve.curve_type in [CurveType.PUMP1, CurveType.PUMP2, CurveType.PUMP3, CurveType.PUMP4]:
                    combobox.addItem(curve.name)
                    if len(edit_these) > 0:
                        if edit_these[column].pump_curve == curve.name:
                            selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(5, column, combobox)
            # for initial status, show on/off
            combobox = QComboBox()
            combobox.addItem('OFF')
            combobox.addItem('ON')
            combobox.setCurrentIndex(0)
            if len(edit_these) > 0:
                if edit_these[column].initial_status == 'ON':
                    combobox.setCurrentIndex(1)
            self.tblGeneric.setCellWidget(6, column, combobox)

        self.installEventFilter(self)

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.refresh_column = -1
        return False

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
