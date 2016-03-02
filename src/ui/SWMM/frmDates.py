import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.options.dates
from ui.SWMM.frmDatesDesigner import Ui_frmDates


class frmDates(QtGui.QMainWindow, Ui_frmDates):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

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
        section = self._parent.project.options.dates
        section.start_date = self.dedStart.date().toString(section.DATE_FORMAT)
        section.start_time = self.tmeStart.time().toString(section.TIME_FORMAT)
        section.report_start_date = self.dedStartReport.date().toString(section.DATE_FORMAT)
        section.report_start_time = self.tmeReport.time().toString(section.TIME_FORMAT)
        section.end_date = self.dedEnd.date().toString(section.DATE_FORMAT)
        section.end_time = self.tmeEnd.time().toString(section.TIME_FORMAT)
        section.sweep_end = self.dedSweepEnd.date().toString(section.DATE_SWEEP_FORMAT)
        section.sweep_start = self.dedSweepStart.date().toString(section.DATE_SWEEP_FORMAT)
        section.dry_days = int(self.txtAntecedent.text())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()