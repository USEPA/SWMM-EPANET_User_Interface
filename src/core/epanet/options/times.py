from enum import Enum
from core.project_base import Section
from core.metadata import Metadata


class StatisticOptions(Enum):
    """statistical post-processing setting"""
    NONE = 1
    AVERAGED = 2
    MINIMUM = 3
    MAXIMUM = 4
    RANGE = 5


class TimesOptions(Section):
    """Defines various time step parameters used in the simulation"""

    SECTION_NAME = "[TIMES]"

    #    attribute,            input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("duration", "Duration"),
        ("hydraulic_timestep", "Hydraulic Timestep"),
        ("quality_timestep", "Quality Timestep"),
        ("rule_timestep", "Rule Timestep"),
        ("pattern_timestep", "Pattern Timestep"),
        ("pattern_start", "Pattern Start"),
        ("report_timestep", "Report Timestep"),
        ("report_start", "Report Start"),
        ("start_clocktime", "Start ClockTime"),
        ("statistic", "Statistic")))
    """Mapping between attribute name and name used in input file"""

    def __init__(self):
        Section.__init__(self)

        ## duration of the simulation; the default of zero runs a single period snapshot analysis.
        self.duration = "0"			            # hours:minutes

        ## determines how often a new hydraulic state of the network is computed
        self.hydraulic_timestep = "1:00"	    # hours:minutes

        ## time step used to track changes in water quality throughout the network
        self.quality_timestep = "0:05"		    # hours:minutes

        ## ime step used to check for changes in system status due to activation of rule-based controls
        self.rule_timestep = "0:05" 		    # hours:minutes

        ## interval between time periods in all time patterns
        self.pattern_timestep = "1:00" 		    # hours:minutes

        ## time offset at which all patterns will start
        self.pattern_start = "0:00"	            # hours:minutes

        ## time interval between which output results are reported
        self.report_timestep = "1:00"		    # hours:minutes

        ## length of time into the simulation at which output results begin to be reported
        self.report_start = "0:00"	            # hours:minutes

        ## time of day (e.g., 3:00 PM) at which the simulation begins
        self.start_clocktime = "12 am"		    # hours:minutes AM/PM

        ## determines what kind of statistical post-processing to do on simulation results
        self.statistic = StatisticOptions.NONE  # NONE/AVERAGED/MINIMUM/MAXIMUM/RANGE

