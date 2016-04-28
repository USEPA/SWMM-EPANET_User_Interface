"""
    EPANET Report Generation
    Based on Ureport.pas from EPANET2W 2.0 9/7/00 Author: L. Rossman
    Converted to Python April 2016 by Mark Gray, RESPEC
"""

import sys
# See Also: from core.epanet.options.report import ReportOptions

class Reports:
    FORMFEED = '\f'
    PAGESIZE = 55
    ULINE = '----------------------------------------------------------------------'
    FMT18 = '  Page 1                                          %22s'
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

    def __init__(self, report_file_name, input_file):
        self.LogoTxt = (
            '**********************************************************************',
            '*                             E P A N E T                            *',
            '*                     Hydraulic and Water Quality                    *',
            '*                     Analysis for Pipe Networks                     *',
            '*                           Version 2.0                              *',
            '**********************************************************************')

        self.F = open(report_file_name, 'w')  # File being written to
        self.input_file = input_file
        self.RptTitle = self.input_file.title.title
        self.PageNum = 0
        self.LineNum = 0
        self.Progstep = 0
        self.Nprogress = 0

    def write_file(self, file_name):
        if file_name:
            with open(file_name, 'w') as writer:
                writer.writelines(self.get_text())
                self.file_name = file_name

    def WriteLine(self, S):
        if (self.LineNum == self.PAGESIZE):
            self.PageNum += 1
            self.F.write('\n')
            self.F.write(self.F, self.FORMFEED)
            self.F.write('\n')
            self.F.write(self.FMT82.format(self.PageNum, self.RptTitle) + '\n')
            self.LineNum = 3
        self.F.write('  ' + S + '\n')
        self.LineNum += 1

    def WriteLogo(self):
        self.PageNum = 1
        self.LineNum = 2
        # TODO: S = self.FMT18.format(DateTimeToStr(Now))
        self.WriteLine(S)
        for line in self.LogoTxt:
            self.WriteLine(line)
        self.Writeline('')
        self.Writeline(self.TXT_INPUT_FILE + self.input_file.file_name)
        self.Writeline('')
        self.Writeline(self.RptTitle)
        self.WriteLine(self.input_file.title.notes)
        self.Writeline('')

    def WriteEnergyHeader(self, ContinueFlag):
        # var
        #   S:  String
        #   S2: String
        if self.LineNum + 11 > self.PAGESIZE:
            self.LineNum = self.PAGESIZE
            if self.input_file.metric:
                S2 = self.TXT_perM3
            else:
                S2 = self.TXT_perMGAL
            S = self.FMT71
        if ContinueFlag:
            S += self.TXT_CONTINUED
            self.Writeline(S)
            self.Writeline(self.ULINE)
            S = self.FMT72
            self.Writeline(S)
            S = self.FMT73.format(S2)
            self.Writeline(S)
            self.Writeline(self.ULINE)

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
    #       if k < 0 then continue
    #       Uoutput.GetPumpEnergy(k,x,Dcharge)
    #       Csum = Csum + x[5]
    #       if (self.LineNum == self.PageSize):
    #           self.WriteEnergyHeader(True)
    #       S = ''  # ('%-15s  %6.2f %6.2f %9.2f %9.2f %9.2f %9.2f'.format([GetID(PUMPS,j),x[0],x[1],x[2],x[3],x[4],x[5]])
    #       self.Writeline(S)
    #     end
    #   self.Writeline(self.ULINE)
    #   S = Format(FMT74,['', Dcharge])
    #   self.Writeline(S)
    #   S = Format(FMT75, ['',Csum+Dcharge])
    #   self.Writeline(S)
        self.Writeline('')

    def WriteNodeHeader(self, T, ContinueFlag):
# var
#   S: String
#     if LineNum + 11 > PAGESIZE then LineNum = PAGESIZE
        S = self.TXT_NODE_RESULTS
#     if Nperiods > 1 then S += self.TXT_AT + BrowserForm.TimeListBox.Items[T]
        S += ':'
