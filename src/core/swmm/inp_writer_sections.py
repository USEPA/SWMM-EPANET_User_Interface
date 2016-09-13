import traceback
from enum import Enum
from core.coordinate import Coordinate
from core.project_base import Section
from core.swmm.curves import CurveType
from core.swmm.curves import Curve
from core.swmm.patterns import PatternType
from core.swmm.patterns import Pattern
from core.swmm.quality import BuildupFunction
from core.swmm.quality import Normalizer
from core.swmm.quality import WashoffFunction
from core.swmm.quality import ConcentrationUnits
from core.swmm.quality import ConcentrationUnitLabels
from core.swmm.quality import Landuse
from core.swmm.quality import Buildup
from core.swmm.quality import Washoff
from core.swmm.quality import Pollutant
from core.swmm.timeseries import TimeSeries
from core.swmm.title import Title
from core.swmm.climatology import TemperatureSource
from core.swmm.climatology import EvaporationFormat
from core.swmm.climatology import WindSource
from core.swmm.climatology import Temperature
from core.swmm.climatology import Evaporation
from core.swmm.climatology import WindSpeed
from core.swmm.climatology import SnowMelt
from core.swmm.climatology import ArealDepletion
from core.swmm.climatology import Adjustments
from core.swmm.hydraulics.link import Link
from core.swmm.hydraulics.link import Conduit
from core.swmm.hydraulics.link import Pump
from core.swmm.hydraulics.link import OrificeType
from core.swmm.hydraulics.link import Orifice
from core.swmm.hydraulics.link import WeirType
from core.swmm.hydraulics.link import RoadSurfaceType
from core.swmm.hydraulics.link import Weir
from core.swmm.hydraulics.link import OutletCurveType
from core.swmm.hydraulics.link import Outlet
from core.swmm.hydraulics.link import CrossSectionShape
from core.swmm.hydraulics.link import CrossSection
from core.swmm.hydraulics.link import Transects
from core.swmm.hydraulics.link import Transect
from core.swmm.hydraulics.node import Junction
from core.swmm.hydraulics.node import OutfallType
from core.swmm.hydraulics.node import Outfall
from core.swmm.hydraulics.node import FlowDividerType
from core.swmm.hydraulics.node import WeirDivider
from core.swmm.hydraulics.node import Divider
from core.swmm.hydraulics.node import StorageCurveType
from core.swmm.hydraulics.node import StorageUnit
from core.swmm.hydraulics.node import DirectInflowType
from core.swmm.hydraulics.node import DirectInflow
from core.swmm.hydraulics.node import DryWeatherInflow
from core.swmm.hydraulics.node import RDIInflow
from core.swmm.hydraulics.node import Treatment
from core.swmm.hydrology.aquifer import Aquifer
from core.swmm.hydrology.lidcontrol import LIDType
from core.swmm.hydrology.lidcontrol import LIDControl
from core.swmm.hydrology.snowpack import SnowPack
from core.swmm.hydrology.subcatchment import Routing
from core.swmm.hydrology.subcatchment import Subcatchment
from core.swmm.hydrology.subcatchment import HortonInfiltration
from core.swmm.hydrology.subcatchment import GreenAmptInfiltration
from core.swmm.hydrology.subcatchment import CurveNumberInfiltration
from core.swmm.hydrology.subcatchment import Groundwater
from core.swmm.hydrology.subcatchment import LIDUsage
from core.swmm.hydrology.subcatchment import Coverage
from core.swmm.hydrology.subcatchment import Coverages
from core.swmm.hydrology.subcatchment import InitialLoading
from core.swmm.hydrology.subcatchment import InitialLoadings
from core.swmm.hydrology.unithydrograph import UnitHydrographEntry
from core.swmm.hydrology.unithydrograph import UnitHydrograph
from core.swmm.options.backdrop import BackdropOptions
from core.swmm.options.general import FlowUnits
from core.swmm.options.general import FlowRouting
from core.swmm.options.general import LinkOffsets
from core.swmm.options.general import General
from core.swmm.options.map import MapUnits
from core.swmm.options.map import MapOptions
from core.swmm.options.report import Report
from core.inp_writer_base import SectionWriter


class CoordinateWriter(SectionWriter):
    """Text version of a coordinate pair's name and X, Y"""

    field_format = " {:16}\t{:10}\t{:10}"

    @staticmethod
    def as_text(coordinate):
        """format contents of this item for writing to file"""
        inp = CoordinateWriter.field_format.format(coordinate.name, coordinate.x, coordinate.y)
        if hasattr(coordinate, "comment") and coordinate.comment:
            inp += "  # " + coordinate.comment
        return inp


class LabelWriter(SectionWriter):
    field_format = ' {:16}\t{:16}\t"{}"\t"{}"\t"{}"\t{}\t{}\t{}'

    @staticmethod
    def as_text(label):
        if label.bold:
            bold = '1'
        else:
            bold = '0'
        if label.italic:
            italic = '1'
        else:
            italic = '0'
        return LabelWriter.field_format.format(label.x, label.y, label.name,
                                               label.anchor_name, label.font, label.size, bold, italic)
        return label


class CurveWriter(SectionWriter):
    """Defines data curves and their X,Y points"""

    field_format = " {:16}\t{:10}\t{:10}\t{:10}\n"

    @staticmethod
    def as_text(curve):
        """format contents of this item for writing to file"""
        inp = ''
        if curve.comment:
            inp = curve.comment + '\n'
        type_name = curve.curve_type.name
        for xy in curve.curve_xy:
            inp += CurveWriter.field_format.format(curve.name, type_name, xy[0], xy[1])
            type_name = "          "
        return inp


class PatternWriter(SectionWriter):
    """Pattern multipliers define how some base quantity is adjusted for each time period"""
    @staticmethod
    def as_text(pattern):
        """format contents of this item for writing to file"""
        count = 6
        section_text = ''
        pattern_text = pattern.pattern_type.name
        for line in pattern.description.splitlines(True):
            section_text += ';' + line
        for multiplier in pattern.multipliers:
            if count == 6:        # add ID to first line and break lines before they get too long
                if section_text:  # If there are already values added, put next value on a new line
                    section_text += '\n'
                section_text += " {:16}{:10}".format(pattern.name, pattern_text)
                pattern_text = ''
                count = 0
            section_text += "\t{:5}".format(multiplier)
            count += 1
        return section_text


