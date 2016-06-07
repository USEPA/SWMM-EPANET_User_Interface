import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
from ui.EPANET.frmPatternEditorDesigner import Ui_frmPatternEditor


class frmPatternEditor(QtGui.QMainWindow, Ui_frmPatternEditor):
    def __init__(self, main_form=None):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Pattern_.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(main_form.project, '1')
        self.selected_pattern_id = '1'
        self._main_form = main_form

    def set_from(self, project, selected_pattern_id):
        # section = core.epanet.project.Pattern()
        section = project.find_section("PATTERNS")
        self.selected_pattern_id = selected_pattern_id
        pattern_list = section.value[0:]
        # assume we want to edit the first one
        for value in pattern_list:
            if value.pattern_id == selected_pattern_id:
                self.txtPatternID.setText(str(value.pattern_id))
                self.txtDescription.setText(str(value.description))
                point_count = -1
                for point in value.multipliers:
                    point_count += 1
                    led = QtGui.QLineEdit(str(point))
                    self.tblMult.setItem(0,point_count,QtGui.QTableWidgetItem(led.text()))

    def cmdOK_Clicked(self):
        # TODO: IF pattern id changed, ask about replacing all occurrences
        section = self._main_form.project.find_section("PATTERNS")
        pattern_list = section.value[0:]
        # assume we are editing the first one
        for value in pattern_list:
            if value.pattern_id == self.selected_pattern_id:
                value.pattern_id = self.txtPatternID.text()
                value.description = self.txtDescription.text()
                value.multipliers = []
                for column in range(self.tblMult.columnCount()):
                    if self.tblMult.item(0,column):
                        x = self.tblMult.item(0,column).text()
                        if len(x) > 0:
                            value.multipliers.append(x)
        self._main_form.list_objects()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
