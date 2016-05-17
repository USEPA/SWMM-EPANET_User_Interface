"""
    EPANET Report Generation
    Based on Ureport.pas from EPANET2W 2.0 9/7/00 Author: L. Rossman
    Converted to Python April 2016 by Mark Gray, RESPEC
"""

import sys
import traceback
from datetime import datetime
from core.epanet.project import Project
import Externals.epanet.output.outputapi
from Externals.epanet.output.ENOutputWrapper import *
import Externals.epanet.output.functionalwrapper
# See Also: from core.epanet.options.report import ReportOptions

class Reports:
    PAGESIZE = 55
    ULINE = '----------------------------------------------------------------------'
    FMT18 = '  Page 1                                          %22s'
    FMT_DATE = '%Y/%m/%d %I:%M%p'
    FMT82 = '  Page %-4d %60s'
    FMT71 = 'Energy Usage:'
    FMT72 = '                  Usage   Avg.     Kw-hr      Avg.      Peak      Cost'
    FMT73 = 'Pump             Factor Effic.     %s        Kw        Kw      /day'
    FMT74 = '%45s Demand Charge: %9.2f'
    FMT75 = '%45s Total Cost:    %9.2f'
    TXT_perM3 = '/m3'
    TXT_perMGAL = '/Mgal'
    TXT_CONTINUED = ' (continued)'
    TXT_INPUT_FILE = 'Input File: '
    TXT_LINK_INFO = 'Link - Node Table:'
    TXT_NODE_RESULTS = 'Node Results'
    TXT_LINK_RESULTS = 'Link Results'
    TXT_AT = ' at '
    TXT_ID = 'ID'
    TXT_NODE = 'Node'
    TXT_LINK = 'Link'
    TXT_START = 'Start'
    TXT_END = 'End'
    MSG_REPORT_SIZE1 = 'This full report will use over '
    MSG_REPORT_SIZE2 = ' Mbytes of disk space. Do you wish to proceed?'
    MSG_WRITING_REPORT = 'Writing full report...'
    MSG_NO_WRITE = 'Could not write full report to file '
    TXT_REPORT_FILTER = 'Report files (*.RPT)|*.RPT|All files|*.*'
    TimeStat = ['Single Period', 'Average', 'Minimum', 'Maximum', 'Range']

    def __init__(self, epanet_project, model_output):
        self.LogoTxt = (
            '**********************************************************************',
            '*                             E P A N E T                            *',
            '*                     Hydraulic and Water Quality                    *',
            '*                     Analysis for Pipe Networks                     *',
            '*                           Version 2.0                              *',
            '**********************************************************************')
        self.F = None  # File being written to
        if isinstance(epanet_project, Project):
            self.project = epanet_project
        elif isinstance(epanet_project, str):
            self.project = Project()
            self.project.read_file(epanet_project)
        else:
            raise Exception("Report Initialization: could not read EPANET project")

        if isinstance(model_output, OutputObject):
            self.output = model_output
        elif isinstance(model_output, str):
            self.output = OutputObject(model_output)
        else:
            raise Exception("Report Initialization: could not read EPANET project")

        if self.project.metric:
            self.unit_system = ENR_UnitsSI
        else:
            self.unit_system = ENR_UnitsUS
        self.RptTitle = self.project.title.title
        self.PageNum = 0
        self.LineNum = 0
        self.Progstep = 0
        self.Nprogress = 0

    # def write_file(self, file_name):
    #     if file_name:
    #         with open(file_name, 'w') as writer:
    #             writer.writelines(self.get_text())
    #             self.file_name = file_name

    def write_line(self, line):
        if (self.LineNum >= self.PAGESIZE):
            self.PageNum += 1
            self.F.write('\n\f\n')  # newline form-feed newline
            self.F.write(self.FMT82.format(self.PageNum, self.RptTitle) + '\n')
            self.LineNum = 3
        self.F.write('  ' + line + '\n')
        self.LineNum += 1

    def write_logo(self):
        self.PageNum = 1
        self.LineNum = 2
        self.write_line(self.FMT18.format(datetime.now().strftime(self.FMT_DATE)))
        for line in self.LogoTxt:
            self.write_line(line)
        self.write_line('')
        self.write_line(self.TXT_INPUT_FILE + self.project.file_name)
        self.write_line('')
        self.write_line(self.RptTitle)
        self.write_line(self.project.title.notes)
        self.write_line('')

    def WriteEnergyHeader(self, ContinueFlag):
        if self.LineNum + 11 > self.PAGESIZE:
            self.LineNum = self.PAGESIZE
            S2 = (self.TXT_perMGAL, self.TXT_perM3)[self.unit_system]
            S = self.FMT71
        if ContinueFlag:
            S += self.TXT_CONTINUED
            self.write_line(S)
            self.write_line(self.ULINE)
            S = self.FMT72
            self.write_line(S)
            S = self.FMT73.format(S2)
            self.write_line(S)
            self.write_line(self.ULINE)

    def WriteEnergy(self):
