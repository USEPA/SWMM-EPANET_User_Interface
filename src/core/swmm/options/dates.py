from enum import Enum

import core.inputfile


class Dates(core.inputfile.Section):
    """SWMM Date Options"""

    SECTION_NAME = "[OPTIONS]"

    # @staticmethod
    # def default():
    #     return Options(Options.SECTION_NAME, None, None, -1)

    def __init__(self, name, value, default_value, index):
        core.inputfile.Section.__init__(self, name, value, None, index)
        # TODO: parse "value" argument to extract values for each field, after setting default values below

        self.start_date = 0
        """Date when the simulation begins"""

        self.start_time = 0
        """Time of day on the starting date when the simulation begins"""

        self.end_date = 0
        """Date when the simulation is to end"""

        self.end_time = 0
        """Time of day on the ending date when the simulation will end"""

        self.report_start_date = 0
        """Date when reporting of results is to begin"""

        self.report_start_time = 0
        """Time of day on the report starting date when reporting is to begin"""

        self.sweep_start = None
        """Day of the year (month/day) when street sweeping operations begin"""

        self.sweep_end = None
        """Day of the year (month/day) when street sweeping operations end"""

        self.dry_days = 0
        """Number of days with no rainfall prior to the start of the simulation"""
