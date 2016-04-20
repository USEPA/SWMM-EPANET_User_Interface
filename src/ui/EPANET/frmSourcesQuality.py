import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
from core.epanet.hydraulics.node import SourceType
from ui.EPANET.frmSourcesQualityDesigner import Ui_frmSourcesQuality


class frmSourcesQuality(QtGui.QMainWindow, Ui_frmSourcesQuality):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(parent.project)
        self._parent = parent
        self.node_id = ''

    def set_from(self, project, node_id):
        self.node_id = node_id
        # section = core.epanet.project.Source()
        section = project.find_section('SOURCES')
        sources_list = section.value[0:]
        # assume we want to edit the first one
        for source in sources_list:
            if source.node_id == node_id:
                self.txtQuality.setText(str(source.baseline_strength))
                self.txtPattern.setText(str(source.pattern_id))
                if source.source_type == SourceType.CONCEN:
                    self.rbnConcentration.setChecked(True)
                elif source.source_type == SourceType.FLOWPACED:
                    self.rbnFlow.setChecked(True)
                elif source.source_type == SourceType.MASS:
                    self.rbnMass.setChecked(True)
                elif source.source_type == SourceType.SETPOINT:
                    self.rbnSetPoint.setChecked(True)

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section('SOURCES')
        sources_list = section.value[0:]
        # section.set_text(str(self.txtControls.toPlainText()))
        for source in sources_list:
            if source.node_id == self.node_id:
                source.baseline_strength = self.txtQuality.text()
                source.pattern_id = self.txtPattern.text()
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
