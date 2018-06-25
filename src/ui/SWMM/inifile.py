from PyQt5.Qt import Qt
from PyQt5.Qt import QSettings
from core.swmm.hydrology.subcatchment import HortonInfiltration
from core.swmm.hydrology.subcatchment import GreenAmptInfiltration
from core.swmm.hydrology.subcatchment import CurveNumberInfiltration
from core.swmm.hydrology.subcatchment import E_InfilModel
from core.swmm.hydraulics.link import CrossSectionShape
from core.swmm.hydraulics.link import CrossSection
import core.swmm.options.general as hyd
import core.swmm.options.dynamic_wave as dw

"""
Read and write initialization data to the SWMM INI file (epaswmm5.ini)
as well as for the current project's INI file.                                             }

Based on Uinifile.pas by L. Rossman, last updated 08/05/15 (5.1.010)
"""

DefGraphOptions = {
    "View3D"            : False,
    "Percent3D"         : 25,
    "PanelColor"        : Qt.white,
    "BackColor"         : Qt.white,
    "BackGradColor"     : Qt.white,
    "LegendPosition"    : 2,
    "LegendColor"       : Qt.white,
    "LegendWidth"       : 20,
    "LegendTransparent" : True,
    "LegendFramed"      : True,
    "LegendVisible"     : False,
    "AxisGridStyle"     : (1, 1, 0),
    "AxisGridColor"     : Qt.gray,
    "LineVisible"       : (True, True, True, True, True, False),
    "LineStyle"         : (0, 0, 0, 0, 0, 0),
    "LineColor"         : (Qt.red, Qt.blue, Qt.magenta, Qt.green, Qt.gray, Qt.cyan),
    "LineWidth"         : (2, 2, 2, 2, 2, 2),
    "PointVisible"      : (False, False, False, False, False, True),
    "PointStyle"        : (0, 0, 0, 0, 0, 0),
    "PointColor"        : (Qt.red, Qt.blue, Qt.magenta, Qt.green, Qt.gray, Qt.cyan),
    "PointSize"         : (3, 3, 3, 3, 3, 3),
    "TitleFontColor"    : Qt.blue,
    "TitleFontName"     : 'Arial',
    "AxisFontName"      : 'Arial',
    "TitleFontSize"     : 12,
    "AxisFontSize"      : 8,
    "TitleFontBold"     : True,
    "TitleFontItalic"   : False,
    "AxisFontBold"      : False,
    "AxisFontItalic"    : False,
    "AreaFillColor"     : Qt.blue,
    "AreaFillStyle"     : "Solid",
    "LabelsVisible"     : True,
    "LabelsTransparent" : False,
    "LabelsArrows"      : False,
    "LabelsBackColor"   : Qt.yellow,
    "DateTimeFormat"    : '',
    "AxisInverted"      : False}


DefProfileOptions = {
    "ConduitColor"      : Qt.white,
    "WaterColor"        : Qt.cyan,
    "LabelsOnAxis"      : True,
    "LabelsOnPlot"      : False,
    "LabelsArrowLength" : 10,
    "LabelsFontSize"    : 8}


# Program preferences

StyleName      = "Windows"
FontName       = "Arial"
LargeFonts     = False               # Dialogs use large fonts
BoldFonts      = False               # Dialogs use bold fonts
Blinking       = True                # Map hilighter blinks
FlyOvers       = True                # Flyover map labels
AutoBackup     = False               # Auto project file backup
ConfirmDelete  = True                # Confirm object deletions
AutoLength     = False               # Automatically computes pipe length
AutoSave       = False               # Auto saves results to disk
RptElapsedTime = True                # Elapsed time is default for reporting
TabDelimited   = False               # Tab separated fields in project file


def InitMapLegends():
    """ Assign default values to map legends. """
    pass
#     DefLegendColor = [$FF0000, $FFFF00, $FF00, $FFFF, $FF]
#     # Assign default values to legend colors
#     for I = 0 to MAXINTERVALS:
#         MapSubcatchColor[I] = DefLegendColor[I]
#         MapNodeColor[I] = DefLegendColor[I]
#         MapLinkColor[I] = DefLegendColor[I]
#
#     # Assign defaults to legend intervals for subcatchment variables
#     for I = 0 to SUBCATCHVIEWS:
#         with SubcatchLegend[I]:
#             Nintervals = MAXINTERVALS
#             ViewVar = I
#             LType = SUBCATCHMENTS
#             for J = 1 to Nintervals:
#                 Intervals[J] = SubcatchVariable[I].DefIntervals[J]
#
#     # Assign defaults to legend intervals for node variables
#     for I = 0 to NODEVIEWS:
#         with NodeLegend[I]:
#             Nintervals = MAXINTERVALS
#             ViewVar = I
#             LType = NODES
#             for J = 1 to Nintervals:
#                 Intervals[J] = NodeVariable[I].DefIntervals[J]
#
#     # Assign defaults to legend intervals for link variables
#     for I = 0 to LINKVIEWS:
#         with LinkLegend[I]:
#             Nintervals = MAXINTERVALS
#             ViewVar = I
#             LType = LINKS
#             for J = 1 to Nintervals:
#                 Intervals[J] = LinkVariable[I].DefIntervals[J]

# def CheckGraphSeriesOptions(I)
# """ Check for valid graph options for data series I """
#     with GraphOptions:
#         if (not LineVisible[I]) and (not PointVisible[I]):
#                 LineVisible[I] = True
#         if (LineStyle[I] < 0) or (LineStyle[I] > 4):
#         LineStyle[I] = DefGraphOptions.LineStyle[I]
#         if LineWidth[I] < 1:
#         LineWidth[I] = DefGraphOptions.LineWidth[I]
#         if (PointStyle[I] < 0) or (PointStyle[I] > 8):
#         PointStyle[I] = DefGraphOptions.PointStyle[I]
#         if PointSize[I] < 1:
#         PointSize[I] = DefGraphOptions.PointSize[I]


def ReadIniFile(session):
    """
        Read map settings, program preferences, current directories,
        and most-recently-used file list from the EPASWMM5.INI file.
    """

    # Initialize graph options with factory settings
    GraphOptions = DefGraphOptions.copy()
    ProfileOptions = DefProfileOptions.copy()

    # Create the .INI file object
