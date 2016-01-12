class HortonInfiltration:
    """Horton Infiltration parameters"""
    def __init__(self):
        self.max_rate = 0.0
        """Maximum infiltration rate on Horton curve (in/hr or mm/hr)"""

        self.min_rate = 0.0
        """Minimum infiltration rate on Horton curve (in/hr or mm/hr)."""

        self.decay = 0.0
        """Decay rate constant of Horton curve (1/hr)."""

        self.dry_time = 0.0
        """Time it takes for fully saturated soil to dry (days)."""

        self.max_volume = 0.0
        """Maximum infiltration volume possible (in or mm)."""


class GreenAmptInfiltration:
    """Green-Ampt Infiltration parameters"""
    def __init__(self):
        self.suction = 0.0
        """Soil capillary suction (in or mm)."""

        self.hydraulic_conductivity = 0.0
        """Soil saturated hydraulic conductivity (in/hr or mm/hr)."""

        self.initial_moisture_deficit = 0.0
        """Initial soil moisture deficit (volume of voids / total volume)."""


class CurveNumberInfiltration:
    """Curve Number Infiltration parameters"""
    def __init__(self):
        self.curve_number = None
        """SCS Curve Number"""

        self.dry_days = 0
        """Time it takes for fully saturated soil to dry (days)."""


class Aquifer:
    """Sub-surface groundwater area that models water infiltrating."""

    def __init__(self, name):
        self.name = name
        """User-assigned name."""

        self.porosity = 0.0
        """Volume of voids / total soil volume (volumetric fraction)."""

        self.wilting_point = 0.0
        """Soil moisture content at which plants cannot survive
            (volumetric fraction). """

        self.field_capacity = 0.0
        """Soil moisture content after all free water has drained off
            (volumetric fraction)."""

        self.conductivity = 0.0
        """Soil's saturated hydraulic conductivity (in/hr or mm/hr)."""

        self.conductivity_slope = 0.0
        """Average slope of log(conductivity) versus soil moisture deficit
            (porosity minus moisture content) curve (unitless)."""

        self.tension_slope = 0.0
        """Average slope of soil tension versus soil moisture content curve
            (inches or mm)."""
        self.upper_evaporation_fraction = 0.0
        """Fraction of total evaporation available for evapotranspiration
            in the upper unsaturated zone."""

        self.lower_evaporation_depth = 0.0
        """Maximum depth into the lower saturated zone over which
            evapotranspiration can occur (ft or m)."""

        self.lower_groundwater_loss_rate = 0.0
        """Rate of percolation from saturated zone to deep groundwater (in/hr or mm/hr)."""

        self.bottom_elevation = 0.0
        """Elevation of the bottom of the aquifer (ft or m)."""

        self.water_table_elevation = 0.0
        """Elevation of the water table in the aquifer
            at the start of the simulation (ft or m)."""

        self.unsaturated_zone_moisture = 0.0
        """Moisture content of the unsaturated upper zone of the aquifer
            at the start of the simulation (volumetric fraction)
            (cannot exceed soil porosity)."""


class Groundwater:
    """Link a subcatchment to an aquifer and to a drainage system node"""

    def __init__(self, aquifer, receiving_node):
        self.aquifer = aquifer
        """Aquifer that supplies groundwater. None = no groundwater flow."""

        self.receiving_node = receiving_node
        """Node that receives groundwater from the aquifer."""

        self.surface_elevation = 0.0
        """Elevation of ground surface for the subcatchment
            that lies above the aquifer (feet or meters)."""

        self.groundwater_flow_coefficient = 0.0
        """Value of A1 in the groundwater flow formula."""

        self.groundwater_flow_exponent = 0.0
        """Value of B1 in the groundwater flow formula."""

        self.surface_water_flow_coefficient = 0.0
        """Value of A2 in the groundwater flow formula."""

        self.surface_water_flow_exponent = 0.0
        """Value of B2 in the groundwater flow formula."""

        self.surface_gw_interaction_coefficient = 0.0
        """Value of A3 in the groundwater flow formula."""

        self.fixed_surface_water_depth = 0.0
        """Fixed depth of surface water at the receiving node (feet or meters)
            (set to zero if surface water depth will vary
             as computed by flow routing).
            This value is used to compute HSW."""

        self.threshold_groundwater_elevation = 0.0
        """Groundwater elevation that must be reached before any flow occurs
            (feet or meters).
            Leave blank to use the receiving node's invert elevation."""
