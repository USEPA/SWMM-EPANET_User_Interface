import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from datetime import datetime
from ui.frmRunSimulation import frmRunSimulation, RunStatus


class frmRunSWMM(frmRunSimulation):

    """
    Execute the SWMM simulation engine (in SWMM5.DLL) and display progress.
    Based on Fsimul.pas from EPA SWMM 5.1 12/2/13 (5.1.000) by L. Rossman
    """

    TXT_SWMM5 = 'SWMM 5.1 - '

    def __init__(self, parent=None):
        frmRunSimulation.__init__(self, parent)

        #  Initialize display of continuity errors
        self.ErrRunoff = 0.0          # Runoff continuity error
        self.ErrFlow = 0.0       # Flow routing continuity error
        self.ErrQual = 0.0            # Quality routing continuity error
        self.lblSurface.setText('')
        self.lblFlow.setText('')
        self.lblQuality.setText('')
        self.txtSurface.setText('')
        self.txtFlow.setText('')
        self.txtQuality.setText('')
        self.fraFinished.setText('')
        self.fraFinished.setVisible(False)
        self.gbxContinuity.setVisible(False)
        self.last_displayed_days = -1  # Old elapsed number of days

        #  Initialize placement and status of images on the ResultsPage
        self.lblIconSuccessful.Visible = False
        # self.lblIconError.Visible = False
        # self.lblIconError.Left = self.lblIconSuccessful.Left
        # self.lblIconError.Top  = self.lblIconSuccessful.Top

        #  Make the ProgressPage be the active page
        #Notebook1.PageIndex = 0

    def Execute(self, temp_dir, main_form):
        """ Run a simulation.
            var
            OldDir: String
            AppTitle: String
        """
        #  Change the current directory to the application's temporary directory
        old_dir = os.curdir()
        os.chdir(temp_dir)

        #  Update the form's display
        #Update

        #  Save the title Windows' uses for the application
        app_title = main_form.getText()

        #  Run the simulation
        self.RunSimulation()

        #  Restore the application's title
        main_form.setText(app_title)

        #  Change back to the original directory
        os.chdir(old_dir)

        #  Display the run's status on the ResultsPage of the form
        self.DisplayRunStatus()
        #Notebook1.PageIndex = 1

    def RunSimulation(self):
        """
            Call into the SWMM DLL engine to perform a simulation.
            The input, report, and binary output files required by the SWMM
            engine have already been created in Fmain.pas' RunSimulation
            procedure through a call to CreateTempFiles.
            var
                Err: Integer                        #  error code (0 = no error)
                S: TStringlist                      #  stringlist used for input data
                Duration: double                    #  simulation duration in days
                ElapsedTime: double                 #  elapsed simulation time in days
                OldTime, NewTime: TDateTime         #  system times for progress meter
                InpFile, RptFile, OutFile: AnsiString  #  Ansi string versions of file names
        """

        # #  Save the current project input data to a temporary file
        self.set_status_text(self.TXT_SAVING)
        # S = TStringlist.Create  # Input will be placed in a stringlist
        # try:
        #     Uexport.ExportProject(S)  # Write input data to the stringlist
        #     Uexport.ExportTempDir(S)  # Add temp. directory name to input
        #     S.SaveToFile(TempInputFile)  # Save input to file
        # finally:
        #     S.Free
        #
        # # Have the SWMM solver read the input data file
        self.set_status_text(self.TXT_READING)
        # self.ProgressLabel.Refresh
        # InpFile = AnsiString(TempInputFile)
        # RptFile = AnsiString(TempReportFile)
        # OutFile = AnsiString(TempOutputFile)
        # Err = swmm_open(PAnsiChar(InpFile), PAnsiChar(RptFile), PAnsiChar(OutFile))
        #
        # #  If there are no input errors, then initialize the simulation
        # if Err == 0:
        #     self.ProgressLabel.Caption = self.TXT_CHECKING
        #     self.ProgressLabel.Refresh
        #     Err = swmm_start(1)
        #
        # # If there are no initialization errors, then...
        # if Err == 0:
        #     #  Get the simulation duration in days
        self.last_displayed_days = -1
        self.total_days = self.compute_total_days()
        #
        #  Gray-out the Hrs:Min display for long-term simulations
        if self.total_days >= self.SHORT_TERM_LIMIT:
            self.txtHrsMin.setVisible(False)
            # Panel2.Font.Color = clGrayText
            # DaysPanel.Caption = '0'
            # HoursPanel.setText('')

        self.set_status_text(self.TXT_COMPUTING)
        #
        #     #  Step through each time period until there is no more time left,
        #     #  an error occurs, or the user stops the run
        #     OldTime = Time
        #     repeat
        #     Application.ProcessMessages
        #     Err = swmm_step(ElapsedTime)
        #     NewTime = Time
        #     if MilliSecondsBetween(NewTime, OldTime) > 100:
        #         UpdateProgressDisplay(ElapsedTime, self.total_days)
        #     OldTime = NewTime
        #     until(ElapsedTime==0) or (Err > 0) or (self.run_status == RunStatus.rsStopped)
        #   # End the simulation and retrieve mass balance errors
        #   swmm_end()
        #   swmm_getMassBalErr(self.ErrRunoff, self.ErrFlow, self.ErrQual)
        # # Close the SWMM solver
        # swmm_close

    def compute_total_days(self):
        #  Compute the simulation duration in days from the Project's simulation options.
        try:
            end_date = datetime.strptime(self._parent.project.options.dates.end_date + ' ' +
                                         self._parent.project.options.dates.end_time, "%m/%d/%Y %H:%M")
            start_date = datetime.strptime(self._parent.project.options.dates.start_date + ' ' +
                                         self._parent.project.options.dates.start_time, "%m/%d/%Y %H:%M")
            return (end_date - start_date).days
        except:
            return 0.0

    def DisplayRunStatus(self):
        #  Displays the final status of the simulation run.

        #  Determine what the final run status is
        # if not (self.run_status == RunStatus.rsShutdown):
        #     if GetFileSize(TempReportFile) <= 0:
        #         self.run_status = RunStatus.rsFailed
        #     else:
        #         self.run_status = Uoutput.CheckRunStatus(TempOutputFile)

        # Display the appropriate run status message
        self.set_status_text(self.StatusLabelDict[self.run_status])

        #  Display mass balance errors if results are available
        if (self.run_status == RunStatus.rsWarning) or (self.run_status == RunStatus.rsSuccess):
            #  Display the information icon
            self.lblIconSuccessful.setVisible(True)
            self.fraFinished.setVisible(True)
            self.gbxContinuity.setTitle(self.TXT_CONTINUITY_ERROR)
            self.gbxContinuity.setVisible(True)

        #  Runoff continuity error
        if self.ErrRunoff != 0.0:
            self.lblSurface.setText(self.TXT_SURF_RUNOFF)
            self.txtSurface.setText('%7.2f %%'.format(self.ErrRunoff))

        #  Flow routing continuity error
        if self.ErrFlow != 0.0:
            self.lblFlow.setText(self.TXT_FLOW_ROUTING)
            self.txtFlow.setText('%7.2f %%'.format(self.ErrFlow))

        #  Quality routing continuity error
        if self.ErrQual != 0.0:
            self.lblQuality.setText(self.TXT_QUAL_ROUTING)
            self.txtQuality.setText('%7.2f %%'.format(self.ErrQual))

        #  If no results are available then display the error icon
        # else:
        #     self.lblIconError.setVisible(True)

        if self._parent:
            try:
                self._parent.showNormal()
            except:
                pass
        self.showNormal()
        self.setWindowState(self.windowState() + QtCore.Qt.WindowStaysOnTopHint)