#     with TIniFile.Create(IniFileDir + INIFILE):
#         # Retrieve Graph Options
#         with GraphOptions:
#             View3D = ReadBool('Graph', 'View3D', View3D)
#             Percent3D = ReadInteger('Graph', 'Percent3D', Percent3D)
#             PanelColor = ReadInteger('Graph', 'PanelColor', PanelColor)
#             BackColor = ReadInteger('Graph', 'BackColor', BackColor)
#             BackGradColor = ReadInteger('Graph', 'BackGradColor', BackGradColor)
#             LegendPosition = ReadInteger('Graph', 'LegendPosition', LegendPosition)
#             LegendColor = ReadInteger('Graph', 'LegendColor', LegendColor)
#             LegendWidth = ReadInteger('Graph', 'LegendWidth', LegendWidth)
#             LegendFramed = ReadBool('Graph', 'LegendFramed', LegendFramed)
#             LegendTransparent = ReadBool('Graph', 'LegendTransparent', LegendTransparent)
#             LegendVisible = ReadBool('Graph', 'LegendVisible', LegendVisible)
#             AxisGridStyle[0] = ReadInteger('Graph', 'X-AxisGrid', AxisGridStyle[0])
#             AxisGridStyle[1] = ReadInteger('Graph', 'Y-AxisGrid', AxisGridStyle[1])
#             for I = 0 to MAXSERIES:
#                 S = IntToStr(I)
#                 LineVisible[I] = ReadBool('Graph', 'LineVisible' + S, LineVisible[I])
#                 LineStyle[I] = ReadInteger('Graph', 'LineStyle' + S, LineStyle[I])
#                 LineColor[I] = ReadInteger('Graph', 'LineColor' + S, LineColor[I])
#                 LineWidth[I] = ReadInteger('Graph', 'LineWidth' + S, LineWidth[I])
#                 PointVisible[I] = ReadBool('Graph', 'PointVisible' + S, PointVisible[I])
#                 PointStyle[I] = ReadInteger('Graph', 'PointStyle' + S, PointStyle[I])
#                 PointColor[I] = ReadInteger('Graph', 'PointColor' + S, PointColor[I])
#                 PointSize[I] = ReadInteger('Graph', 'PointSize' + S, PointSize[I])
#                 CheckGraphSeriesOptions(I)
#             TitleFontColor = ReadInteger('Graph', 'TitleFontColor', TitleFontColor)
#             TitleFontName = ReadString('Graph', 'TitleFontName', TitleFontName)
#             TitleFontSize = ReadInteger('Graph', 'TitleFontSize', TitleFontSize)
#             TitleFontBold = ReadBool('Graph', 'TitleFontBold', TitleFontBold)
#             TitleFontItalic = ReadBool('Graph', 'TitleFontItalic', TitleFontItalic)
#             AxisFontName = ReadString('Graph', 'AxisFontName', AxisFontName)
#             AxisFontSize = ReadInteger('Graph', 'AxisFontSize', AxisFontSize)
#             AxisFontBold = ReadBool('Graph', 'AxisFontBold', AxisFontBold)
#             AxisFontItalic = ReadBool('Graph', 'AxisFontItalic', AxisFontItalic)
#             AreaFillColor = ReadInteger('Graph', 'AreaFillColor', AreaFillColor)
#             AreaFillStyle = TBrushStyle(ReadInteger('Graph',
#                                                     'AreaFillStyle', Ord(AreaFillStyle)))
#             LabelsVisible = ReadBool('Graph', 'LabelsVisible', LabelsVisible)
#             LabelsTransparent = ReadBool('Graph', 'LabelsTransparent', LabelsTransparent)
#             LabelsArrows = ReadBool('Graph', 'LabelsArrows', LabelsArrows)
#             LabelsBackColor = ReadInteger('Graph', 'LabelsBackColor', LabelsBackColor)
#
#         # Retrieve Profile Plot options
#         with ProfileOptions:
#             ConduitColor = ReadInteger('ProfilePlot', 'ConduitColor', ConduitColor)
#             WaterColor = ReadInteger('ProfilePlot', 'WaterColor', WaterColor)
#             LabelsOnAxis = ReadBool('ProfilePlot', 'LabelsOnAxis', LabelsOnAxis)
#             LabelsOnPlot = ReadBool('ProfilePlot', 'LabelsOnPlot', LabelsOnPlot)
#             LabelsArrowLength = ReadInteger('ProfilePlot', 'LabelsArrowLength',
#                                                      LabelsArrowLength)
#
#         # Retrieve directory names
#         S = ReadString('Directories', 'DataDir', ProjectDir)
#         if (DirectoryExists(S)):
#             ProjectDir = S
#             SetCurrentDir(S)
# {
#         S = ReadString('Directories', 'TempDir', TempDir)
#         if S[Length(S)] <> '\': S = S + '\'
#         if (DirectoryExists(S)): TempDir = S
# }
#         # Retrieve general preferences
#         FontName = ReadString('Preferences', 'FontName', 'Arial')
#         LargeFonts = ReadBool('Preferences', 'LargeFonts', False)
#         BoldFonts = ReadBool('Preferences', 'BoldFonts', False)
#         Blinking = ReadBool('Preferences', 'Blinking', True)
#         FlyOvers = ReadBool('Preferences', 'FlyOvers', True)
#         AutoBackup = ReadBool('Preferences', 'AutoBackup', False)
#         ConfirmDelete = ReadBool('Preferences', 'ConfirmDelete', True)
#         AutoSave = ReadBool('Preferences', 'AutoSave', False)
#         RptElapsedTime = ReadBool('Preferences', 'RptElapsedTime', True)
#         TabDelimited = ReadBool('Preferences', 'TabDelimited', False)
#
#         # Retrieve MRU file names
#         MainForm.MRUList.Clear
#         for I = 0 to Uglobals.MAXMRUINDEX:
#             MainForm.MRUList.Add(ReadString('MRU', IntToStr(I), ''))
#
#         # Retrieve placement parameters for the Property Editor form
#         with PropEditForm:
#             Top = (Screen.Height - Height) div 2
#             Left = (Screen.Width - Width) div 2
#             Left = ReadInteger('Property Editor', 'Left', Left)
#             Top    = ReadInteger('Property Editor', 'Top', Top)
#             Width = ReadInteger('Property Editor', 'Width', Width)
#             Height = ReadInteger('Property Editor', 'Height', Height)
#             if Width >= Screen.Width: Width = Screen.Width div 2
#             if Height >= Screen.Height: Height = Screen.Height
#             if Left + Width > Screen.Width: Left = Screen.Width - Width
#             if Top + Height > Screen.Height: Top = Screen.Height - Height
#             Editor.HeaderSplit = ReadInteger('Property Editor', 'HeaderSplit',
#                                                         Editor.HeaderSplit)
#
#         # Retrieve output variable display precision
#         for I = SUBCATCHOUTVAR1 to SUBCATCHVIEWS:
#             SubcatchUnits[I].Digits = ReadInteger('Display Precision', SubcatchVariable[I].Name, 2)
#         for I = NODEOUTVAR1 to NODEVIEWS:
#             NodeUnits[I].Digits = ReadInteger('Display Precision', NodeVariable[I].Name, 2)
#         for I = LINKOUTVAR1 to LINKVIEWS:
#             LinkUnits[I].Digits = ReadInteger('Display Precision', LinkVariable[I].Name, 2)


def SaveIniFile():
    """
        Save map settings, program preferences, current directories,
        and most-recently-used file list to the EPASWMM5.INI file.
    """
    # Create the .INI file object
    # with TIniFile.Create(IniFileDir + INIFILE):
    #     # Save Graph options
    #     with GraphOptions:
    #         WriteBool('Graph', 'View3D', View3D)
    #         WriteInteger('Graph', 'Percent3D', Percent3D)
    #         WriteInteger('Graph', 'PanelColor', PanelColor)
    #         WriteInteger('Graph', 'BackColor', BackColor)
    #         WriteInteger('Graph', 'BackGradColor', BackGradColor)
    #         WriteInteger('Graph', 'LegendPosition', LegendPosition)
    #         WriteInteger('Graph', 'LegendColor', LegendColor)
    #         WriteInteger('Graph', 'LegendWidth', LegendWidth)
    #         WriteBool('Graph', 'LegendFramed', LegendFramed)
    #         WriteBool('Graph', 'LegendTransparent', LegendTransparent)
    #         WriteBool('Graph', 'LegendVisible', LegendVisible)
    #         WriteInteger('Graph', 'X-AxisGrid', AxisGridStyle[0])
    #         WriteInteger('Graph', 'Y-AxisGrid', AxisGridStyle[1])
    #         for I = 0 to MAXSERIES:
    #             S = IntToStr(I)
    #             WriteBool('Graph', 'LineVisible' + S, LineVisible[I])
    #             WriteInteger('Graph', 'LineStyle' + S, LineStyle[I])
    #             WriteInteger('Graph', 'LineColor' + S, LineColor[I])
    #             WriteInteger('Graph', 'LineWidth' + S, LineWidth[I])
    #             WriteBool('Graph', 'PointVisible' + S, PointVisible[I])
    #             WriteInteger('Graph', 'PointStyle' + S, PointStyle[I])
    #             WriteInteger('Graph', 'PointColor' + S, PointColor[I])
    #             WriteInteger('Graph', 'PointSize' + S, PointSize[I])
    #         WriteInteger('Graph', 'TitleFontColor',TitleFontColor)
    #         WriteString('Graph', 'TitleFontName', TitleFontName)
    #         WriteInteger('Graph', 'TitleFontSize', TitleFontSize)
    #         WriteBool('Graph', 'TitleFontBold', TitleFontBold)
    #         WriteBool('Graph', 'TitleFontItalic', TitleFontItalic)
    #         WriteString('Graph', 'AxisFontName', AxisFontName)
    #         WriteInteger('Graph', 'AxisFontSize', AxisFontSize)
    #         WriteBool('Graph', 'AxisFontBold', AxisFontBold)
    #         WriteBool('Graph', 'AxisFontItalic', AxisFontItalic)
    #         WriteInteger('Graph', 'AreaFillColor', AreaFillColor)
    #         WriteInteger('Graph', 'AreaFillStyle', Ord(AreaFillStyle))
    #         WriteBool('Graph', 'LabelsVisible', LabelsVisible)
    #         WriteBool('Graph', 'LabelsTransparent', LabelsTransparent)
    #         WriteBool('Graph', 'LabelsArrows', LabelsArrows)
    #         WriteInteger('Graph', 'LabelsBackColor', LabelsBackColor)
    #
    #     # Save Profile Plot options
    #     with ProfileOptions:
    #         WriteInteger('ProfilePlot', 'ConduitColor', ConduitColor)
    #         WriteInteger('ProfilePlot', 'WaterColor', WaterColor)
    #         WriteBool('ProfilePlot', 'LabelsOnAxis', LabelsOnAxis)
    #         WriteBool('ProfilePlot', 'LabelsOnPlot', LabelsOnPlot)
    #         WriteInteger('ProfilePlot', 'LabelsArrowLength', LabelsArrowLength)
    #
    #     # Save directory names
    #     WriteString('Directories', 'DataDir', ProjectDir)
    #     WriteString('Directories', 'TempDir', TempDir)
    #
    #     # Save general program preferences
    #     WriteBool('Preferences', 'LargeFonts', LargeFonts)
    #     WriteBool('Preferences', 'BoldFonts', BoldFonts)
    #     WriteString('Preferences', 'StyleName', StyleName)
    #     WriteBool('Preferences', 'Blinking', Blinking)
    #     WriteBool('Preferences', 'FlyOvers', FlyOvers)
    #     WriteBool('Preferences', 'AutoBackup', AutoBackup)
    #     WriteBool('Preferences', 'ConfirmDelete', ConfirmDelete)
    #     WriteBool('Preferences', 'AutoSave', AutoSave)
    #     WriteBool('Preferences', 'RptElapsedTime', RptElapsedTime)
    #     WriteBool('Preferences', 'TabDelimited', TabDelimited)
    #
    #     # Save MRU file names
    #     for I = 0 to MainForm.MRUList.Count-1:
    #         WriteString('MRU', IntToStr(I), MainForm.MRUList[I])
    #
    #     # Save Property Editor form's position
    #     with PropEditForm:
    #         WriteInteger('Property Editor', 'Left', Left)
    #         WriteInteger('Property Editor', 'Top', Top)
    #         WriteInteger('Property Editor', 'Width', Width)
    #         WriteInteger('Property Editor', 'Height', Height)
    #         WriteInteger('Property Editor', 'HeaderSplit', Editor.HeaderSplit)
    #
    #     # Save output variable display precision
    #     for I = SUBCATCHOUTVAR1 to SUBCATCHVIEWS:
    #          WriteInteger('Display Precision', SubcatchVariable[I].Name,
    #                                     SubcatchUnits[I].Digits)
    #     for I = NODEOUTVAR1 to NODEVIEWS:
    #          WriteInteger('Display Precision', NodeVariable[I].Name,
    #                                  NodeUnits[I].Digits)
    #     for I = LINKOUTVAR1 to LINKVIEWS:
    #          WriteInteger('Display Precision', LinkVariable[I].Name,
    #                                     LinkUnits[I].Digits)


