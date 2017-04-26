from core.project_base import Section
from core.metadata import Metadata


class Dates(Section):
    """SWMM Date Options"""

    SECTION_NAME = "[OPTIONS]"

    #    attribute,           input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("start_date",        "START_DATE"),
        ("start_time",        "START_TIME"),
        ("report_start_date", "REPORT_START_DATE"),
        ("report_start_time", "REPORT_START_TIME"),
        ("end_date",          "END_DATE"),
        ("end_time",          "END_TIME"),
        ("sweep_start",       "SWEEP_START"),
        ("sweep_end",         "SWEEP_END"),
        ("dry_days",          "DRY_DAYS")))
    """Mapping between attribute name and name used in input file"""

    DATE_FORMAT = "MM/dd/yyyy"
    DATE_SWEEP_FORMAT = "MM/dd"
    TIME_FORMAT = "hh:mm:ss"

    def __init__(self):
        Section.__init__(self)

        self.start_date = "1/1/2002"
        """Date when the simulation begins"""

        self.start_time = "0:00"
        """Time of day on the starting date when the simulation begins"""

        self.end_date = "1/1/2002"
        """Date when the simulation is to end"""

        self.end_time = "24:00"
        """Time of day on the ending date when the simulation will end"""

        self.report_start_date = "1/1/2002"
        """Date when reporting of results is to begin"""

        self.report_start_time = "0:00"
        """Time of day on the report starting date when reporting is to begin"""

        self.sweep_start = "1/1"
        """Day of the year (month/day) when street sweeping operations begin"""

        self.sweep_end = "12/31"
        """Day of the year (month/day) when street sweeping operations end"""

        self.dry_days = 0.0
        """Number of days with no rainfall prior to the start of the simulation"""
