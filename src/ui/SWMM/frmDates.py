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
        section = project.find_section("OPTIONS")
        self.dedStart.setDate(section.start_date)
        self.tmeStart.setTime(section.start_time)
        self.dedStartReport.setDate(section.report_start_date)
        self.tmeReport.setTime(section.report_start_time)
        self.dedEnd.setDate(section.end_date)
        self.tmeEnd.setTime(section.end_time)
        self.dedSweepEnd.setdate(section.sweep_end)
        self.dedSweepStart.setDate(section.sweep_start)
        self.txtAntecedent.setText(section.dry_days)

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("OPTIONS")
        section.start_date = self.dedStart.text()
        section.start_time = self.tmeStart.text()
        section.report_start_date = self.dedStartReport.text()
        section.report_start_time = self.tmeReport.text()
        section.end_date = self.dedEnd.text()
        section.end_time = self.tmeEnd.text()
        section.sweep_end = self.dedSweepEnd.text()
        section.sweep_start = self.dedSweepStart.text()
        section.dry_days = self.txtAntecedent.text()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()