import os
import traceback
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMessageBox
import Externals.swmm.model.swmm5 as pyswmm
from datetime import datetime
from ui.frmRunSimulation import frmRunSimulation, RunStatus
from ui.model_utility import process_events


class frmRunSWMM(frmRunSimulation):

    """
    Execute the SWMM simulation engine (in SWMM5.DLL) and display progress.
    Based on Fsimul.pas from EPA SWMM 5.1 12/2/13 (5.1.000) by L. Rossman
    """

    TXT_SWMM5 = 'SWMM 5.1 - '

    def __init__(self, model_api, project, main_form):
        frmRunSimulation.__init__(self, main_form)
        self.model_api = model_api
        self.project = project

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
        # self.fraFinished.setText('')
        self.fraFinished.setVisible(False)
        self.fraRunning.setVisible(True)
        self.fraFinished.setVisible(False)
        self.StatusLabel.Caption = self.TXT_STATUS_INIT
        self.cmdStop.setVisible(False)
        self.cmdMinimize.setVisible(False)
        self.cmdOK.setVisible(False)
        self.gbxContinuity.setVisible(False)

        #  Initialize placement and status of images on the ResultsPage
        self.lblIconSuccessful.Visible = False
        # self.lblIconError.Visible = False
        # self.lblIconError.Left = self.lblIconSuccessful.Left
        # self.lblIconError.Top  = self.lblIconSuccessful.Top

        #  Make the ProgressPage be the active page
        # Notebook1.PageIndex = 0

    def Execute(self):
        """
            Call into the SWMM DLL engine to perform a simulation.
        """
        """ TODO?
            The input, report, and binary output files required by the SWMM
            engine have already been created in Fmain.pas' RunSimulation
            procedure through a call to CreateTempFiles.
        """
        self.fraRunning.setVisible(True)
        self.fraFinished.setVisible(False)
        self.fraBottom.setVisible(True)
        self.set_status(RunStatus.rsCompiling)


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
        self.cmdStop.setVisible(True)
        self.cmdMinimize.setVisible(True)
        self.cmdOK.setVisible(False)
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
        self.showNormal()
        self.set_status(RunStatus.rsCompiling)

        try:
            total_days = self.compute_total_days()
            if total_days:  # If we could compute a number of simulation days, prepare progress and date/time controls
                self.progressBar.setVisible(True)
                self.lblTime.setVisible(True)
                self.fraTime.setVisible(True)

                if total_days >= self.SHORT_TERM_LIMIT:
                    self.lblHrsMin.setVisible(False)
                    self.txtHrsMin.setVisible(False)
                else:  # Prepare the elapsed time display for shorter simulations
                    self.lblHrsMin.setVisible(True)
                    self.txtHrsMin.setVisible(True)
                    self.txtHrsMin.setText("00:00")
            else:  # No computed number of simulation days, so hide progress and date/time controls
                self.progressBar.setVisible(False)
                self.lblTime.setVisible(False)
                self.fraTime.setVisible(False)

            self.set_status(RunStatus.rsComputing)

            print("Running SWMM " + str(self.model_api.swmm_getVersion()))
            self.model_api.swmm_run()

            self.model_api.swmm_open()
            self.model_api.swmm_start()
            date_updated = datetime.now()
            while self.run_status == RunStatus.rsComputing and self.model_api.errcode == 0:
                elapsed_days = self.model_api.swmm_step()
                if elapsed_days > 0:
                    if total_days:
                        date_now = datetime.now()
                        if (date_now - date_updated).microseconds > 100000:
                            self.update_progress_days(elapsed_days, total_days)
                            self.update_progress_bar(elapsed_days, total_days)
                            process_events()
                            date_updated = date_now
                else:
                    self.model_api.swmm_end()
                    break

                #  Step through each time period until there is no more time left,
                #  an error occurs, or the user stops the run
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

            self.ErrRunoff, self.ErrFlow, self.ErrQual = self.model_api.swmm_getMassBalErr()

            if self.model_api.Errflag:
                print("\n\nSWMM completed. There are errors.\n")
                self.set_status(RunStatus.rsError)
            elif self.model_api.Warnflag:
                print("\n\nSWMM completed. There are warnings.\n")
                self.set_status(RunStatus.rsWarning)
            else:
                print("\n\nSWMM completed.\n")
                self.set_status(RunStatus.rsSuccess)

        except Exception as e:  # Close solver if an exception occurs
            self.set_status(RunStatus.rsError)
            msg = "Exception running simulation: " + '\n' + str(e) + '\n' + str(traceback.print_exc())
            print(msg)
            QMessageBox.information(None, "SWMM", msg, QMessageBox.Ok)
            self.set_status(RunStatus.rsShutdown)
        finally:
            try:
                self.lblSuccessful.setText(self.StatusLabel.text())
                self.fraRunning.setVisible(False)
                self.gbxContinuity.setVisible(False)
                self.fraFinished.setVisible(True)
                self.cmdStop.setVisible(False)
                self.cmdMinimize.setVisible(False)
                self.cmdOK.setVisible(True)
                self.update()
                process_events()
            except:  # Ignore exception closing model object
                pass
            try:
                # self.model_api.swmm_report()
                self.model_api.swmm_close()
            except:  # Ignore exception closing model object
                pass

    def compute_total_days(self):
        #  Compute the simulation duration in days from the Project's simulation options.
        try:
            end_date = datetime.strptime(self._main_form.project.options.dates.end_date + ' ' +
                                         self._main_form.project.options.dates.end_time, "%m/%d/%Y %H:%M")
            start_date = datetime.strptime(self._main_form.project.options.dates.start_date + ' ' +
                                           self._main_form.project.options.dates.start_time, "%m/%d/%Y %H:%M")
            return (end_date - start_date).days + 1
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

        if self._main_form:
            try:
                self._main_form.showNormal()
            except:
                pass
        self.showNormal()
        self.setWindowState(self.windowState() + QtCore.Qt.WindowStaysOnTopHint)