def LoadDefaultsFromFile(theIniFile):
    """
        Read default property values from theIniFile, which can be either
        the EPASWMM5.INI file or a project ini file.
    """
#     with theIniFile:
#         # Retrieve default ID labeling prefixes & increment
#         Project.IDIncrement = ReadInteger('Labels', 'Increment', Project.IDIncrement)
#         for I = 0 to MAXCLASS:
#             if Project.IsVisual(I): Project.IDPrefix[I] =
#                 ReadString('Labels', ObjectLabels[I], Project.IDPrefix[I])
#
#         # Retrieve default properties
#         with Project:
#             DefProp[SUBCATCH].Data[SUBCATCH_AREA_INDEX] =
#                 ReadString('Defaults', 'SUBCATCH_AREA',
#                     DefProp[SUBCATCH].Data[SUBCATCH_AREA_INDEX])
#             DefProp[SUBCATCH].Data[SUBCATCH_WIDTH_INDEX] =
#                     ReadString('Defaults', 'SUBCATCH_WIDTH',
#                         DefProp[SUBCATCH].Data[SUBCATCH_WIDTH_INDEX])
#             DefProp[SUBCATCH].Data[SUBCATCH_SLOPE_INDEX] =
#                 ReadString('Defaults', 'SUBCATCH_SLOPE',
#                     DefProp[SUBCATCH].Data[SUBCATCH_SLOPE_INDEX])
#             DefProp[SUBCATCH].Data[SUBCATCH_IMPERV_INDEX] =
#                 ReadString('Defaults', 'SUBCATCH_IMPERV',
#                     DefProp[SUBCATCH].Data[SUBCATCH_IMPERV_INDEX])
#             DefProp[SUBCATCH].Data[SUBCATCH_IMPERV_N_INDEX] =
#                 ReadString('Defaults', 'SUBCATCH_IMPERV_N',
#                     DefProp[SUBCATCH].Data[SUBCATCH_IMPERV_N_INDEX])
#             DefProp[SUBCATCH].Data[SUBCATCH_PERV_N_INDEX] =
#                 ReadString('Defaults', 'SUBCATCH_PERV_N',
#                     DefProp[SUBCATCH].Data[SUBCATCH_PERV_N_INDEX])
#             DefProp[SUBCATCH].Data[SUBCATCH_IMPERV_DS_INDEX] =
#                 ReadString('Defaults', 'SUBCATCH_IMPERV_DS',
#                     DefProp[SUBCATCH].Data[SUBCATCH_IMPERV_DS_INDEX])
#             DefProp[SUBCATCH].Data[SUBCATCH_PERV_DS_INDEX] =
#                 ReadString('Defaults', 'SUBCATCH_PERV_DS',
#                     DefProp[SUBCATCH].Data[SUBCATCH_PERV_DS_INDEX])
#             DefProp[SUBCATCH].Data[SUBCATCH_PCTZERO_INDEX] =
#                 ReadString('Defaults', 'SUBCATCH_PCTZERO',
#                     DefProp[SUBCATCH].Data[SUBCATCH_PCTZERO_INDEX])
#
#             S = ReadString('Defaults', 'NODE_INVERT',
#                          DefProp[JUNCTION].Data[NODE_INVERT_INDEX])
#             for J = JUNCTION to STORAGE:
#                 DefProp[J].Data[NODE_INVERT_INDEX] = S
#
#             S = ReadString('Defaults', 'NODE_DEPTH',
#                          DefProp[JUNCTION].Data[JUNCTION_MAX_DEPTH_INDEX])
#             DefProp[JUNCTION].Data[JUNCTION_MAX_DEPTH_INDEX] = S
#             DefProp[DIVIDER].Data[DIVIDER_MAX_DEPTH_INDEX] = S
#             DefProp[STORAGE].Data[STORAGE_MAX_DEPTH_INDEX] = S
#
#             S = ReadString('Defaults', 'PONDED_AREA',
#                          DefProp[JUNCTION].Data[JUNCTION_PONDED_AREA_INDEX])
#             DefProp[JUNCTION].Data[JUNCTION_PONDED_AREA_INDEX] = S
#             DefProp[DIVIDER].Data[DIVIDER_PONDED_AREA_INDEX] = S
#             DefProp[STORAGE].Data[STORAGE_PONDED_AREA_INDEX] = S
#
#             DefProp[CONDUIT].Data[CONDUIT_LENGTH_INDEX] =
#                     ReadString('Defaults', 'CONDUIT_LENGTH',
#                         DefProp[CONDUIT].Data[CONDUIT_LENGTH_INDEX])
#             DefProp[CONDUIT].Data[CONDUIT_SHAPE_INDEX] =
#                     ReadString('Defaults', 'CONDUIT_SHAPE',
#                         DefProp[CONDUIT].Data[CONDUIT_SHAPE_INDEX])
#             DefProp[CONDUIT].Data[CONDUIT_GEOM1_INDEX] =
#                     ReadString('Defaults', 'CONDUIT_GEOM1',
#                         DefProp[CONDUIT].Data[CONDUIT_GEOM1_INDEX])
#             DefProp[CONDUIT].Data[CONDUIT_GEOM2_INDEX] =
#                     ReadString('Defaults', 'CONDUIT_GEOM2',
#                         DefProp[CONDUIT].Data[CONDUIT_GEOM2_INDEX])
#             DefProp[CONDUIT].Data[CONDUIT_GEOM3_INDEX] =
#                     ReadString('Defaults', 'CONDUIT_GEOM3',
#                         DefProp[CONDUIT].Data[CONDUIT_GEOM3_INDEX])
#             DefProp[CONDUIT].Data[CONDUIT_GEOM4_INDEX] =
#                     ReadString('Defaults', 'CONDUIT_GEOM4',
#                         DefProp[CONDUIT].Data[CONDUIT_GEOM4_INDEX])
#             DefProp[CONDUIT].Data[CONDUIT_ROUGHNESS_INDEX] =
#                     ReadString('Defaults', 'CONDUIT_ROUGHNESS',
#                         DefProp[CONDUIT].Data[CONDUIT_ROUGHNESS_INDEX])
#
#             DefProp[OPTION].Data[FLOW_UNITS_INDEX] =
#                     ReadString('Defaults', 'FLOW_UNITS',
#                         DefProp[OPTION].Data[FLOW_UNITS_INDEX])
#             DefProp[OPTION].Data[INFILTRATION_INDEX] =
#                     ReadString('Defaults', 'INFILTRATION',
#                         DefProp[OPTION].Data[INFILTRATION_INDEX])
#             DefProp[OPTION].Data[ROUTING_MODEL_INDEX] =
#                     ReadString('Defaults', 'ROUTING_MODEL',
#                         DefProp[OPTION].Data[ROUTING_MODEL_INDEX])
#             DefProp[OPTION].Data[FORCE_MAIN_EQN_INDEX] =
#                     ReadString('Defaults', 'FORCE_MAIN_EQUATION',
#                         DefProp[OPTION].Data[FORCE_MAIN_EQN_INDEX])
#             DefProp[OPTION].Data[LINK_OFFSETS_INDEX] =
#                     ReadString('Defaults', 'LINK_OFFSETS',
#                         DefProp[OPTION].Data[LINK_OFFSETS_INDEX])
#
#             with Project.Options:
#                 Data[FLOW_UNITS_INDEX]        = DefProp[OPTION].Data[FLOW_UNITS_INDEX]
#                 Data[INFILTRATION_INDEX]    = DefProp[OPTION].Data[INFILTRATION_INDEX]
#                 Data[ROUTING_MODEL_INDEX] = DefProp[OPTION].Data[ROUTING_MODEL_INDEX]
#                 Data[FORCE_MAIN_EQN_INDEX] = DefProp[OPTION].Data[FORCE_MAIN_EQN_INDEX]
#                 Data[LINK_OFFSETS_INDEX]     = DefProp[OPTION].Data[LINK_OFFSETS_INDEX]
#
# ##    Modified for release 5.1.0101.    ##                                                                         #(5.1.010)
#             with Project.Options:
#                 if SameText(Data[INFILTRATION_INDEX], InfilOptions[HORTON_INFIL])
#                 or SameText(Data[INFILTRATION_INDEX], InfilOptions[MOD_HORTON_INFIL])
#              : CopyStringArray(DefHortonInfil, TmpInfil)
#                 else if SameText(Data[INFILTRATION_INDEX], InfilOptions[GREEN_AMPT_INFIL])
#                 or SameText(Data[INFILTRATION_INDEX], InfilOptions[MOD_GREEN_AMPT_INFIL])
#              : CopyStringArray(DefGreenAmptInfil, TmpInfil)
#                 else if SameText(Data[INFILTRATION_INDEX], InfilOptions[CURVE_NUMBER_INFIL])
#              : CopyStringArray(DefCurveNumInfil, TmpInfil)
# ##
#             for I = 0 to MAXINFILPROPS:
#                 Uproject.DefInfil[I] = ReadString('Defaults', 'INFIL_PARAM' +
#                                                                 IntToStr(I+1), TmpInfil[I])
#                 if Length(Trim(Uproject.DefInfil[I])) == 0
#              : Uproject.DefInfil[I] = TmpInfil[I]
#     finally


