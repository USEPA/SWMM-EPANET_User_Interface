import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from ui.frmGenericPropertyEditorDesigner import Ui_frmGenericPropertyEditor
from ui.SWMM.frmGroundwaterFlowDesigner import Ui_frmGroundwaterFlow
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from ui.help import HelpHandler
from ui.SWMM.frmGroundwaterEquation import frmGroundwaterEquation
from ui.SWMM.frmGroundwaterEquationDeep import frmGroundwaterEquationDeep


class frmGroundwaterFlow(QtGui.QMainWindow, Ui_frmGroundwaterFlow):
    def __init__(self, main_form, edit_these, title):
        QtGui.QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/groundwaterfloweditordialog.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        self.setupUi(self)
        self.setWindowTitle(title)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.backend = PropertyEditorBackend(self.tblGeneric, self.lblNotes, main_form, edit_these)

        for column in range(0, self.tblGeneric.columnCount()):
            # for aquifers, show available aquifers
            aquifer_section = main_form.project.find_section("AQUIFERS")
            aquifer_list = aquifer_section.value[0:]
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in aquifer_list:
                combobox.addItem(value.name)
                if edit_these[column].aquifer == value.name:
                    selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(1, column, combobox)
            # also set special text plus button cells
            self.set_lateral_equation(column)
            self.set_deep_equation(column)

        self.installEventFilter(self)

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.set_lateral_equation(self.refresh_column)
                self.set_deep_equation(self.refresh_column)
                self.refresh_column = -1
        return False

    def set_lateral_equation(self, column):
        # text plus button for custom lateral equation
        tb = TextPlusButton(self)
        tb.textbox.setText('NO')
        groundwater_section = self.project.groundwater
        groundwater_list = groundwater_section.value[0:]
        for value in groundwater_list:
            if value.subcatchment == str(self.tblGeneric.item(0,column).text()) and len(value.custom_lateral_flow_equation) > 0:
                tb.textbox.setText('YES')
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_lateral(column))
        self.tblGeneric.setCellWidget(14, column, tb)

    def set_deep_equation(self, column):
        # text plus button for custom deep equation
        tb = TextPlusButton(self)
        tb.textbox.setText('NO')
        groundwater_section = self.project.groundwater
        groundwater_list = groundwater_section.value[0:]
        for value in groundwater_list:
            if value.subcatchment == str(self.tblGeneric.item(0,column).text()) and len(value.custom_deep_flow_equation) > 0:
                tb.textbox.setText('YES')
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_deep(column))
        self.tblGeneric.setCellWidget(15, column, tb)

    def make_show_lateral(self, column):
        def local_show():
            editor = frmGroundwaterEquation(self._main_form, str(self.tblGeneric.item(0, column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def make_show_deep(self, column):
        def local_show():
            editor = frmGroundwaterEquationDeep(self._main_form, str(self.tblGeneric.item(0, column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