#     if ContinueFlag then S = S + TXT_CONTINUED
        self.Writeline(S)
        self.Writeline(self.ULINE)
#     S = Format('%-15s %10s%10s%10s%10s',[TXT_NODE, NodeVariable[DEMAND].Name,
#       NodeVariable[HEAD].Name, NodeVariable[PRESSURE].Name,
#         NodeVariable[NODEQUAL].Name])
        self.Writeline(S)
#     S = Format('%-15s %10s%10s%10s%10s',[TXT_ID, NodeUnits[DEMAND].Units,
#       NodeUnits[HEAD].Units, NodeUnits[PRESSURE].Units,
#         NodeUnits[NODEQUAL].Units])
        self.Writeline(S)
        self.Writeline(self.ULINE)

    def WriteLinkHeader(self, T, ContinueFlag):
# var
#   S: String
#     if LineNum + 11 > PAGESIZE then LineNum = PAGESIZE
        S = self.TXT_LINK_RESULTS
#     if Nperiods > 1 then S = S + TXT_AT + BrowserForm.TimeListBox.Items[T]
#     S = S + ':'
#     if ContinueFlag then S = S + TXT_CONTINUED
        self.Writeline(S)
        self.Writeline(self.ULINE)
#     S = Format('%-15s %10s%10s%10s%10s',[TXT_LINK, LinkVariable[FLOW].Name,
#       LinkVariable[VELOCITY].Name, LinkVariable[HEADLOSS].Name,
#         LinkVariable[LINKSTAT].Name])
        self.Writeline(S)
#     S = Format('%-15s %10s%10s%10s',[TXT_ID, LinkUnits[FLOW].Units,
#       LinkUnits[VELOCITY].Units, LinkUnits[HEADLOSS].Units])
        self.Writeline(S)
        self.Writeline(self.ULINE)

    def WriteLinkInfoHeader(self, ContinueFlag):
# var
#   S: String
        S = self.TXT_LINK_INFO
        if ContinueFlag:
            S += self.TXT_CONTINUED
        self.Writeline(S)
        self.Writeline(self.ULINE)
#     S = Format('%-15s%-15s%-15s%10s%10s',[TXT_LINK, TXT_START, TXT_END,
#       LinkVariable[LINKLENGTH].Name, LinkVariable[DIAMETER].Name])
#     Writeline(S)
#     S = Format('%-15s%-15s%-15s%10s%10s',[TXT_ID, TXT_NODE, TXT_NODE,
#       LinkUnits[LINKLENGTH].Units, LinkUnits[DIAMETER].Units])
#     Writeline(S)
#     Writeline(ULINE)

    def WriteLinkInfo(self):
# var
#   I,J: Integer
#   ID,N1,N2,L,D,S: String
#   aLink: TLink
# begin
#   try
        self.WriteLinkInfoHeader(False)
#     for I = PIPES to VALVES do
#     begin
#       for J = 0 to Network.Lists[I].Count-1 do
#       begin
#         MainForm.UpdateProgressBar(Nprogress, ProgStep)
#         if Link(I,J).Zindex < 0 then continue
#         aLink = Link(I,J)
#         ID = GetID(I,J)
#         N1 = aLink.Node1.ID
#         N2 = aLink.Node2.ID
#         L = Uoutput.GetLinkValStr(LINKLENGTH,0,I,J)
#         D = Uoutput.GetLinkValStr(DIAMETER,0,I,J)
#         if (LineNum == PageSize) then WriteLinkInfoHeader(True)
#         S = Format('%-15s%-15s%-15s%10s%10s',[ID,N1,N2,L,D])
#         if I > PIPES then S = S + ' ' + ObjectLabel[I]
#         Writeline(S)
#       end
#     end
        self.Writeline('')

    def WriteNodeTable(self, T):
# var
#   I,J: Integer
#   ID,D,H,P,C,S: String
# begin
#   try
        self.WriteNodeHeader(T, False)