def SaveDefaultsToFile(theIniFile):
    """
        Save default property values to theIniFile, which can be either
        the EPASWMM5.INI file or a project ini file.
    """
    with theIniFile:
        pass
        # Save default ID labeling prefixes & increment
        # WriteInteger('Labels', 'Increment', Project.IDIncrement)
        # for I = 0 to MAXCLASS:
        #     if Project.IsVisual(I):
        #         WriteString('Labels', ObjectLabels[I], Project.IDPrefix[I])
        #
        # # Save default properties
        # with Project:
        #     WriteString('Defaults', 'SUBCATCH_AREA',
        #         DefProp[SUBCATCH].Data[SUBCATCH_AREA_INDEX])
        #     WriteString('Defaults', 'SUBCATCH_WIDTH',
        #         DefProp[SUBCATCH].Data[SUBCATCH_WIDTH_INDEX])
        #     WriteString('Defaults', 'SUBCATCH_SLOPE',
        #         DefProp[SUBCATCH].Data[SUBCATCH_SLOPE_INDEX])
        #     WriteString('Defaults', 'SUBCATCH_IMPERV',
        #         DefProp[SUBCATCH].Data[SUBCATCH_IMPERV_INDEX])
        #     WriteString('Defaults', 'SUBCATCH_IMPERV_N',
        #         DefProp[SUBCATCH].Data[SUBCATCH_IMPERV_N_INDEX])
        #     WriteString('Defaults', 'SUBCATCH_PERV_N',
        #         DefProp[SUBCATCH].Data[SUBCATCH_PERV_N_INDEX])
        #     WriteString('Defaults', 'SUBCATCH_IMPERV_DS',
        #         DefProp[SUBCATCH].Data[SUBCATCH_IMPERV_DS_INDEX])
        #     WriteString('Defaults', 'SUBCATCH_PERV_DS',
        #         DefProp[SUBCATCH].Data[SUBCATCH_PERV_DS_INDEX])
        #     WriteString('Defaults', 'SUBCATCH_PCTZERO',
        #         DefProp[SUBCATCH].Data[SUBCATCH_PCTZERO_INDEX])
        #
        #     WriteString('Defaults', 'NODE_INVERT',
        #         DefProp[JUNCTION].Data[NODE_INVERT_INDEX])
        #     WriteString('Defaults', 'NODE_DEPTH',
        #         DefProp[JUNCTION].Data[JUNCTION_MAX_DEPTH_INDEX])
        #     WriteString('Defaults', 'PONDED_AREA',
        #         DefProp[JUNCTION].Data[JUNCTION_PONDED_AREA_INDEX])
        #
        #     WriteString('Defaults', 'CONDUIT_LENGTH',
        #         DefProp[CONDUIT].Data[CONDUIT_LENGTH_INDEX])
        #     WriteString('Defaults', 'CONDUIT_SHAPE',
        #         DefProp[CONDUIT].Data[CONDUIT_SHAPE_INDEX])
        #     WriteString('Defaults', 'CONDUIT_GEOM1',
        #         DefProp[CONDUIT].Data[CONDUIT_GEOM1_INDEX])
        #     WriteString('Defaults', 'CONDUIT_GEOM2',
        #         DefProp[CONDUIT].Data[CONDUIT_GEOM2_INDEX])
        #     WriteString('Defaults', 'CONDUIT_GEOM3',
        #         DefProp[CONDUIT].Data[CONDUIT_GEOM3_INDEX])
        #     WriteString('Defaults', 'CONDUIT_GEOM4',
        #         DefProp[CONDUIT].Data[CONDUIT_GEOM4_INDEX])
        #     WriteString('Defaults', 'CONDUIT_ROUGHNESS',
        #         DefProp[CONDUIT].Data[CONDUIT_ROUGHNESS_INDEX])
        #
        #     WriteString('Defaults', 'FLOW_UNITS',
        #         DefProp[OPTION].Data[FLOW_UNITS_INDEX])
        #     WriteString('Defaults', 'INFILTRATION',
        #         DefProp[OPTION].Data[INFILTRATION_INDEX])
        #     WriteString('Defaults', 'ROUTING_MODEL',
        #         DefProp[OPTION].Data[ROUTING_MODEL_INDEX])
        #     WriteString('Defaults', 'FORCE_MAIN_EQUATION',
        #         DefProp[OPTION].Data[FORCE_MAIN_EQN_INDEX])
        #     WriteString('Defaults', 'LINK_OFFSETS',
        #         DefProp[OPTION].Data[LINK_OFFSETS_INDEX])
        #     for I = 0 to MAXINFILPROPS:
        #         WriteString('Defaults', 'INFIL_PARAM' + IntToStr(I+1),
        #             Uproject.DefInfil[I])


def ReadDefaults():
    """
        Initializes default object properties and reads in previously saved
        default properties from the EPASWMM5.INI file.
    """
    # Use default settings for map legends
    InitMapLegends

    # # Copy defaults (e.g., DefJunction)
    # # to current defaults (e.g., DefProp[JUNCTION].Data)
    # with Project:
    #     Uutils.CopyStringArray(DefRaingage,     DefProp[RAINGAGE].Data)
    #     Uutils.CopyStringArray(DefSubcatch,     DefProp[SUBCATCH].Data)
    #     Uutils.CopyStringArray(DefJunction,     DefProp[JUNCTION].Data)
    #     Uutils.CopyStringArray(DefOutfall,        DefProp[OUTFALL].Data)
    #     Uutils.CopyStringArray(DefDivider,        DefProp[DIVIDER].Data)
    #     Uutils.CopyStringArray(DefStorage,        DefProp[STORAGE].Data)
    #     Uutils.CopyStringArray(DefConduit,        DefProp[CONDUIT].Data)
    #     Uutils.CopyStringArray(DefPump,             DefProp[PUMP].Data)
    #     Uutils.CopyStringArray(DefOrifice,        DefProp[ORIFICE].Data)
    #     Uutils.CopyStringArray(DefWeir,             DefProp[WEIR].Data)
    #     Uutils.CopyStringArray(DefOutlet,         DefProp[OUTLET].Data)
    #     Uutils.CopyStringArray(DefPollutant,    DefProp[POLLUTANT].Data)
    #     Uutils.CopyStringArray(DefOptions,        DefProp[OPTION].Data)
    #     Uutils.CopyStringArray(DefProp[OPTION].Data, Options.Data)
    #
    # # Assign defaults to ID label prefixes & ID increment
    # Project.IDIncrement = 1
    # for I = 0 to MAXCLASS do Project.IDPrefix[I] = ''
    #
    # # Read defaults from the EPASWMM5.INI file
    # theIniFile = TIniFile.Create(IniFileDir + INIFILE)
    # with theIniFile:
    # try
    #     LoadDefaultsFromFile(theIniFile)
    # finally
    #     Free
    # ResultsSaved = False
    # UpdateFlag = False
    # Uupdate.UpdateUnits


