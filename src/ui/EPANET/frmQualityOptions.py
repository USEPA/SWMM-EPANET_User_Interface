import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
import core.epanet.options.quality
from core.epanet.options.quality import QualityOptions
from core.epanet.options.quality import QualityAnalysisType
from ui.EPANET.frmQualityOptionsDesigner import Ui_frmQualityOptions


class frmQualityOptions(QtGui.QMainWindow, Ui_frmQualityOptions):

    def __init__(self, main_form=None):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Anal0041.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

        self.quality_dict = {
            QualityAnalysisType.NONE: self.rbnNone,
            QualityAnalysisType.AGE: self.rbnAge,
            QualityAnalysisType.CHEMICAL: self.rbnChemical,
            QualityAnalysisType.TRACE: self.rbnTrace}
        """Mapping from Quality enum type to radio button"""

        self.set_from(main_form.project)
        self._main_form = main_form

    def set_from(self, project):
        quality_options = project.options.quality
        self.quality_dict.get(quality_options.quality).setChecked(True)
        self.txtChemicalName.setText(str(quality_options.chemical_name))
        self.txtMassUnits.setText(str(quality_options.mass_units))
        self.txtDiffusivity.setText(str(quality_options.diffusivity))
        self.txtTolerance.setText(str(quality_options.tolerance))
        self.txtTraceNode.setText(str(quality_options.trace_node))

    def cmdOK_Clicked(self):
        quality_options = self._main_form.project.options.quality
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
