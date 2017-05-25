import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmTimeSeriesSelectionDesigner import Ui_frmTimeSeriesSelection
from ui.help import HelpHandler
import Externals.swmm.outputapi.SMOutputWrapper as SMO


class frmTimeSeriesSelection(QtGui.QMainWindow, Ui_frmTimeSeriesSelection):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self._main_form = main_form
        self.help_topic = "swmm/src/src/time_series_selection_dialog.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.cboObjectType.currentIndexChanged.connect(self.cboObjectType_currentIndexChanged)
        self.cboVariable.currentIndexChanged.connect(self.cboVariable_currentIndexChanged)
        self.txtObject.textChanged.connect(self.txtObject_textChanged)
        self.rbnLeft.setChecked(True)
        self.onObjectSelected = self._main_form.objectsSelected
        self.onObjectSelected.connect(self.set_selected_object)

    def set_from(self, project, output, listener):
        self.project = project
        self.output = output
        self.listener = listener
        self.cboObjectType.clear()
        if project and self.output:
            # Add object type labels to cboObjectType if there are any of each type in output. Always add System.
            for label in SMO.swmm_output_object_labels:
                if label == SMO.SwmmOutputSystem.type_label or self.output.get_items(label):
                    self.cboObjectType.addItem(label)
            self.cboObjectType.setCurrentIndex(0)

    def txtObject_textChanged(self):
        self.cboVariable_currentIndexChanged()

    def cboObjectType_currentIndexChanged(self):
        has_objects = False
        attribute_names = ["None"]
        object_type = SMO.swmm_output_get_object_type(self.cboObjectType.currentText())
        if object_type:
            attribute_names = [attribute.name for attribute in object_type.attributes]
            has_objects = (object_type != SMO.SwmmOutputSystem)

        self.cboVariable.clear()
        for item in attribute_names:
            self.cboVariable.addItem(item)

        self.lblSpecify.setEnabled(has_objects)
        self.txtObject.setVisible(has_objects)
        if has_objects:
            self.lblSpecify.setText(self.cboObjectType.currentText() + " Name")
        else:
            self.lblSpecify.setText(self.cboObjectType.currentText() + " does not need a name")

    def cboVariable_currentIndexChanged(self):
        """
        set default legend text for the data serie
        Returns:
        """
        otype = self.cboObjectType.currentText()
        if otype.startswith("Sub"):
            otype = "Sub"
        elif otype.startswith("Sys"):
            otype = "Sys"
        vartype = self.cboVariable.currentText()
        self.txtLegend.setText(otype + "-" + self.txtObject.text() + "-" + vartype)
        pass

    def set_selected_object(self, layer_name, object_ids):
        if layer_name and object_ids:
            otype = self.cboObjectType.currentText()
            if layer_name.lower()[:3] == otype.lower()[:3]:
                if object_ids[0].startswith("subcentroid"):
                    self.txtObject.setText(object_ids[0][len("subcentroid-"):])
                else:
                    self.txtObject.setText(object_ids[0])
            elif (layer_name.lower().startswith("junction") or \
                  layer_name.lower().startswith("outfall") or \
                  layer_name.lower().startswith("divider") or \
                  layer_name.lower().startswith("storage")) and \
                  otype.lower().startswith("node"):
                self.txtObject.setText(object_ids[0])
            elif (layer_name.lower().startswith("conduit") or \
                  layer_name.lower().startswith("pump") or \
                  layer_name.lower().startswith("orifice") or \
                  layer_name.lower().startswith("weir") or \
                  layer_name.lower().startswith("outlet")) and \
                    otype.lower().startswith("link"):
                self.txtObject.setText(object_ids[0])

    def cmdOK_Clicked(self):
        if self.txtObject.isVisible():
            object_name = self.txtObject.text()
        else:
            object_name = "-1"  # TODO: be able to skip this field for System since user seeing -1 is a bit ugly
        if self.rbnRight.isChecked():
            axis = "Right"
        else:
            axis = "Left"
        legend = self.txtLegend.text()
        if not legend:  # Default to variable name as legend text if not specified
            legend = self.cboVariable.currentText()
        self.listener(self.cboObjectType.currentText(),
                      object_name,
                      self.cboVariable.currentText(),
                      axis,
                      legend)
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