# var
#   j,k: Integer
#   x: array[0..5] of Single
#   Dcharge: Single
#   Csum: Single
#   S: String
        self.WriteEnergyHeader(False)
        Csum = 0.0
    #  for j = 0 to Network.Lists[PUMPS].Count-1 do
    #     begin
    #       k = Link(PUMPS,j).Zindex
    #       if k < 0: continue
    #       Uoutput.GetPumpEnergy(k,x,Dcharge)
    #       Csum = Csum + x[5]
    #       if (self.LineNum == self.PageSize):
    #           self.WriteEnergyHeader(True)
    #       S = ''  # ('{:15}  %6.2f %6.2f %9.2f %9.2f %9.2f %9.2f'.format([GetID(PUMPS,j),x[0],x[1],x[2],x[3],x[4],x[5]])
    #       self.write_line(S)
    #     end
    #   self.write_line(self.ULINE)
    #   S = Format(FMT74,['', Dcharge])
    #   self.write_line(S)
    #   S = Format(FMT75, ['',Csum+Dcharge])
    #   self.write_line(S)
        self.write_line('')

    def WriteNodeHeader(self, T, ContinueFlag):
        if self.LineNum + 11 > self.PAGESIZE:
            self.LineNum = self.PAGESIZE
        S = self.TXT_NODE_RESULTS
        if self.output.numPeriods > 1:
            S += self.TXT_AT + self.TimeStat[T]
        S += ':'
        if ContinueFlag: S += self.TXT_CONTINUED
        self.write_line(S)
        self.write_line(self.ULINE)
        self.output.get_Node
        S = '{:15} {:10}{:10}{:10}{:10}'.format(self.TXT_NODE,
                                                ENR_NodeAttributeNames[ENR_demand],
                                                ENR_NodeAttributeNames[ENR_head],
                                                ENR_NodeAttributeNames[ENR_pressure],
                                                ENR_NodeAttributeNames[ENR_quality])
        self.write_line(S)
        S = '{:15} {:10}{:10}{:10}{:10}'.format(self.TXT_ID,
                                                ENR_NodeAttributeUnits[ENR_demand][self.unit_system],
                                                ENR_NodeAttributeNames[ENR_head][self.unit_system],
                                                ENR_NodeAttributeNames[ENR_pressure][self.unit_system],
                                                ENR_NodeAttributeNames[ENR_quality][self.unit_system])
        self.write_line(S)
        self.write_line(self.ULINE)

    def WriteLinkHeader(self, T, ContinueFlag):
        if self.LineNum + 11 > self.PAGESIZE:
            self.LineNum = self.PAGESIZE
        S = self.TXT_LINK_RESULTS
        if self.output.numPeriods > 1:
            S += self.TXT_AT + self.TimeStat[T]
        S += ':'
        if ContinueFlag:
            S += self.TXT_CONTINUED
        self.write_line(S)
        self.write_line(self.ULINE)
        S = '{:15} {:10}{:10}{:10}{:10}'.format(self.TXT_LINK,
                                                ENR_LinkAttributeNames[ENR_flow],
                                                ENR_LinkAttributeNames[ENR_velocity],
                                                ENR_LinkAttributeNames[ENR_headloss],
                                                ENR_LinkAttributeNames[ENR_status])
        self.write_line(S)
        S = '{:15} {:10}{:10}{:10}'.format(self.TXT_ID,
                                           ENR_LinkAttributeUnits[ENR_flow][self.unit_system],
                                           ENR_LinkAttributeUnits[ENR_velocity][self.unit_system],
                                           ENR_LinkAttributeUnits[ENR_headloss][self.unit_system])
        self.write_line(S)
        self.write_line(self.ULINE)

    def WriteLinkInfoHeader(self, ContinueFlag):
        S = self.TXT_LINK_INFO
        if ContinueFlag:
            S += self.TXT_CONTINUED
        self.write_line(S)
        self.write_line(self.ULINE)
        S = '{:15}{:15}{:15}{:10}{:10}'.format(self.TXT_LINK, self.TXT_START, self.TXT_END, "Length", "Diameter")
        self.write_line(S)

        len_units = ('ft','m')[self.unit_system]
        dia_units = ('in','mm')[self.unit_system]
        S = '{:15}{:15}{:15}{:10}{:10}'.format(self.TXT_ID, self.TXT_NODE, self.TXT_NODE, len_units, dia_units)
        self.write_line(S)
        self.write_line(self.ULINE)

    def WriteLinkInfo(self):
        self.WriteLinkInfoHeader(False)
        for conduits in (self.project.pipes, self.project.pumps, self.project.valves):
            # TODO: update progress bar: MainForm.UpdateProgressBar(Nprogress, ProgStep)
            for conduit in conduits.value:
                # Note: Pascal report got these values from binary, we get them here from input
                # length = self.output.get_LinkValue(conduits.id, 0, 1) # Uoutput.GetLinkValStr(LINKLENGTH,0,I,J)
                if (self.LineNum >= self.PAGESIZE):
                    self.WriteLinkInfoHeader(True)
                if hasattr(conduit, "length"):
                    length = conduit.length
                else:
                    length = ""
                if hasattr(conduit, "diameter"):
                    diameter = conduit.diameter
                else:
                    diameter = ""
                S = '{:15}{:15}{:15}{:10}{:10}'.format(conduit.id, conduit.inlet_node, conduit.outlet_node,
                                                       length, diameter)
                if conduits is self.project.pumps:
                    S += ' Pump'
                elif conduits is self.project.valves:
                    S += ' Valve'
                self.write_line(S)
        self.write_line('')

    def WriteNodeTable(self, T):
        self.WriteNodeHeader(T, False)
        for nodes in (self.project.junctions, self.project.reservoirs, self.project.tanks):
            for node in nodes.value:
                #         MainForm.UpdateProgressBar(Nprogress, ProgStep)
                node_index = self.output.get_NodeIndex(node.id)
                demand =   self.output.get_NodeValue(node_index, T, ENR_demand)
                head =     self.output.get_NodeValue(node_index, T, ENR_head)
                pressure = self.output.get_NodeValue(node_index, T, ENR_pressure)
                quality =  self.output.get_NodeValue(node_index, T, ENR_quality)
                S = '{:15} {:10}{:10}{:10}{:10}'.format(node.id, demand, head, pressure, quality)
                if nodes is self.project.reservoirs:
                    S += ' Reservoir'
                elif nodes is self.project.tanks:
                    S += ' Tank'
                if (self.LineNum == self.PAGESIZE):
                    self.WriteNodeHeader(T, True)
                self.write_line(S)
        self.write_line('')

    def WriteLinkTable(self, T):
