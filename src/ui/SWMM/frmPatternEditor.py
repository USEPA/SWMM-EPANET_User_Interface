import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QTableWidgetItem, QMessageBox
import ui.convenience
from core.swmm.patterns import PatternType
from core.swmm.patterns import Pattern
from ui.SWMM.frmPatternEditorDesigner import Ui_frmPatternEditor
from ui.help import HelpHandler


class frmPatternEditor(QMainWindow, Ui_frmPatternEditor):
    def __init__(self, main_form, edit_these=[], new_item=None, calling_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/timepatterneditordialog.htm"
        self.helper = HelpHandler(self)
        self.setupUi(self)
        self.cboType.clear()
        ui.convenience.set_combo_items(PatternType, self.cboType)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.cboType.currentIndexChanged.connect(self.cboType_currentIndexChanged)
        self._main_form = main_form
        self.calling_form = calling_form
        self.project = main_form.project
        self.section = self.project.patterns
        self.new_item = new_item
        if new_item:
            self.set_from(new_item)
        elif edit_these:
            if isinstance(edit_these, list):  # edit first pattern if given a list
                self.set_from(edit_these[0])
            else:
                self.set_from(edit_these)

        if (main_form.program_settings.value("Geometry/" + "frmPatternEditor_geometry") and
                main_form.program_settings.value("Geometry/" + "frmPatternEditor_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmPatternEditor_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmPatternEditor_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_from(self, pattern):
        if not isinstance(pattern, Pattern):
            pattern = self.section.value[pattern]
        if isinstance(pattern, Pattern):
            self.editing_item = pattern
            self.cboType_currentIndexChanged(0)
            self.txtPatternID.setText(str(pattern.name))
            self.txtDescription.setText(str(pattern.description))
            ui.convenience.set_combo(self.cboType, pattern.pattern_type)
            point_count = -2
            for point in pattern.multipliers:
                point_count += 1
                led = QLineEdit(str(point))
                self.tblMult.setItem(point_count,1,QTableWidgetItem(led.text()))

    def cmdOK_Clicked(self):
        edited_names = []
        if not self.new_item and self.editing_item.name != self.txtPatternID.text():
            # check if the new pattern name is unique
            section_field_name = self._main_form.section_types[type(self.editing_item)]
            if hasattr(self._main_form.project, section_field_name):
                section = getattr(self._main_form.project, section_field_name)
                if section.value:
                    for itm in section.value:
                        if itm.name == self.txtPatternID.text():
                            QMessageBox.information(None,"SWMM Pattern Editor",
                                                          "Pattern name " + self.txtPatternID.text() +
                                                          " is already in use.",
                                                           QMessageBox.Ok)
                            self.txtPatternID.setText(self.editing_item.name)
                            return
            edited_names.append((self.editing_item.name, self.editing_item))
            QMessageBox.information(None,"SWMM Pattern Editor",
                                          "All references to Pattern " +
                                          self.editing_item.name +
                                          " will be replaced with " + self.txtPatternID.text(),
                                          QMessageBox.Ok)
            self._main_form.mark_project_as_unsaved()

        orig_name = self.editing_item.name
        orig_description = self.editing_item.description
        orig_pattern_type = self.editing_item.pattern_type
        orig_multipliers = self.editing_item.multipliers

        self.editing_item.name = self.txtPatternID.text()
        self.editing_item.description = self.txtDescription.text()
        self.editing_item.pattern_type = PatternType[self.cboType.currentText()]
        self.editing_item.multipliers = []
        for row in range(self.tblMult.rowCount()):
            if self.tblMult.item(row,0):
                x = self.tblMult.item(row,0).text()
                if len(x) > 0:
                    self.editing_item.multipliers.append(x)

        if orig_name != self.editing_item.name or \
            orig_description != self.editing_item.description or \
            orig_pattern_type != self.editing_item.pattern_type or \
            orig_multipliers != self.editing_item.multipliers:
            self._main_form.mark_project_as_unsaved()

        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self._main_form.add_item(self.new_item)
            self._main_form.mark_project_as_unsaved()
        else:
            pass
            if len(edited_names) > 0:
                self._main_form.edited_name(edited_names)

        # regardless if pattern id is changed, refresh pattern references at all places
        self._main_form.project.refresh_pattern_object_references()
        if self.calling_form:
            self.calling_form.refresh_patterns()

        self._main_form.program_settings.setValue("Geometry/" + "frmPatternEditor_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmPatternEditor_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboType_currentIndexChanged(self, newIndex):
        pattern_type = PatternType[self.cboType.currentText()]
        if pattern_type == PatternType.DAILY:
            self.tblMult.setColumnCount(1)
            self.tblMult.setRowCount(7)
            self.tblMult.setHorizontalHeaderLabels(("Multiplier",""))
            self.tblMult.setVerticalHeaderLabels(("Sun","Mon","Tue","Wed","Thu","Fri","Sat"))
        elif pattern_type == PatternType.HOURLY or pattern_type == PatternType.WEEKEND:
            self.tblMult.setColumnCount(1)
            self.tblMult.setRowCount(24)
            self.tblMult.setHorizontalHeaderLabels(("Multiplier",""))
            self.tblMult.setVerticalHeaderLabels(("12 AM","1 AM","2 AM","3 AM","4 AM","5 AM","6 AM","7 AM","8 AM","9 AM","10 AM","11 AM","12 PM","1 PM","2 PM","3 PM","4 PM","5 PM","6 PM","7 PM","8 PM","9 PM","10 PM","11 PM"))
        elif pattern_type == PatternType.MONTHLY:
            self.tblMult.setColumnCount(1)
            self.tblMult.setRowCount(12)
            self.tblMult.setHorizontalHeaderLabels(("Multiplier",""))
            self.tblMult.setVerticalHeaderLabels(("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"))
