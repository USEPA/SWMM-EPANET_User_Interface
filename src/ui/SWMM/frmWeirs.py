import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydraulics.link import Weir
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.text_plus_button import TextPlusButton
from ui.SWMM.frmCrossSection import frmCrossSection


class frmWeirs(frmGenericPropertyEditor):

    SECTION_NAME = "[WEIRS]"
    SECTION_TYPE = Weir

    def __init__(self, main_form, edit_these=[]):
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
                if isinstance(edit_these[0], basestring):  # Translate list from names to objects
                    edit_names = edit_these
                    edit_objects = [item for item in self.project_section.value if item.name in edit_these]
                    edit_these = edit_objects

            else:  # Edit all items in section
                edit_these = []
                edit_these.extend(self.project_section.value)

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
            # for can surcharge, show true/false
            combobox = QtGui.QComboBox()
            combobox.addItem('True')
            combobox.addItem('False')
            if edit_these[column].can_surcharge == 'True':
                combobox.setCurrentIndex(0)
            else:
                combobox.setCurrentIndex(1)
            self.tblGeneric.setCellWidget(14, column, combobox)

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
