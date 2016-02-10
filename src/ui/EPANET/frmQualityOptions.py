import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
import core.epanet.options.quality
from core.epanet.options.quality import QualityOptions
from core.epanet.options.quality import QualityAnalysisType
from ui.EPANET.frmQualityOptionsDesigner import Ui_frmQualityOptions


class frmQualityOptions(QtGui.QMainWindow, Ui_frmQualityOptions):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

        self.quality_dict = {
            QualityAnalysisType.NONE: self.rbnNone,
            QualityAnalysisType.AGE: self.rbnAge,
            QualityAnalysisType.CHEMICAL: self.rbnChemical,
            QualityAnalysisType.TRACE: self.rbnTrace}
        """Mapping from Quality enum type to radio button"""

        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        section = project.options.quality
        self.quality_dict.get(section.quality).setChecked(True)
        self.txtChemicalName.setText(str(section.chemical_name))
        self.txtMassUnits.setText(str(section.mass_units))
        self.txtDiffusivity.setText(str(section.diffusivity))
        self.txtTolerance.setText(str(section.tolerance))
        self.txtTraceNode.setText(str(section.trace_node))

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("OPTIONS")
        if self.rbnNone.isChecked():
            section.quality = "None"
        if self.rbnChemical.isChecked():
            section.quality = "Chemical"
        if self.rbnAge.isChecked():
            section.quality = "Age"
        if self.rbnTrace.isChecked():
            section.quality = "Trace"
        section.chemical_name = self.txtChemicalName.text()
        section.mass_units = self.txtMassUnits.text()
        section.relative_diffusivity = self.txtDiffusivity.text()
        section.tolerance = self.txtTolerance.text()
        section.trace_node = self.txtTraceNode.text()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
