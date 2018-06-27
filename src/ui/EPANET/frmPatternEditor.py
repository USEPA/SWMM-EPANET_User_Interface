import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QTableWidgetItem, QMessageBox
from ui.EPANET.frmPatternEditorDesigner import Ui_frmPatternEditor
from core.epanet.patterns import Pattern
from PyQt5.QtCore import *


class frmPatternEditor(QMainWindow, Ui_frmPatternEditor):
    def __init__(self, main_form, edit_these, new_item):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Pattern_.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.selected_pattern_name = ''
        self._main_form = main_form
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

    def set_from(self, pattern):
        if not isinstance(pattern, Pattern):
            pattern = self.section.value[pattern]
        if isinstance(pattern, Pattern):
            self.editing_item = pattern
            self.tblMult.setColumnCount(max(len(pattern.multipliers) + 1, self.tblMult.columnCount()))
        self.txtPatternID.setText(str(pattern.name))
        self.txtDescription.setText(str(pattern.description))
        point_count = -1
        for point in pattern.multipliers:
            point_count += 1
            led = QLineEdit(str(point))
            if point_count == self.tblMult.columnCount():
                self.tblMult.insertColumn(self.tblMult.columnCount()+1)
            self.tblMult.setItem(0,point_count,QTableWidgetItem(led.text()))

    def cmdOK_Clicked(self):
        # TODO: IF pattern id changed, ask about replacing all occurrences
        edited_names = []
        if not self.new_item and self.editing_item.name != self.txtPatternID.text():
            # check if the new pattern name is unique
            section_field_name = self._main_form.section_types[type(self.editing_item)]
            if hasattr(self._main_form.project, section_field_name):
                section = getattr(self._main_form.project, section_field_name)
                if section.value:
                    for itm in section.value:
                        if itm.name == self.txtPatternID.text():
                            QMessageBox.information(None, "EPANET Pattern Editor",
                                                          "Pattern name " + self.txtPatternID.text() +
                                                          " is already in use.",
                                                          QMessageBox.Ok)
                            self.txtPatternID.setText(self.editing_item.name)
                            return
            edited_names.append((self.editing_item.name, self.editing_item))
            QMessageBox.information(None,"EPANET Pattern Editor",
                                          "All references to Pattern " +
                                          self.editing_item.name +
                                          " will be replaced with " + self.txtPatternID.text(),
                                          QMessageBox.Ok)

        self.editing_item.name = self.txtPatternID.text()
        self.editing_item.description = self.txtDescription.text()
        self.editing_item.multipliers = []
        for column in range(self.tblMult.columnCount()):
            if self.tblMult.item(0,column):
                x = self.tblMult.item(0,column).text()
                if len(x) > 0:
                    self.editing_item.multipliers.append(x)
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self._main_form.add_item(self.new_item)
        else:
            pass
            if len(edited_names) > 0:
                self._main_form.edited_name(edited_names)

        # regardless if pattern id is changed, refresh pattern references at all places
        self._main_form.project.refresh_pattern_object_references()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if self.tblMult.currentColumn() + 1 == self.tblMult.columnCount():
                self.tblMult.insertColumn(self.tblMult.columnCount())



