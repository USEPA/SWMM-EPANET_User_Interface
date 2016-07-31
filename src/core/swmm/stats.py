# from enum import Enum
# import datetime
# from dateutil.relativedelta import relativedelta
# import numpy as np
# import pandas as pd
# import Externals.swmm.outputapi.SMOutputWrapper as SMO
# import core.swmm.globals as globals
#
# #-------------------------------------------------------------------}
# #                    Unit:    Ustats.pas                            }
# #                    Project: EPA SWMM                              }
# #                    Version: 5.1                                   }
# #                    Date:    12/2/13     (5.1.000)                 }
# #                    Author:  L. Rossman                            }
# #                                                                   }
# #   This unit computes frequency statistics on the events that      }
# #   have occurred during a simulation by calling the def       }
# #   GetStats(StatsSel, EventList, Results). StatsSel is a           }
# #   TStatsSelection record that defines the variable and type of    }
# #   event being analyzed. EventList is a TList that will contain    }
# #   and ordered listing of TStatsEvent records. Results is a        }
# #   TStatsResults record that contains summary event statistics.    }
# #-------------------------------------------------------------------}
#
# class EStatsCat(Enum):
#     BASIC = 0
#     FLOW = 1
#     QUAL = 2
#
# class EPlotPosition(Enum):
#     ppFrequency = 0
#     ppYears = 1
#     ppMonths = 2
#
# class ETimePeriod(Enum):
#     tpVariable = 0
#     tpDaily = 1
#     tpMonthly = 2
#     tpAnnual = 3
#
# class EStatsType(Enum): #TStatsType
#     stMean = 0
#     stPeak = 1
#     stTotal = 2
#     stDuration = 3
#     stDelta = 4
#     stMeanConcen = 5
#     stPeakConcen = 6
#     stMeanLoad = 7
#     stPeakLoad = 8
#     stTotalLoad = 9
#
# class EStatsQuant(Enum):
#     sqValue = 0
#     sqLoad = 1
#
# # Record which contains the properties of a single event
# class TStatsEvent:
#     def __init__(self):
#         self.StartDate = datetime.now() #TDateTime
#         self.Value = 0.0 #Single
#         self.Duration = 0.0 # duration in milliseconds or seconds, Single
#         self.Rank = 0 #Integer
#
# # Record which contains information about what kind of report to generate
# class TStatsSelection:
#     def __init__(self):
#         self.ObjectID       = ""               # ID of object being analyzed
#         self.ObjectType     = globals.ObjectType.UNKNOWN # Subcatch, Node or Link, or system
#         self.ObjectTypeText = "UNKNOWN"        # Subcatch, Node or Link, or system
#         self.Variable       = 0                # Index of variable analyzed, basic, flow, or qual
#         self.VariableText   = "UNKNOWN"        # Text of variable analyzed, e.g. precipitation
#         self.MinEventDelta  = 0.0              # Min. inter-event hours allowed
#         self.MinEventValue  = 0.0              # Min. value for event to exist
#         self.MinEventVolume = 0.0              # Min. flow vol. for event to exist
#         self.PlotParameter  = 0.0              # e.g., = 0 for Weibull probability
#         self.TimePeriod     = ETimePeriod.tpVariable    # Event-depent, Daily, Monthly, Annual
#         self.TimePeriodText = "UNKNOWN"        # Event-depent, Daily, Monthly, Annual
#         self.PlotPosition   = EPlotPosition.ppFrequency # Frequency, Yearly, Monthly Ret. Per.
#         self.StatsType      = EStatsType.stMean    # Index of Mean, Peak, Total, Duration, Delta
#         self.StatsTypeText  = "UNKNOWN"        # Mean, Peak, Total, Duration, Delta
#         self.VarIndex       = 0                # Index of variable analyzed in output file
#         self.FlowVarIndex   = 0                # Index of flow variable in output file
#         self.IsQualParam    = False            # True if variable is quality
#         self.IsRainParam    = False            # True if variable is rainfall
#
# # Record which contains statistical analysis results
# class TStatsResults:
#     def __init__(self):
#         self.Duration       = 0                # Period of analysis (yrs or months)
#         self.Timespan       = None             # relativedelta in datetime
#         self.Mean           = 0.0              # Mean value
#         self.StdDev         = 0.0              # Standard deviation
#         self.Skew           = 0.0              # Skewness Coeff.
#         self.Xmin           = 0.0              # Minmimum value
#         self.Xmax           = 0.0              # Maximum value
#         self.EventFreq      = 0.0              # Event frequency
#
# class Uglobals:
#     Nsubcatchs = 0  # Integer;             # Number of subcatchments
#     Nnodes = 0  # Integer;             # Number of nodes
#     Nlinks = 0  # Integer;             # Number of links
#     Npolluts = 0  # Integer;             # Number of pollutants
#     NsysViews = 0  # Integer;             # Number of system view variables
#     Qunits = 0  # Integer;             # Index of flow units
#     Zsubcatch  # PSingleArray;        # Values of subcatch view variable
#     Znode  # PSingleArray;        # Values of node view variable
#     Zlink  # PSingleArray;        # Values of link view variable
#     FlowDir  # PByteArray;          # Flow direction (+-) of each link
#     RunFlag = True  # Boolean;             # Analysis ran OK (True/False)
#     RunStatus  # TRunStatus;          # Current run status flag
#     DynWaveFlag = False  # Boolean;             # Dynamic Wave routing used
#     Nperiods = 0  # LongInt;             # Total number of time periods
#     CurrentPeriod  # LongInt;             # Time period being viewed
#     StartDateTime  # TDateTime;           # Starting date/time
#     EndDateTime  # TDateTime;           # Ending date/time
#     DeltaDateTime  # TDateTime;           # Reporting time step (in days)
#     CurrentDateTime  # TDateTime;          # Current date/time being viewed
#
# class StatisticUtility(object):
#     def __init__(self, output):
#         self.TXT_FINDING_EVENTS = 'Finding events... '
#         self.TXT_RANKING_EVENTS = 'Ranking events... '
#         self.output = SMO.SwmmOutputObject(output)
#
#         # The following arrays of flow conversion factors are for
#         # CFS, GPM, MGD, CMS, LPS, and MLD, respectively.
#
#         # Conversion factors for flow to million liters per day
#         self.QtoMLD = (2.446589, 0.005451, 3.785414, 86.4, 0.0864, 1.0)
#
#         # Conversion from flow time units to days
#         self.QtimeToDays = (86400.0, 1440.0, 1.0, 86400.0, 86400.0, 1.0)
#
#         self.Stats = None #TStatsSelection()  # Local copy of stat. event defn.
#
#         #These are class wise temporary variables
#         self.TotalPeriods = 0.0  # Total number of event periods
#         self.EventPeriods = 0.0  # Number of periods with events
#         self.WetStart = None  # TDateTime  # Start date/time of wet period
#         self.WetEnd = None  # TDateTime  # date/time of wet period
#         self.DryEnd = None  # TDateTime  # date/time of following dry period
#         self.Nwet = 0  # Number of wet periods in an event
#         self.Ysum = 0.0  # Cumulative sum of event variable
#         self.Ymax = 0.0  # Maximum value of event variable
#         self.Vsum = 0.0  # Cumulative flow volume in an event
#         pass
#
#     def GetStats(self, StatsSel, EventList):
#         Results = TStatsResults()
#         #-----------------------------------------------------------------------------
#         #  Analyzes simulation results to find the frequency of events as
#         #  defined by the StatsSel argument. EventList contains a rank ordered
#         #  listing of each event while Results contains summary event statistics.
#         #-----------------------------------------------------------------------------
#         self.Stats = TStatsSelection(StatsSel)
#         # Application.ProcessMessages
#         # MainForm.ShowProgressBar(TXT_FINDING_EVENTS)
#         self.FindDuration(EventList, Results)
#         self.FindEvents(EventList)
#         # MainForm.ShowProgressBar(TXT_RANKING_EVENTS)
#         self.RankEvents(EventList)
#         self.FindStats(EventList, Results)
#         StatsSel = self.Stats #??? what for ???
#         return Results
#
#     def FindDuration(self, EventList, Results): # : TStatsResults)
#         #-----------------------------------------------------------------------------
#         #  Finds the duration of the total simulation period.
#         #-----------------------------------------------------------------------------
#         #  D1, D2: TDateTime
#         #  Months: Integer
#         #  Years:  Integer
#
#         # Set the capacity of the EventList
#         #EventList.Capacity = Uglobals.Nperiods
#
#         # Evaluate start and days
#         #D1 = Uglobals.StartDateTime
#         #D2 = Uglobals.StartDateTime + (Uglobals.Nperiods-1)*Uglobals.DeltaDateTime
#         D1 = self.output.StartDate      #Uglobals.StartDateTime
#         #D2 = D1 + (self.output.num_periods - 1) * self.output.
#         D2 = self.output.EndDate
#         Results.Timespan = relativedelta(D2, D1)
#
#         # Find duration in months & years
#         #Months = Floor((D2 - D1)/(365/12) + 0.5)
#         #Years  = Floor((D2 - D1)/365 + 0.5)
#         # Assign value to PlotPosition
#         if abs(Results.Timespan.years) < 3:
#             #Stats.PlotPosition = ppMonths
#             Results.Duration = Results.Timespan.months
#         else:
#             #Stats.PlotPosition = ppYears
#             Results.Duration = Results.Timespan.years
#
#     def FindEvents(self, EventList, output, aTser):  # TList
#         # -----------------------------------------------------------------------------
#         #  Identifies all events that occurred over the simulation period.
#         # -----------------------------------------------------------------------------
#         #  T       : LongInt
#         #  Q       : Single
#         #  Y       : Single
#         #  CF      : Single
#         #  Date1   : TDateTime
#         #  Date2   : TDateTime
#         #  Progress: LongInt
#         #  ProgStep: LongInt
#         #  theObject : TObject          # Reference to object being analyzed
#
#         # Initialize total periods and number with events
#         self.TotalPeriods = 0
#         self.EventPeriods = 0
#
#         # Initialize wet/dry period conditions
#         self.InitConditions(aTser.index[0])
#
#         # Find step size to use with the MainForm's ProgressBar
#         # MainForm.ShowProgressBar('Reading Time Series:')
#         # ProgStep = Nperiods div (MainForm.ProgressBar.Max div MainForm.ProgressBar.Step)
#         # Progress = 0
#         # Application.ProcessMessages
#         # MainForm.ShowProgressBar(TXT_FINDING_EVENTS)
#         #theObject = Uoutput.GetObject(Stats.ObjectType, Stats.ObjectID)
#
#         # Examine each reporting period
#         for T in range(0, output.num_periods - 2):
#             # Get the current and next reporting dates
#             Date1 = aTser.index[T]
#             Date2 = aTser.index[T + 1]
#
#             # See if a new event period has begun
#             if self.IsNewEventPeriod(Date1, Date2):
#                 self.TotalPeriods += 1
#
#             # If in a wet period, see if a new event has begun
#             if self.Nwet > 0:
#                 self.AddNewEvent(EventList, Date1)
#
#             # Get current values of the event variable (Y) and flow (Q)
#             #Y = Uoutput.GetValue(Stats.ObjectType, Stats.VarIndex, T, theObject)
#             Y = aTser[T] #ToDo: handle more than one time series in this dataframe
#             if self.Stats.FlowVarIndex == self.Stats.VarIndex:
#                 Q = Y
#             elif self.Stats.FlowVarIndex >= 0:
#                 Q = 0.0 #Uoutput.GetValue(Stats.ObjectType, Stats.FlowVarIndex, T, theObject)
#             else:
#                 Q = 0
#
#             # Update event properties
#             self.DryEnd = Date2
#             if (Q != globals.MiscConstants.MISSING and
#                 Y != globals.MiscConstants.MISSING and
#                 Y > self.Stats.MinEventValue):
#                 # Convert variables to absolute value
#                 Q = abs(Q)
#                 Y = abs(Y)
#
#                 # Update the event volume (Vsum)
#                 CF = self.QtimeToDays[Uglobals.Qunits]
#                 if self.Stats.IsRainParam:
#                     CF = 24
#                 self.Vsum += Q * Uglobals.DeltaDateTime * CF
#
#                 # If computing mass load statistics, convert concentration to load
#                 if self.Stats.IsQualParam and self.Stats.StatsType >= EStatsType.stMeanLoad:
#                     Y = Y * Q * self.QtoMLD[Uglobals.Qunits]
#
#             # Start a new wet period
#             if self.Nwet == 0:
#                 WetStart = Date1
#             self.Nwet += 1
#             self.WetEnd = Date2
#
#             # Update sum and max. value
#             self.Ysum += Y
#             if Y > self.Ymax:
#                 self.Ymax = Y
#
#             # Update MainForm's progress bar
#             # MainForm.UpdateProgressBar(Progress, ProgStep)
#
#         # After processing all time periods, add the last wet period event
#         # to the event list
#         Dry = self.Stats.MinEventDelta / 24.0 + self.WetEnd + 1.0  # (5.0.012 - LR)
#         self.AddNewEvent(EventList, Uglobals.StartDateTime +
#                     (Uglobals.Nperiods - 1) * Uglobals.DeltaDateTime)
#
#         # Make sure we have at least one event period
#         if self.TotalPeriods == 0:
#             TotalPeriods = 1
#
#         # Reclaim any unused capacity in the event list
#         EventList.Capacity = EventList.Count
#
#     def IsNewEventPeriod(Date1, Date2, StatsTimePeriod):
#         # -----------------------------------------------------------------------------
#         #  Determines if a new event period has begun or not.
#         # -----------------------------------------------------------------------------
#         #  Date1, Date2: the beginning and end of a time step, pandas TimeStamp
#         #  StatTimePeriod:  user-specified
#         #
#         Result = False
#         if StatsTimePeriod == "Event-dependent":
#             Result = True
#         elif StatsTimePeriod == "Daily":
#             if Date1.day != Date2.day:
#                 Result = True
#         elif StatsTimePeriod == "Monthly":
#             if Date1.month != Date2.month:
#                 Result = True
#         elif StatsTimePeriod == "Annual":
#             if Date2.year > Date1.year:
#                 Result = True
#         return Result
#
#
#     # def FindEvents_ori(EventList): #TList
#     #   #-----------------------------------------------------------------------------
#     #   #  Identifies all events that occurred over the simulation period.
#     #   #-----------------------------------------------------------------------------
#     #   #  T       : LongInt
#     #   #  Q       : Single
#     #   #  Y       : Single
#     #   #  CF      : Single
#     #   #  Date1   : TDateTime
#     #   #  Date2   : TDateTime
#     #   #  Progress: LongInt
#     #   #  ProgStep: LongInt
#     #   #  theObject : TObject          # Reference to object being analyzed
#     #
#     #   # Initialize total periods and number with events
#     #   TotalPeriods = 0
#     #   EventPeriods = 0
#     #
#     #   # Initialize wet/dry period conditions
#     #   InitConditions(Uglobals.StartDateTime)
#     #
#     #   # Find step size to use with the MainForm's ProgressBar
#     #   # MainForm.ShowProgressBar('Reading Time Series:')
#     #   # ProgStep = Nperiods div (MainForm.ProgressBar.Max div MainForm.ProgressBar.Step)
#     #   # Progress = 0
#     #   # Application.ProcessMessages
#     #   # MainForm.ShowProgressBar(TXT_FINDING_EVENTS)
#     #   theObject = Uoutput.GetObject(Stats.ObjectType, Stats.ObjectID)
#     #
#     #   # Examine each reporting period
#     #   for T in range(0, Uglobals.Nperiods-1):
#     #
#     #     # Get the current and next reporting dates
#     #     Date1 = Uglobals.StartDateTime + T * Uglobals.DeltaDateTime
#     #     Date2 = Date1 + Uglobals.DeltaDateTime
#     #
#     #     # See if a new event period has begun
#     #     if IsNewEventPeriod(Date1, Date2): TotalPeriods = TotalPeriods + 1
#     #
#     #     # If in a wet period, see if a new event has begun
#     #     if Nwet > 0: AddNewEvent(EventList, Date1)
#     #
#     #     # Get current values of the event variable (Y) and flow (Q)
#     #     Y = Uoutput.GetValue(Stats.ObjectType, Stats.VarIndex, T, theObject)
#     #     if Stats.FlowVarIndex == Stats.VarIndex: Q = Y
#     #     elif Stats.FlowVarIndex >= 0:
#     #         Q = Uoutput.GetValue(Stats.ObjectType, Stats.FlowVarIndex, T, theObject)
#     #     else: Q = 0
#     #
#     #     # Update event properties
#     #     Dry = Date2
#     #     if (Q != MISSING) and (Y != MISSING) and (Y > Stats.MinEventValue):
#     #       # Convert variables to absolute value
#     #       Q = Abs(Q)
#     #       Y = Abs(Y)
#     #
#     #       # Update the event volume (Vsum)
#     #       CF = QtimeToDays[Uglobals.Qunits]
#     #       if Stats.IsRainParam: CF = 24
#     #       Vsum += Q * Uglobals.DeltaDateTime * CF
#     #
#     #       # If computing mass load statistics, convert concentration to load
#     #       if Stats.IsQualParam and (Stats.StatsType >= stMeanLoad)
#     #      : Y = Y * Q * QtoMLD[Uglobals.Qunits]
#     #
#     #       # Start a new wet period
#     #       if Nwet == 0: WetStart = Date1
#     #       Inc(Nwet)
#     #       Wet = Date2
#     #
#     #       # Update sum and max. value
#     #       Ysum += Y
#     #       if Y > Ymax: Ymax = Y
#     #
#     #     # Update MainForm's progress bar
#     #     # MainForm.UpdateProgressBar(Progress, ProgStep)
#     #
#     #   # After processing all time periods, add the last wet period event
#     #   # to the event list
#     #   Dry = Stats.MinEventDelta/24.0 + Wet + 1.0                            #(5.0.012 - LR)
#     #   AddNewEvent(EventList, Uglobals.StartDateTime +
#     #       (Uglobals.Nperiods-1)*Uglobals.DeltaDateTime)
#     #
#     #   # Make sure we have at least one event period
#     #   if TotalPeriods == 0: TotalPeriods = 1
#     #
#     #   # Reclaim any unused capacity in the event list
#     #   EventList.Capacity = EventList.Count
#
#     # def IsNewEventPeriod_ori(self, Date1, Date2):
#     #   #-----------------------------------------------------------------------------
#     #   #  Determines if a new event period has begun or not.
#     #   #-----------------------------------------------------------------------------
#     #   #  Month1, Month2: Word
#     #   #  Year1, Year2  : Word
#     #   #  Day1, Day2    : Word
#     #
#     #   Result = False
#     #   DecodeDate(Date1, Year1, Month1, Day1)
#     #   DecodeDate(Date2, Year2, Month2, Day2)
#     #   if Stats.TimePeriod == tpVariable:
#     #     Result = True
#     #   elif Stats.TimePeriod == tpDaily:
#     #     if Day1 != Day2: Result = True
#     #   elif Stats.TimePeriod == tpMonthly:
#     #     if Month1 != Month2: Result = True
#     #   elif Stats.TimePeriod == tpAnnual:
#     #     if Year2 > Year1: Result = True
#     #   return Result
#
#     def InitConditions(self, NewDate):
#         #-----------------------------------------------------------------------------
#         #  Initializes the properties of an event.
#         #-----------------------------------------------------------------------------
#         self.WetStart = NewDate
#         self.WetEnd   = NewDate
#         self.DryEnd   = NewDate
#         self.Ysum   = 0
#         self.Ymax   = 0
#         self.Vsum   = 0
#         self.Nwet   = 0
#
#     def AddNewEvent(self, EventList, NewDate, StatsTimePeriodText): #: TList const, : TDateTime
#         #-----------------------------------------------------------------------------
#         #  Sees if a new event has occurred and adds it to the event list.
#         #-----------------------------------------------------------------------------
#         #  NewEvent : Boolean
#         #  AnEvent  : TStatsEvent
#         #  Year1,
#         #  Year2,
#         #  Day      : Word
#         #  Month1,
#         #  Month2   : Word
#
#         # Try to see if a new event has just occurred prior to the new date
#         NewEvent = False
#         if StatsTimePeriodText == "Event-dependent":
#             # For a variable event period, the current wet period constitutes
#             # a new event if the current time period is dry and the length of
#             # the dry period exceeds the stipulated minimum
#             if 24*(self.DryEnd - self.WetEnd) >= self.Stats.MinEventDelta:
#                 NewEvent = True
#
#         elif StatsTimePeriodText == "Daily":
#             # For daily events, a new event occurs if the new date (in integer days)
#             # exceeds the start of the current wet period (in integer days)
#             #if Floor(NewDate) > Floor(WetStart):
#             if NewDate > self.WetStart:
#                 NewEvent = True
#
#         elif StatsTimePeriodText == "Monthly":
#             # For monthly events, a new event occurs if the new month is different
#             # from that of the start of the current wet period
#             #DecodeDate(NewDate, Year1, Month1, Day)
#             #DecodeDate(WetStart, Year2, Month2, Day)
#             if NewDate.month != self.WetStart.month:
#                 NewEvent = True
#
#         elif StatsTimePeriodText == "Annual":
#             # For annual events, a new event occurs if the new year is different
#             # from that of the start of the current wet period
#             #DecodeDate(NewDate, Year1, Month1, Day)
#             #DecodeDate(WetStart, Year2, Month2, Day)
#             if NewDate.year != self.WetStart.year:
#                 NewEvent = True
#
#         # If a new event was found to occur,: add it to the event list
#         if NewEvent and (self.Nwet > 0) and (self.Vsum > self.Stats.MinEventVolume):
#             # Create a new event
#             AnEvent = TStatsEvent()
#             # Assign it a start date and duration
#             if self.stats.StatsTimePeriod == ETimePeriod.tpVariable:
#                 AnEvent.StartDate = self.WetStart
#                 AnEvent.Duration  = 24 * (self.WetEnd - self.WetStart)   # in hours
#                 EventPeriods += (self.WetEnd - self.WetStart) / Uglobals.DeltaDateTime
#             else:
#                 AnEvent.StartDate = self.WetStart
#                 AnEvent.Duration = self.Nwet * 24 * Uglobals.DeltaDateTime     # in hours
#                 EventPeriods += 1
#
#             # Assign the event a value
#             if Stats.StatsType == stMean:
#                 AnEvent.Value = Ysum/Nwet
#             elif Stats.StatsType == stPeak:
#                 AnEvent.Value = Ymax
#             elif Stats.StatsType == stTotal:
#                 AnEvent.Value = Vsum
#             elif Stats.StatsType == stDuration:
#                 AnEvent.Value = anEvent.Duration
#             elif Stats.StatsType == stDelta:
#                 AnEvent.Value = GetEventDelta(EventList)  # inter-event hours
#             elif Stats.StatsType == stMeanConcen or Stats.StatsType == stMeanLoad:
#                 AnEvent.Value = Ysum/Nwet
#             elif Stats.StatsType == stPeakConcen or Stats.StatsType == stPeakLoad:
#                 AnEvent.Value = Ymax
#             elif Stats.StatsType == stTotalLoad:
#                 AnEvent.Value = Ysum*Uglobals.DeltaDateTime
#             else:
#                 AnEvent.Value = 0.0
#
#         # Add the new event to the event list and initiialize the next event
#         EventList.Add(AnEvent)
#         InitConditions(NewDate)
#
#     def GetEventDelta(self, EventList): # Single
#         #-----------------------------------------------------------------------------
#         #  Computes the time between events for the most recent event and its
#         #  predeccessor.
#         #-----------------------------------------------------------------------------
#         #  LastEvent: TStatsEvent
#         #  LastStartDate : TDateTime
#         #  LastDate: TDateTime
#         #  Year1, Year2, Day, Month1, Month2 : Word
#
#         # Find the starting and ending dates of the previous event
#         if EventList.Count == 0:
#             LastStartDate = StartDateTime
#             LastDate = LastStartDate
#         else:
#             LastEvent = EventList.Items[EventList.Count-1]
#             LastStartDate = LastEvent.StartDate
#             LastDate = LastStartDate + LastEvent.Duration/24
#
#         if Stats.TimePeriod == tpVariable:
#             # For variable time period events, the inter-event time is the
#             # difference between the midpoints of the current event and the
#             # previous event
#             Result = 24 * ((WetStart - LastStartDate) + (Wet - LastDate)) / 2.0
#         elif Stats.TimePeriod == tpMonthly:
#             # For monthly events, the inter-event time is the difference
#             # between the start month of the current event and start month
#             # of the previous event
#             DecodeDate(LastStartDate, Year1, Month1, Day)
#             DecodeDate(WetStart, Year2, Month2, Day)
#             if Month2 >= Month1:
#                 Result = Month2 - Month1
#             else:
#                 Result = Month2 + (12 - Month1)
#         elif Stats.TimePeriod == tpAnnual:
#             # For annual events, the time is the difference between the starting
#             # year of the current and previous events
#             DecodeDate(LastStartDate, Year1, Month1, Day)
#             DecodeDate(WetStart, Year2, Month2, Day)
#             Result = Year2 - Year1
#         else:
#             # For daily events, the time is the difference between the starting
#             # whole day of the current and previous events
#             Result = Floor(WetStart) - Floor(LastStartDate)
#
#     def Compare(self, Event1, Event2): # Integer
#         #-----------------------------------------------------------------------------
#         # The comparison function used for sorting events
#         #-----------------------------------------------------------------------------
#         #  V1, V2: Single
#         V1 = TStatsEvent(Event1).Value
#         V2 = TStatsEvent(Event2).Value
#         if V1 < V2:
#             Result = 1
#         elif V1 > V2:
#             Result = -1
#         else:
#             Result = 0
#
#     def RankEvents(self, EventList):
#         #def RankEvents(EventList: TList)
#         # -----------------------------------------------------------------------------
#         #  Rank the events in the event list with respect to the event variable.
#         # -----------------------------------------------------------------------------
#         #  I  : Integer
#         #  N  : Integer
#         #  E1 : TStatsEvent
#         #  E2 : TStatsEvent
#         #  EventList is a list of objects of type: TStatsEvent
#         # Call the TList Sort method to sort the objects in the event list,
#         # using the Compare function as the comparison function.
#         # EventList.Sort(@Compare)
#         EventList.sort() #ToDo, need to figure out how to sort
#
#         # Starting from the  of the sorted event list, assign ranks to
#         #  each event (events with the same value have the same rank)
#         N = EventList.Count
#         if N > 0:
#             E1 = EventList.Items[N - 1]
#             E1.Rank = N
#             for I in xrange(N - 2, 0, -1):
#                 E2 = EventList.Items[I]
#                 if E1.Value == E2.Value:
#                     E2.Rank = E1.Rank
#                 else:
#                     E2.Rank = I + 1 #this means sort is in descending order
#                 E1 = E2 #or perhaps: E1 = EventList.Items[I]
#
#     def FindStats(self, EventList):
#         #def FindStats(EventList: TList var Results: TStatsResults):
#         #-----------------------------------------------------------------------------
#         #  Finds summary statistics of the identified events.
#         #-----------------------------------------------------------------------------
#         #  I:  Integer
#         #  J:  Integer
#         #  N:  Integer
#         #  A:  array[1..3] of Extended
#         #  G:  Extended
#         #  X:  Extended
#         #  T:  Extended
#         #  T1: Extended
#         #  T2: Extended
#         #  E:  TStatsEvent
#
#         I = 0
#         J = 0
#         N = 0
#         A = np.zeros(4)
#         G = 0.0
#         X = 0.0
#         T = 0.0
#         T1 = 0.0
#         T2 = 0.0
#         E = None #TStatsEvent
#
#         # Initialize results
#         Results = TStatsResults()
#         Results.EventFreq = 0
#         Results.Xmin = 0
#         Results.Xmax = 0
#         Results.StdDev = 0
#         Results.Mean = 0
#         Results.Skew = 0
#         # Exit if too few events
#         N = EventList.Count
#         if N < 1: return None
#
#         # Find max. and min. event values
#         E = EventList.Items[0]
#         Results.Xmax = E.Value
#         E = EventList.Items[N - 1]
#         Results.Xmin = E.Value
#
#         # Find event frequency
#         Results.EventFreq = self.EventPeriods / self.TotalPeriods
#
#         # Find sums of 1st three moments
#         for J in range(0, N-1):
#             E = EventList.Items[J]
#             X = E.Value
#             A[1] += X ** 1
#             A[2] += X ** 2
#             A[3] += X ** 3
#
#         # Apply formulas to find mean, std. dev., & skewness from  # sums of first three moments
#         G = 0
#         T = N
#         T1 = A[3] - 3 * A[1] * A[2] / T + 2 / T / T * (A[1] ** 3)
#         T2 = A[2] / T - (A[1] / T) ** 2
#         if T2 < 0:
#             T2 = 0
#         if T2 > 0:
#             T2 **= 1.5
#         if T2 != 0:
#             G = T1 / T2 / T
#         T1 = A[2] - A[1] * A[1] / T
#         if T1 < 0:
#             T1 = 0
#         T2 = T
#         if N > 1:
#             T2 = T - 1
#         Results.StdDev = (T1/T2) ** 0.5 #Sqrt(T1 / T2)
#         Results.Mean = A[1] / T
#         Results.Skew = G
#         return Results
#
#     def close():
#         pass