class LanduseWriter(SectionWriter):
    """Identifies the various categories of land uses within the drainage area. Each subcatchment area
        can be assigned a different mix of land uses. Each land use can be subjected to a different
        street sweeping schedule."""

    field_format = " {:15}\t{:10}\t{:10}\t{:10}"

    @staticmethod
    def as_text(landuse):
        inp = ''
        if landuse.comment:
            inp = landuse.comment + '\n'
        inp += LanduseWriter.field_format.format(landuse.name,
                                                 landuse.street_sweeping_interval,
                                                 landuse.street_sweeping_availability,
                                                 landuse.last_swept)
        return inp


class BuildupWriter(SectionWriter):
    """Specifies the rate at which pollutants build up over different land uses between rain events."""

    field_format = "{:16}\t{:16}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}"

    """A different set of buildup property labels is used depending on the External Time Series buildup option"""

    @staticmethod
    def as_text(buildup):
        c1 = buildup.max_buildup
        if buildup.function == BuildupFunction.EXT:
            c2 = buildup.scaling_factor
            c3 = buildup.timeseries
        else:
            c2 = buildup.rate_constant
            c3 = buildup.power_sat_constant
        return BuildupWriter.field_format.format(buildup.land_use_name,
                                           buildup.pollutant,
                                           buildup.function.name,
                                           c1,
                                           c2,
                                           c3,
                                           buildup.normalizer.name)


class WashoffWriter(SectionWriter):
    """Specifies the rate at which pollutants are washed off from different land uses during rain events."""

    field_format = "{:16}\t{:16}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}"

    @staticmethod
    def as_text(washoff):
        return WashoffWriter.field_format.format(washoff.land_use_name,
                                           washoff.pollutant,
                                           washoff.function.name,
                                           washoff.coefficient,
                                           washoff.exponent,
                                           washoff.cleaning_efficiency,
                                           washoff.bmp_efficiency)


class PollutantWriter(SectionWriter):
    """Identifies the pollutants being analyzed"""
    field_format = " {:16}\t{:6}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:16}\t{:10}\t{:10}\t{:10}"

    @staticmethod
    def as_text(pollutant):
        return PollutantWriter.field_format.format(pollutant.name,
                                             ConcentrationUnitLabels[pollutant.units.value],
                                             pollutant.rain_concentration,
                                             pollutant.gw_concentration,
                                             pollutant.ii_concentration,
                                             pollutant.decay_coefficient,
                                             SectionWriter.yes_no(pollutant.snow_only),
                                             pollutant.co_pollutant,
                                             pollutant.co_fraction,
                                             pollutant.dwf_concentration,
                                             pollutant.initial_concentration)


class TimeSeriesWriter(SectionWriter):
    """One time series from the TIMESERIES section"""

    field_format = "{:16}\t{:10}\t{:10}\t{:10}"

    @staticmethod
    def as_text(time_series):
        text_list = []

        if time_series.comment:
            text_list.append(time_series.comment)

        if time_series.file:
            text_list.append(time_series.name + "\tFILE\t" + time_series.file)
        else:
            for step in zip(time_series.dates, time_series.times, time_series.values):
                text_list.append(TimeSeriesWriter.field_format.format(time_series.name, step[0], step[1], step[2]))
        return '\n'.join(text_list)


class TitleWriter(SectionWriter):
    """SWMM descriptive title"""

    SECTION_NAME = "[TITLE]"

    @staticmethod
    def as_text(title):
        """format contents of this item for writing to file"""
        return Title.SECTION_NAME + '\n' + title.title


class TemperatureWriter(SectionWriter):
    """temperature, wind speed, snow melt, and areal depletion parameters"""

    SECTION_NAME = "[TEMPERATURE]"

    field_format = "{:18}"

    @staticmethod
    def as_text(temperature):
        # If not set, need to leave entire section out of inp file
        if temperature.source == TemperatureSource.UNSET:
            return ''

        text_list = [temperature.SECTION_NAME]

        if temperature.comment:
            text_list.append(temperature.comment)

        field_start = TemperatureWriter.field_format.format(temperature.source.name) + '\t'
        if temperature.source == TemperatureSource.TIMESERIES and temperature.timeseries:
            text_list.append(field_start + temperature.timeseries)
        elif temperature.source == TemperatureSource.FILE and temperature.filename:
            text_list.append(field_start + temperature.filename + '\t' + temperature.start_date)

        text_list.append(temperature.wind_speed.as_text())  #xw9/13/2016 bug here, not fixed
        text_list.append(temperature.snow_melt.as_text())   #xw bug here
        text_list.append(temperature.areal_depletion.as_text())   #xw bug here
        return '\n'.join(text_list)


class EvaporationWriter(SectionWriter):
    """How daily evaporation rates vary with time for the study area"""

    SECTION_NAME = "[EVAPORATION]"

    @staticmethod
    def as_text(evaporation):
        text_list = [evaporation.SECTION_NAME]
        if evaporation.comment:
            text_list.append(evaporation.comment)
        if evaporation.format != EvaporationFormat.UNSET:
            format_line = evaporation.format.name + '\t'
            if evaporation.format == EvaporationFormat.CONSTANT:
                format_line += evaporation.constant
            elif evaporation.format == EvaporationFormat.MONTHLY:
                format_line += '\t'.join(evaporation.monthly)
            elif evaporation.format == EvaporationFormat.TIMESERIES:
                format_line += evaporation.timeseries
            elif evaporation.format == EvaporationFormat.TEMPERATURE:
                pass
            elif evaporation.format == EvaporationFormat.FILE:
                format_line += '\t'.join(evaporation.monthly_pan_coefficients)
            text_list.append(format_line)
        if evaporation.recovery_pattern:
            text_list.append("RECOVERY\t" + evaporation.recovery_pattern)
        if evaporation.dry_only:
            text_list.append("DRY_ONLY\tYES")
        elif evaporation.dry_only_specified:
            text_list.append("DRY_ONLY\tNO")
        if len(text_list) > 1:
            return '\n'.join(text_list)
        return ''


