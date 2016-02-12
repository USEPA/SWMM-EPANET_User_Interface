

class UnitHydrograph:
    """Specifies the shapes of the triangular unit hydrographs that determine the amount of
        rainfall-dependent infiltration/inflow (RDII) entering the drainage system"""

    def __init__(self):
        self.group_name = "Unnamed"
        """str: Name assigned to the UH Group"""

        self.rain_gage_used = ""
        """str: Name of the rain gage that supplies rainfall data to the unit hydrographs in the group"""

        self.hydrograph_months = ""
        """str: Month for which hydrograph parameters will be defined"""

        self.unit_hydrograph_values = ()
        """tuple: R-T-K shape parameters for each set of unit hydrographs in selected months of the year"""

        self.initial_abstraction_depth = 0.0
        """float: Maximum depth of initial abstraction available"""

        self.initial_abstraction_rate = 0.0
        """float: Rate at which any utilized initial abstraction is made available again"""

        self.initial_abstraction_amount = 0.0
        """float: Amount of initial abstraction that has already been utilized at the start of the simulation"""



