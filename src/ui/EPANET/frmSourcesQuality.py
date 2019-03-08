import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
from core.epanet.hydraulics.node import SourceType
from core.epanet.hydraulics.node import Source
from ui.EPANET.frmSourcesQualityDesigner import Ui_frmSourcesQuality


class frmSourcesQuality(QMainWindow, Ui_frmSourcesQuality):

    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Source_Q.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        # self.set_from(parent.project)
        self._main_form = main_form
        self.node_name = ''

    def set_from(self, project, node_name):
        self.node_name = node_name
        # section = core.epanet.project.Source()
        section = project.sources
        sources_list = section.value[0:]
        # assume we want to edit the first one
        for source in sources_list:
            if source.name == node_name:
                self.txtQuality.setText(str(source.baseline_strength))
                self.txtPattern.setText(str(source.pattern_name))
                if source.source_type == SourceType.CONCEN:
                    self.rbnConcentration.setChecked(True)
                elif source.source_type == SourceType.FLOWPACED:
                    self.rbnFlow.setChecked(True)
                elif source.source_type == SourceType.MASS:
                    self.rbnMass.setChecked(True)
                elif source.source_type == SourceType.SETPOINT:
                    self.rbnSetPoint.setChecked(True)

    def cmdOK_Clicked(self):
        section = self._main_form.project.sources
        sources_list = section.value[0:]
        # section.set_text(str(self.txtControls.toPlainText()))
        if len(sources_list) == 0:
            new_item = Source()
            new_item.name = self.node_name
            section.value.append(new_item)
            sources_list = section.value[0:]
            self._main_form.session.mark_project_as_unsaved()
        for source in sources_list:
            if source.name == self.node_name:
                if source.baseline_strength != self.txtQuality.text() or \
                    source.pattern_name != self.txtPattern.text():
                    self._main_form.session.mark_project_as_unsaved()
                if self.rbnConcentration.isChecked and source.source_type != SourceType.CONCEN:
                    self._main_form.session.mark_project_as_unsaved()
                elif self.rbnFlow.isChecked() and source.source_type != SourceType.FLOWPACED:
                    self._main_form.session.mark_project_as_unsaved()
                elif self.rbnMass.isChecked() and source.source_type != SourceType.MASS:
                    self._main_form.session.mark_project_as_unsaved()
                elif self.rbnSetPoint.isChecked() and source.source_type != SourceType.SETPOINT:
                    self._main_form.session.mark_project_as_unsaved()

                source.baseline_strength = self.txtQuality.text()
                source.pattern_name = self.txtPattern.text()
                if self.rbnConcentration.isChecked():
                    source.source_type = SourceType.CONCEN
                elif self.rbnFlow.isChecked():
                    source.source_type = SourceType.FLOWPACED
                elif self.rbnMass.isChecked():
                    source.source_type = SourceType.MASS
                elif self.rbnSetPoint.isChecked():
                    source.source_type = SourceType.SETPOINT
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
