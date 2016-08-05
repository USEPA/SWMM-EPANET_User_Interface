from enum import Enum
import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import Externals.swmm.outputapi.SMOutputWrapper as SMO

#-------------------------------------------------------------------}
#                    Unit:    Ustats.pas                            }
#                    Project: EPA SWMM                              }
#                    Version: 5.1                                   }
#                    Date:    12/2/13     (5.1.000)                 }
#                    Author:  L. Rossman                            }
#                                                                   }
#   This unit computes frequency statistics on the events that      }
#   have occurred during a simulation by calling the def       }
#   GetStats(StatsSel, EventList, Results). StatsSel is a           }
#   TStatsSelection record that defines the variable and type of    }
#   event being analyzed. EventList is a TList that will contain    }
#   and ordered listing of TStatsEvent records. Results is a        }
#   TStatsResults record that contains summary event statistics.    }
#-------------------------------------------------------------------}

class EObjectType(Enum):
    SUBCATCHMENTS = 0
    NODES = 1
    LINKS = 2
    SYS = 3
    UNKNOWN = 4

class MiscConstants():
    """
    # Miscellaneous global constants
    """
    FLOWTOL         = 0.005             #Zero flow tolerance
    MISSING         = -1.0e10           #Missing value
    NOXY            = -9999999          #Missing map coordinate

    #NOPOINT: TPoint = (X: -9999999; Y: -9999999)
    #NORECT: TRect   = (Left: -9999999; Top: -9999999; Right: -9999999; Bottom: -9999999)

    NODATE          = -693594   # 1/1/0001
    NA              = '#N/A'
    NONE            = 0
    NOVIEW          = 0
    PLUS            = 1
    MINUS           = 2
    DefMeasError    = 5
    DefIDIncrement  = 1
    DefMaxTrials    = 8
    DefMinSurfAreaUS = '12.557' #(ft2)
    DefMinSurfAreaSI = '1.14'   #(m2)
    DefHeadTolUS     = '0.005'  #(ft)
    DefHeadTolSI     = '0.0015' #(m)

class EStatsCat(Enum):
    BASIC = 0
    FLOW = 1
    QUAL = 2

class EPlotPosition(Enum):
    ppFrequency = 0
    ppYears = 1
    ppMonths = 2

class ETimePeriod(Enum):
    tpVariable = 0
    tpDaily = 1
    tpMonthly = 2
    tpAnnual = 3

class EStatsType(Enum): #TStatsType
    stMean = 0
    stPeak = 1
    stTotal = 2
    stDuration = 3
    stDelta = 4
    stMeanConcen = 5
    stPeakConcen = 6
    stMeanLoad = 7
    stPeakLoad = 8
    stTotalLoad = 9

class EStatsQuant(Enum):
    sqValue = 0
    sqLoad = 1

# Record which contains the properties of a single event
class TStatsEvent:
    def __init__(self):
        self.StartDate = datetime.now() #TDateTime
        self.Value = 0.0 #Single
        self.Duration = 0.0 # duration in milliseconds or seconds, Single
        self.Rank = 0 #Integer

