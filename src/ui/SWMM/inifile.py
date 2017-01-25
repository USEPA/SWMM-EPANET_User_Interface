from PyQt4.Qt import Qt

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
    def __init__(self, file_name, project, qsetting):
        ini_setting.__init__(self, file_name, qsetting)
        self.project = project
        self.model = "swmm"

