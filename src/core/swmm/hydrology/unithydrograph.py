import core.swmm.hydrology.raingage


class UnitHydrograph:
    """Specifies the shapes of the triangular unit hydrographs that determine the amount of
        rainfall-dependent infiltration/inflow (RDII) entering the drainage system"""

    def __init__(self, name):
        self.group_name = name
        """Name assigned to the UH Group"""

        self.rain_gage_used = core.swmm.hydrology.raingage.RainGage()
        """Name of the rain gage that supplies rainfall data to the unit hydrographs in the group"""

        self.hydrograph_months = ""
        """Month for which hydrograph parameters will be defined"""

        self.unit_hydrograph_values = ()
        """R-T-K shape parameters for each set of unit hydrographs in selected months of the year"""

        self.initial_abstraction_depth = 0.0
        """Maximum depth of initial abstraction available"""

        self.initial_abstraction_rate = 0.0
        """Rate at which any utilized initial abstraction is made available again"""

        self.initial_abstraction_amount = 0.0
        """Amount of initial abstraction that has already been utilized at the start of the simulation"""