# var
#   I,J: Integer
#   ID,Q,V,H,S,R: String
# begin
#   try
        self.WriteLinkHeader(T, False)
#     for I = PIPES to VALVES do
#     begin
#       for J = 0 to Network.Lists[I].Count-1 do
#       begin
#         MainForm.UpdateProgressBar(Nprogress, ProgStep)
#         if Link(I,J).Zindex < 0: continue
#         ID = GetID(I,J)
#         Q = Uoutput.GetLinkValStr(FLOW,T,I,J)
#         V = Uoutput.GetLinkValStr(VELOCITY,T,I,J)
#         H = Uoutput.GetLinkValStr(HEADLOSS,T,I,J)
#         S = Uoutput.GetLinkValStr(LINKSTAT,T,I,J)
#         if (LineNum == self.PAGESIZE): WriteLinkHeader(T,True)
#         R = Format('{:15} {:10}{:10}{:10}{:10}',[ID,Q,V,H,S])
#         if I > PIPES: R = R + ' ' + ObjectLabel[I]
#         self.write_line(R)
#       end
#     end
#     self.write_line('')

    def WriteResults(self):
# var
#   N: Integer
# begin
#   try
#     for N = 0 to self.output.numPeriods-1 do
#     begin
#       Application.ProcessMessages
#       WriteNodeTable(N)
#       Application.ProcessMessages
#       WriteLinkTable(N)
#     end
        pass

    def write_report(self, report_file_name):
        #   MainForm.ShowProgressBar(MSG_WRITING_REPORT)
        with open(report_file_name, 'w') as self.F:
            try:
                Total = self.output.nodeCount + self.output.linkCount
                Total *= self.output.numPeriods
                Total += self.output.linkCount
                #     with MainForm.ProgressBar do
                #       N = Max div Step
                #     ProgStep = Round(Total/N)
                #     Nprogress = 0
                self.write_logo()
                #     Application.ProcessMessages
                self.WriteLinkInfo()
                if self.output.pumpCount > 0:
                    self.WriteEnergy()
                self.WriteResults()
                # Result = True
                #   finally
                #   end
                #   CloseFile(F)
                #   MainForm.HideProgressBar
            finally:
                print "Finished writing report " + report_file_name

#    def CreateFullReport(self, Filename):
# var
#   R: Boolean
#   Size: Single
#   Fname: String
# // Check for huge file size
#   Size = (Nlinks + (Nnodes + Nlinks)*self.output.numPeriods)*60*1e-6
#   if Size > 10:
#     if MessageDlg(MSG_REPORT_SIZE1 + IntToStr(Trunc(Size)) +
#       MSG_REPORT_SIZE2, mtConfirmation, [mbYes,mbNo], 0) == mrNo
#        : Exit
# 
# // Get a report file name
#   Fname = ''
#   with MainForm.SaveDialog do
#   begin
# 
#   // Set options for Save File dialog
#     Filter = TXT_REPORT_FILTER
#     if Length(InputFileName) > 0: Filename :=
#       ChangeFileExt(ExtractFileName(InputFileName),'.rpt')
#     else Filename = '*.rpt'
# 
#   // Execute Save File dialog & write report to file
#     if Execute: Fname = Filename
#     if Length(Fname) > 0:
#     begin
#       Screen.Cursor = crHourGlass
#       R = self.WriteReport(Filename)
#       Screen.Cursor = crDefault
#       if not R:
#         MessageDlg(MSG_NO_WRITE + ExtractFileName(Filename),
#           mtError, [mbOK], 0)
