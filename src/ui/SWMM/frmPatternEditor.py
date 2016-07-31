import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import ui.convenience
from core.swmm.patterns import PatternType
from ui.SWMM.frmPatternEditorDesigner import Ui_frmPatternEditor


class frmPatternEditor(QtGui.QMainWindow, Ui_frmPatternEditor):
    def __init__(self, main_form=None):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/timepatterneditordialog.htm"
        self.setupUi(self)
        self.cboType.clear()
        ui.convenience.set_combo_items(PatternType, self.cboType)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.cboType.currentIndexChanged.connect(self.cboType_currentIndexChanged)
        self.set_from(main_form.project, '1')
        self.selected_pattern_id = '1'
        self._main_form = main_form

    def set_from(self, project, selected_pattern_id):
        # section = core.swmm.project.Pattern()
        section = project.patterns
        self.selected_pattern_id = selected_pattern_id
        pattern_list = section.value[0:]
        for value in pattern_list:
             if value.name == selected_pattern_id:
                 self.txtPatternID.setText(str(value.name))
                 self.txtDescription.setText(str(value.description))
                 ui.convenience.set_combo(self.cboType, value.pattern_type)
                 point_count = -2
                 for point in value.multipliers:
                     point_count += 1
                     led = QtGui.QLineEdit(str(point))
                     self.tblMult.setItem(point_count,1,QtGui.QTableWidgetItem(led.text()))

    def cmdOK_Clicked(self):
        # TODO: IF pattern id changed, ask about replacing all occurrences
        section = self._main_form.project.patterns
        pattern_list = section.value[0:]
        # assume we are editing the first one
        for value in pattern_list:
            if value.name:
                value.name = self.txtPatternID.text()
                value.description = self.txtDescription.text()
                value.pattern_type = core.swmm.patterns.PatternType[self.cboType.currentText()]
                value.multipliers = []
                for row in range(self.tblMult.rowCount()):
                    if self.tblMult.item(row,0):
                        x = self.tblMult.item(row,0).text()
                        if len(x) > 0:
                            value.multipliers.append(x)
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboType_currentIndexChanged(self, newIndex):
        pattern_type = core.swmm.patterns.PatternType[self.cboType.currentText()]
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