#     for I = JUNCS to TANKS do
#     begin
#       for J = 0 to Network.Lists[I].Count-1 do
#       begin
#         MainForm.UpdateProgressBar(Nprogress, ProgStep)
#         if Node(I,J).Zindex < 0 then continue
#         ID = GetID(I,J)
#         D = Uoutput.GetNodeValStr(DEMAND,T,I,J)
#         H = Uoutput.GetNodeValStr(HEAD,T,I,J)
#         P = Uoutput.GetNodeValStr(PRESSURE,T,I,J)
#         C = Uoutput.GetNodeValStr(NODEQUAL,T,I,J)
#         if (LineNum == PageSize) then WriteNodeHeader(T,True)
#         S = Format('%-15s %10s%10s%10s%10s',[ID,D,H,P,C])
#         if I > JUNCS then S = S + ' ' + ObjectLabel[I]
#         Writeline(S)
#       end
#     end
#     Writeline('')


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
#         if Link(I,J).Zindex < 0 then continue
#         ID = GetID(I,J)
#         Q = Uoutput.GetLinkValStr(FLOW,T,I,J)
#         V = Uoutput.GetLinkValStr(VELOCITY,T,I,J)
#         H = Uoutput.GetLinkValStr(HEADLOSS,T,I,J)
#         S = Uoutput.GetLinkValStr(LINKSTAT,T,I,J)
#         if (LineNum == PageSize) then WriteLinkHeader(T,True)
#         R = Format('%-15s %10s%10s%10s%10s',[ID,Q,V,H,S])
#         if I > PIPES then R = R + ' ' + ObjectLabel[I]
#         Writeline(R)
#       end
#     end
#     Writeline('')

    def WriteResults(self):
# var
#   N: Integer
# begin
#   try
#     for N = 0 to Nperiods-1 do
#     begin
#       Application.ProcessMessages
#       WriteNodeTable(N)
#       Application.ProcessMessages
#       WriteLinkTable(N)
#     end
        pass

    def WriteReport(self, Fname):
# var
#   Total: Single
#   N: Integer
# begin
#   Result = False
#   MainForm.ShowProgressBar(MSG_WRITING_REPORT)
#   AssignFile(F,Fname)
#   {$I-}
#   Rewrite(F)
#   {$I+}
#   if (IOResult == 0) then
#   try
#     Total = Nnodes + Nlinks
#     Total = Total * Nperiods + Nlinks
#     with MainForm.ProgressBar do
#       N = Max div Step
#     ProgStep = Round(Total/N)
#     Nprogress = 0
#     WriteLogo
#     Application.ProcessMessages
#     WriteLinkInfo
#     if Npumps > 0 then WriteEnergy
#     WriteResults
#     Result = True
#   finally
#   end
#   CloseFile(F)
#   MainForm.HideProgressBar
        pass

    def CreateFullReport(self):
# var
#   R: Boolean
#   Size: Single
#   Fname: String
# // Check for huge file size
#   Size = (Nlinks + (Nnodes + Nlinks)*Nperiods)*60*1e-6
#   if Size > 10 then
#     if MessageDlg(MSG_REPORT_SIZE1 + IntToStr(Trunc(Size)) +
#       MSG_REPORT_SIZE2, mtConfirmation, [mbYes,mbNo], 0) == mrNo
#         then Exit
# 
# // Get a report file name
#   Fname = ''
#   with MainForm.SaveDialog do
#   begin
# 
#   // Set options for Save File dialog
#     Filter = TXT_REPORT_FILTER
#     if Length(InputFileName) > 0 then Filename :=
#       ChangeFileExt(ExtractFileName(InputFileName),'.rpt')
#     else Filename = '*.rpt'
# 
#   // Execute Save File dialog & write report to file
#     if Execute then Fname = Filename
#     if Length(Fname) > 0 then
#     begin
#       Screen.Cursor = crHourGlass
#       R = WriteReport(Filename)
#       Screen.Cursor = crDefault
#       if not R then
#         MessageDlg(MSG_NO_WRITE + ExtractFileName(Filename),
#           mtError, [mbOK], 0)
        pass
