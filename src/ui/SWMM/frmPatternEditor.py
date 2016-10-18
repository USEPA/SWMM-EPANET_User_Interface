import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import ui.convenience
from core.swmm.patterns import PatternType
from core.swmm.patterns import Pattern
from ui.SWMM.frmPatternEditorDesigner import Ui_frmPatternEditor


class frmPatternEditor(QtGui.QMainWindow, Ui_frmPatternEditor):
    def __init__(self, main_form, edit_these, new_item):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/timepatterneditordialog.htm"
        self.setupUi(self)
        self.cboType.clear()
        ui.convenience.set_combo_items(PatternType, self.cboType)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.cboType.currentIndexChanged.connect(self.cboType_currentIndexChanged)
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
            self.txtPatternID.setText(str(pattern.name))
            self.txtDescription.setText(str(pattern.description))
            ui.convenience.set_combo(self.cboType, pattern.pattern_type)
            point_count = -2
            for point in pattern.multipliers:
                point_count += 1
                led = QtGui.QLineEdit(str(point))
                self.tblMult.setItem(point_count,1,QtGui.QTableWidgetItem(led.text()))

    def cmdOK_Clicked(self):
        # TODO: IF pattern id changed, ask about replacing all occurrences
        self.editing_item.name = self.txtPatternID.text()
        self.editing_item.description = self.txtDescription.text()
        self.editing_item.pattern_type = PatternType[self.cboType.currentText()]
        self.editing_item.multipliers = []
        for row in range(self.tblMult.rowCount()):
            if self.tblMult.item(row,0):
                x = self.tblMult.item(row,0).text()
                if len(x) > 0:
                    self.editing_item.multipliers.append(x)
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self._main_form.add_item(self.new_item)
        else:
            pass
            # TODO: self._main_form.edited_?
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
