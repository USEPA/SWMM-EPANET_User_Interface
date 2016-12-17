import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
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
        QtCore.QObject.connect(self.rbnChemical, QtCore.SIGNAL("clicked()"), self.analysis_option_changed)
        QtCore.QObject.connect(self.txtChemicalName, QtCore.SIGNAL("textChanged(QString)"), self.chemical_name_changed)

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
            msgbox = QtGui.QMessageBox()
            msgbox.setIcon(QtGui.QMessageBox.Information)
            msgbox.setText(warning_msg)
            msgbox.setWindowTitle("Quality Analysis Options")
            msgbox.setStandardButtons(QtGui.QMessageBox.Ok)
            ret = msgbox.exec_()
            return
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

    def chemical_name_changed(self, aName):
        #print "name change: " + aName
        pass

    def analysis_option_changed(self):
        pass

    def cmdCancel_Clicked(self):
        self.close()