class WindSpeedWriter(SectionWriter):
    """wind speed parameters, stored as part of [TEMPERATURE] section"""

    SECTION_NAME = "WINDSPEED"

    @staticmethod
    def as_text(wind_speed):
        inp = TemperatureWriter.field_format.format(WindSpeed.SECTION_NAME) + '\t' + wind_speed.source.name
        if wind_speed.source == WindSource.MONTHLY:
            if len(wind_speed.wind_speed_monthly) > 0:
                inp += '\t' + '\t'.join(wind_speed.wind_speed_monthly)
            else:
                inp = ''
        elif wind_speed.source == WindSource.FILE:
            pass
        else:
            inp = ''
        return inp


class SnowMeltWriter(SectionWriter):
    """snow melt parameters"""

    SECTION_NAME = "SNOWMELT"

    @staticmethod
    def as_text(snow_melt):
        return TemperatureWriter.field_format.format(SnowMelt.SECTION_NAME) + '\t' +\
               snow_melt.snow_temp + '\t' +\
               snow_melt.ati_weight + '\t' +\
               snow_melt.negative_melt_ratio + '\t' +\
               snow_melt.elevation + '\t' +\
               snow_melt.latitude + '\t' +\
               snow_melt.time_correction


class ArealDepletionWriter(SectionWriter):
    """areal depletion parameters"""

    SECTION_NAME = "ADC"

    @staticmethod
    def as_text(areal_depletion):
        text_list = []
        if len(areal_depletion.adc_impervious) > 0:
            text_list.append("ADC IMPERVIOUS\t" + '\t'.join(areal_depletion.adc_impervious))
        if len(areal_depletion.adc_impervious) > 0:
            text_list.append("ADC PERVIOUS\t" + '\t'.join(areal_depletion.adc_pervious))
        return '\n'.join(text_list)


class AdjustmentsWriter(SectionWriter):
    """Specifies optional monthly adjustments to be made to temperature, evaporation rate,
    rainfall intensity and hydraulic conductivity in each time period of a simulation."""

    SECTION_NAME = "[ADJUSTMENTS]"

    @staticmethod
    def as_text(adjustments):
        text_list = []
        for (data, default, label) in ((adjustments.temperature,       "0.0", "TEMPERATURE"),
                                       (adjustments.evaporation,       "0.0", "EVAPORATION"),
                                       (adjustments.rainfall,          "1.0", "RAINFALL"),
                                       (adjustments.soil_conductivity, "1.0", "CONDUCTIVITY")):
            values = AdjustmentsWriter.format_values(data, default)
            if values:
                text_list.append(label + '\t' + values)

        # Only add section name and comment if there is some content in this section
        if len(text_list) > 0:
            text_list.insert(0, AdjustmentsWriter.SECTION_NAME)
            if adjustments.comment:
                text_list.insert(1, adjustments.comment)
        return '\n'.join(text_list)

    @staticmethod
    def format_values(data, default):
        """Format list of data values into a string. Blank values are replaced by default.
         If all are blank or default, return empty string, otherwise return tab-separated values."""
        formatted = ''
        any_value = False
        if data and len(data) > 11:
            for value in data:
                value = str(value).strip()
                if len(value) == 0:
                    value = default
                elif value != default and value != default.rstrip(".0"):
                    any_value = True
                if formatted:
                    formatted += '\t'
                formatted += value
        if any_value:
            return formatted
        else:
            return ''


class ConduitWriter(SectionWriter):
    """A conduit link (pipe or channel) in a SWMM model drainage system that conveys water from one node to another."""

    field_format = "{:16}\t{:16}\t{:16}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{}"

    @staticmethod
    def as_text(conduit):
        """format contents of this item for writing to file"""
        if conduit.name:
            return ConduitWriter.field_format.format(conduit.name, conduit.inlet_node, conduit.outlet_node,
                                                     conduit.length, conduit.roughness,
                                                     conduit.inlet_offset, conduit.outlet_offset,
                                                     conduit.initial_flow, conduit.maximum_flow, conduit.comment)
        elif conduit.comment:
            return conduit.comment


class LossWriter(SectionWriter):
    """Convert minor head loss coefficients, flap gates, and seepage rates for a conduit into text."""

    field_format = "{:16}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}"

    @staticmethod
    def as_text(conduit):
        """format conduit loss information for writing to file"""
        if conduit.name and (conduit.entry_loss_coefficient
                             or conduit.exit_loss_coefficient
                             or conduit.loss_coefficient
                             or conduit.seepage):
            return LossWriter.field_format.format(conduit.name,
                                                  conduit.entry_loss_coefficient,
                                                  conduit.exit_loss_coefficient,
                                                  conduit.loss_coefficient,
                                                  SectionWriter.yes_no(conduit.flap_gate),
                                                  conduit.seepage)
        else:
            return None


class PumpWriter(SectionWriter):
    """A pump link in a SWMM model"""

    field_format = "{:16}\t{:16}\t{:16}\t{:16}\t{:8}\t{:8}\t{:8}\t{}"

    @staticmethod
    def as_text(pump):
        """format contents of this item for writing to file"""
        if pump.name:
            return PumpWriter.field_format.format(pump.name, pump.inlet_node, pump.outlet_node, pump.pump_curve,
                                            pump.initial_status, pump.startup_depth, pump.shutoff_depth, pump.comment)
        elif pump.comment:
            return pump.comment


