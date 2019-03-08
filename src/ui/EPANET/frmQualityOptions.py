import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import core.epanet.options.quality
from core.epanet.options.quality import QualityOptions
from core.epanet.options.quality import QualityAnalysisType
from ui.EPANET.frmQualityOptionsDesigner import Ui_frmQualityOptions


class frmQualityOptions(QMainWindow, Ui_frmQualityOptions):

    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Anal0041.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.rbnChemical.clicked.connect(self.analysis_option_changed)
        # seChanged.connect(self.chemical_name_changed)
        self.txtChemicalName.textChanged.connect(self.chemical_name_changed)

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

    def check_options(self):
        if self.rbnTrace.isChecked():
            if not self.txtTraceNode.text().strip():
                return "Must specify a node id for trace analysis."
        if self.rbnChemical.isChecked():
            if not self.txtChemicalName.text().strip():
                return "Must specify a chemical name for chemical analysis."

    def cmdOK_Clicked(self):
        warning_msg = self.check_options()
        if warning_msg:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText(warning_msg)
            msgbox.setWindowTitle("Quality Analysis Options")
            msgbox.setStandardButtons(QMessageBox.Ok)
            ret = msgbox.exec_()
            return
        quality_options = self._main_form.project.options.quality
        saved_quality = quality_options.quality
        if self.rbnNone.isChecked():
            quality_options.quality = QualityAnalysisType.NONE
        if self.rbnChemical.isChecked():
            quality_options.quality = QualityAnalysisType.CHEMICAL
        if self.rbnAge.isChecked():
            quality_options.quality = QualityAnalysisType.AGE
        if self.rbnTrace.isChecked():
            quality_options.quality = QualityAnalysisType.TRACE
        if saved_quality != quality_options.quality or \
            quality_options.chemical_name != self.txtChemicalName.text() or \
            quality_options.mass_units != self.txtMassUnits.text() or \
            str(quality_options.diffusivity) != self.txtDiffusivity.text() or \
            str(quality_options.tolerance) != self.txtTolerance.text() or \
            quality_options.trace_node != self.txtTraceNode.text():
            self._main_form.mark_project_as_unsaved()

        quality_options.chemical_name = self.txtChemicalName.text()
        quality_options.mass_units = self.txtMassUnits.text()
        quality_options.diffusivity = self.txtDiffusivity.text()
        quality_options.tolerance = self.txtTolerance.text()
        quality_options.trace_node = self.txtTraceNode.text()
        self.close()

    def chemical_name_changed(self, aName):
        #print "name change: " + aName
        pass

    def analysis_option_changed(self):
        pass

    def cmdCancel_Clicked(self):
        self.close()
