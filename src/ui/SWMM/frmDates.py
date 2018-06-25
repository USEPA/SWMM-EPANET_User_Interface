import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
import core.swmm.options.dates
from ui.SWMM.frmDatesDesigner import Ui_frmDates
from ui.model_utility import ParseData


class frmDates(QMainWindow, Ui_frmDates):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/simulationoptions_dates.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

    def set_from(self, project):
        # section = core.swmm.options.dates.Dates
        section = project.options.dates
        self.dedStart.setDate(QtCore.QDate.fromString(section.start_date, section.DATE_FORMAT))
        self.tmeStart.setTime(QtCore.QTime.fromString(section.start_time, section.TIME_FORMAT))
        self.dedStartReport.setDate(QtCore.QDate.fromString(section.report_start_date, section.DATE_FORMAT))
        self.tmeReport.setTime(QtCore.QTime.fromString(section.report_start_time, section.TIME_FORMAT))
        self.dedEnd.setDate(QtCore.QDate.fromString(section.end_date, section.DATE_FORMAT))
        self.tmeEnd.setTime(QtCore.QTime.fromString(section.end_time, section.TIME_FORMAT))
        self.dedSweepEnd.setDate(QtCore.QDate.fromString(section.sweep_end, section.DATE_SWEEP_FORMAT))
        self.dedSweepStart.setDate(QtCore.QDate.fromString(section.sweep_start, section.DATE_SWEEP_FORMAT))
        self.txtAntecedent.setText(str(section.dry_days))

    def cmdOK_Clicked(self):
        section = self._main_form.project.options.dates
        section.start_date = self.dedStart.date().toString(section.DATE_FORMAT)
        section.start_time = self.tmeStart.time().toString(section.TIME_FORMAT)
        section.report_start_date = self.dedStartReport.date().toString(section.DATE_FORMAT)
        section.report_start_time = self.tmeReport.time().toString(section.TIME_FORMAT)
        section.end_date = self.dedEnd.date().toString(section.DATE_FORMAT)
        section.end_time = self.tmeEnd.time().toString(section.TIME_FORMAT)
        section.sweep_end = self.dedSweepEnd.date().toString(section.DATE_SWEEP_FORMAT)
        section.sweep_start = self.dedSweepStart.date().toString(section.DATE_SWEEP_FORMAT)
        val, val_is_good = ParseData.floatTryParse(self.txtAntecedent.text())
        if val_is_good and val >= 0:
            section.dry_days = val
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
