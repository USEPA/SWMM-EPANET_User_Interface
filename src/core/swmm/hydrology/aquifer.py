from core.inputfile import Section
from core.metadata import Metadata


class Aquifer(Section):
    """Sub-surface groundwater area that models water infiltrating."""

    field_format = " {:16}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}"

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

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)  # set_text will call __init__ without new_text to do the initialization below
        else:
            Section.__init__(self)

            self.name = ''
            """User-assigned name."""

            self.porosity = ''
            """Volume of voids / total soil volume (volumetric fraction)."""

            self.wilting_point = ''
            """Soil moisture content at which plants cannot survive
                (volumetric fraction). """

            self.field_capacity = ''
            """Soil moisture content after all free water has drained off
                (volumetric fraction)."""

            self.conductivity = ''
            """Soil's saturated hydraulic conductivity (in/hr or mm/hr)."""

            self.conductivity_slope = ''
            """Average slope of log(conductivity) versus soil moisture deficit
                (porosity minus moisture content) curve (unitless)."""

            self.tension_slope = ''
            """Average slope of soil tension versus soil moisture content curve
                (inches or mm)."""

            self.upper_evaporation_fraction = ''
            """Fraction of total evaporation available for evapotranspiration
                in the upper unsaturated zone."""

            self.lower_evaporation_depth = ''
            """Maximum depth into the lower saturated zone over which
                evapotranspiration can occur (ft or m)."""

            self.lower_groundwater_loss_rate = ''
            """Rate of percolation from saturated zone to deep groundwater (in/hr or mm/hr)."""

            self.bottom_elevation = ''
            """Elevation of the bottom of the aquifer (ft or m)."""

            self.water_table_elevation = ''
            """Elevation of the water table in the aquifer
                at the start of the simulation (ft or m)."""

            self.unsaturated_zone_moisture = ''
            """Moisture content of the unsaturated upper zone of the aquifer
                at the start of the simulation (volumetric fraction)
                (cannot exceed soil porosity)."""

            self.upper_evaporation_pattern = ''
            """ID of monthly pattern of adjustments to upper evaporation fraction (optional)"""

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += Aquifer.field_format.format(self.name,
                                           self.porosity,
                                           self.wilting_point,
                                           self.field_capacity,
                                           self.conductivity,
                                           self.conductivity_slope,
                                           self.tension_slope,
                                           self.upper_evaporation_fraction,
                                           self.lower_evaporation_depth,
                                           self.lower_groundwater_loss_rate,
                                           self.bottom_elevation,
                                           self.water_table_elevation,
                                           self.unsaturated_zone_moisture,
                                           self.upper_evaporation_pattern)
        return inp

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 0:
            self.name = fields[0]
        if len(fields) > 1:
            self.porosity = fields[1]
        if len(fields) > 2:
            self.wilting_point = fields[2]
        if len(fields) > 3:
            self.field_capacity = fields[3]
        if len(fields) > 4:
            self.conductivity = fields[4]
        if len(fields) > 5:
            self.conductivity_slope = fields[5]
        if len(fields) > 6:
            self.tension_slope = fields[6]
        if len(fields) > 7:
            self.upper_evaporation_fraction = fields[7]
        if len(fields) > 8:
            self.lower_evaporation_depth = fields[8]
        if len(fields) > 9:
            self.lower_groundwater_loss_rate = fields[9]
        if len(fields) > 10:
            self.bottom_elevation = fields[10]
        if len(fields) > 11:
            self.water_table_elevation = fields[11]
        if len(fields) > 12:
            self.unsaturated_zone_moisture = fields[12]
        if len(fields) > 13:
            self.upper_evaporation_pattern = fields[13]
