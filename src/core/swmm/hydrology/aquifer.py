from core.project_base import Section
from core.metadata import Metadata


class Aquifer(Section):
    """Sub-surface groundwater area that models water infiltrating."""


    #    attribute,             input_name, label,              default,      english,    metric, hint
    metadata = Metadata((
        ("name",                        '', "Aquifer Name",          "",      '',         '',
         "User-assigned aquifer name."),
        ("porosity",                    '', "Porosity",              "0.5",   "fraction", "fraction",
         "Volume of voids / total soil volume."),
        ("wilting_point",               '', "Wilting Point",         "0.15",  "fraction", "fraction",
         "Residual moisture content of a completely dry soil."),
        ("field_capacity",              '', "Field Capacity",        "0.30",  "fraction", "fraction",
         "Soil moisture content after all free water has drained off."),
        ("conductivity",                '', "Conductivity",          "5.0",   "in/hr",    "mm/hr",
         "Soil's saturated hydraulic conductivity."),
        ("conductivity_slope",          '', "Conductivity Slope",    "10.0",  '',         '',
         "Slope of log(conductivity) v. soil moisture deficit curve."),
        ("tension_slope",               '', "Tension Slope",         "15.0",  '',         '',
         "Slope of soil tension v. soil moisture content curve."),
        ("upper_evaporation_fraction",  '', "Upper Evap. Fraction",  "0.35",  '',         '',
         "Fraction of total evaporation available for upper unsaturated zone."),
        ("lower_evaporation_depth",     '', "Lower Evap. Depth",     "14.0",  "ft",       "m",
         "Depth into saturated zone over which evaporation can occur."),
        ("lower_groundwater_loss_rate", '', "Lower GW Loss Rate",    "0.002", "in/hr",    "mm/hr",
         "Rate of seepage to deep groundwater when aquifer is completely saturated."),
        ("bottom_elevation",            '', "Bottom Elevation",      "0.0",   "ft",       "m",
         "Elevation of the bottom of the aquifer."),
        ("water_table_elevation",       '', "Water Table Elevation", "10.0",  "ft",       "m",
         "Initial water table elevation."),
        ("unsaturated_zone_moisture",   '', "Unsat. Zone Moisture",  "0.30",  "fraction", "fraction",
         "Initial moisture content of the unsaturated upper zone."),
        ("upper_evaporation_pattern",   '', "Upper Evap. Pattern",   "",      '',         '',
         "Monthly pattern of adjustments to upper evaporation fraction. (optional)")
    ))

    def __init__(self):
        Section.__init__(self)

        self.name = "Unnamed"
        """User-assigned name."""

        self.porosity = "0.5"
        """Volume of voids / total soil volume (volumetric fraction)."""

        self.wilting_point = "0.15"
        """Soil moisture content at which plants cannot survive
            (volumetric fraction). """

        self.field_capacity = "0.30"
        """Soil moisture content after all free water has drained off
            (volumetric fraction)."""

        self.conductivity = "5.0"
        """Soil's saturated hydraulic conductivity (in/hr or mm/hr)."""

        self.conductivity_slope = "10.0"
        """Average slope of log(conductivity) versus soil moisture deficit
            (porosity minus moisture content) curve (unitless)."""

        self.tension_slope = "15.0"
        """Average slope of soil tension versus soil moisture content curve
            (inches or mm)."""

        self.upper_evaporation_fraction = "0.35"
        """Fraction of total evaporation available for evapotranspiration
            in the upper unsaturated zone."""

        self.lower_evaporation_depth = "14.0"
        """Maximum depth into the lower saturated zone over which
            evapotranspiration can occur (ft or m)."""

        self.lower_groundwater_loss_rate = "0.002"
        """Rate of percolation from saturated zone to deep groundwater (in/hr or mm/hr)."""

        self.bottom_elevation = "0.0"
        """Elevation of the bottom of the aquifer (ft or m)."""

        self.water_table_elevation = "10.0"
        """Elevation of the water table in the aquifer
            at the start of the simulation (ft or m)."""

        self.unsaturated_zone_moisture = "0.30"
        """Moisture content of the unsaturated upper zone of the aquifer
            at the start of the simulation (volumetric fraction)
            (cannot exceed soil porosity)."""

        self.upper_evaporation_pattern = ''
        """ID of monthly pattern of adjustments to upper evaporation fraction (optional)"""
