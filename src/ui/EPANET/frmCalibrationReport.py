import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSizePolicy
from ui.help import HelpHandler
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
# import matplotlib.pyplot as plt
import numpy as np
from ui.EPANET.frmCalibrationReportDesigner import Ui_frmCalibrationReport
import core.epanet.calibration as pcali
import sys

TXT_REPORT = 'Calibration Report - %s'
TXT_NETWORK = '  Network       %3d%12.2f%12.2f%8.3f%8.3f'
TXT_NO_DATA = ' *** No observed data during simulation period. ***'
TXT_CORRELATION = '  Correlation Between Means: %6.3f'
TXT_TITLE = ' Calibration Statistics for %s'
TXT_HEADING1 = '                Num    Observed    Computed    Mean     RMS'
TXT_HEADING2 = '  Location      Obs        Mean        Mean   Error   Error'
TXT_HEADING3 = '  ---------------------------------------------------------'
TXT_LOC_STATS = '  %-14s%3d%12.2f%12.2f%8.3f%8.3f'

class frmCalibrationReport(QMainWindow, Ui_frmCalibrationReport):
    def __init__(self, main_form, project, output, aECaliType):
        QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "epanet/src/src/Cali0078.htm"
        self.setupUi(self)
        # self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.setWindowTitle('EPANET Calibration Report - ' + aECaliType.name)
        self._main_form = main_form
        self.output = output
        self.project = project
        self.calitype = aECaliType
        self.cali = None

        self.update_error_stats()
        self.txtStatistics.setReadOnly(True)
        self.display_location_network_stats()
        self.display_correlationplot()
        self.display_barplot()
        self.tabWidget.setCurrentIndex(0)

    def update_error_stats(self):
        lcali = None
        for lcali in self.project.calibrations.value:
            if lcali.etype == self.calitype:
                break
        if lcali is None:
            return
        #get simulated data
        #from Externals.epanet.outputapi import ENOutputWrapper
        #self.output = ENOutputWrapper.OutputObject()
        import pandas as pd
        #sim_tser = pd.Series()
        self.cali = lcali
        sim_tser = None
        strobs = pcali.CalibrationDataset.colname_obs
        strsim = pcali.CalibrationDataset.colname_sim
        for ldsid in lcali.hobjects:
            ldataset = lcali.hobjects[ldsid] #get the calibration dataset
            if ldataset.is_selected and ldataset.need_to_calculate_stats:
                if lcali.is_flow:
                    sim_tser = self.output.get_time_series('Link', ldataset.id, lcali.etype.name)
                else:
                    sim_tser = self.output.get_time_series('Node', ldataset.id, lcali.etype.name)
                ldataset.read_simulated_values(sim_tser,
                                            self.output.reportStart,
                                            self.output.reportStep,
                                            self.output.simDuration,
                                            self.output.num_periods)
                ldataset.calc_stats()
        #lcali = pcali.Calibration()
        lcali.update_network_sum_stats()
        lcali.calc_Rcoeff()

    def display_location_network_stats(self):
        #self.cali = pcali.Calibration() #dev only
        self.txtStatistics.clear()
        self.txtStatistics.append(TXT_TITLE % self.cali.name)
        self.txtStatistics.append(' ')
        self.txtStatistics.append(TXT_HEADING1)
        self.txtStatistics.append(TXT_HEADING2)
        self.txtStatistics.append(TXT_HEADING3)
        if self.cali.netsum_sim_stats_ctr == 0:
            self.txtStatistics.append(' ')
            self.txtStatistics.append(TXT_NO_DATA)
        else:
            #DisplayLocationStats
            for lid in self.cali.hobjects:
                ldataset = self.cali.hobjects[lid]
                #ldataset = pcali.CalibrationDataset() #dev only
                if ldataset.is_selected and not ldataset.need_to_calculate_stats:
                    #DisplayStats
                    self.txtStatistics.append(TXT_LOC_STATS % (lid,
                                                               ldataset.sum_sim_stats_ctr,
                                                               ldataset.mean_obs,
                                                               ldataset.mean_sim,
                                                               ldataset.mean_err,
                                                               ldataset.mean_rms))

            #DisplayNetworkStats
            self.txtStatistics.append(TXT_HEADING3)
            self.txtStatistics.append(TXT_NETWORK % (self.cali.netsum_sim_stats_ctr,
                                                     self.cali.netmean_obs,
                                                     self.cali.netmean_sim,
                                                     self.cali.netmean_err,
                                                     self.cali.netmean_rms))
            self.txtStatistics.append(' ')
            self.txtStatistics.append(TXT_CORRELATION % (self.cali.calc_Rcoeff()))
            pass
        pass

    def display_correlationplot(self):
        # correlation plot tab
        #self.setParent(self._main_form)
        if self.cali is not None:
            correlation_plot = CorrelationPlot(self.tabCorrelation,
                                      width=6,
                                      height=2,
                                      dpi=100)
            correlation_plot.setData(self.cali)
            layout = QVBoxLayout(self.tabCorrelation)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(correlation_plot)
            self.tabCorrelation.setLayout(layout)
            #self.widgetPlot = correlation_plot
        pass

    def display_barplot(self):
        # Bar plot tab
        #self.setParent(self._main_form)
        if self.cali is not None:
            bar_plot = BarPlot(self.tabMean,
                                      width=6,
                                      height=2,
                                      dpi=100)
            bar_plot.setData(self.cali)
            layout = QVBoxLayout(self.tabMean)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(bar_plot)
            self.tabCorrelation.setLayout(layout)
        pass

    def cmdCancel_Clicked(self):
        self.close()