class OrificeWriter(SectionWriter):
    field_format = "{:16}\t{:16}\t{:16}\t{:12}\t{:10}\t{:10}\t{:8}\t{:10}\t{}"

    @staticmethod
    def as_text(orifice):
        """format contents of this item for writing to file"""
        if orifice.name:
            return OrificeWriter.field_format.format(orifice.name, orifice.inlet_node, orifice.outlet_node,
                                                     orifice.type.name, orifice.inlet_offset,
                                                     orifice.discharge_coefficient,
                                                     SectionWriter.yes_no(orifice.flap_gate),
                                                     orifice.initial_flow, orifice.o_rate, orifice.comment)
        elif orifice.comment:
            return orifice.comment


class WeirWriter(SectionWriter):

    field_format = "{:16}\t{:16}\t{:16}\t{:12}\t{:10}\t{:10}\t{:8}\t{:8}\t{:10}\t{:10}\t{:10}\t{:10}\t{}"

    @staticmethod
    def as_text(weir):
        """format contents of this item for writing to file"""
        if weir.name:
            if weir.type == WeirType.ROADWAY:
                road_width = weir.road_width
                road_surface = weir.road_surface.name
            else:
                road_width = ''
                road_surface = ''
            return WeirWriter.field_format.format(weir.name, weir.inlet_node, weir.outlet_node,
                                                     weir.type.name, weir.inlet_offset, weir.discharge_coefficient,
                                                     SectionWriter.yes_no(weir.flap_gate),
                                                     weir.end_contractions,
                                                     weir.end_coefficient,
                                                     SectionWriter.yes_no(weir.can_surcharge),
                                                     road_width, road_surface, weir.comment)
        elif weir.comment:
            return weir.comment


class OutletWriter(SectionWriter):

    field_format = "{:16}\t{:16}\t{:16}\t{:10}\t{:15}\t"

    @staticmethod
    def as_text(outlet):
        """format contents of this item for writing to file"""
        inp = OutletWriter.field_format.format(outlet.name, outlet.inlet_node, outlet.outlet_node,
                                               str(outlet.inlet_offset),
                                               outlet.curve_type.name.replace('_', '/'))
        if outlet.curve_type in (OutletCurveType.TABULAR_DEPTH, OutletCurveType.TABULAR_HEAD):
            inp += "{:16}".format(str(outlet.rating_curve))
        elif outlet.curve_type in (OutletCurveType.FUNCTIONAL_DEPTH, OutletCurveType.FUNCTIONAL_HEAD):
            inp += "{:16}\t{:10}".format(outlet.coefficient, outlet.exponent)
        elif outlet.comment:
            return outlet.comment
        inp += "\t{:8}".format(SectionWriter.yes_no(outlet.flap_gate))
        return inp


class CrossSectionWriter(SectionWriter):
    """Make a string representation of a CrossSection of a Conduit, Orifice, or Weir"""

    field_format_shape =     "{:16}\t{:12}\t{:16}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}"
    field_format_custom =    "{:16}\t{:12}\t{:16}\t{:10}\t{:10}"
    # field_format_irregular = "{:16}\t{:12}\t{:16}"

    @staticmethod
    def as_text(cross_section):
        inp = ''
        if cross_section.comment:
            inp = cross_section.comment + '\n'
        if cross_section.shape == CrossSectionShape.CUSTOM:
            inp += CrossSectionWriter.field_format_custom.format(cross_section.link, cross_section.shape.name, cross_section.geometry1, cross_section.curve, cross_section.barrels)
        # elif cross_section.shape == CrossSectionShape.IRREGULAR:
        #     inp += CrossSectionWriter.field_format_irregular.format(cross_section.link, cross_section.shape.name, cross_section.transect)
        else:
            inp += CrossSectionWriter.field_format_shape.format(cross_section.link,
                                                                cross_section.shape.name,
                                                                cross_section.geometry1,
                                                                cross_section.geometry2,
                                                                cross_section.geometry3,
                                                                cross_section.geometry4,
                                                                cross_section.barrels,
                                                                cross_section.culvert_code)
        return inp


class TransectsWriter(SectionWriter):

    SECTION_NAME = "[TRANSECTS]"
    DEFAULT_COMMENT = ";;Transect Data in HEC-2 format"

    @staticmethod
    def as_text(transects):
        """Contents of this section formatted for writing to file"""
        if transects.value or (transects.comment and transects.comment != transects.DEFAULT_COMMENT):
            text_list = [transects.SECTION_NAME]
            if transects.comment:
                text_list.append(transects.comment)
            else:
                text_list.append(transects.DEFAULT_COMMENT)
            for item in transects.value:
                item_str = str(item)
                text_list.append(item_str.rstrip('\n'))  # strip any newlines from end of each item
            return '\n'.join(text_list)
        else:
            return ''


class TransectWriter(SectionWriter):
    """the cross-section geometry of a natural channel or conduit with irregular shapes"""

    field_format_nc = "NC\t{:8}\t{:8}\t{:8}"
    field_format_x1 = "X1\t{:16}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}"
    field_format_gr = "\t{:8}\t{:8}"

    @staticmethod
    def as_text(transect):
        lines = []
        if len(transect.stations) > 0:
            if transect.comment:
                if transect.comment.startswith(';'):
                    lines.append(transect.comment)
                else:
                    lines.append(';' + transect.comment.replace('\n', '\n;'))
            if transect.n_left or transect.n_right or transect.n_channel:
                if len(transect.n_left) == 0:
                    transect.n_left = '0'
                if len(transect.n_right) == 0:
                    transect.n_right = '0'
                if len(transect.n_channel) == 0:
                    transect.n_channel = '0'
                if len((transect.n_left + transect.n_right + transect.n_channel).replace('.', '').replace('0', '')) > 0:
                    lines.append(TransectWriter.field_format_nc.format(transect.n_left, transect.n_right, transect.n_channel))
            lines.append(TransectWriter.field_format_x1.format(transect.name,
                                                     len(transect.stations),
                                                     transect.overbank_left,
                                                     transect.overbank_right,
                                                     "0.0", "0.0",
                                                     transect.meander_modifier,
                                                     transect.stations_modifier,
                                                     transect.elevations_modifier))
            line = "GR"
            stations_this_line = 0
            for station in transect.stations:
                line += TransectWriter.field_format_gr.format(station[0], station[1])
                stations_this_line += 1
                if stations_this_line > 4:
                    lines.append(line)
                    line = "GR"
                    stations_this_line = 0
            if stations_this_line > 0:
                lines.append(line)

        return '\n'.join(lines)


