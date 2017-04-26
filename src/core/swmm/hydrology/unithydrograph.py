from core.project_base import Section


class UnitHydrographEntry:
    def __init__(self):

        ## str: Month for which hydrograph parameters will be defined
        self.hydrograph_month = ''

        ## str: term of RDII response: SHORT or MEDIUM or LONG
        self.term = "SHORT"

        ## str: Parameter R
        self.response_ratio = '0'

        ## str: Parameter T (hours)
        self.time_to_peak = '0'

        ## str: Parameter K
        self.recession_limb_ratio = '0'

        ## str: Maximum depth of initial abstraction available (Dmax)
        self.initial_abstraction_depth = ''

        ## str: Rate at which any utilized initial abstraction is made available again (Drec)
        self.initial_abstraction_rate = ''

        ## str: Amount of initial abstraction already utilized at the start of the simulation (D0)
        self.initial_abstraction_amount = ''


class UnitHydrograph(Section):
    """Specifies the shapes of the triangular unit hydrographs that determine the amount of
        rainfall-dependent infiltration/inflow (RDII) entering the drainage system"""

    first_row_format = "{:16}\t{:16}"

    def __init__(self):
        Section.__init__(self)

        ## str: Name assigned to this Unit Hydrograph group
        self.name = "Unnamed"

        ## str: Name of the rain gage that supplies rainfall data to the unit hydrographs in the group
        self.rain_gage_name = "None"

        ## UnitHydrographEntry: each active combination of parameters for this unit hydrograph
        self.value = []