def SaveDefaults():
    """ Save default properties to the EPASWMM5.INI file. """
    pass
    # theIniFile = TIniFile.Create(IniFileDir + INIFILE)
    # with theIniFile:
    # try
    #     SaveDefaultsToFile(theIniFile)
    # finally
    #     Free


##    Re-written for release 5.1.002.    ##                                                                        #(5.1.002)
def ReadMainFormSize():
    """ Read main form's position and size from the EPASWMM5.INI file. """
    pass
    # with TIniFile.Create(IniFileDir + INIFILE):
    # try
    #     with MainForm:
    #         Top = (Screen.Height - Height) div 2
    #         Left = (Screen.Width - Width) div 2
    #         T = ReadInteger('MainForm', 'Top', Top)
    #         L = ReadInteger('MainForm', 'Left', Left)
    #         W = ReadInteger('MainForm', 'Width', Width)
    #         H = ReadInteger('MainForm', 'Height', Height)
    #
    #         if T + H > Screen.Height:
    #             T = 0
    #             if H > Screen.Height: H = Screen.Height
    #         if L + W > Screen.Width:
    #             L = 0
    #             if W > Screen.Width: W = Screen.Width
    #         SetBounds(L, T, W, H)
    #
    #         BrowserPageControl.Width =
    #             ReadInteger('BrowserPanel', 'Width', BrowserPageControl.Width)
    #         H = ReadInteger('BrowserPanel', 'Split', ItemsPanel.Height)
    #         if (H < MulDiv(BrowserPageControl.Height, 9, 10))
    #         and (H > BrowserPageControl.Height div 10)
    #      : ItemsPanel.Height = H
#
# ##    Added for release 5.1.007.    ##                                                                                 #(5.1.007)
#             with StdToolbar:
#                 Visible = ReadBool('StdToolbar', 'Visible', Visible)
#                 Left = ReadInteger('StdToolbar', 'Left', Left)
#                 Top = ReadInteger('StdToolbar', 'Top', Top)
#             with MapToolbar:
#                 Visible = ReadBool('MapToolbar', 'Visible', Visible)
#                 Left = ReadInteger('MapToolbar', 'Left', Left)
#                 Top = ReadInteger('MapToolbar', 'Top', Top)
#             with ObjToolbar:
#                 Visible = ReadBool('ObjectToolbar', 'Visible', Visible)
#                 Left = ReadInteger('ObjectToolbar', 'Left', Left)
#                 Top = ReadInteger('ObjectToolbar', 'Top', Top)
#
#     finally
#         Free


##    Re-written for release 5.1.002.    ##                                                                        #(5.1.002)
def SaveMainFormSize():
    """ Save main form's position and size to the EPASWMM5.INI file. """
    pass
#     with TIniFile.Create(IniFileDir + INIFILE):
#     try
#         with MainForm:
#             WriteInteger('MainForm', 'Left', Left)
#             WriteInteger('MainForm', 'Top', Top)
#             WriteInteger('MainForm', 'Width', Width)
#             WriteInteger('MainForm', 'Height', Height)
#             WriteInteger('BrowserPanel', 'Width', BrowserPageControl.Width)
#             WriteInteger('BrowserPanel', 'Split', ItemsPanel.Height)
#
# ##    Added for release 5.1.007.    ##                                                                                 #(5.1.007)
#             WriteBool('StdToolbar', 'Visible', StdToolbar.Visible)
#             WriteInteger('StdToolbar', 'Left', StdToolbar.Left)
#             WriteInteger('StdToolbar', 'Top', StdToolbar.Top)
#             WriteBool('MapToolbar', 'Visible', MapToolbar.Visible)
#             WriteInteger('MapToolbar', 'Left', MapToolbar.Left)
#             WriteInteger('MapToolbar', 'Top', MapToolbar.Top)
#             WriteBool('ObjectToolbar', 'Visible', ObjToolbar.Visible)
#             WriteInteger('ObjectToolbar', 'Left', ObjToolbar.Left)
#             WriteInteger('ObjectToolbar', 'Top', ObjToolbar.Top)
#
#     finally
#         Free


def ReadProjIniFile(Fname):
    """ Read previously saved options from the project's INI file. """
    pass
    # theIniFile = TIniFile.Create(Fname)
    # with theIniFile:
    # try:
    #     # Read map display options
    #     with MapForm.Map.Options:
    #         ShowGageIDs = ReadBool('Map', 'ShowGageIDs', ShowGageIDs)
    #         ShowSubcatchIDs = ReadBool('Map', 'ShowSubcatchIDs', ShowSubcatchIDs)
    #         ShowSubcatchValues = ReadBool('Map', 'ShowSubcatchValues', ShowSubcatchValues)
    #         ShowSubcatchLinks = ReadBool('Map', 'ShowSubcatchLinks', ShowSubcatchLinks)
    #
    #         ShowNodeIDs = ReadBool('Map', 'ShowNodeIDs', ShowNodeIDs)
    #         ShowNodeValues = ReadBool('Map', 'ShowNodeValues', ShowNodeValues)
    #         ShowNodesBySize = ReadBool('Map', 'ShowNodesBySize', ShowNodesBySize)
    #         ShowNodeBorder = ReadBool('Map', 'ShowNodeBorder', ShowNodeBorder)
    #
    #         ShowLinkIDs = ReadBool('Map', 'ShowLinkIDs', ShowLinkIDs)
    #         ShowLinkValues = ReadBool('Map', 'ShowLinkValues', ShowLinkValues)
    #         ShowLinksBySize = ReadBool('Map', 'ShowLinksBySize', ShowLinksBySize)
    #         ShowLinkBorder = ReadBool('Map', 'ShowLinkBorder', ShowLinkBorder)
    #
    #         ShowGages = ReadBool('Map', 'ShowGages', ShowGages)
    #         ShowSubcatchs = ReadBool('Map', 'ShowSubcatchs', ShowSubcatchs)
    #         ShowNodes = ReadBool('Map', 'ShowNodes', ShowNodes)
    #         ShowLinks = ReadBool('Map', 'ShowLinks', ShowLinks)
    #         ShowNodeSymbols = ReadBool('Map', 'ShowNodeSymbols', ShowNodeSymbols)
    #         ShowLinkSymbols = ReadBool('Map', 'ShowLinkSymbols', ShowLinkSymbols)
    #
    #         ShowLabels = ReadBool('Map', 'ShowLabels', ShowLabels)
    #         LabelsTranspar = ReadBool('Map', 'LabelsTranspar', LabelsTranspar)
    #         NotationTranspar = ReadBool('Map', 'NotationTranspar', NotationTranspar)
    #
    #         SubcatchFillStyle = ReadInteger('Map', 'SubcatchFillStyle', SubcatchFillStyle)
    #         SubcatchLineSize = ReadInteger('Map', 'SubcatchLineSize', SubcatchLineSize)
    #         SubcatchSnapTol = ReadInteger('Map', 'SubcatchSnapTol', SubcatchSnapTol)
    #         SubcatchSize = ReadInteger('Map', 'SubcatchSize', SubcatchSize)
    #         NodeSize = ReadInteger('Map', 'NodeSize', NodeSize)
    #         LinkSize = ReadInteger('Map', 'LinkSize', LinkSize)
    #         NotationSize = ReadInteger('Map', 'NotationSize', NotationSize)
    #
    #         ArrowStyle = TArrowStyle(ReadInteger('Map', 'ArrowStyle', Ord(ArrowStyle)))
    #         ArrowSize = ReadInteger('Map', 'ArrowSize', ArrowSize)
    #
    #         ColorIndex = ReadInteger('Map', 'ColorIndex', ColorIndex)
    #         NotationZoom = ReadInteger('Map', 'NotationZoom', NotationZoom)
    #         LabelZoom = ReadInteger('Map', 'LabelZoom', LabelZoom)
    #         SymbolZoom = ReadInteger('Map', 'SymbolZoom', SymbolZoom)
    #         ArrowZoom = ReadInteger('Map', 'ArrowZoom', ArrowZoom)
    #
    #     # Read backdrop image options
    #     with Mapform.Map.Backdrop:
    #         Visible = ReadBool('Backdrop', 'Visible', Visible)
    #         Watermark = ReadBool('Backdrop', 'Watermark', Watermark)
    #
    #     # Read legend colors & intervals
    #     N = ReadInteger('Legends', 'NumIntervals', MAXINTERVALS)
    #     for I = 0 to N:
    #         MapSubcatchColor[I] = ReadInteger('Legends', 'MapSubcatchColor' +
    #                                                          IntToStr(I), MapSubcatchColor[I])
    #     for I = 0 to N:
    #         MapNodeColor[I] = ReadInteger('Legends', 'MapNodeColor' + IntToStr(I),
    #                                                  MapNodeColor[I])
    #     for I = 0 to N:
    #         MapLinkColor[I] = ReadInteger('Legends', 'MapLinkColor' + IntToStr(I),
    #                                                  MapLinkColor[I])
    #
    #     for I = 1 to SUBCATCHVIEWS:
    #         S = ReadString('Legends', 'SubcatchLegend' + IntToStr(I), '')
    #         ExtractValues(S, 1, N, SubcatchLegend[I].Intervals)
    #     for I = 1 to NODEVIEWS:
    #         S = ReadString('Legends', 'NodeLegend' + IntToStr(I), '')
    #         ExtractValues(S, 1, N, NodeLegend[I].Intervals)
    #     for I = 1 to LINKVIEWS:
    #         S = ReadString('Legends', 'LinkLegend' + IntToStr(I), '')
    #         ExtractValues(S, 1, N, LinkLegend[I].Intervals)
    #
    #     # Retrieve default project properties from file
    #     LoadDefaultsFromFile(theIniFile)
    #     for I = 0 to MAXCLASS:
    #         Project.NextID[I] = ReadInteger('Labels', ObjectLabels[I] + '_NextID', 1)
    #
    #     # Read printed Page Layout info
    #     with PageLayout:
    #         LMargin = StrToFloat(ReadString('Page', 'LeftMargin', FloatToStr(LMargin)))
    #         RMargin = StrToFloat(ReadString('Page', 'RightMargin', FloatToStr(RMargin)))
    #         TMargin = StrToFloat(ReadString('Page', 'TopMargin', FloatToStr(TMargin)))
    #         BMargin = StrToFloat(ReadString('Page', 'BottomMargin', FloatToStr(BMargin)))
    #     with MainForm.PageSetupDialog:
    #         Header.Text            = ReadString('Page', 'HeaderText', Header.Text)
    #         Header.Alignment = TAlignment(ReadInteger('Page', 'HeaderAlignment',
    #                                                     Ord(Header.Alignment)))
    #         Header.Enabled     = ReadBool('Page', 'HeaderEnabled', Header.Enabled)
    #         Footer.Text            = ReadString('Page', 'FooterText', Footer.Text)
    #         Footer.Alignment = TAlignment(ReadInteger('Page', 'FooterAlignment',
    #                                                     Ord(Footer.Alignment)))
    #         Footer.Enabled     = ReadBool('Page', 'FooterEnabled', Footer.Enabled)
    #         PageNumbers            = TPageNumbers(ReadInteger('Page', 'PageNumbers',
    #                                                     Ord(PageNumbers)))
    #     TitleAsHeader = ReadBool('Page', 'TitleAsHeader', TitleAsHeader)
    #     Orientation     = ReadInteger('Page', 'Orientation', Orientation)
    #
    #     # Read names of calibration data files
    #     for I = Low(CalibData) to High(CalibData):
    #         CalibData[I].FileName = ReadString('Calibration', 'File'+IntToStr(I), '')
    #
    #     # Read date/time format for time series graphs
    #     GraphOptions.DateTimeFormat = ReadString('Graph', 'DateTimeFormat', '')
    #
    #     # See if past results were saved to file
    #     ResultsSaved = ReadBool('Results', 'Saved', ResultsSaved)
    #     UpdateFlag = not ReadBool('Results', 'Current', True)
    # finally:
    #     Free


