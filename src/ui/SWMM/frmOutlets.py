import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydraulics.link import Outlet
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from core.swmm.curves import CurveType


class frmOutlets(frmGenericPropertyEditor):

    SECTION_NAME = "[OUTLETS]"
    SECTION_TYPE = Outlet

    def __init__(self, main_form):
        self.help_topic = "swmm/src/src/outletproperties.htm"
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
            self.tblGeneric.setCellWidget(6, column, combobox)
            # tabular curve name
            curves_section = self.project.find_section("CURVES")
            curves_list = curves_section.value[0:]
            combobox = QtGui.QComboBox()
            combobox.addItem('*')
            selected_index = 0
            for value in curves_list:
                if value.curve_type == CurveType.RATING:
                    combobox.addItem(value.curve_id)
                    if edit_these[column].rating_curve == value.curve_id:
                        selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(10, column, combobox)

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
