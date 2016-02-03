

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

        self.upper_evaporation_pattern = Pattern
        """Monthly pattern of adjustments to upper evaporation fraction (optional)"""