def SaveProjIniFile(Fname):
    """ Save various options to the project's INI file. """
    pass
    # theIniFile = TIniFile.Create(Fname)
    # with theIniFile:
    # try
    #         # Write current version
    #         WriteInteger('SWMM5', 'Version', Uglobals.VERSIONID2)
    #
    #         # Write map display options
    #         with MapForm.Map.Options:
    #             WriteBool('Map', 'ShowGageIDs', ShowGageIDs)
    #             WriteBool('Map', 'ShowSubcatchIDs', ShowSubcatchIDs)
    #             WriteBool('Map', 'ShowSubcatchValues', ShowSubcatchValues)
    #             WriteBool('Map', 'ShowSubcatchLinks', ShowSubcatchLinks)
    #
    #             WriteBool('Map', 'ShowNodeIDs', ShowNodeIDs)
    #             WriteBool('Map', 'ShowNodeValues', ShowNodeValues)
    #             WriteBool('Map', 'ShowNodesBySize', ShowNodesBySize)
    #             WriteBool('Map', 'ShowNodeBorder', ShowNodeBorder)
    #
    #             WriteBool('Map', 'ShowLinkIDs', ShowLinkIDs)
    #             WriteBool('Map', 'ShowLinkValues', ShowLinkValues)
    #             WriteBool('Map', 'ShowLinksBySize', ShowLinksBySize)
    #             WriteBool('Map', 'ShowLinkBorder', ShowLinkBorder)
    #
    #             WriteBool('Map', 'ShowGages', ShowGages)
    #             WriteBool('Map', 'ShowSubcatchs', ShowSubcatchs)
    #             WriteBool('Map', 'ShowNodes', ShowNodes)
    #             WriteBool('Map', 'ShowLinks', ShowLinks)
    #             WriteBool('Map', 'ShowNodeSymbols', ShowNodeSymbols)
    #             WriteBool('Map', 'ShowLinkSymbols', ShowLinkSymbols)
    #
    #             WriteBool('Map', 'ShowLabels', ShowLabels)
    #             WriteBool('Map', 'LabelsTranspar', LabelsTranspar)
    #             WriteBool('Map', 'NotationTranspar', NotationTranspar)
    #
    #             WriteInteger('Map', 'SubcatchFillStyle', SubcatchFillStyle)
    #             WriteInteger('Map', 'SubcatchLineSize', SubcatchLineSize)
    #             WriteInteger('Map', 'SubcatchSnapTol', SubcatchSnapTol)
    #             WriteInteger('Map', 'SubcatchSize', SubcatchSize)
    #             WriteInteger('Map', 'NodeSize', NodeSize)
    #             WriteInteger('Map', 'LinkSize', LinkSize)
    #             WriteInteger('Map', 'NotationSize', NotationSize)
    #
    #             WriteInteger('Map', 'ArrowStyle', Ord(ArrowStyle))
    #             WriteInteger('Map', 'ArrowSize', ArrowSize)
    #
    #             WriteInteger('Map', 'ColorIndex', ColorIndex)
    #             WriteInteger('Map', 'NotationZoom', NotationZoom)
    #             WriteInteger('Map', 'LabelZoom', LabelZoom)
    #             WriteInteger('Map', 'SymbolZoom', SymbolZoom)
    #             WriteInteger('Map', 'ArrowZoom', ArrowZoom)
    #
    #         # Write map backdrop options
    #         with Mapform.Map.Backdrop:
    #             WriteBool('Backdrop', 'Visible', Visible)
    #             WriteBool('Backdrop', 'Watermark', Watermark)
    #
    #         # Write legend colors & intervals
    #         WriteInteger('Legends', 'NumIntervals', MAXINTERVALS)
    #         N = MAXINTERVALS
    #         for I = 0 to N:
    #             WriteInteger('Legends', 'MapSubcatchColor' + IntToStr(I),
    #                 MapSubcatchColor[I])
    #         for I = 0 to N:
    #             WriteInteger('Legends', 'MapNodeColor' + IntToStr(I), MapNodeColor[I])
    #         for I = 0 to N:
    #             WriteInteger('Legends', 'MapLinkColor' + IntToStr(I), MapLinkColor[I])
    #         for I = 1 to SUBCATCHVIEWS:
    #             S = ''
    #             for J = 1 to N do S = S +
    #                 FloatToStr(SubcatchLegend[I].Intervals[J]) + ','
    #             WriteString('Legends', 'SubcatchLegend' + IntToStr(I), S)
    #         for I = 1 to NODEVIEWS:
    #             S = ''
    #             for J = 1 to N do S = S + FloatToStr(NodeLegend[I].Intervals[J]) + ','
    #             WriteString('Legends', 'NodeLegend' + IntToStr(I), S)
    #         for I = 1 to LINKVIEWS:
    #             S = ''
    #             for J = 1 to N do S = S + FloatToStr(LinkLegend[I].Intervals[J]) + ','
    #             WriteString('Legends', 'LinkLegend' + IntToStr(I), S)
    #
    #         # Save default project properties
    #         SaveDefaultsToFile(theIniFile)
    #         for I = 0 to MAXCLASS:
    #             WriteInteger('Labels', ObjectLabels[I] + '_NextID', Project.NextID[I])
    #
    #         # Save printed Page Layout info
    #         with PageLayout:
    #             WriteString('Page', 'LeftMargin', FloatToStr(LMargin))
    #             WriteString('Page', 'RightMargin', FloatToStr(RMargin))
    #             WriteString('Page', 'TopMargin', FloatToStr(TMargin))
    #             WriteString('Page', 'BottomMargin', FloatToStr(BMargin))
    #         with MainForm.PageSetupDialog:
    #             WriteString('Page', 'HeaderText', Header.Text)
    #             WriteInteger('Page', 'HeaderAlignment', Ord(Header.Alignment))
    #             WriteBool('Page', 'HeaderEnabled', Header.Enabled)
    #             WriteString('Page', 'FooterText', Footer.Text)
    #             WriteInteger('Page', 'FooterAlignment', Ord(Footer.Alignment))
    #             WriteBool('Page', 'FooterEnabled', Footer.Enabled)
    #             WriteInteger('Page', 'PageNumbers', Ord(PageNumbers))
    #         WriteBool('Page', 'TitleAsHeader', TitleAsHeader)
    #         WriteInteger('Page', 'Orientation', Orientation)
    #
    #         # Save names of calibration data files
    #         for I = Low(CalibData) to High(CalibData):
    #             WriteString('Calibration', 'File'+IntToStr(I), CalibData[I].FileName)
    #
    #         # Write date/time format for time series graphs
    #         WriteString('Graph', 'DateTimeFormat', GraphOptions.DateTimeFormat)
    #
    #         # Write flag for saved results
    #         WriteBool('Results', 'Saved', ResultsSaved)
    #         WriteBool('Results', 'Current', (not UpdateFlag))
    # except
    # theIniFile.Free


