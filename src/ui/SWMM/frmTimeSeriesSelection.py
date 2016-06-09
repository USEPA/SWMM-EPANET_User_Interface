import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmTimeSeriesSelectionDesigner import Ui_frmTimeSeriesSelection
from ui.help import HelpHandler
import Externals.swmm.outputapi.SMOutputWrapper as SMO


class frmTimeSeriesSelection(QtGui.QMainWindow, Ui_frmTimeSeriesSelection):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self._main_form = main_form
        self.help_topic = "swmm/src/src/controlrules.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.cboObjectType.currentIndexChanged.connect(self.cboObjectType_currentIndexChanged)
        self.rbnLeft.setChecked(True)

    def set_from(self, project, output, listener):
        self.project = project
        self.output = output
        self.listener = listener
        self.cboObjectType.clear()
        if project and self.output:
            # Add object type labels to cboObjectType if there are any of each type in output. Always add System.
            for object_type_label in SMO.SMO_objectTypeLabels:
                if object_type_label == SMO.SMO_system.TypeLabel or self.output.get_items(object_type_label):
                    self.cboObjectType.addItem(object_type_label)
            self.cboObjectType.setCurrentIndex(0)

    def cboObjectType_currentIndexChanged(self):
        has_objects = False
        attribute_names = ["None"]
        object_type = SMO.SMO_getObjectType(self.cboObjectType.currentText())
        if object_type:
            attribute_names = object_type.AttributeNames
            has_objects = (object_type != SMO.SMO_system)

        self.cboVariable.clear()
        for item in attribute_names:
            self.cboVariable.addItem(item)

        self.lblSpecify.setEnabled(has_objects)
        self.txtObject.setVisible(has_objects)
        if has_objects:
            self.lblSpecify.setText(self.cboObjectType.currentText() + " Name")
        else:
            self.lblSpecify.setText(self.cboObjectType.currentText() + " does not need a name")

    def cmdOK_Clicked(self):
        if self.rbnRight.isChecked():
            axis = "Right"
        else:
            axis = "Left"
        if self.txtObject.isVisible():
            object_id = self.txtObject.text()
        else:
            object_id = "-1"  # TODO: be able to skip this field for System since user seeing -1 is a bit ugly
        self.listener(self.cboObjectType.currentText(),
                      object_id,
                      self.cboVariable.currentText(),
                      axis,
                      self.txtLegend.text())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