class JunctionWriter(SectionWriter):
    """A Junction node"""

    field_format = "{:16}\t{:10}\t{:10}\t{:10}\t{:10}\t{}"

    @staticmethod
    def as_text(junction):
        """format contents of this item for writing to file"""
        return JunctionWriter.field_format.format(junction.name, junction.elevation,
                                        junction.max_depth, junction.initial_depth, junction.surcharge_depth, junction.ponded_area)


class OutfallWriter(SectionWriter):
    """Write Outfall properties"""

    field_format = "{:16}\t{:10}\t{:10}\t{:16}\t{:8}\t{:8}"

    @staticmethod
    def as_text(outfall):
        """format contents of this item for writing to file"""

        if outfall.outfall_type == OutfallType.FIXED:
            source = str(outfall.fixed_stage)
        elif outfall.outfall_type == OutfallType.TIDAL:
            source = outfall.tidal_curve
        elif outfall.outfall_type == OutfallType.TIMESERIES:
            source = outfall.time_series_name
        else:
            source = ''

        inp = OutfallWriter.field_format.format(outfall.name, outfall.elevation, outfall.outfall_type.name,
                                                source, SectionWriter.yes_no(outfall.tide_gate), outfall.route_to)
        return inp


class DividerWriter(SectionWriter):
    """Write Divider properties"""

    field_format = "{:16}\t{:10}\t{:16}\t{:10}\t{}{:10}\t{:10}\t{:10}\t{:10}"

    @staticmethod
    def as_text(divider):
        """format contents of this item for writing to file"""

        middle_part = ''
        if divider.flow_divider_type == FlowDividerType.CUTOFF:
            middle_part = "{:10}\t".format(str(divider.min_diversion_flow))
        elif divider.flow_divider_type == FlowDividerType.TABULAR:
            middle_part = "{:10}\t".format(divider.divider_curve)
        elif divider.flow_divider_type == FlowDividerType.WEIR:
            middle_part = "{:10}\t{:10}\t{:10}\t".format(str(divider.min_diversion_flow),
                                                         str(divider.weir_max_depth),
                                                         str(divider.weir_coefficient))

        inp = DividerWriter.field_format.format(divider.name,
                                                str(divider.elevation),
                                                divider.diverted_link,
                                                divider.flow_divider_type.name,
                                                middle_part,
                                                str(divider.max_depth),
                                                str(divider.initial_depth),
                                                str(divider.surcharge_depth),
                                                str(divider.ponded_area))
        return inp


class StorageWriter(SectionWriter):
    """Write Divider properties"""

    field_format = "{:16}\t{:8}\t{:10}\t{:10}\t{:10}\t{:28}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}"

    @staticmethod
    def as_text(storage):
        """format contents of this item for writing to file"""

        middle_part = ''
        if storage.storage_curve_type == StorageCurveType.TABULAR:
            middle_part = str(storage.storage_curve)
        elif storage.storage_curve_type == StorageCurveType.FUNCTIONAL:
            middle_part = "{:8}  {:8}  {:8}".format(str(storage.coefficient),
                                                    str(storage.exponent),
                                                    str(storage.constant))

        inp = StorageWriter.field_format.format(storage.name,
                                                str(storage.elevation),
                                                str(storage.max_depth),
                                                str(storage.initial_depth),
                                                storage.storage_curve_type.name,
                                                middle_part,
                                                str(storage.ponded_area),
                                                str(storage.evaporation_factor),
                                                str(storage.seepage_suction_head),
                                                str(storage.seepage_hydraulic_conductivity),
                                                str(storage.seepage_initial_moisture_deficit))
        return inp


class DirectInflowWriter(SectionWriter):
    """Defines characteristics of inflows added directly into a node"""

    field_format = "{:16}\t{:16}\t{:16}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}"

    @staticmethod
    def as_text(direct_inflow):
        inp = ''
        if direct_inflow.comment:
            inp = direct_inflow.comment + '\n'
        if direct_inflow.constituent.upper() == "FLOW":
            inp_format = "FLOW"
        else:
            inp_format = direct_inflow.format.name
        inp += DirectInflowWriter.field_format.format(direct_inflow.node,
                                        direct_inflow.constituent,
                                        direct_inflow.timeseries,
                                        inp_format,
                                        direct_inflow.conversion_factor,
                                        direct_inflow.scale_factor,
                                        direct_inflow.baseline,
                                        direct_inflow.baseline_pattern)
        return inp


class DryWeatherInflowWriter(SectionWriter):
    """Specifies dry weather flow and its quality entering the drainage system at a specific node"""

    field_format = "{:16}\t{:16}\t{:10}"

    @staticmethod
    def as_text(dry_weather_inflow):
        inp = ''
        if dry_weather_inflow.comment:
            inp = dry_weather_inflow.comment + '\n'
        inp += DryWeatherInflowWriter.field_format.format(dry_weather_inflow.node,
                                        dry_weather_inflow.constituent,
                                        dry_weather_inflow.average) + '\t' + '\t'.join(dry_weather_inflow.time_patterns)
        return inp


class RDIInflowWriter(SectionWriter):
    """Defines characteristics of Rainfall-Dependent Infiltration/Inflows entering the system at a node"""

    field_format = "{:16}\t{:16}\t{:10}"

    @staticmethod
    def as_text(rdi_inflow):
        inp = ''
        if rdi_inflow.comment:
            inp = rdi_inflow.comment + '\n'
        inp += RDIInflowWriter.field_format.format(rdi_inflow.node,
                                        rdi_inflow.hydrograph_group,
                                        rdi_inflow.sewershed_area)
        return inp