# Record which contains information about what kind of report to generate
class TStatsSelection:
    def __init__(self):
        self.ObjectID       = ""               # ID of object being analyzed
        self.ObjectType     = EObjectType.UNKNOWN.value # Subcatch, Node or Link, or system
        self.ObjectTypeText = "UNKNOWN"        # Subcatch, Node or Link, or system
        self.Variable       = 0                # Index of variable analyzed, basic, flow, or qual
        self.VariableText   = "UNKNOWN"        # Text of variable analyzed, e.g. precipitation
        self.MinEventDelta  = 0.0              # Min. inter-event hours allowed
        self.MinEventValue  = 0.0              # Min. value for event to exist
        self.MinEventVolume = 0.0              # Min. flow vol. for event to exist
        self.PlotParameter  = 0.0              # e.g., = 0 for Weibull probability
        self.TimePeriod     = ETimePeriod.tpVariable # Event-depent, Daily, Monthly, Annual
        self.TimePeriodText = "UNKNOWN"        # Event-depent, Daily, Monthly, Annual
        self.PlotPosition   = EPlotPosition.ppFrequency.value # Frequency, Yearly, Monthly Ret. Per.
        self.StatsType      = EStatsType.stMean.value    # Index of Mean, Peak, Total, Duration, Delta
        self.StatsTypeText  = "UNKNOWN"        # Mean, Peak, Total, Duration, Delta
        self.VarIndex       = 0                # Index of variable analyzed in output file
        self.FlowVarIndex   = -1                # Index of flow variable in output file
        self.IsQualParam    = False            # True if variable is quality
        self.IsRainParam    = False            # True if variable is rainfall
        self.Tser           = None             # time series for the chosen output
        self.TserFlow       = None             # flow time series for the chosen quality output

# Record which contains statistical analysis results
class TStatsResults:
    def __init__(self):
        self.Duration       = 0                # Period of analysis (yrs or months)
        self.Timespan       = None             # relativedelta in datetime
        self.Mean           = 0.0              # Mean value
        self.StdDev         = 0.0              # Standard deviation
        self.Skew           = 0.0              # Skewness Coeff.
        self.Xmin           = 0.0              # Minmimum value
        self.Xmax           = 0.0              # Maximum value
        self.EventFreq      = 0.0              # Event frequency

# class Uglobals:
#     Nsubcatchs = 0  # Integer;             # Number of subcatchments
#     Nnodes = 0  # Integer;             # Number of nodes
#     Nlinks = 0  # Integer;             # Number of links
#     Npolluts = 0  # Integer;             # Number of pollutants
#     NsysViews = 0  # Integer;             # Number of system view variables
#     Qunits = 0  # Integer;             # Index of flow units
#     Zsubcatch = None  # PSingleArray;        # Values of subcatch view variable
#     Znode = None  # PSingleArray;        # Values of node view variable
#     Zlink = None  # PSingleArray;        # Values of link view variable
#     FlowDir = None  # PByteArray;          # Flow direction (+-) of each link
#     RunFlag = True  # Boolean;             # Analysis ran OK (True/False)
#     RunStatus = 0  # TRunStatus;          # Current run status flag
#     DynWaveFlag = False  # Boolean;             # Dynamic Wave routing used
#     Nperiods = 0  # LongInt;             # Total number of time periods
#     CurrentPeriod = 0  # LongInt;             # Time period being viewed
#     StartDateTime = pd.Timestamp('1900-01-01')  # TDateTime;           # Starting date/time
#     EndDateTime =  pd.Timestamp('1900-01-01') # TDateTime;           # Ending date/time
#     DeltaDateTime = 1  # TDateTime;           # Reporting time step (in days)
#     CurrentDateTime = pd.Timestamp('1900-01-01')  # TDateTime;          # Current date/time being viewed