class BasePlot(FigureCanvas):
    def __init__(self, main_form=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(bottom=0.2)
        self.axes = fig.add_subplot(111)
        #self.axes.hold(False)

        FigureCanvas.__init__(self, fig)
        self.setParent(main_form)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def setTitle(self, aTitle):
        if self.axes is not None:
            self.axes.set_title(aTitle)
        pass

    def setXlabel(self, aLabel):
        if self.axes is not None:
            self.axes.set_xlabel(aLabel, fontsize=10)
        # self.ax = plt.AxesSubplot() #debug only
        pass

    def setYlabel(self, aLabel):
        if self.axes is not None:
            self.axes.set_ylabel(aLabel)
        pass

class CorrelationPlot(BasePlot):
    def __init__(self, main_form=None, width=5, height=4, dpi=100):
        BasePlot.__init__(self, main_form, width, height, dpi)
        pass

    def setData(self, aData):
        #aData = pcali.Calibration()
        omin = sys.float_info.max
        omax = sys.float_info.min * -1
        smin = sys.float_info.max
        smax = sys.float_info.min * -1
        colors = self.get_colors(aData)
        for oid in aData.hobjects:
            ldataset = aData.hobjects[oid]
            #ldataset = pcali.CalibrationDataset() #dev only
            if ldataset.is_selected and not ldataset.need_to_calculate_stats:
                if ldataset.data[pcali.CalibrationDataset.colname_obs].min() < omin:
                    omin = ldataset.data[pcali.CalibrationDataset.colname_obs].min()
                if ldataset.data[pcali.CalibrationDataset.colname_obs].max() > omax:
                    omax = ldataset.data[pcali.CalibrationDataset.colname_obs].max()

                if ldataset.data[pcali.CalibrationDataset.colname_sim].min() < smin:
                    smin = ldataset.data[pcali.CalibrationDataset.colname_sim].min()
                if ldataset.data[pcali.CalibrationDataset.colname_sim].max() > smax:
                    smax = ldataset.data[pcali.CalibrationDataset.colname_sim].max()

                self.axes.scatter(
                    ldataset.data[pcali.CalibrationDataset.colname_obs].values,
                    ldataset.data[pcali.CalibrationDataset.colname_sim].values,
                    s=10, c=colors[oid], marker="o", label=oid)
        self.axes.legend(loc='upper left')
        self.axes.plot([min(omin, smin), max(omax, smax)],
                       [min(omin, smin), max(omax, smax)],'r--')
        #self.axes.plot((0, 1), 'r--')

        self.setTitle('Correlation Plot for %s' % aData.name)
        self.setXlabel('Observed')
        self.setYlabel('Computed')
        pass

    def get_colors(self, aData):
        ids = []
        for oid in aData.hobjects:
            ldataset = aData.hobjects[oid]
            #ldataset = pcali.CalibrationDataset() #dev only
            if ldataset.is_selected and not ldataset.need_to_calculate_stats:
                ids.append(ldataset.id)

        cmap = plt.get_cmap('jet')
        colors = cmap(np.linspace(0, 1, len(ids)))
        dict_colors = {}
        for i in xrange(0, len(ids)):
            dict_colors[ids[i]] = colors[i]
        return dict_colors

class BarPlot(BasePlot):
    def __init__(self, main_form=None, width=5, height=4, dpi=100):
        BasePlot.__init__(self, main_form, width, height, dpi)
        pass

    def setData(self, aData):
        #aData = pcali.Calibration()
        N = 0
        obs_means = []
        sim_means = []
        obj_ids = []
        for oid in aData.hobjects:
            ldataset = aData.hobjects[oid]
            #ldataset = pcali.CalibrationDataset() #dev only
            if ldataset.is_selected and not ldataset.need_to_calculate_stats:
                N += 1
                obj_ids.append(ldataset.id)
                obs_means.append(ldataset.mean_obs)
                sim_means.append(ldataset.mean_sim)

        ind = 0
        wid = 0.0
        if N == 0:
            return
        else:
            ind = np.arange(N)
            wid = 0.35

        bar_sim = self.axes.bar(ind, sim_means, wid, color='r')
        bar_obs = self.axes.bar(ind + wid, obs_means, wid, color='g')

        fontP = FontProperties()
        fontP.set_size('small')
        self.axes.legend((bar_sim[0], bar_obs[0]), ('Computed', 'Observed'),
                         prop=fontP,
                         loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=2)

        self.axes.set_xticks(ind + wid)
        self.axes.set_xticklabels(obj_ids)

        self.setTitle('Comparison of Mean Values for %s' % aData.name)
        self.setXlabel('Location')
        #self.setYlabel('')

        self.autolabel(bar_sim)
        self.autolabel(bar_obs)
        pass

    def autolabel(self, rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            self.axes.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%.2f' % height,
                    ha='center', va='bottom')