class TreatmentWriter(SectionWriter):
    """Define the treatment properties of a node using a treatment expression"""

    field_format = "{:16}\t{:16}\t{}"

    hint = "Treatment expressions have the general form:\n" \
           "  R = f(P, R_P, V)\n" \
           "or\n" \
           "  C = f(P, R_P, V)\n" \
           "where:\n" \
           "  R   = fractional removal,\n" \
           "  C   = outlet concentration,\n" \
           "  P   = one or more pollutant names,\n" \
           "  R_P = one or more pollutant removals\n" \
           "        (prepend R_ to pollutant name),\n" \
           "  V   = one or more process variables:\n" \
           "        FLOW (inflow rate)\n" \
           "        DEPTH (water depth)\n" \
           "        HRT (hydraulic residence time)\n" \
           "        DT (time step in seconds)\n" \
           "        AREA (surface area).\n" \
           "Some example expressions are:\n" \
           "  C = BOD * exp(-0.05*HRT)\n" \
           "  R = 0.75 * R_TSS"

    @staticmethod
    def as_text(treatment):
        inp = ''
        if treatment.comment:
            inp = treatment.comment + '\n'
        inp += TreatmentWriter.field_format.format(treatment.node,
                                        treatment.pollutant,
                                        treatment.function)
        return inp


class AquiferWriter(SectionWriter):
    """Sub-surface groundwater area that models water infiltrating."""

    field_format = " {:16}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}"

    @staticmethod
    def as_text(aquifer):
        inp = ''
        if aquifer.comment:
            inp = aquifer.comment + '\n'
        inp += AquiferWriter.field_format.format(aquifer.name,
                                           aquifer.porosity,
                                           aquifer.wilting_point,
                                           aquifer.field_capacity,
                                           aquifer.conductivity,
                                           aquifer.conductivity_slope,
                                           aquifer.tension_slope,
                                           aquifer.upper_evaporation_fraction,
                                           aquifer.lower_evaporation_depth,
                                           aquifer.lower_groundwater_loss_rate,
                                           aquifer.bottom_elevation,
                                           aquifer.water_table_elevation,
                                           aquifer.unsaturated_zone_moisture,
                                           aquifer.upper_evaporation_pattern)
        return inp


class LIDControlWriter(SectionWriter):
    """Defines scale-independent LID controls that can be deployed within subcatchments"""

    @staticmethod
    def as_text(lid_control):
        """format contents of this item for writing to file"""
        text_list = []
        if lid_control.comment:
            text_list.append(lid_control.comment)
        text_list .append(lid_control.name + '\t' + lid_control.lid_type.name)
        for field_names in LIDControl.LineTypes:
            if getattr(lid_control, field_names[0]):
                line = lid_control.name + '\t' + field_names[1]
                for field_name in field_names[2:]:
                    line += '\t' + str(getattr(lid_control, field_name))
                text_list.append(line)
        return '\n'.join(text_list)


class SnowPackWriter(SectionWriter):
    """Snow pack parameters"""


    @staticmethod
    def as_text(snow_pack):
        """format contents of this item for writing to file"""
        text_list = []
        if snow_pack.comment:
            text_list.append(snow_pack.comment)
        for field_names in snow_pack.LineTypes:
            if getattr(snow_pack, field_names[0]):               # If the flag for this group of fields is true,
                line = snow_pack.name + '\t' + field_names[1]    # add a line with name, group name,
                for field_name in field_names[2:]:          # and the field values in this group.
                    line += '\t' + str(getattr(snow_pack, field_name))
                text_list.append(line)
        return '\n'.join(text_list)


class SubcatchmentWriter(SectionWriter):
    """Subcatchment geometry, location, parameters, and time-series data"""

    field_format = "{:16}\t{:16}\t{:16}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}\t{:16}"

    @staticmethod
    def as_text(subcatchment):
        inp = SubcatchmentWriter.field_format.format(subcatchment.name,
                                                     subcatchment.rain_gage,
                                                     subcatchment.outlet,
                                                     subcatchment.area,
                                                     subcatchment.percent_impervious,
                                                     subcatchment.width,
                                                     subcatchment.percent_slope,
                                                     subcatchment.curb_length,
                                                     subcatchment.snow_pack)
        return inp


class SubareaWriter(SectionWriter):
    """Subcatchment geometry, location, parameters, and time-series data"""

    field_format = "{:16}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}"

    @staticmethod
    def as_text(subcatchment):
        if subcatchment.subarea_routing == Routing.OUTLET:
            percent_routed = ""
        else:
            percent_routed = str(subcatchment.percent_routed)
        inp = SubareaWriter.field_format.format(subcatchment.name,
                                                subcatchment.n_imperv,
                                                subcatchment.n_perv,
                                                subcatchment.storage_depth_imperv,
                                                subcatchment.storage_depth_perv,
                                                subcatchment.percent_zero_impervious,
                                                subcatchment.subarea_routing.name,
                                                percent_routed)
        return inp


class HortonInfiltrationWriter(SectionWriter):
    """Horton Infiltration parameters"""

    field_format = "{:16}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}"

    @staticmethod
    def as_text(horton_infiltration):
        inp = ''
        if horton_infiltration.comment:
            inp = horton_infiltration.comment + '\n'
        inp += HortonInfiltrationWriter.field_format.format(horton_infiltration.subcatchment,
                                        horton_infiltration.max_rate,
                                        horton_infiltration.min_rate,
                                        horton_infiltration.decay,
                                        horton_infiltration.dry_time,
                                        horton_infiltration.max_volume)
        return inp


class GreenAmptInfiltrationWriter(SectionWriter):
    """Green-Ampt Infiltration parameters"""

    field_format = "{:16}\t{:10}\t{:10}\t{:10}"

    @staticmethod
    def as_text(green_ampt_infiltration):
        inp = ''
        if green_ampt_infiltration.comment:
            inp = green_ampt_infiltration.comment + '\n'
        inp += GreenAmptInfiltrationWriter.field_format.format(green_ampt_infiltration.subcatchment,
                                        green_ampt_infiltration.suction,
                                        green_ampt_infiltration.hydraulic_conductivity,
                                        green_ampt_infiltration.initial_moisture_deficit)
        return inp


