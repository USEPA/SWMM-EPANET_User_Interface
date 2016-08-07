import os
from enum import Enum
import traceback
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import Externals.epanet.model.epanet2 as pyepanet
from datetime import datetime
from ui.frmRunSimulation import frmRunSimulation, RunStatus
from ui.model_utility import process_events


class frmRunEPANET(frmRunSimulation):

    """
    Execute the network hydraulic and water quality solver (contained in EPANET2.DLL)
    and display its progress.
    Based on Fsimul.pas from EPANET2W Version 2.0 by L. Rossman
    """

    def __init__(self, model_api, project, main_form):
        frmRunSimulation.__init__(self, main_form)
        self.model_api = model_api
        self.project = project

        #  Initialize display of continuity errors
        self.ErrRunoff = 0.0  # Runoff continuity error
        self.ErrFlow = 0.0  # Flow routing continuity error
        self.ErrQual = 0.0  # Quality routing continuity error
        # self.lblSurface.setText('')
        # self.lblFlow.setText('')
        # self.lblQuality.setText('')
        # self.txtSurface.setText('')
        # self.txtFlow.setText('')
        # self.txtQuality.setText('')
        self.fraRunning.setVisible(True)
        self.fraFinished.setVisible(False)
        self.StatusLabel.Caption = self.TXT_STATUS_INIT
        self.cmdStop.setVisible(False)
        self.cmdMinimize.setVisible(False)
        self.cmdOK.setVisible(False)
        self.gbxContinuity.setVisible(False)
        self._total_days = 0  # total model time period duration, set while running

        #  Initialize placement and status of images on the ResultsPage
        self.lblIconSuccessful.Visible = False
        # self.lblIconError.Visible = False
        # self.lblIconError.Left = self.lblIconSuccessful.Left
        # self.lblIconError.Top  = self.lblIconSuccessful.Top

        #  Make the ProgressPage be the active page
        # Notebook1.PageIndex = 0

    def Execute(self):
        self.fraRunning.setVisible(True)
        self.fraFinished.setVisible(False)
        self.fraBottom.setVisible(True)
        self.set_status_text(self.TXT_STATUS_COMPILING)
        self.cmdStop.setVisible(True)
        self.cmdMinimize.setVisible(True)
        self.cmdOK.setVisible(False)
        # var
        #   OldDir: String
        # begin
        # // Change to temporary directory
        #   GetDir(0,OldDir)
        #   ChDir(TempDir)
        #
        # // Update the form's display
        #self.Update()
        #
        self.showNormal()
        self.set_status(RunStatus.rsCompiling)

        # TODO: decide whether to save input file in its own folder (only if modified) or in temp folder
        #   Uexport.ExportDataBase(TempInputFile,False)
        #
        # // Open solver and read in network data
        try:
            self._last_displayed_days = -1
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

            self.model_api.ENopen()

            # Solve for hydraulics & water quality, then close solver
            if self.run_status != RunStatus.rsCancelled:
                self.RunHydraulics(total_days)
            if self.run_status != RunStatus.rsCancelled:
                self.RunQuality(total_days)
            if self.run_status != RunStatus.rsCancelled:
                self.set_status(RunStatus.rsSuccess)
        except Exception as e:  # Close solver if an exception occurs
            self.set_status_text(self.TXT_STATUS_ERROR)
            msg = "Exception running simulation: " + '\n' + str(e) + '\n' + str(traceback.print_exc())
            print(msg)
            QtGui.QMessageBox.information(None, "EPANET", msg, QtGui.QMessageBox.Ok)
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
            except:  # Ignore exception closing model object?
                pass
            try:
                self.model_api.ENreport()
                self.model_api.ENclose()
            except:  # Ignore exception closing model object?
                pass

    def compute_total_days(self):
        #  Compute the simulation duration in days from the Project's simulation options.
        try:
            (hours, minutes) = self.project.times.duration.split(':')
            return float(hours) / 24 + float(minutes) / 1440
        except:
            try:
                hours = self.project.times.duration.split()[0]
                return float(hours) / 24
            except:
                pass
        return 0.0

    def RunHydraulics(self, total_days):
        # // Runs hydraulic simulation
        # var
        #   err: Integer
        #   t, tstep: Longint
        #   h: Single
        #   slabel: String
        try:
            self.set_status_text(self.TXT_SOLVING_HYD)
            self.model_api.ENopenH()
            self.model_api.ENinitH(1)
            self._last_displayed_days = -1

            seconds_this_step = 1
            elapsed_days = 0.0

            while seconds_this_step != 0 and self.run_status != RunStatus.rsCancelled:  # and err <= 100
                elapsed_seconds = self.model_api.ENrunH()
                # if err:
                    # print("ENrunH returned " + str(err))
                    # raise Exception("Error from model on ENrunH: " + str(err))
                seconds_this_step = self.model_api.ENnextH()
                # elapsed_days += (seconds_this_step / 3600)
                elapsed_days = elapsed_seconds / 3600.0 / 24.0
                self.update_progress_days(elapsed_days, total_days)
                # Multiply total_days by 2 to leave room for progress during RunQuality
                self.update_progress_bar(elapsed_days, total_days * 2)
                self.update_progress_days(elapsed_days, total_days)
                # print ("RunH:", elapsed_days, elapsed_seconds / 3600, seconds_this_step)
                process_events()

        finally:
            try:
                self.model_api.ENcloseH()
            except:  # Ignore exception on close?
                pass

            # begin
            # // Open hydraulics solver
            #   err := 0
            #   StatusLabel.Caption := TXT_REORDERING
            #   StatusLabel.Refresh
            #   try
            #     if ENopenH() = 0 then
            #     begin
            #
            #     // Initialize hydraulics solver
            #       ENinitH(1)
            #       h := 0
            #       slabel := TXT_SOLVING_HYD
            #
            #     // Solve hydraulics in each period
            #       repeat
            #         StatusLabel.Caption := Format('%s %.2f',[slabel,h])
            #         Application.ProcessMessages
            #         err := ENrunH(t)
            #         tstep := 0
            #         if err <= 100 then err := ENnextH(tstep)
            #         h := h + tstep/3600
            #       until (tstep = 0) or (err > 100) or (RunStatus = rsCancelled)
            #     end
            #
            #   // Close hydraulics solver & ignore warning conditions
            #     ENcloseH()
            #     if err <= 100 then err := 0
            #     Result := err
            #
            # // Exception handler
            #   except
            #     ENcloseH()
            #     raise
            #   end
            # end

    def RunQuality(self, total_days):
        """
        Run water quality simulation
        var
            err: Integer
            t, tstep: Longint
            h: Single
            slabel: String
        """

        try:
            self.set_status_text(self.TXT_SOLVING_WQ)
            self.model_api.ENopenQ()
            self.model_api.ENinitQ(1)
            self._last_displayed_days = -1

            err = None
            seconds_this_step = 1
            elapsed_days = 0.0

            while seconds_this_step != 0 and self.run_status != RunStatus.rsCancelled:  # and err <= 100
                elapsed_seconds = self.model_api.ENrunQ()
                # if err:
                    # print("ENrunQ returned " + str(err))
                    # raise Exception("Error code from model on ENrunQ: " + str(err))
                seconds_this_step = self.model_api.ENnextQ()
                #elapsed_days += (seconds_this_step / 3600)
                elapsed_days = elapsed_seconds / 3600.0 / 24.0
                self.update_progress_days(elapsed_days, total_days)
                # Add and multiply by 2 to pick up progress where RunHydraulics left off
                self.update_progress_bar(elapsed_days + total_days, total_days * 2)
                # print (elapsed_days, elapsed_seconds / 3600, seconds_this_step)
                # print ("RunQ:", elapsed_days, elapsed_seconds / 3600 / 24, seconds_this_step)
                process_events()
        finally:
            try:
                self.model_api.ENcloseQ()
            except:  # Ignore exception on close?
                pass
        #
    # begin
    # // Open WQ solver
    #   h := 0
    #   if UpperCase(Trim(Network.Options.Data[QUAL_PARAM_INDEX])) = 'NONE'
    #   then slabel := TXT_SAVING_HYD
    #   else slabel := TXT_SOLVING_WQ
    #   try
    #     if ENopenQ() = 0 then
    #     begin
    #
    #   // Initialize WQ solver & solve WQ in each period
    #       ENinitQ(1)
    #       repeat
    #         StatusLabel.Caption := Format('%s %.2f',[slabel,h])
    #         err := ENrunQ(t)
    #         tstep := 0
    #         if err <= 100 then err := ENnextQ(tstep)
    #         h := h + tstep/3600
    #         Application.ProcessMessages
    #       until (tstep = 0) or (err > 100) or (RunStatus = rsCancelled)
    #     end
    #
    #   // Close WQ solver & ignore warning conditions
    #     ENcloseQ()
    #
    #   except
    #     ENcloseQ()
    #     raise
    #   end
    # end
    #
    #
    def DisplayRunStatus(self):
        # Display final status of simulation run
        self.set_status_text(self.StatusLabelDict[self.run_status])
    # //----------------------------------------------
    # begin
    # // Retrieve final run status
    #   if not (RunStatus in [rsCancelled, rsShutdown]) then
    #   begin
    #     if GetFileSize(TempReportFile) <= 0 then RunStatus := rsFailed
    #     else RunStatus := Uoutput.CheckRunStatus(TempOutputFile)
    #   end
    #
    # // Display run status message
    #   case RunStatus of
    #     rsShutdown:     StatusLabel.Caption := TXT_STATUS_SHUTDOWN
    #     rsNone:         StatusLabel.Caption := TXT_STATUS_NONE
    #     rsWrongVersion: StatusLabel.Caption := TXT_STATUS_WRONGVERSION
    #     rsFailed:       StatusLabel.Caption := TXT_STATUS_FAILED
    #     rsError:        StatusLabel.Caption := TXT_STATUS_ERROR
    #     rsWarning:      StatusLabel.Caption := TXT_STATUS_WARNING
    #     rsSuccess:      StatusLabel.Caption := TXT_STATUS_SUCCESS
    #     rsCancelled:    StatusLabel.Caption := TXT_STATUS_CANCELLED
    #   end
    # end
    #
    # end.
