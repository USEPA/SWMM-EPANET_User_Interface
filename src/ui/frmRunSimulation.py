import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
from enum import Enum
from ui.frmRunSimulationDesigner import Ui_frmRunSimulation
from ui.model_utility import process_events, transl8


class RunStatus(Enum):
    rsSuccess = 0
    rsWarning = 1
    rsError = 2
    rsWrongVersion = 3
    rsFailed = 4
    rsShutdown = 5
    # rsStopped = 6      # Was in SWMM not EPANET
    rsImportError = 7  # Was in SWMM not EPANET
    rsCancelled = 8    # Was in EPANET not SWMM
    rsNone = 9
    rsInit = 10
    rsComputing = 11
    rsCompiling = 12
    rsHydraulics = 13
    rsWQ = 14


class frmRunSimulation(QMainWindow, Ui_frmRunSimulation):

    SHORT_TERM_LIMIT = 20  # Simulations running fewer days than this will have time of day displayed while running
    context = "RunSimulation"
    TXT_STATUS_COMPUTING =    transl8(context, "Computing...")
    TXT_STATUS_WRONGVERSION = transl8(context, "Wrong version of simulator.")
    TXT_STATUS_FAILED =       transl8(context, "Run was unsuccessful due to system error.")
    TXT_STATUS_ERROR =        transl8(context, "Run was unsuccessful. See Status Report for reasons.")
    TXT_STATUS_WARNING =      transl8(context, "Warning messages were generated. See Status Report for details.")
    TXT_STATUS_SUCCESS =      transl8(context, "Run was successful.")
    TXT_STATUS_SHUTDOWN =     transl8(context, "Simulator performed an illegal operation and was shut down.")
    # TXT_STATUS_STOPPED =    transl8(context, "Run was successful but was stopped before completion.")
    TXT_STATUS_IMPORT_ERROR = transl8(context, "Import Error")
    TXT_STATUS_CANCELLED =    transl8(context, "Run cancelled by user.")
    TXT_STATUS_NONE =         transl8(context, "Unable to run simulator.")
    TXT_STATUS_INIT =         transl8(context, "Initializing")
    TXT_STATUS_COMPILING =    transl8(context, "Compiling network data...")

    TXT_REORDERING  =         transl8(context, "Re-ordering network nodes...")
    TXT_SOLVING_HYD =         transl8(context, "Solving hydraulics")
    TXT_SAVING_HYD  =         transl8(context, "Saving hydraulics")
    TXT_SOLVING_WQ  =         transl8(context, "Solving quality")

    TXT_COMPLETE =            transl8(context, " complete")
    TXT_SAVING =              transl8(context, "Saving project data...")
    TXT_READING =             transl8(context, "Reading project data..")
    TXT_CHECKING =            transl8(context, "Checking project data...")
    TXT_CONTINUITY_ERROR =    transl8(context, "Continuity Error")

    TXT_SURF_RUNOFF  =        transl8(context, "Surface Runoff:")
    TXT_FLOW_ROUTING =        transl8(context, "Flow Routing:")
    TXT_QUAL_ROUTING =        transl8(context, "Quality Routing:")

    StatusLabelDict = {
        RunStatus.rsSuccess:      TXT_STATUS_SUCCESS,
        RunStatus.rsWarning:      TXT_STATUS_WARNING,
        RunStatus.rsError:        TXT_STATUS_ERROR,
        RunStatus.rsWrongVersion: TXT_STATUS_WRONGVERSION,
        RunStatus.rsFailed:       TXT_STATUS_FAILED,
        RunStatus.rsShutdown:     TXT_STATUS_SHUTDOWN,
        # RunStatus.rsStopped:      TXT_STATUS_STOPPED,
        RunStatus.rsImportError:  TXT_STATUS_IMPORT_ERROR,
        RunStatus.rsCancelled:    TXT_STATUS_CANCELLED,
        RunStatus.rsNone:         TXT_STATUS_NONE,
        RunStatus.rsInit:         TXT_STATUS_INIT,
        RunStatus.rsComputing:    TXT_STATUS_COMPUTING,
        RunStatus.rsCompiling:    TXT_STATUS_COMPILING,
        RunStatus.rsHydraulics:   TXT_SOLVING_HYD,
        RunStatus.rsWQ:           TXT_SOLVING_WQ
    }

    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        self.progressBar.setValue(0)
        # It looks redundant to have both lines below, but the first is needed to establish the run_status attribute
        self.run_status = RunStatus.rsInit
        self.set_status(RunStatus.rsInit)
        self.cmdStop.clicked.connect(self.stop_clicked)
        self.cmdMinimize.clicked.connect(self.minimize_clicked)
        self.cmdOK.clicked.connect(self.ok_clicked)
        self._main_form = main_form
        self._last_displayed_days = -1

    def ok_clicked(self):
        self.close()
        #     #  OnClick procedure for the OK button.
        #     self.hide()
        #     self.ModalResult = mrOK

    def minimize_clicked(self):
        #  OnClick procedure for the Minimize button.
        self.showMinimized()
        if self._main_form:
            try:
                self._main_form.showMinimized()
            except:
                pass

    # procedure TSimulationForm.CancelBtnClick(Sender: TObject)
    #   RunStatus := rsCancelled

    def stop_clicked(self):
        #  OnClick procedure for the Stop button.
        self.set_status(RunStatus.rsCancelled)
        self.cmdStop.setVisible(False)
        self.cmdOK.setVisible(True)
        self.cmdOK.setFocus()
        # // Restore original directory
        #   ChDir(OldDir)

    def set_status(self, status):
        self.run_status = status
        self.set_status_text(self.StatusLabelDict[self.run_status])

    def set_status_text(self, text):
        self.StatusLabel.setText(text)
        self.StatusLabel.update()
        process_events()

    def update_progress_bar(self, elapsed, total):
        if total <= 0:
            percent = 0
        else:
            percent = int(elapsed * 100 / total)
        if percent != self.progressBar.value():
            self.progressBar.setValue(percent)
            # self.progressBar.update()
            # process_events()

    def update_progress_days(self, elapsed_days, total_days):
        int_days = int(elapsed_days)
        update = False
        if int_days != self._last_displayed_days:
            self._last_displayed_days = int_days
            self.txtDays.setText(str(int_days))
            self.txtDays.update()
            update = True
        if total_days <= self.SHORT_TERM_LIMIT:
            float_hours = (elapsed_days - int_days) * 24
            int_hours = int(float_hours)
            minutes = int((float_hours - int_hours) * 60)
            self.txtHrsMin.setText("{:02}:{:02}".format(int_hours, minutes))
            self.txtHrsMin.update()
            update = True
        if update:
            process_events()
