import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.EPANET.frmPatternEditorDesigner import Ui_frmPatternEditor
from core.epanet.patterns import Pattern


class frmPatternEditor(QtGui.QMainWindow, Ui_frmPatternEditor):
    def __init__(self, main_form, edit_these, new_item):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Pattern_.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
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
        self.txtPatternID.setText(str(pattern.name))
        self.txtDescription.setText(str(pattern.description))
        point_count = -1
        for point in pattern.multipliers:
            point_count += 1
            led = QtGui.QLineEdit(str(point))
            self.tblMult.setItem(0,point_count,QtGui.QTableWidgetItem(led.text()))

    def cmdOK_Clicked(self):
        # TODO: IF pattern id changed, ask about replacing all occurrences
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
            # TODO: self._main_form.edited_?
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