class StatisticUtility(object):
    def __init__(self, output):
        self.TXT_FINDING_EVENTS = 'Finding events... '
        self.TXT_RANKING_EVENTS = 'Ranking events... '
        self.output = output #SMO.SwmmOutputObject(output)

        # The following arrays of flow conversion factors are for
        # CFS, GPM, MGD, CMS, LPS, and MLD, respectively.

        # Conversion factors for flow to million liters per day
        self.QtoMLD = (2.446589, 0.005451, 3.785414, 86.4, 0.0864, 1.0)

        # Conversion from flow time units to days
        self.QtimeToDays = (86400.0, 1440.0, 1.0, 86400.0, 86400.0, 1.0)
        #Notes (Fstats.pas):
        #RainVolumeText: array[0..5] of String = ('(in)', '(in)', '(in)', '(mm)', '(mm)', '(mm)');
        #FlowVolumeText: array[0..5] of String =
        #('(ft3)'  , '(gal)'    , '(Mgal)'  , '(m3)'  , '(liters)'  , '(Mliters)');
        #('(ft3/s)', '(gal/min)', '(Mgal/d)', '(m3/s)', '(liters/s)', '(Mliters/d)');

        self.Stats = None #TStatsSelection()  # Local copy of stat. event defn.

        #These are class wise temporary variables
        self.TotalPeriods = 0.0  # Total number of event periods
        self.EventPeriods = 0.0  # Number of time steps/periods within an event
        self.WetStart = None  # TDateTime  # Start date/time of wet period
        self.WetEnd = None  # TDateTime  # date/time of wet period
        self.DryEnd = None  # TDateTime  # date/time of following dry period
        self.Nwet = 0  # Number of wet periods in an event
        self.Ysum = 0.0  # Cumulative sum of event variable
        self.Ymax = 0.0  # Maximum value of event variable
        self.Vsum = 0.0  # Cumulative flow volume in an event
        self.deltaDateTime = 0.0 # trying to be the replacement of Uglobals.DeltaDateTime
        if self.output is not None:
            self.deltaDateTime = self.output.reportStepDays()

        pass

    def GetStats(self, StatsSel, EventList, Results):
        #Results = TStatsResults()
        #-----------------------------------------------------------------------------
        #  Analyzes simulation results to find the frequency of events as
        #  defined by the StatsSel argument. EventList contains a rank ordered
        #  listing of each event while Results contains summary event statistics.
        #-----------------------------------------------------------------------------
        self.Stats = StatsSel #TStatsSelection
        # Application.ProcessMessages
        # MainForm.ShowProgressBar(TXT_FINDING_EVENTS)
        self.Stats.Tser = self.output.get_time_series(self.Stats.ObjectTypeText, \
                                                self.Stats.ObjectID, \
                                                self.Stats.VariableText)

        self.FindDuration(EventList, Results)
        self.CategorizeStats(self.Stats)
        self.FindEvents(EventList, self.output, self.Stats)
        # MainForm.ShowProgressBar(TXT_RANKING_EVENTS)
        self.RankEvents(EventList, self.output, self.Tser)
        self.FindStats(EventList, Results)
        #StatsSel = self.Stats #don't think this is necessary
        #return Results

    def FindDuration(self, EventList, Results): # : TStatsResults)
        #-----------------------------------------------------------------------------
        #  Finds the duration of the total simulation period.
        #-----------------------------------------------------------------------------
        #  D1, D2: TDateTime
        #  Months: Integer
        #  Years:  Integer

        # Set the capacity of the EventList
        #EventList.Capacity = Uglobals.Nperiods

        # Evaluate start and days
        #D1 = Uglobals.StartDateTime
        #D2 = Uglobals.StartDateTime + (Uglobals.Nperiods-1)*Uglobals.DeltaDateTime
        D1 = self.output.StartDate      #Uglobals.StartDateTime
        #D2 = D1 + (self.output.num_periods - 1) * self.output.
        D2 = self.output.EndDate
        Results.Timespan = relativedelta(D2, D1)

        # Find duration in months & years
        #Months = Floor((D2 - D1)/(365/12) + 0.5)
        #Years  = Floor((D2 - D1)/365 + 0.5)
        # Assign value to PlotPosition
        if abs(Results.Timespan.years) < 3:
            #Stats.PlotPosition = ppMonths
            Results.Duration = Results.Timespan.months
        else:
            #Stats.PlotPosition = ppYears
            Results.Duration = Results.Timespan.years

    def FindEvents(self, EventList, output, aStats):  # TList
        # -----------------------------------------------------------------------------
        #  Identifies all events that occurred over the simulation period.
        # -----------------------------------------------------------------------------
        #  T       : LongInt
        #  Q       : Single
        #  Y       : Single
        #  CF      : Single
        #  Date1   : TDateTime
        #  Date2   : TDateTime
        #  Progress: LongInt
        #  ProgStep: LongInt
        #  theObject : TObject          # Reference to object being analyzed

        # Initialize total periods and number with events
        self.TotalPeriods = 0
        self.EventPeriods = 0

        # Initialize wet/dry period conditions
        #self.InitConditions(aStats.Tser.index[0])
        self.InitConditions(output.StartDate)

        # Find step size to use with the MainForm's ProgressBar
        # MainForm.ShowProgressBar('Reading Time Series:')
        # ProgStep = Nperiods div (MainForm.ProgressBar.Max div MainForm.ProgressBar.Step)
        # Progress = 0
        # Application.ProcessMessages
        # MainForm.ShowProgressBar(TXT_FINDING_EVENTS)
        #theObject = Uoutput.GetObject(Stats.ObjectType, Stats.ObjectID)

        # Examine each reporting period
        for T in xrange(0, output.num_periods): #range last element doesn't include the last number
            # Get the current and next reporting dates
            #Date1 = aStats.Tser.index[T]
            #Date2 = aStats.Tser.index[T + 1]
            Date1 = output.StartDate + relativedelta(days=T * self.deltaDateTime)
            Date2 = Date1 + relativedelta(days=self.deltaDateTime)

            #Confirmed: the Uglobals.DeltaDateTime is "Reporting time step (in days)"
            #self.deltaDateTime = abs(relativedelta(Date2, Date1).days)

            # See if a new event period has begun
            if self.IsNewEventPeriod(Date1, Date2, aStats.TimePeriod):
                self.TotalPeriods += 1

            # If in a wet period, see if a new event has begun
            if self.Nwet > 0:
                self.AddNewEvent(EventList, Date1, aStats)

            # Get current values of the event variable (Y) and flow (Q)
            Y = aStats.Tser[T] #ToDo: handle more than one time series in this dataframe
            if aStats.TserFlow is None:
                Q = 0
            else:
                Q = aStats.TserFlow[T]

            #Y = Uoutput.GetValue(Stats.ObjectType, Stats.VarIndex, T, theObject)
            #if self.Stats.FlowVarIndex == self.Stats.VarIndex:
            #    Q = Y
            #elif self.Stats.FlowVarIndex >= 0:
            #    Q = 0.0 #Uoutput.GetValue(Stats.ObjectType, Stats.FlowVarIndex, T, theObject)
            #else:
            #    Q = 0

            # Update event properties
            self.DryEnd = Date2
            if (Q != MiscConstants.MISSING and
                Y != MiscConstants.MISSING and
                Y > aStats.MinEventValue):
                # Convert variables to absolute value
                Q = abs(Q)
                Y = abs(Y)

                # Update the event volume (Vsum)
                #CF = self.QtimeToDays[Uglobals.Qunits]
                CF = self.QtimeToDays[self.output.flowUnits]
                if aStats.IsRainParam:
                    CF = 24
                #self.Vsum += Q * Uglobals.DeltaDateTime * CF
                self.Vsum += Q * self.deltaDateTime * CF

                # If computing mass load statistics, convert concentration to load
                if aStats.IsQualParam and aStats.StatsType >= EStatsType.stMeanLoad.value:
                    #Y = Y * Q * QtoMLD[Uglobals.Qunits]
                    Y *= Q * self.QtoMLD[self.output.flowUnits]

                # Start a new wet period
                if self.Nwet == 0:
                    self.WetStart = Date1
                self.Nwet += 1
                self.WetEnd = Date2

                # Update sum and max. value
                self.Ysum += Y
                if Y > self.Ymax:
                    self.Ymax = Y

            # Update MainForm's progress bar
            # MainForm.UpdateProgressBar(Progress, ProgStep)

        # After processing all time periods, add the last wet period event
        # to the event list
        #self.DryEnd = aStats.MinEventDelta / 24.0 + self.WetEnd + 1.0  # (5.0.012 - LR)
        self.DryEnd = self.WetEnd + relativedelta(days= 1, hours= aStats.MinEventDelta)
        #self.AddNewEvent(EventList, Uglobals.StartDateTime +
        #            (Uglobals.Nperiods - 1) * Uglobals.DeltaDateTime)
        lrdelta =  (self.output.num_periods - 1) * self.deltaDateTime
        lnewdate =  self.output.StartDate + relativedelta(days=lrdelta)

        self.AddNewEvent(EventList, lnewdate, aStats)

        # Make sure we have at least one event period
        if self.TotalPeriods == 0:
            self.TotalPeriods = 1

        # Reclaim any unused capacity in the event list
        #EventList.Capacity = EventList.Count

    def IsNewEventPeriod(self, Date1, Date2, StatsTimePeriod):
        # -----------------------------------------------------------------------------
        #  Determines if a new event period has begun or not.
        # -----------------------------------------------------------------------------
        #  Date1, Date2: the beginning and end of a time step, pandas TimeStamp
        #  StatTimePeriod:  user-specified
        #
        Result = False

        if StatsTimePeriod == ETimePeriod.tpVariable:
            Result = True
        elif StatsTimePeriod == ETimePeriod.tpDaily:
            if Date1.day != Date2.day:
                Result = True
        elif StatsTimePeriod == ETimePeriod.tpMonthly:
            if Date1.month != Date2.month:
                Result = True
        elif StatsTimePeriod == ETimePeriod.tpAnnual:
            if Date2.year > Date1.year:
                Result = True
        return Result

    def InitConditions(self, NewDate):
        # type: (object) -> object
        #-----------------------------------------------------------------------------
        #  Initializes the properties of an event.
        #-----------------------------------------------------------------------------
        self.WetStart = NewDate
        self.WetEnd   = NewDate
        self.DryEnd   = NewDate
        self.Ysum   = 0
        self.Ymax   = 0
        self.Vsum   = 0
        self.Nwet   = 0

    def AddNewEvent(self, EventList, NewDate, aStats): #: TList const, : TDateTime
        #-----------------------------------------------------------------------------
        #  Sees if a new event has occurred and adds it to the event list.
        #-----------------------------------------------------------------------------
        #  NewEvent : Boolean
        #  AnEvent  : TStatsEvent
        #  Year1,
        #  Year2,
        #  Day      : Word
        #  Month1,
        #  Month2   : Word

        # Try to see if a new event has just occurred prior to the new date
        NewEvent = False
        if "Event" in aStats.TimePeriodText:
            # For a variable event period, the current wet period constitutes
            # a new event if the current time period is dry and the length of
            # the dry period exceeds the stipulated minimum
            #if 24*(self.DryEnd - self.WetEnd) >= aStats.MinEventDelta:
            #    NewEvent = True
            rdiff = relativedelta(self.DryEnd, self.WetEnd)
            if (rdiff.days * 24.0 + rdiff.hours) >= aStats.MinEventDelta:
                NewEvent = True

        elif "Daily" in aStats.TimePeriodText:
            # For daily events, a new event occurs if the new date (in integer days)
            # exceeds the start of the current wet period (in integer days)
            #if Floor(NewDate) > Floor(WetStart):
            #if np.floor(NewDate) > np.floor(self.WetStart):
            rdiff = relativedelta(NewDate, self.WetStart)
            if rdiff.days >= 1:
                NewEvent = True

        elif "Monthly" in aStats.TimePeriodText:
            # For monthly events, a new event occurs if the new month is different
            # from that of the start of the current wet period
            #DecodeDate(NewDate, Year1, Month1, Day)
            #DecodeDate(WetStart, Year2, Month2, Day)
            if NewDate.month != self.WetStart.month:
                NewEvent = True

        elif "Annual" in aStats.TimePeriodText:
            # For annual events, a new event occurs if the new year is different
            # from that of the start of the current wet period
            #DecodeDate(NewDate, Year1, Month1, Day)
            #DecodeDate(WetStart, Year2, Month2, Day)
            if NewDate.year != self.WetStart.year:
                NewEvent = True

        # If a new event was found to occur,: add it to the event list
        if NewEvent and (self.Nwet > 0) and (self.Vsum > aStats.MinEventVolume):
            # Create a new event
            AnEvent = TStatsEvent()
            # Assign it a start date and duration
            # Looks like Uglobals.DeltaDateTime is in days
            if "Event" in aStats.StatsTimePeriodText:    # self.stats.StatsTimePeriod == ETimePeriod.tpVariable:
                AnEvent.StartDate = self.WetStart
                #AnEvent.Duration  = 24 * (self.WetEnd - self.WetStart)   # in hours
                rdiff = relativedelta(self.WetEnd, self.WetStart)
                AnEvent.Duration = rdiff.days * 24.0 + rdiff.hours
                #self.EventPeriods += (self.WetEnd - self.WetStart) / Uglobals.DeltaDateTime
                #self.EventPeriods += (self.WetEnd - self.WetStart) / self.deltaDateTime
                self.EventPeriods += (AnEvent.Duration / 24.0) / self.deltaDateTime
            else:
                AnEvent.StartDate = self.WetStart
                #AnEvent.Duration = self.Nwet * 24 * Uglobals.DeltaDateTime     # in hours
                AnEvent.Duration = self.Nwet * 24.0 * self.deltaDateTime # in hours
                self.EventPeriods += 1

            # Assign the event a value
            if aStats.StatsType == EStatsType.stMean.value:
                AnEvent.Value = self.Ysum/self.Nwet
            elif aStats.StatsType == EStatsType.stPeak.value:
                AnEvent.Value = self.Ymax
            elif aStats.StatsType == EStatsType.stTotal.value:
                AnEvent.Value = self.Vsum
            elif aStats.StatsType == EStatsType.stDuration.value:
                AnEvent.Value = AnEvent.Duration
            elif aStats.StatsType == EStatsType.stDelta.value:
                AnEvent.Value = self.GetEventDelta(EventList, aStats)  # inter-event hours
            elif aStats.StatsType == EStatsType.stMeanConcen.value or \
                 aStats.StatsType == EStatsType.stMeanLoad.value:
                AnEvent.Value = self.Ysum/self.Nwet
            elif aStats.StatsType == EStatsType.stPeakConcen.value or \
                 aStats.StatsType == EStatsType.stPeakLoad.value:
                AnEvent.Value = self.Ymax
            elif aStats.StatsType == EStatsType.stTotalLoad.value:
                #AnEvent.Value = self.Ysum * Uglobals.DeltaDateTime
                AnEvent.Value = self.Ysum * self.deltaDateTime
            else:
                AnEvent.Value = 0.0
            # Add the new event to the event list and initiialize the next event
            EventList.append(AnEvent)
            self.InitConditions(NewDate)

    def GetEventDelta(self, EventList, aStats): # Single
        #-----------------------------------------------------------------------------
        #  Computes the time between events for the most recent event and its
        #  predeccessor.
        #-----------------------------------------------------------------------------
        #  LastEvent: TStatsEvent
        #  LastStartDate : TDateTime
        #  LastDate: TDateTime
        #  Year1, Year2, Day, Month1, Month2 : Word

        # Find the starting and ending dates of the previous event
        if len(EventList) == 0:
            LastStartDate = self.output.StartDate
            LastDate = LastStartDate
        else:
            LastEvent = EventList.Items[len(EventList)-1]
            LastStartDate = LastEvent.StartDate
            #LastDate = LastStartDate + LastEvent.Duration/24.0
            LastDate = LastStartDate + relativedelta(hours=LastEvent.Duration)

        if aStats.TimePeriod == EStatsType.tpVariable.value:
            # For variable time period events, the inter-event time is the
            # difference between the midpoints of the current event and the
            # previous event
            #Result = 24 * ((self.WetStart - LastStartDate) + (self.WetEnd - LastDate)) / 2.0
            rdiff = relativedelta(self.WetStart, LastStartDate)
            Result = rdiff.days * 24.0 + rdiff.hours
            rdiff = relativedelta(self.WetEnd, LastDate)
            Result += rdiff.days * 24.0 + rdiff.hours
            Result /= 2.0

        elif aStats.TimePeriod == EStatsType.tpMonthly.value:
            # For monthly events, the inter-event time is the difference
            # between the start month of the current event and start month
            # of the previous event
            #DecodeDate(LastStartDate, Year1, Month1, Day)
            #DecodeDate(WetStart, Year2, Month2, Day)
            lmonth1 = LastStartDate.month
            lmonth2 = self.WetStart.month
            if lmonth2 >= lmonth1:
                Result = lmonth2 - lmonth1
            else:
                Result = lmonth2 + (12 - lmonth1)
        elif aStats.TimePeriod == EStatsType.tpAnnual.value:
            # For annual events, the time is the difference between the starting
            # year of the current and previous events
            #DecodeDate(LastStartDate, Year1, Month1, Day)
            #DecodeDate(WetStart, Year2, Month2, Day)
            lYear1 = LastStartDate.year
            lYear2 = self.WetStart.year
            Result = lYear2 - lYear1
        else:
            # For daily events, the time is the difference between the starting
            # whole day of the current and previous events
            #Result = np.floor(self.WetStart) - np.floor(LastStartDate)
            rdiff = relativedelta(self.WetStart, LastStartDate)
            Result = rdiff.days

        return Result

    def Compare(self, Event1, Event2): # Integer
        #-----------------------------------------------------------------------------
        # The comparison function used for sorting events
        #-----------------------------------------------------------------------------
        #  V1, V2: Single
        #Event1 = TStatsEvent() for debugging and document only
        #Event2 = TStatsEvent() for debugging and document only
        V1 = Event1.Value
        V2 = Event2.Value
        if V1 < V2:
            Result = 1
        elif V1 > V2:
            Result = -1
        else:
            Result = 0

        return Result

    def RankEvents(self, EventList):
        #def RankEvents(EventList: TList)
        # -----------------------------------------------------------------------------
        #  Rank the events in the event list with respect to the event variable.
        # -----------------------------------------------------------------------------
        #  I  : Integer
        #  N  : Integer
        #  E1 : TStatsEvent
        #  E2 : TStatsEvent
        #  EventList is a list of objects of type: TStatsEvent
        # Call the TList Sort method to sort the objects in the event list,
        # using the Compare function as the comparison function.
        #ToDo, how to sort
        # EventList.Sort(@Compare)
        EventList.Sort(self.Compare)
        #EventList.sort(key=lambda x: x.Value)
        #import operator as op
        #EventList.sort(key=op.attrgetter('Value'))

        # Starting from the  of the sorted event list, assign ranks to
        #  each event (events with the same value have the same rank)
        N = len(EventList)
        if N > 0:
            E1 = EventList.Items[N - 1]
            E1.Rank = N
            for I in xrange(N - 2, -1, -1):
                E2 = EventList.Items[I]
                if E1.Value == E2.Value:
                    E2.Rank = E1.Rank
                else:
                    E2.Rank = I + 1
                #ToDo: not sure what this means
                E1 = E2 #or perhaps: E1 = EventList.Items[I]

    def FindStats(self, EventList, Results):
        #def FindStats(EventList: TList var Results: TStatsResults):
        #-----------------------------------------------------------------------------
        #  Finds summary statistics of the identified events.
        #-----------------------------------------------------------------------------
        #  I:  Integer
        #  J:  Integer
        #  N:  Integer
        #  A:  array[1..3] of Extended
        #  G:  Extended
        #  X:  Extended
        #  T:  Extended
        #  T1: Extended
        #  T2: Extended
        #  E:  TStatsEvent

        I = 0
        J = 0
        N = 0
        A = np.zeros(4)
        G = 0.0
        X = 0.0
        T = 0.0
        T1 = 0.0
        T2 = 0.0
        E = None #TStatsEvent

       # Exit if too few events
        N = len(EventList)
        if N < 1: return None

        # Initialize results
        #Results = TStatsResults()
        Results.EventFreq = 0.0
        Results.Xmin = 0.0
        Results.Xmax = 0.0
        Results.StdDev = 0.0
        Results.Mean = 0.0
        Results.Skew = 0.0

        # Find max. and min. event values
        # (obviously this is AFTER the events are sorted)
        E = EventList[0]
        Results.Xmax = E.Value
        E = EventList[N - 1]
        Results.Xmin = E.Value

        # Find event frequency
        Results.EventFreq = self.EventPeriods * 1.0 / (self.TotalPeriods * 1.0)

        # Find sums of 1st three moments
        for J in xrange(0, N):
            E = EventList[J]
            X = E.Value
            A[1] += X ** 1
            A[2] += X ** 2
            A[3] += X ** 3

        # Apply formulas to find mean, std. dev., & skewness from  # sums of first three moments
        G = 0
        T = N
        T1 = A[3] - 3 * A[1] * A[2] / T + 2 / T / T * (A[1] ** 3)
        T2 = A[2] / T - (A[1] / T) ** 2
        if T2 < 0:
            T2 = 0
        if T2 > 0:
            T2 **= 1.5
        if T2 != 0:
            G = T1 / T2 / T
        T1 = A[2] - A[1] * A[1] / T
        if T1 < 0:
            T1 = 0
        T2 = T
        if N > 1:
            T2 = T - 1
        Results.StdDev = (T1/T2) ** 0.5 #Sqrt(T1 / T2)
        Results.Mean = A[1] / T
        Results.Skew = G
        #return Results

    def CategorizeStats(self, aStats):
        '''
        This routine examines and then categorizes the output attribute in terms of whether
        it is quality related (ie a pollutant) or rain related attribute.
        For quality attribute, need to find the corresponding flow for use of statistic calculation
        related to volume and loading of the pollutant
        Logic originates from Dstats.pas, GetVariableTypes()
        Args:
            aStats: a TStatsSelection object that contains the conditions for a statistic
        Returns:
            Doesn't return anything, but instead set the 'aStats' IsQualParam, IsRainParam parameter
            also retrieve its corresponding flow
        '''
        #aStats = TStatsSelection()
        if aStats.ObjectType == EObjectType.SUBCATCHMENTS.value:
            if aStats.Variable >= len(SMO.SwmmOutputSubcatchment.attributes) - 1:
                aStats.IsQualParam = True
                aStats.TserFlow = self.output.get_time_series(self.Stats.ObjectTypeText, \
                                                      self.Stats.ObjectID, \
                                                      "Runoff")
            else:
                aStats.TserFlow = aStats.Tser
                if "Precip" in aStats.VariableText or \
                   "Evap" in aStats.VariableText or \
                   "Infil" in aStats.VariableText:
                   aStats.IsRainParam = True

        elif aStats.ObjectType == EObjectType.NODES.value:
            if aStats.Variable >= len(SMO.SwmmOutputNode.attributes) - 1:
                aStats.IsQualParam = True

            if "Inflow" in aStats.VariableText or "Overflow" in aStats.VariableText:
                aStats.TserFlow = aStats.Tser

        elif aStats.ObjectType == EObjectType.LINKS.value:
            if aStats.Variable >= len(SMO.SwmmOutputLink.attributes) - 1:
                aStats.IsQualParam = True

            self.Stats.TserFlow = self.output.get_time_series(self.Stats.ObjectTypeText, \
                                                              self.Stats.ObjectID, \
                                                              "Flow")

        elif aStats.ObjectType == EObjectType.SYS.value:
            if "Precip" in aStats.VariableText or \
               "Rain" in aStats.VariableText or \
               "Evap" in aStats.VariableText or \
               "Infil" in aStats.VariableText:
                aStats.IsRainParam = True

            aStats.TserFlow = aStats.Tser


    def close(self):
        pass