def ExtractValues(S, N1, N2, X):
    """
        Parse the string S into a sequence of numbers and places these
        numbers in the array X at positions N1 to N2.
    """
    pass
    # Snew = StringReplace(S, ',', ' ', [rfReplaceAll])
    # Slist = TStringlist.Create
    # try
    #     Uutils.Tokenize(Snew, Slist, N)
    #     if N > 0:
    #         Nmax = N2 - N1 + 1
    #         if Nmax > N: Nmax = N
    #         N = N1
    #         for J = 0 to Nmax-1:
    #             if Uutils.GetSingle(Slist[J], Y): X[N] = Y
    #             Inc(N)
    # finally
    #     Slist.Free

from ui.inifile import ini_setting
class DefaultsSWMM(ini_setting):
    def __init__(self, file_name, project):
        ini_setting.__init__(self, file_name)
        self.project = project
        self.model = "swmm"

        # [Labels] label prefix
        self.model_object_keys = ["Rain Gage", "Subcatchment", "Junction", "Outfall", "Divider",
                                  "Storage Unit", "Conduit", "Pump", "Regulator"]
        self.model_object_def_prefix = ["RG", "S", "J", "O", "D", "SU", "C", "P", "R"]

        self.id_increment_key = "ID Increment"
        self.id_def_increment = 1
        self.id_increment = 1

        # [Defaults]
        self.keyprefix_subcatch = "SUBCATCH_"
        self.keyprefix_infil = "INFIL_"
        self.keyprefix_node = "NODE_"
        self.keyprefix_link = "LINK_"
        self.keyprefix_conduit = "CONDUIT_"
        self.keyprefix_xsection = "XSECTION_"
        self.infil_model_key = "Infiltration Model"
        self.infil_model_horton = HortonInfiltration()
        self.infil_model_horton.set_defaults()
        self.infil_model_ga = GreenAmptInfiltration()
        self.infil_model_ga.set_defaults()
        self.infil_model_cn = CurveNumberInfiltration()
        self.infil_model_cn.set_defaults()
        self.properties_sub_keys = ["Area", "Width", "% Slope", "% Imperv", "N-Imperv", "N-Perv",
                           "Dstore-Imperv", "Dstore-Perv", "%Zero-Imperv", self.infil_model_key]
        self.properties_sub_def_values = [5.0, 500.0, 0.5, 25.0, 0.01, 0.1, 0.05, 0.05, 25.0, "HORTON"]

        # [Defaults]
        # default xsection
        self.xsection_def = CrossSection()
        self.xsection_def.shape = CrossSectionShape.CIRCULAR
        self.xsection_def.barrels = 1
        self.xsection_def.geometry1 = 1.0
        # user choice
        self.xsection = CrossSection()
        self.xsection.shape = CrossSectionShape.CIRCULAR
        self.xsection.barrels = 1
        self.xsection.geometry1 = 1.0
        self.xsection_key = "Conduit Geometry"
        self.parameters_keys = ["Node Invert", "Node Max. Depth", "Node Ponded Area", "Conduit Length",
                                self.xsection_key, "Conduit Roughness", "Flow Units", "Link Offsets",
                                "Routing Method", "Force Main Equation"]
        self.parameters_def_values = [0, 0, 0, 400, "CIRCULAR", 0.01, "CFS", "DEPTH", "KINWAVE", "H_W"]

        self.model_object_prefix = {}
        for key in self.model_object_keys:
            self.model_object_prefix[key] = self.model_object_def_prefix[self.model_object_keys.index(key)]
            if self.config:
                val, vtype = self.get_setting_value("Labels", key)
                if val is not None:
                    self.model_object_prefix[key] = val

        self.id_increment, vtype = self.get_setting_value("Labels", self.id_increment_key)
        if self.id_increment is None:
            self.id_increment = 1

        group = "Defaults"
        self.properties_sub_values = {}
        for key in self.properties_sub_keys:
            self.properties_sub_values[key] = self.properties_sub_def_values[self.properties_sub_keys.index(key)]
            if self.config:
                val, vtype = self.get_setting_value(group, self.keyprefix_subcatch + key)
                if val is not None:
                    self.properties_sub_values[key] = val

        if self.config:
            # retrieve infiltration model parameters
            infil_model_name, vtype = self.get_setting_value(group, self.infil_model_key)
            if not infil_model_name:
                infil_model_name, vtype = self.get_setting_value(group, "INFILTRATION")
            if infil_model_name:
                infil_model_type = E_InfilModel[infil_model_name]
                key = self.keyprefix_infil + "PARAM"
                if infil_model_type == E_InfilModel.HORTON or \
                    infil_model_type == E_InfilModel.MODIFIED_HORTON:
                    self.infil_model_horton.max_rate, vtype = self.get_setting_value(group, key + "1")
                    self.infil_model_horton.min_rate, vtype = self.get_setting_value(group, key + "2")
                    self.infil_model_horton.decay, vtype = self.get_setting_value(group, key + "3")
                    self.infil_model_horton.dry_time, vtype = self.get_setting_value(group, key + "4")
                    pass
                elif infil_model_type == E_InfilModel.GREEN_AMPT or \
                   infil_model_type == E_InfilModel.MODIFIED_GREEN_AMPT:
                    self.infil_model_ga.suction, vtype = self.get_setting_value(group, key + "1")
                    self.infil_model_ga.hydraulic_conductivity, vtype = self.get_setting_value(group, key + "2")
                    self.infil_model_ga.initial_moisture_deficit, vtype = self.get_setting_value(group, key + "3")
                    pass
                elif infil_model_type == E_InfilModel.CURVE_NUMBER:
                    self.infil_model_cn.curve_number, vtype = self.get_setting_value(group, key + "1")
                    self.infil_model_cn.dry_days, vtype = self.get_setting_value(group, key + "2")
                    pass

        self.parameters_values = {}
        for key in self.parameters_keys:
            self.parameters_values[key] = self.parameters_def_values[self.parameters_keys.index(key)]
            if self.config:
                val, vtype = self.get_setting_value(group, key)
                if val is not None:
                    self.parameters_values[key] = val

        if self.config:
            # retrieve cross section parameters
            xsect_name, vtype = self.get_setting_value(group, self.keyprefix_conduit + "SHAPE")
            if xsect_name is not None:
                self.xsection.shape = CrossSectionShape[xsect_name]
                key_prefix = self.keyprefix_conduit + "GEOM"
                self.xsection.geometry1, vtype = self.get_setting_value(group, key_prefix + "1")
                self.xsection.geometry2, vtype = self.get_setting_value(group, key_prefix + "2")
                self.xsection.geometry3, vtype = self.get_setting_value(group, key_prefix + "3")
                self.xsection.geometry4, vtype = self.get_setting_value(group, key_prefix + "4")

        if self.config is None:
            self.init_config()

    def init_config(self):
        # if a new qsettings has not been created such as when no project is created
        # then, create an empty qsettings
        self.config = QSettings(QSettings.IniFormat, QSettings.UserScope, "EPA", self.model, None)
        self.config.setValue("Model/Name", self.model)
        for key in self.model_object_keys:
            self.config.setValue("Labels/" + key, self.model_object_prefix[key])
        for key in self.properties_sub_keys:
            self.config.setValue("Defaults/" + self.keyprefix_subcatch + key, self.properties_sub_values[key])
        for key in self.parameters_keys:
            self.config.setValue("Defaults/" + key, self.parameters_values[key])

    def sync_defaults_label(self):
        """
        sync object label/prefix with internal qsettings
        """
        for key in self.model_object_keys:
            if self.config:
                self.config.setValue("Labels/" + key, self.model_object_prefix[key])
        if self.config:
            self.config.setValue("Labels/" + self.id_increment_key, str(self.id_increment))

    def sync_defaults_sub_property(self):
        """
        sync subcatchment properties with internal qsettings
        """
        group = "Defaults/"
        for key in self.properties_sub_keys:
            if self.config:
                self.config.setValue(group + self.keyprefix_subcatch + key, self.properties_sub_values[key])
        # record infiltration model parameters
        infil_model_name = self.properties_sub_values[self.infil_model_key]
        infil_model_type = E_InfilModel[infil_model_name]
        self.config.setValue(group + self.infil_model_key, infil_model_name)
        key_prefix = group + self.keyprefix_infil + "PARAM"
        if infil_model_type == E_InfilModel.HORTON or \
           infil_model_type == E_InfilModel.MODIFIED_HORTON:
            self.config.setValue(key_prefix + "1", unicode(self.infil_model_horton.max_rate))
            self.config.setValue(key_prefix + "2", unicode(self.infil_model_horton.min_rate))
            self.config.setValue(key_prefix + "3", unicode(self.infil_model_horton.decay))
            self.config.setValue(key_prefix + "4", unicode(self.infil_model_horton.dry_time))
            self.config.setValue(key_prefix + "5", "0")
            self.config.setValue(key_prefix + "6", "")
        elif infil_model_type == E_InfilModel.GREEN_AMPT or \
             infil_model_type == E_InfilModel.MODIFIED_GREEN_AMPT:
            self.config.setValue(key_prefix + "1", unicode(self.infil_model_ga.suction))
            self.config.setValue(key_prefix + "2", unicode(self.infil_model_ga.hydraulic_conductivity))
            self.config.setValue(key_prefix + "3", unicode(self.infil_model_ga.initial_moisture_deficit))
            self.config.setValue(key_prefix + "4", "")
            self.config.setValue(key_prefix + "5", "")
            self.config.setValue(key_prefix + "6", "")
        elif infil_model_type == E_InfilModel.CURVE_NUMBER:
            self.config.setValue(key_prefix + "1", unicode(self.infil_model_cn.curve_number))
            self.config.setValue(key_prefix + "2", unicode(self.infil_model_cn.dry_days))
            self.config.setValue(key_prefix + "3", "")
            self.config.setValue(key_prefix + "4", "")
            self.config.setValue(key_prefix + "5", "")
            self.config.setValue(key_prefix + "6", "")
        if self.project:
            #update the default infiltration model name in the global project option
            self.project.options.infiltration = infil_model_name

    def sync_defaults_parameter(self):
        """
        sync hydraulic parameters with internal qsettings
        """
        for key in self.parameters_keys:
            if self.config:
                self.config.setValue("Defaults/" + key, self.parameters_values[key])
        if self.project:
            self.sync_project_hydraulic_parameters()

        # record cross section parameters
        group = "Defaults/"
        xsect_name = self.parameters_values[self.xsection_key]
        xsect_type = CrossSectionShape[xsect_name]
        self.config.setValue(group + self.keyprefix_conduit + "SHAPE", self.xsection.shape.name)
        key_prefix = group + self.keyprefix_conduit + "GEOM"
        self.config.setValue(key_prefix + "1", unicode(self.xsection.geometry1))
        self.config.setValue(key_prefix + "2", unicode(self.xsection.geometry2))
        self.config.setValue(key_prefix + "3", unicode(self.xsection.geometry3))
        self.config.setValue(key_prefix + "4", unicode(self.xsection.geometry4))

    def sync_project_hydraulic_parameters(self):
        group = "Defaults/"
        hydraulics_options = self.project.options
        for key in self.parameters_keys:
            val = self.parameters_values[key]
            self.config.setValue(group + key, unicode(val))
            if "flow unit" in key.lower():
                hydraulics_options.flow_units = hyd.FlowUnits[val]
            elif "link offset" in key.lower():
                hydraulics_options.link_offsets = hyd.LinkOffsets[val]
            elif "routing" in key.lower():
                hydraulics_options.flow_routing = hyd.FlowRouting[val]
            elif "force main" in key.lower():
                hydraulics_options.dynamic_wave.force_main_equation = dw.ForceMainEquation[val]
            elif "node invert" in key.lower():
                #hydraulics_options.node_invert = float(val)
                pass
            elif "node max. depth" in key.lower():
                #hydraulics_options.node_max_depth = float(val)
                pass
            elif "node ponded area" in key.lower():
                #hydraulics_options.node_ponded_area = float(val)
                pass
            elif "conduit length" in key.lower():
                #hydraulics_options.conduit_length = float(val)
                pass
            elif "conduit geometry" in key.lower():
                #hydraulics_options.conduit_geometry = float(val)
                pass
            elif "conduit roughness" in key.lower():
                #hydraulics_options.conduit_roughness = float(val)
                pass

    def apply_default_attributes(self, item):
        """
        Set default attributes for new model object
        Args:
            item: newly created model object
        """
        item_type = item.__class__.__name__
        if item_type == "Junction" or item_type == "Outfall" or item_type== "Divider" or \
                item_type == "StorageUnit":
            item.elevation = self.parameters_values["Node Invert"]
            if item_type == "Junction" or item_type == "Divider" or item_type == "StorageUnit":
                item.max_depth = self.parameters_values["Node Max. Depth"]
            if item_type == "Junction":
                item.ponded_area = self.parameters_values["Node Ponded Area"]
        elif item_type == "Conduit":
            # from core.swmm.hydraulics.link import Conduit
            # item = Conduit()
            item.length = self.parameters_values["Conduit Length"]
            item.roughness = self.parameters_values["Conduit Roughness"]
        elif item_type == "CrossSection":
            # from core.swmm.hydraulics.link import CrossSection
            # from core.swmm.hydraulics.link import CrossSectionShape
            # item = CrossSection()
            item.barrels = self.xsection.barrels
            item.shape = self.xsection.shape
            item.geometry1 = self.xsection.geometry1
            item.geometry2 = self.xsection.geometry2
            item.geometry3 = self.xsection.geometry3
            item.geometry4 = self.xsection.geometry4
        elif item_type == "Subcatchment":
            # from core.swmm.hydrology.subcatchment import Subcatchment
            # item = Subcatchment()
            item.area = self.properties_sub_values["Area"]
            item.width = self.properties_sub_values["Width"]
            item.percent_slope = self.properties_sub_values["% Slope"]
            item.percent_impervious = self.properties_sub_values["% Imperv"]
            item.n_imperv = self.properties_sub_values["N-Imperv"]
            item.n_perv = self.properties_sub_values["N-Perv"]
            item.storage_depth_imperv = self.properties_sub_values["Dstore-Imperv"]
            item.storage_depth_perv = self.properties_sub_values["Dstore-Perv"]
            item.percent_zero_impervious = self.properties_sub_values["%Zero-Imperv"]
            #self.apply_default_infiltration_attributes(item)
            #item.infiltration_parameters = None
            #infil_model_name = self.properties_sub_values[self.infil_model_key]
            ## as the project_setting is an entity that exists during project session
            ## its ok to reference an instance variable here
            #if "HORTON" in infil_model_name.upper() :
            #    item.infiltration_parameters = self.infil_model_horton
            #elif "GREEN" in infil_model_name.upper():
            #    item.infiltration_parameters = self.infil_model_ga
            #elif "CURVE" in infil_model_name.upper():
            #    item.infiltration_parameters = self.infil_model_cn
            pass

    def apply_default_infiltration_attributes(self, infil_item):
        if not infil_item: return
        enum_val = E_InfilModel[self.properties_sub_values[self.infil_model_key]]
        if enum_val == E_InfilModel.HORTON or \
           enum_val == E_InfilModel.MODIFIED_HORTON:
            for attr in HortonInfiltration.metadata:
                infil_item.__dict__[attr.attribute] = \
                       self.infil_model_horton.__dict__[attr.attribute]
            #infil_item.subcatchment = sub_id
        elif enum_val == E_InfilModel.GREEN_AMPT or \
             enum_val == E_InfilModel.MODIFIED_GREEN_AMPT:
            #infil_item = GreenAmptInfiltration()
            for attr in GreenAmptInfiltration.metadata:
                infil_item.__dict__[attr.attribute] = \
                    self.infil_model_ga.__dict__[attr.attribute]
            #infil_item.subcatchment = sub_id
        elif enum_val == E_InfilModel.CURVE_NUMBER:
            #infil_item = CurveNumberInfiltration()
            for attr in CurveNumberInfiltration.metadata:
                infil_item.__dict__[attr.attribute] = \
                    self.infil_model_cn.__dict__[attr.attribute]
            #infil_item.subcatchment = sub_id
        pass


