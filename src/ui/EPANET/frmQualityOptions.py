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
        quality_options = project.options.quality
        self.quality_dict.get(quality_options.quality).setChecked(True)
        self.txtChemicalName.setText(str(quality_options.chemical_name))
        self.txtMassUnits.setText(str(quality_options.mass_units))
        self.txtDiffusivity.setText(str(quality_options.diffusivity))
        self.txtTolerance.setText(str(quality_options.tolerance))
        self.txtTraceNode.setText(str(quality_options.trace_node))

    def cmdOK_Clicked(self):
        quality_options = self._parent.project.options.quality
        if self.rbnNone.isChecked():
            quality_options.quality = QualityAnalysisType.NONE
        if self.rbnChemical.isChecked():
            quality_options.quality = QualityAnalysisType.CHEMICAL
        if self.rbnAge.isChecked():
            quality_options.quality = QualityAnalysisType.AGE
        if self.rbnTrace.isChecked():
            quality_options.quality = QualityAnalysisType.TRACE
        quality_options.chemical_name = self.txtChemicalName.text()
        quality_options.mass_units = self.txtMassUnits.text()
        quality_options.diffusivity = self.txtDiffusivity.text()
        quality_options.tolerance = self.txtTolerance.text()
        quality_options.trace_node = self.txtTraceNode.text()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