class CurveNumberInfiltrationWriter(SectionWriter):
    """Curve Number Infiltration parameters"""

    field_format = "{:16}\t{:10}\t{:10}\t{:10}"

    @staticmethod
    def as_text(curve_number_infiltration):
        inp = ''
        if curve_number_infiltration.comment:
            inp = curve_number_infiltration.comment + '\n'
        inp += CurveNumberInfiltrationWriter.field_format.format(curve_number_infiltration.subcatchment,
                                        curve_number_infiltration.curve_number,
                                        curve_number_infiltration.hydraulic_conductivity,
                                        curve_number_infiltration.dry_days)
        return inp


class GroundwaterWriter(SectionWriter):
    """Link a subcatchment to an aquifer and to a drainage system node"""

    field_format = "{:16}\t{:16}\t{:16}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}"

    @staticmethod
    def as_text(groundwater):
        inp = ''
        if groundwater.comment:
            inp = groundwater.comment + '\n'
        inp += GroundwaterWriter.field_format.format(groundwater.subcatchment,
                                        groundwater.aquifer,
                                        groundwater.receiving_node,
                                        groundwater.surface_elevation,
                                        groundwater.groundwater_flow_coefficient,
                                        groundwater.groundwater_flow_exponent,
                                        groundwater.surface_water_flow_coefficient,
                                        groundwater.surface_water_flow_exponent,
                                        groundwater.surface_gw_interaction_coefficient,
                                        groundwater.fixed_surface_water_depth,
                                        groundwater.threshold_groundwater_elevation,
                                        groundwater.bottom_elevation,
                                        groundwater.water_table_elevation,
                                        groundwater.unsaturated_zone_moisture)
        return inp


class LIDUsageWriter(SectionWriter):
    """Specifies how an LID control will be deployed in a subcatchment"""

    field_format = " {:15}\t{:16}\t{:7}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:24}"  # TODO: add fields? \t{:24}\t{:16}

    @staticmethod
    def as_text(lid_usage):
        inp = ''
        if lid_usage.comment:
            inp = lid_usage.comment + '\n'
        inp += LIDUsageWriter.field_format.format(lid_usage.subcatchment_name,
                                            lid_usage.control_name,
                                            lid_usage.number_replicate_units,
                                            lid_usage.area_each_unit,
                                            lid_usage.top_width_overland_flow_surface,
                                            lid_usage.percent_initially_saturated,
                                            lid_usage.percent_impervious_area_treated,
                                            lid_usage.send_outflow_pervious_area,
                                            lid_usage.detailed_report_file)
        return inp


class CoverageWriter(SectionWriter):
    """Specifies the percentage of a subcatchments area that is covered by each category of land use."""

    field_format = "{:16}\t{:16}\t{:10}"

    @staticmethod
    def as_text(coverage):
        return CoverageWriter.field_format.format(coverage.subcatchment_name, coverage.land_use_name, coverage.percent_subcatchment_area)


class CoveragesWriter(SectionWriter):
    """Specifies the percentage of a subcatchments area that is covered by each category of land use."""

    SECTION_NAME = "[COVERAGES]"
    DEFAULT_COMMENT = ";;Subcatchment  \tLand Use        \tPercent\n"\
                      ";;--------------\t----------------\t----------"

    @staticmethod
    def as_text(coverages):
        lines = []
        if len(coverages.value) > 0:
            lines.append(coverages.SECTION_NAME)
            if coverages.comment:
                if coverages.comment.startswith(';'):
                    lines.append(coverages.comment)
                else:
                    lines.append(';' + coverages.comment.replace('\n', '\n;'))
            num_this_line = 0
            for coverage in coverages.value:
                lines.append(CoverageWriter.as_text(coverage))
        return '\n'.join(lines)


class InitialLoadingWriter(SectionWriter):
    """Specifies a pollutant buildup that exists on a subcatchment at the start of a simulation."""

    field_format = "{:16}\t{:16}\t{:10}"

    @staticmethod
    def as_text(initial_loading):
        inp = ''
        if initial_loading.comment:
            inp = initial_loading.comment + '\n'
        inp += InitialLoadingWriter.field_format.format(initial_loading.subcatchment_name, initial_loading.pollutant_name, initial_loading.initial_buildup)
        return inp


class InitialLoadingsWriter(SectionWriter):
    """Specifies the pollutant buildup that exists on each subcatchment at the start of a simulation."""

    SECTION_NAME = "[LOADINGS]"
    DEFAULT_COMMENT = ";;Subcatchment  \tPollutant       \tBuildup\n"\
                      ";;--------------\t----------------\t----------"

    @staticmethod
    def as_text(initial_loadings):
        lines = []
        if len(initial_loadings.value) > 0:
            lines.append(initial_loadings.SECTION_NAME)
            lines.append(initial_loadings.DEFAULT_COMMENT)
            # if initial_loadings.comment:
            #     if initial_loadings.comment.startswith(';'):
            #         lines.append(initial_loadings.comment)
            #     else:
            #         lines.append(';' + initial_loadings.comment.replace('\n', '\n;'))
            for loading in initial_loadings.value:
                lines.append(loading.as_text())
        return '\n'.join(lines)


class RainGageWriter(SectionWriter):
    """Specifies a pollutant buildup that exists on a subcatchment at the start of a simulation."""

    field_format = "{:16}\t{:9}\t{:8}\t{:8}\t"

    @staticmethod
    def as_text(rain_gage):
        inp = RainGageWriter.field_format.format(
                rain_gage.name,
                rain_gage.rain_format.name,
                rain_gage.rain_interval,
                rain_gage.snow_catch_factor)
        if rain_gage.timeseries:
            inp += "{:10}\t{:16}".format("TIMESERIES", rain_gage.timeseries)
        else:
            inp += '{:10}\t"{:16}"\t{:10}\t{:5}'.format(
                "FILE",
                rain_gage.data_file_name,
                rain_gage.data_file_station_id,
                rain_gage.data_file_rain_units)
        if rain_gage.comment:
            inp += " # " + rain_gage.comment
        return inp


