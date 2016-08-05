import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.stats as ostatistics
#from core.swmm.stats import TStatsSelection
from ui.help import HelpHandler
from ui.SWMM.frmStatisticsReportSelectionDesigner import Ui_frmStatisticsReportSelection
from ui.SWMM.frmStatisticsReport import frmStatisticsReport
from ui.help import HelpHandler
import Externals.swmm.outputapi.SMOutputWrapper as SMO
import core.swmm.Uglobals as Uglobals

class frmStatisticsReportSelection(QtGui.QMainWindow, Ui_frmStatisticsReportSelection):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/statisticsselectiondialog.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

        self._main_form = main_form
        self.cboCategory.addItems(["Subcatchment", "Node", "Link", "System"])
        self.cboCategory.currentIndexChanged.connect(self.cboCategory_currentIndexChanged)
        self.cboVariable.currentIndexChanged.connect(self.cboVariable_currentIndexChanged)
        self.cboEvent.addItems(["Event-Dependent","Daily","Monthly","Annual"])
        self.cboEvent.currentIndexChanged.connect(self.cboEvent_currentIndexChanged)
        self.txtMinEventValue.setText('0')
        self.txtMinEventVolume.setText('0')
        self.txtMinEventDelta.setText('6')
        self.stats = ostatistics.TStatsSelection()

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboCategory.setCurrentIndex(1)
        self.cboCategory.setCurrentIndex(0)
        self.cboEvent.setCurrentIndex(1)

    def cboCategory_currentIndexChanged(self, newIndex):
        object_type = SMO.swmm_output_object_types[newIndex]
        self.lstName.clear()
        if newIndex != 3:
            for item in self.output.all_items[newIndex]:
                self.lstName.addItem(item)
            self.lstName.setItemSelected(self.lstName.item(0), True)
            self.cboVariable.clear()
            for attribute in object_type.attributes:
                self.cboVariable.addItem(attribute.name)
        else:
            self.cboVariable.clear()
            self.cboVariable.addItems(['Temperature', 'Precipitation', 'Snow Depth', 'Infiltration', 'Runoff',
                                       'DW Inflow', 'GW Inflow', 'I&I Inflow', 'Direct Inflow', 'Total Inflow',
                                       'Flooding', 'Outflow', 'Storage', 'Evaporation', 'PET'])

    def cboVariable_currentIndexChanged(self, newIndex):
        self.cboStatistic.clear()
        if self.cboCategory.currentIndex() == 0:
            # subcatchment
            if newIndex < 8:
                self.cboStatistic.addItems(['Mean', 'Peak', 'Total', 'Duration', 'Inter-Event Time'])  # flow stats
            else:
                self.cboStatistic.addItems(['Mean Concen.','Peak Concen.','Mean Load','Peak Load','Total Load'])   #qual stats
        elif self.cboCategory.currentIndex() == 1:
            # node
            if newIndex < 2 or newIndex > 5:
                self.cboStatistic.addItems(['Mean', 'Peak'])   # basic stats
            else:
                self.cboStatistic.addItems(['Mean', 'Peak', 'Total', 'Duration', 'Inter-Event Time'])  # flow stats
        elif self.cboCategory.currentIndex() == 2:
            if newIndex == 0:
                self.cboStatistic.addItems(['Mean', 'Peak', 'Total', 'Duration', 'Inter-Event Time'])  # flow stats
            elif newIndex < 5:
                self.cboStatistic.addItems(['Mean', 'Peak'])   # basic stats
            else:
                self.cboStatistic.addItems(['Mean Concen.','Peak Concen.','Mean Load','Peak Load','Total Load'])   #qual stats
        elif self.cboCategory.currentIndex() == 3:
            if newIndex == 2 or newIndex == 13:
                self.cboStatistic.addItems(['Mean', 'Peak'])   # basic stats
            else:
                self.cboStatistic.addItems(['Mean', 'Peak', 'Total', 'Duration', 'Inter-Event Time'])  # flow stats
        self.lblPrecip.setText(self.cboVariable.currentText())

    def cboEvent_currentIndexChanged(self, newIndex):
        if self.cboEvent.currentIndex() == 0:
            self.lblSeparation.setEnabled(True)
            self.txtMinEventDelta.setEnabled(True)
        else:
            self.lblSeparation.setEnabled(False)
            self.txtMinEventDelta.setEnabled(False)

    def cmdOK_Clicked(self):
        self._frmStatisticsReport = frmStatisticsReport(self._main_form)
        selected_id = ''
        for id_index in self.lstName.selectedIndexes():
            selected_id = str(id_index.data())
        #self._frmStatisticsReport.set_from(self.project, self.output, self.cboCategory.currentText(),
        #                                   selected_id, self.cboVariable.currentText(),
        #                                   self.cboEvent.currentText(), self.cboStatistic.currentText(),
        #                                   self.txtMinEventValue.text(), self.txtMinEventVolume.text(),
        #                                   self.txtMinEventDelta.text())

        #ToDo: ensure type order is the same as in the type Enum
        self.stats.ObjectType = self.cboCategory.currentIndex()
        self.stats.ObjectTypeText = self.cboCategory.currentText()
        self.stats.ObjectID = id_index.data()
        self.stats.Variable = self.cboVariable.currentIndex()
        self.stats.VariableText = self.cboVariable.currentText()
        eventTxt = self.cboEvent.currentText()
        if eventTxt in "Event-Dependent":
            self.stats.TimePeriod = ostatistics.ETimePeriod.tpVariable
        elif eventTxt in "Daily":
            self.stats.TimePeriod = ostatistics.ETimePeriod.tpDaily
        elif eventTxt in "Monthly":
            self.stats.TimePeriod = ostatistics.ETimePeriod.tpMonthly
        elif eventTxt in "Annual":
            self.stats.TimePeriod = ostatistics.ETimePeriod.tpAnnual

        self.stats.TimePeriodText = eventTxt
        self.stats.VarIndex = self.cboStatistic.currentIndex()
        self.stats.StatsType = self.cboStatistic.currentIndex()
        self.stats.StatsTypeText = self.cboStatistic.currentText()
        self.stats.MinEventValue = float(self.txtMinEventValue.text())
        self.stats.MinEventVolume = float(self.txtMinEventVolume.text())
        self.stats.MinEventDelta = float(self.txtMinEventDelta.text())

        self._frmStatisticsReport.set_from(self.project, self.output, self.stats)
        # def set_from(self, project, output, type_label, object_id, attribute_name, event_name, stat_name,
        #              event_threshold_value, event_volume, separation_time):
        #     self.project = project
        #     self.output = output
        #
        #     self.type_label = type_label  # Subcatchment
        #     self.object_id = object_id  # 1
        #     self.attribute_name = attribute_name  # Precipitation
        #     self.event_name = event_name  # Daily
        #     self.stat_name = stat_name  # Mean
        #     self.event_threshold_value = event_threshold_value  # 0
        #     self.event_volume = event_volume  # 0
        #     self.separation_time = separation_time  # 6

        self._frmStatisticsReport.show()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

