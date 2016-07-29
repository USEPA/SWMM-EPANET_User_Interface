import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
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

    def set_from(self, project, output, stats):
        self.project = project
        self.output =  SMO.SwmmOutputObject(output)
        self.stats = UStats.TStatsSelection(stats)
        #self.type_label = type_label      # Subcatchment
        #self.object_id = object_id          # 1
        #self.attribute_name = attribute_name  # Precipitation
        #self.event_name = event_name        # Daily
        #self.stat_name = stat_name          # Mean
        #self.event_threshold_value = event_threshold_value   # 0
        #self.event_volume = event_volume         # 0
        #self.separation_time = separation_time   # 6
        #self.setWindowTitle('SWMM Statistics ' + '- ' + self.type_label + ' ' + self.object_id + ' ' + self.attribute_name)
        self.setWindowTitle('SWMM Statistics ' + '- ' + self.stats.ObjectTypeText + ' ' + self.stats.ObjectID + ' ' + self.self.VariableText)
        self.textEdit.setReadOnly(True)

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

        Tser = self.output.get_time_series(self.stats.ObjectTypeText,
                                           self.stats.ObjectID,
                                           self.stats.StatsTypeText)

        lStop = "STOP"



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
        self.textEdit.setReadOnly(True)

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

        self.textEdit.setText(summary_string)

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
