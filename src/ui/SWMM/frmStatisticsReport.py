import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.help import HelpHandler
from ui.SWMM.frmStatisticsReportDesigner import Ui_frmStatisticsReport
from ui.help import HelpHandler
import numpy as np
from pandas import Series, DataFrame
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import datetime
import core.swmm.stats as UStats
import Externals.swmm.outputapi.SMOutputWrapper as SMO
import core.swmm.swmm_project as SMP

StatsText = \
    ('  S U M M A R Y   S T A T I S T I C S',
     '  ===================================',
     '  Object  .............. %s %s',
     '  Variable ............. %s %s',
     '  Event Period ......... %s',
     '  Event Statistic ...... %s %s',
     '  Event Threshold ...... %s > %.4f %s',
     '  Event Threshold ...... Event Volume > %.4f %s',
     '  Event Threshold ...... Separation Time >= %.1f  (hr)',
     '  Period of Record ..... %s to %s',
     ' ',
     '  Number of Events ..... %d',
     '  Event Frequency*...... %.3f',
     '  Minimum Value ........ %.3f',
     '  Maximum Value ........ %.3f',
     '  Mean Value ........... %.3f',
     '  Std. Deviation ....... %.3f',
     '  Skewness Coeff. ...... %.3f');

class frmStatisticsReport(QtGui.QMainWindow, Ui_frmStatisticsReport):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/viewingastatisticsreport.htm"
        self.helper = HelpHandler(self)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(parent.project)
        self._main_form = main_form
        self.stats = None
        self.statsResult = None #UStats.TStatsResults()

    def set_from(self, project, output, stats):
        self.project = project
        self.output = output #SMO.SwmmOutputObject(output)
        self.stats = stats #UStats.TStatsSelection(stats)
        #self.type_label = type_label      # Subcatchment
        #self.object_id = object_id          # 1
        #self.attribute_name = attribute_name  # Precipitation
        #self.event_name = event_name        # Daily
        #self.stat_name = stat_name          # Mean
        #self.event_threshold_value = event_threshold_value   # 0
        #self.event_volume = event_volume         # 0
        #self.separation_time = separation_time   # 6
        #self.setWindowTitle('SWMM Statistics ' + '- ' + self.type_label + ' ' + self.object_id + ' ' + self.attribute_name)
        self.setWindowTitle('SWMM Statistics ' + '- ' + self.stats.ObjectTypeText + ' ' + self.stats.ObjectID + ' ' + self.stats.VariableText)
        self.txtStatsMemo.setReadOnly(True)

        # y_values, units = output.get_series_by_name(type_label, object_id, attribute, start_index, num_steps)
        units = '(in/hr)'
        volume_units = '(in)'
        start_date = '01/01/1998'
        end_date = '01/02/1998'

        # Ustats.GetStats(Stats, EventList, Results)
        self.EventList = []
        results_n = '2'
        results_frequency = '0.194'
        results_minimum = '0.300'
        results_maximum = '0.410'
        results_mean = '0.355'
        results_std_deviation = '0.078'
        results_skewness_coeff = '0.000'

        if self.stats.TimePeriodText == "Event-Dependent":
            frequency_note = '  *Fraction of all reporting periods belonging to an event.'
            self.event_units = units
            #self.stats.TimePeriodText == 'Variable'
        elif self.stats.TimePeriodText == "Daily":
            frequency_note = '  *Fraction of all days containing an event.'
            self.event_units = '(days)'
        elif self.stats.TimePeriodText == "Monthly":
            frequency_note = '  *Fraction of all months containing an event.'
            self.event_units = '(months)'
        else:
            frequency_note = '  *Fraction of all years containing an event.'
            self.event_units = '(years)'

        #Tser = self.output.get_time_series(self.stats.ObjectTypeText, \
        #                                   self.stats.ObjectID, \
        #                                   self.stats.VariableText)
        #lStop = "STOP"

        lUtil = UStats.StatisticUtility(self.output)
        self.statsResult = UStats.TStatsResults()
        lUtil.GetStats(self.stats, self.EventList, self.statsResult)
        self.RefreshResults()

    def RefreshResults(self):
        if self.statsResult is None:
            exit()

        self.RefreshStatsPage()
        self.RefreshTablePage()
        #self.RefreshHistoPage()
        #self.RefreshFreqPage()

        pass

    def RefreshStatsPage(self):
        # List the object & type of statistical analysis performed
        #self.stats = UStats.TStatsSelection() #debug only
        #self.output = SMO.SwmmOutputObject() #debug only
        line0 = StatsText[0]
        line1 = StatsText[1]
        line2 = StatsText[2] % (self.stats.ObjectTypeText, self.stats.ObjectID)
        #self.output.pollutants.values()[0].name
        #self.output.pollutants.values()[0].units
        lunit = self.output.get_item_unit(self.stats.ObjectTypeText, \
                                          self.stats.ObjectID, \
                                          self.stats.VariableText)
        line3 = StatsText[3] % (self.stats.VariableText, "(" + lunit + ")")
        line4 = StatsText[4] % (self.stats.TimePeriodText)
        line5 = StatsText[5] % (self.stats.StatsTypeText, lunit) #self.stats.StatsUnitsLabel)
        line6 = ""
        if self.stats.MinEventValue >= 0:
            line6= StatsText[6] % (self.stats.VariableText, self.stats.MinEventValue, lunit) #self.stats.VarUnits)
        line7= ""
        if self.stats.MinEventVolume >= 0:
            if self.stats.IsRainParam:
                line7 = StatsText[7] % (self.stats.MinEventVolume, UStats.TStatsUnits.RainVolumeText[self.stats.Variable])
            else:
                line7 = StatsText[7] % (self.stats.MinEventVolume, UStats.TStatsUnits.FlowVolumeText[self.stats.Variable])
        line8 = ""
        if (self.stats.TimePeriod == UStats.ETimePeriod.tpVariable) and (self.stats.MinEventDelta > 0):
            line8 = StatsText[8] % (self.stats.MinEventDelta)
        line9 = StatsText[9] % (str(self.output.StartDate), str(self.output.EndDate))
        # List the number & frequency of events
        line10 = StatsText[10]
        line11 = StatsText[11] % (len(self.EventList))
        line12 = StatsText[12] % (self.statsResult.EventFreq)
        # Display summary statistics
        if len(self.EventList) > 0:
            line13 = StatsText[13] % (self.statsResult.Xmin)
            line14 = StatsText[14] % (self.statsResult.Xmax)
            line15 = StatsText[15] % (self.statsResult.Mean)
            line16 = StatsText[16] % (self.statsResult.StdDev)
            line17 = StatsText[17] % (self.statsResult.Skew)

        line18 = "" #StatsMemo.Lines.Add('')
        #StatsMemo.Lines.Add(FrequencyNoteText[Ord(Stats.TimePeriod)])
        line19 = UStats.TStatsUnits.FrequencyNoteText[self.stats.TimePeriod.value]
        self.txtStatsMemo.append(line0)
        self.txtStatsMemo.append(line1)
        self.txtStatsMemo.append(line2)
        self.txtStatsMemo.append(line3)
        self.txtStatsMemo.append(line4)
        self.txtStatsMemo.append(line5)
        self.txtStatsMemo.append(line6)
        self.txtStatsMemo.append(line7)
        self.txtStatsMemo.append(line8)
        self.txtStatsMemo.append(line9)
        self.txtStatsMemo.append(line10)
        self.txtStatsMemo.append(line11)
        self.txtStatsMemo.append(line12)
        self.txtStatsMemo.append(line13)
        self.txtStatsMemo.append(line14)
        self.txtStatsMemo.append(line15)
        self.txtStatsMemo.append(line16)
        self.txtStatsMemo.append(line17)
        self.txtStatsMemo.append(line18)
        self.txtStatsMemo.append(line19)
        pass

    def RefreshTablePage(self):
        # Events Tab (grid)
        ColHeadingText1 = (' ',    ' ',          ' ',        ' ', 'Exceedance', 'Return')
        ColHeadingText2 = (' ',    ' ',          'Duration', ' ', 'Frequency',  'Period')
        ColHeadingText3 = ('Rank', 'Start Date', '(hours)',  ' ', '(percent)',  '(years)')
        lunit = self.output.get_item_unit(self.stats.ObjectTypeText, \
                                          self.stats.ObjectID, \
                                          self.stats.VariableText)
        TimePeriodLabel = UStats.TStatsUnits.TimePeriodText[self.stats.TimePeriod.value]
        #StatsTypeLabel = self.stats.StatsTypeText
        #StatsUnitsLabel = lunit
        ColHeading1 = list(ColHeadingText1)
        ColHeading2 = list(ColHeadingText2)
        ColHeading3 = list(ColHeadingText3)
        ColHeading1[2] = TimePeriodLabel
        ColHeading1[3] = TimePeriodLabel
        ColHeading2[3] = self.stats.StatsTypeText
        ColHeading3[3] = "(" + lunit + ")"
        if self.stats.PlotPosition == UStats.EPlotPosition.ppMonths:
            ColHeading3[5] = '(months)'
        else:
            ColHeading3[5] = '(years)'

        if self.stats.StatsType == UStats.EStatsType.stDelta:
            ColHeading1[3] = 'Inter-Event'
            ColHeading2[3] = 'Time'

        #Set up number of rows/cols in the table
        num_cols = 6
        self.tableWidget.setColumnCount(num_cols)
        if len(self.EventList) == 0:
            num_rows = 2
        else:
            num_rows = len(self.EventList) + 1
        self.tableWidget.setRowCount(num_rows)
        self.tableWidget.verticalHeader().setVisible(False)
        #column_headers = ""
        #self.tableWidget.setHorizontalHeaderLabels(column_headers)
        for c in xrange(0, num_cols):
            header_item = QtGui.QTableWidgetItem(ColHeading1[c] + '\n' +
                                                 ColHeading2[c] + '\n' +
                                                 ColHeading3[c])
            self.tableWidget.setHorizontalHeaderItem(c, header_item)

        #Set up data grid
        row = 0
        for e in self.EventList:
            #e = UStats.TStatsEvent() #debug only
            datestr = datetime.datetime.strftime(e.StartDate, '%m/%d/%Y')
            self.tableWidget.setItem(row, 0, QtGui.QTableWidgetItem(str(e.Rank)))
            self.tableWidget.setItem(row, 1, QtGui.QTableWidgetItem(datestr))
            self.tableWidget.setItem(row, 2, QtGui.QTableWidgetItem(str(e.Duration)))
            self.tableWidget.setItem(row, 3, QtGui.QTableWidgetItem('%.3f' % (e.Value)))
            #self.tableWidget.setItem(row, 4, QtGui.QTableWidgetItem(str(e.Frequency)))
            #self.tableWidget.setItem(row, 5, QtGui.QTableWidgetItem(str(e.ReturnPeriod)))
            row += 1

        pass

    def RefreshHistoPage(self):
        pass

    def RefreshFreqPage(self):
        pass

    def set_from_old(self, project, output, object_name, object_id, variable_name, event_name, stat_name,
                 threshold_value, event_volume, separation_time):
        self.project = project
        self.output = output

        self.object_name = object_name      # Subcatchment
        self.object_id = object_id          # 1
        self.variable_name = variable_name  # Precipitation
        self.event_name = event_name        # Daily
        self.stat_name = stat_name          # Mean
        self.threshold_value = threshold_value   # 0
        self.event_volume = event_volume         # 0
        self.separation_time = separation_time   # 6

        self.setWindowTitle('SWMM Statistics ' + '- ' + self.object_name + ' ' + self.object_id + ' ' + self.variable_name)
        self.txtStatsMemo.setReadOnly(True)

        # y_values, units = output.get_series_by_name(type_label, object_id, attribute, start_index, num_steps)
        units = '(in/hr)'
        volume_units = '(in)'
        start_date = '01/01/1998'
        end_date = '01/02/1998'

        # Ustats.GetStats(Stats, EventList, Results)

        EventList = []
        results_n = '2'
        results_frequency = '0.194'
        results_minimum = '0.300'
        results_maximum = '0.410'
        results_mean = '0.355'
        results_std_deviation = '0.078'
        results_skewness_coeff = '0.000'

        if self.event_name == "Event-Dependent":
            frequency_note = '  *Fraction of all reporting periods belonging to an event.'
            self.event_name = 'Variable'
            self.event_units = units
        elif self.event_name == "Daily":
            frequency_note = '  *Fraction of all days containing an event.'
            self.event_units = '(days)'
        elif self.event_name == "Monthly":
            frequency_note = '  *Fraction of all months containing an event.'
            self.event_units = '(months)'
        else:
            frequency_note = '  *Fraction of all years containing an event.'
            self.event_units = '(years)'

        summary_string = '  S U M M A R Y   S T A T I S T I C S' + '\n' + '  ===================================' + '\n' + \
                              '  Object  .............. ' + self.object_name + ' ' + self.object_id  + '\n' + \
                              '  Variable ............. ' + self.variable_name + '  ' + units + '\n' + \
                              '  Event Period ......... ' + self.event_name + '\n' + \
                              '  Event Statistic ...... ' + self.stat_name + '  ' + self.event_units + '\n' + \
                              '  Event Threshold ...... ' + self.variable_name + ' > ' + self.threshold_value + '  ' + units + '\n' + \
                              '  Event Threshold ...... Event Volume > ' + self.event_volume + ' ' + volume_units + '\n' + \
                              '  Event Threshold ...... Separation Time >= ' + self.separation_time + ' (hr)' + '\n' + \
                              '  Period of Record ..... ' + start_date + ' to ' + end_date + '\n' + \
                              ' ' + '\n' + \
                              '  Number of Events ..... ' + results_n + '\n' + \
                              '  Event Frequency*...... ' + results_frequency + '\n' + \
                              '  Minimum Value ........ ' + results_minimum + '\n' + \
                              '  Maximum Value ........ ' + results_maximum + '\n' + \
                              '  Mean Value ........... ' + results_mean + '\n' + \
                              '  Std. Deviation ....... ' + results_std_deviation + '\n' + \
                              '  Skewness Coeff. ...... ' + results_skewness_coeff + '\n' + \
                              ' ' + '\n' + frequency_note

        self.txtStatsMemo.setText(summary_string)

        # Events Tab (grid)

        if self.event_name == 'Variable':
            self.event_name = 'Event'

        column_headers = ['Rank',
                          'Start Date',
                          self.event_name + '\n' + 'Duration' + '\n' + '(hours)',
                          self.event_name + '\n' + self.stat_name + '\n' + self.event_units,
                          'Exceedance' + '\n' + 'Frequency' + '\n' + '(percent)',
                          'Return' + '\n' + 'Period' + '\n' + '(months)']

        if self.stat_name == 'Inter-Event Time':
            column_headers[3] = 'Inter-Event' + '\n' + 'Time' + '\n' + self.event_units

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        if len(EventList) == 0:
            num_rows = 2
        else:
            num_rows = len(EventList) + 1
        self.tableWidget.setRowCount(num_rows)

        # Histogram Tab

        histogram = MyHistogram(self.widgetHistogram, width=6, height=2, dpi=100)
        self.setParent(self._main_form)
        self.widgetHistogram = histogram

        # Frequency Tab

        frequency = MyFrequencyPlot(self.widgetFrequency, width=6, height=2, dpi=100)
        self.setParent(self._main_form)
        self.widgetFrequency = frequency

    def cmdCancel_Clicked(self):
        self.close()

class MyHistogram(FigureCanvas):

    def __init__(self, main_form=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)

        plt.hist([1, 2, 1], bins=[0, 1, 2, 3])

        FigureCanvas.__init__(self, fig)
        self.setParent(main_form)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class MyFrequencyPlot(FigureCanvas):

    def __init__(self, main_form=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)

        y = (0.0, 3.0, 0.01)
        x = (0,1,2)
        self.axes.plot(x, y)

        FigureCanvas.__init__(self, fig)
        self.setParent(main_form)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