class UnitHydrographWriter(SectionWriter):
    """Specifies the shapes of the triangular unit hydrographs that determine the amount of
        rainfall-dependent infiltration/inflow (RDII) entering the drainage system"""

    first_row_format = "{:16}\t{:16}"
    field_format = "{:16}\t{:16}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}"

    @staticmethod
    def as_text(unit_hydrograph):
        text_list = []

        if unit_hydrograph.comment:
            text_list.append(unit_hydrograph.comment)

        text_list.append(unit_hydrograph.first_row_format.format(unit_hydrograph.name, unit_hydrograph.rain_gage_name))

        for entry in unit_hydrograph.value:
            text_list.append(UnitHydrographWriter.field_format.format(unit_hydrograph.name,
                                                      entry.hydrograph_month,
                                                      entry.term,
                                                      entry.response_ratio,
                                                      entry.time_to_peak,
                                                      entry.recession_limb_ratio,
                                                      entry.initial_abstraction_depth,
                                                      entry.initial_abstraction_rate,
                                                      entry.initial_abstraction_amount))
        return '\n'.join(text_list)


class BackdropOptionsWriter(SectionWriter):
    """Identifies a backdrop image and dimensions for the network map"""

    SECTION_NAME = "[BACKDROP]"

    @staticmethod
    def as_text(backdrop_options):
        text_list = [BackdropOptions.SECTION_NAME]
        if backdrop_options.dimensions:
            text_list.append(" {:17}\t{:16}\t{:16}\t{:16}\t{:16}".format("DIMENSIONS",
                             backdrop_options.dimensions[0], backdrop_options.dimensions[1], backdrop_options.dimensions[2], backdrop_options.dimensions[3]))
        if backdrop_options.units:
            text_list.append(" {:17}\t{}".format("UNITS", backdrop_options.units))
        if backdrop_options.file:
            text_list.append(" {:17}\t{}".format("FILE", backdrop_options.file))
        if backdrop_options.offset:
            text_list.append(" {:17}\t{:16}\t{:16}".format("OFFSET",
                             backdrop_options.offset[0], backdrop_options.offset[1]))
        if backdrop_options.scaling:
            text_list.append(" {:17}\t{:16}\t{:16}".format("SCALING",
                             backdrop_options.scaling[0], backdrop_options.scaling[1]))
        return '\n'.join(text_list)


class GeneralWriter(SectionWriter):
    """SWMM General Options"""

    SECTION_NAME = "[OPTIONS]"

    section_comments = (";; Dates", ";; Time Steps", ";; Dynamic Wave")

    @staticmethod
    def as_text(general):
        """Contents of this item formatted for writing to file"""
        # First, add the values in this section stored directly in this class
        # Omit COMPATIBILITY option if it is 5, this is assumed now and is no longer listed as an option in 5.1
        text_list = [SectionWriter.as_text(general).replace(GeneralWriter.field_format.format("COMPATIBILITY", "5"), '')]
        if general.dates is not None:  # Add the values stored in Dates class
            text_list.append(General.section_comments[0])
            text_list.append(SectionWriter.as_text(general.dates).replace(general.SECTION_NAME + '\n', ''))
        if general.time_steps is not None:  # Add the values stored in TimeSteps class
            text_list.append(General.section_comments[1])
            text_list.append(SectionWriter.as_text(general.time_steps).replace(general.SECTION_NAME + '\n', ''))
        if general.dynamic_wave is not None:  # Add the values stored in DynamicWave class
            text_list.append(General.section_comments[2])
            text_list.append(SectionWriter.as_text(general.dynamic_wave).replace(general.SECTION_NAME + '\n', ''))
        return '\n'.join(text_list)


class MapOptionsWriter(SectionWriter):
    """SWMM Map Options"""

    SECTION_NAME = "[MAP]"

    @staticmethod
    def as_text(map_options):
        text_list = [MapOptions.SECTION_NAME]
        if map_options.dimensions:
            text_list.append(" {:17}\t{:16}\t{:16}\t{:16}\t{:16}".format("DIMENSIONS",
                             map_options.dimensions[0], map_options.dimensions[1], map_options.dimensions[2], map_options.dimensions[3]))
        if map_options.units:
            if isinstance(map_options.units, Enum):
                units_name = map_options.units.name
            else:
                units_name = str(map_options.units)
            text_list.append(" {:17}\t{}".format("UNITS", units_name))
        return '\n'.join(text_list)


class ReportWriter(SectionWriter):
    """Report Options"""

    SECTION_NAME = "[REPORT]"
    DEFAULT_COMMENT = ";;Reporting Options"

    @staticmethod
    def as_text(report):
        """format contents of this item for writing to file"""
        # Use default get_text, but need to skip LID if it is NONE
        lines = []
        for line in SectionWriter.as_text(report).splitlines():
            if line.split() != ["LID", "NONE"]:
                lines.append(line)
        return '\n'.join(lines)


class TagsWriter(SectionWriter):
    """Write tags to a string"""

    SECTION_NAME = "[TAGS]"

    field_format = "{:10}{:16}\t{:16}"

    @staticmethod
    def as_text(project):
        text_list = [TagsWriter.SECTION_NAME]
        section_map = {"Gage      ": [project.raingages.value],
                       "Subcatch  ": [project.subcatchments.value],
                       "Node      ": [project.junctions.value, project.outfalls.value,
                                      project.dividers.value, project.storage.value],
                       "Link      ": [project.conduits.value, project.pumps.value, project.orifices.value,
                                      project.weirs.value, project.outlets.value]}
        for object_type_name, sections in section_map.items():
            for section in sections:
                for item in section:
                    if hasattr(item, "tag") and item.tag:
                        name = "Unknown"
                        if hasattr(item, "name") and item.name:
                            name = item.name
                        text_list.append(TagsWriter.field_format.format(object_type_name, item.name, item.tag))
        if len(text_list) > 1:
            return '\n'.join(text_list)
        else:
            return ''
