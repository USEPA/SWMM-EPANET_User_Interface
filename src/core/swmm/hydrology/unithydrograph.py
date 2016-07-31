from core.project_base import Section


class UnitHydrographEntry:
    def __init__(self):
        self.hydrograph_month = ''
        """str: Month for which hydrograph parameters will be defined"""

        self.term = ''
        """str: term of RDII response: SHORT or MEDIUM or LONG """

        self.response_ratio = ''
        """str: Parameter R"""

        self.time_to_peak = ''
        """str: Parameter T (hours)"""

        self.recession_limb_ratio = ''
        """str: Parameter K"""

        self.initial_abstraction_depth = ''
        """str: Maximum depth of initial abstraction available (Dmax)"""

        self.initial_abstraction_rate = ''
        """str: Rate at which any utilized initial abstraction is made available again (Drec)"""

        self.initial_abstraction_amount = ''
        """str: Amount of initial abstraction already utilized at the start of the simulation (D0)"""

class UnitHydrograph(Section):
    """Specifies the shapes of the triangular unit hydrographs that determine the amount of
        rainfall-dependent infiltration/inflow (RDII) entering the drainage system"""

    first_row_format = "{:16}\t{:16}"

    def __init__(self):
        Section.__init__(self)

        self.name = "Unnamed"
        """str: Name assigned to this Unit Hydrograph group"""

        self.rain_gage_id = ''
        """str: Name of the rain gage that supplies rainfall data to the unit hydrographs in the group"""

        self.value = []
        """UnitHydrographEntry: each active combination of parameters for this unit hydrograph"""


