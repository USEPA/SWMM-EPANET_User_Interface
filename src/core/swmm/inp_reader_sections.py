import traceback
import shlex
from core.coordinate import Coordinate
from core.inp_reader_base import SectionReader
from core.project_base import ProjectBase, Section
from core.swmm.climatology import Adjustments
from core.swmm.climatology import ArealDepletion
from core.swmm.climatology import Evaporation
from core.swmm.climatology import EvaporationFormat
from core.swmm.climatology import SnowMelt
from core.swmm.climatology import Temperature
from core.swmm.climatology import TemperatureSource
from core.swmm.climatology import WindSource
from core.swmm.climatology import WindSpeed
from core.swmm.curves import Curve
from core.swmm.curves import CurveType
from core.swmm.hydraulics.control import Controls
from core.swmm.hydraulics.link import Conduit
from core.swmm.hydraulics.link import CrossSection
from core.swmm.hydraulics.link import CrossSectionShape
from core.swmm.hydraulics.link import Link
from core.swmm.hydraulics.link import Orifice
from core.swmm.hydraulics.link import Weir
from core.swmm.hydraulics.link import Outlet, OutletCurveType
from core.swmm.hydraulics.link import Pump
from core.swmm.hydraulics.link import Transect
from core.swmm.hydraulics.link import Transects
from core.swmm.hydraulics.node import DirectInflow
from core.swmm.hydraulics.node import DirectInflowType
from core.swmm.hydraulics.node import DryWeatherInflow
from core.swmm.hydraulics.node import Junction
from core.swmm.hydraulics.node import Outfall, OutfallType
from core.swmm.hydraulics.node import Divider, FlowDividerType
from core.swmm.hydraulics.node import StorageUnit, StorageCurveType
from core.swmm.hydraulics.node import RDIInflow
from core.swmm.hydraulics.node import Treatment
from core.swmm.hydrology.aquifer import Aquifer
from core.swmm.hydrology.lidcontrol import LIDControl
from core.swmm.hydrology.lidcontrol import LIDType
from core.swmm.hydrology.raingage import RainGage
from core.swmm.hydrology.snowpack import SnowPack
from core.swmm.hydrology.subcatchment import Coverage
from core.swmm.hydrology.subcatchment import Coverages
from core.swmm.hydrology.subcatchment import CurveNumberInfiltration
from core.swmm.hydrology.subcatchment import GreenAmptInfiltration
from core.swmm.hydrology.subcatchment import Groundwater
from core.swmm.hydrology.subcatchment import HortonInfiltration
from core.swmm.hydrology.subcatchment import InitialLoading
from core.swmm.hydrology.subcatchment import InitialLoadings
from core.swmm.hydrology.subcatchment import LIDUsage
from core.swmm.hydrology.subcatchment import Subcatchment, Routing
from core.swmm.hydrology.unithydrograph import UnitHydrograph
from core.swmm.hydrology.unithydrograph import UnitHydrographEntry
from core.swmm.labels import Label
from core.swmm.options.backdrop import BackdropOptions
from core.swmm.options.general import FlowRouting
from core.swmm.options.general import General
from core.swmm.options.map import MapOptions
from core.swmm.options.report import Report
from core.swmm.patterns import Pattern
from core.swmm.patterns import PatternType
from core.swmm.quality import Buildup
from core.swmm.quality import BuildupFunction
from core.swmm.quality import ConcentrationUnitLabels
from core.swmm.quality import ConcentrationUnits
from core.swmm.quality import Landuse
from core.swmm.quality import Normalizer
from core.swmm.quality import Pollutant
from core.swmm.quality import Washoff
from core.swmm.quality import WashoffFunction
from core.swmm.timeseries import TimeSeries
from core.swmm.title import Title
from core.indexed_list import IndexedList


class CoordinateReader(SectionReader):
    @staticmethod
    def read(new_text):
        coordinate = Coordinate()
        fields = new_text.split()
        if len(fields) > 2:
            coordinate.name, coordinate.x, coordinate.y = fields[0:3]
            return coordinate
        else:
            return None


class CoordinatesReader(SectionReader):
    """Read coordinates of nodes into node objects."""

    @staticmethod
    def read(new_text, project):
        disposable_section = Section()
        disposable_section.SECTION_NAME = "[COORDINATES]"
        project.coordinates.value = IndexedList([], ['name'])
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(disposable_section, line)
            coordinate = CoordinateReader.read(line)
            if coordinate:
                found = False
                for node_group in project.nodes_groups():
                    if node_group and node_group.value:
                        for node in node_group.value:
                            if node.name == coordinate.name:
                                node.x = coordinate.x
                                node.y = coordinate.y
                                found = True
                                project.coordinates.value.append(node)
                                break
                if not found:
                    print "Node not found in model for coordinate " + coordinate.name
                    project.coordinates.value.append(coordinate)


class LabelReader(SectionReader):
    @staticmethod
    def read(new_text):
        label = Label()
        fields = shlex.split(new_text)
        if len(fields) > 2:
            label.x, label.y, label.name = fields[0:3]

            if len(fields) > 3:
                label.anchor_name = fields[3]  # name of an anchor node (optional)
            if len(fields) > 4:
                label.font = fields[4]
            if len(fields) > 5:
                label.size = fields[5]
            if len(fields) > 6:
                label.bold = (fields[6] and fields[6] != '0')
            if len(fields) > 7:
                label.italic = (fields[7] and fields[7] != '0')
        return label


class CurveReader(SectionReader):
    """Defines data curves and their X,Y points"""

    @staticmethod
    def read(new_text):
        curve = Curve()
        for line in new_text.splitlines():
            SectionReader.set_comment_check_section(curve, line)
            if line.strip():
                fields = line.split()
                if len(fields) > 2:
                    curve.name = fields[0]
                    try:
                        curve.curve_type = CurveType[fields[1].upper()]
                        x_index = 2
                    except:
                        x_index = 1
                    for x in range(x_index, len(fields) - 1, 2):
                        curve.curve_xy.append((fields[x], fields[x + 1]))
        return curve


class PatternReader(SectionReader):
    """Pattern multipliers define how some base quantity is adjusted for each time period"""
    @staticmethod
    def read(new_text):
        pattern = Pattern()
        for line in new_text.splitlines():
            comment_split = str.split(line, ';', 1)
            if len(comment_split) > 1:
                pattern.description += line[1:].strip()
                line = comment_split[0].strip()
            if line:
                fields = line.split()
                if len(fields) > 1:
                    pattern.name = fields[0]
                    check_type = fields[1].upper()
                    try:
                        pattern.pattern_type = PatternType[check_type]
                        first_multiplier = 2
                    except:
                        first_multiplier = 1
                    pattern.multipliers.extend(fields[first_multiplier:])
        return pattern


class LanduseReader(SectionReader):
    """Identifies the various categories of land uses within the drainage area. Each subcatchment area
        can be assigned a different mix of land uses. Each land use can be subjected to a different
        street sweeping schedule."""

    @staticmethod
    def read(new_text):
        landuse = Landuse()
        fields = new_text.split()
        if len(fields) > 0:
            landuse.name = fields[0]
        if len(fields) > 1:
            landuse.street_sweeping_interval = fields[1]
        if len(fields) > 2:
            landuse.street_sweeping_availability =  fields[2]
        if len(fields) > 3:
            landuse.last_swept = fields[3]
        return landuse


class BuildupReader(SectionReader):
    """Specifies the rate at which pollutants build up over different land uses between rain events."""

    @staticmethod
    def read(new_text):
        buildup = Buildup()
        fields = new_text.split()
        if len(fields) > 6:
            buildup.land_use_name = fields[0]
            buildup.pollutant = fields[1]
            buildup.function =  BuildupFunction[fields[2].upper()]
            buildup.max_buildup = fields[3]
            buildup.scaling_factor = fields[4]
            buildup.timeseries = fields[5]
            # C2, C3 mean different things for different values of function, assign to both
            buildup.rate_constant = fields[4]
            buildup.power_sat_constant = fields[5]
            if fields[6].upper()[0:4] == "CURB":  # In some input files, CURBLENGTH is written as CURB, allow either
                buildup.normalizer = Normalizer.CURBLENGTH
                # If is is not curb length, it defaults to the other value: AREA
        return buildup


class WashoffReader(SectionReader):
    """Specifies the rate at which pollutants are washed off from different land uses during rain events."""

    @staticmethod
    def read(new_text):
        washoff = Washoff()
        fields = new_text.split()
        if len(fields) > 1:
            washoff.land_use_name = fields[0]
            washoff.pollutant = fields[1]
        if len(fields) > 2:
            washoff.function = WashoffFunction[fields[2].upper()]
        if len(fields) > 3:
            washoff.coefficient = fields[3]
        if len(fields) > 4:
            washoff.exponent = fields[4]
        if len(fields) > 5:
            washoff.cleaning_efficiency = fields[5]
        if len(fields) > 6:
            washoff.bmp_efficiency = fields[6]
        return washoff


class PollutantReader(SectionReader):
    """Read the pollutants being analyzed"""

    @staticmethod
    def read(new_text):
        pollutant = Pollutant()
        fields = new_text.split()
        if len(fields) > 5:
            pollutant.name = fields[0]
            pollutant.units = ConcentrationUnits(ConcentrationUnitLabels.index(fields[1].upper()))
            pollutant.rain_concentration = fields[2]
            pollutant.gw_concentration = fields[3]
            pollutant.ii_concentration = fields[4]
            pollutant.decay_coefficient = fields[5]
        if len(fields) > 6:
            pollutant.snow_only = fields[6].upper() == "YES"
        if len(fields) > 7:
            pollutant.co_pollutant = fields[7]
        if len(fields) > 8:
            pollutant.co_fraction = fields[8]
        if len(fields) > 9:
            pollutant.dwf_concentration = fields[9]
        if len(fields) > 10:
            pollutant.initial_concentration = fields[10]
        return pollutant


class TimeSeriesReader(SectionReader):
    """One time series from the TIMESERIES section"""

    @staticmethod
    def read(new_text):
        time_series = TimeSeries()
        needs_date = 1
        needs_time = 2
        needs_value = 3
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(time_series, line)
            try:
                fields = line.split()
                if len(fields) > 1:
                    if time_series.name:
                        if time_series.name != fields[0]:
                            raise ValueError("TimeSeriesReader.read: Different Timeseries names " +
                                             time_series.name + ', ' + fields[0])
                    else:
                        time_series.name = fields[0]
                    if fields[1].upper() == "FILE":
                        time_series.file = ' '.join(fields[2:])
                    else:
                        state = needs_date
                        next_field = 1
                        while next_field < len(fields):
                            if state == needs_date:
                                if TimeSeries.is_date(fields[next_field]):
                                    time_series.dates.append(fields[next_field])
                                    next_field += 1
                                    if next_field == len(fields):
                                        break
                                else:
                                    time_series.dates.append('')
                                state = needs_time

                            if state == needs_time:
                                time_series.times.append(fields[next_field])
                                next_field += 1
                                if next_field == len(fields):
                                    break
                                state = needs_value

                            if state == needs_value:
                                time_series.values.append(fields[next_field])
                                next_field += 1
                                state = needs_date

                        if (len(time_series.dates) != len(time_series.times)) or (len(time_series.times) != len(time_series.values)):
                            raise ValueError("TimeSeriesReader.read: Different lengths:" "\nDates = " +
                                             str(len(time_series.dates)) +
                                             "\nTimes = " + str(len(time_series.times)) +
                                             "\nValues = " + str(len(time_series.values)))
            except Exception as ex:
                raise ValueError("Could not set timeseries from line: " + line + '\n' + str(ex))
        return time_series


class TitleReader(SectionReader):
    """SWMM descriptive title"""

    SECTION_NAME = "[TITLE]"

    @staticmethod
    def read(new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        title = Title()
        # Skip section name and blank lines/spaces/tabs at beginning or end
        lines = new_text.replace(title.SECTION_NAME, '').strip().splitlines()
        if len(lines) > 0:
            title.title = '\n'.join(lines)
        return title


class TemperatureReader(SectionReader):
    """temperature, wind speed, snow melt, and areal depletion parameters"""

    SECTION_NAME = "[TEMPERATURE]"


    @staticmethod
    def read(new_text):
        # type: (object) -> object
        temperature = Temperature()
        areal_depletion_text = ''
        for line in new_text.splitlines():
            try:
                line = SectionReader.set_comment_check_section(temperature, line)
                fields = line.split()
                if len(fields) > 1:
                    if fields[0].upper() == "TIMESERIES":
                        temperature.timeseries = ' '.join(fields[1:])
                        temperature.source = TemperatureSource.TIMESERIES
                    elif fields[0].upper() == "FILE":
                        # Check for optional start date as last field
                        if TimeSeries.is_date(fields[-1]):
                            temperature.start_date = fields[-1]
                            temperature.filename = ' '.join(fields[1:-1])
                        else:
                            temperature.filename = ' '.join(fields[1:])
                        temperature.source = TemperatureSource.FILE
                    elif fields[0].upper() == WindSpeed.SECTION_NAME:
                        temperature.wind_speed = WindSpeedReader.read(line)
                    elif fields[0].upper() == SnowMelt.SECTION_NAME:
                        temperature.snow_melt = SnowMeltReader.read(line)
                    elif fields[0].upper() == ArealDepletion.SECTION_NAME:
                        if areal_depletion_text:
                            areal_depletion_text += '\n'
                        areal_depletion_text += line
            except:
                print(temperature.SECTION_NAME + " skipping input line: " + line)
        if areal_depletion_text:
            temperature.areal_depletion = ArealDepletionReader.read(areal_depletion_text)
        return temperature


class EvaporationReader(SectionReader):
    """How daily evaporation rates vary with time for the study area"""

    SECTION_NAME = "[EVAPORATION]"

    @staticmethod
    def read(new_text):
        evaporation = Evaporation()
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(evaporation, line)
            fields = line.split()
            if len(fields) > 0:
                first_token = fields[0].upper()
                if len(fields) > 1 or first_token == "TEMPERATURE" or first_token == "FILE":
                    if first_token == "DRY_ONLY":
                        evaporation.dry_only_specified = True
                        evaporation.dry_only = fields[1].upper() == "YES"
                    elif first_token == "RECOVERY":
                        evaporation.recovery_pattern = ' '.join(fields[1:])
                    else:
                        try:
                            evaporation.format = EvaporationFormat[first_token]
                            if evaporation.format == EvaporationFormat.CONSTANT:
                                evaporation.constant = fields[1]
                            elif evaporation.format == EvaporationFormat.MONTHLY:
                                evaporation.monthly = fields[1:]
                            elif evaporation.format == EvaporationFormat.TIMESERIES:
                                evaporation.timeseries = fields[1]
                            elif evaporation.format == EvaporationFormat.TEMPERATURE:
                                pass
                            elif evaporation.format == EvaporationFormat.FILE:
                                evaporation.monthly_pan_coefficients = fields[1:]
                        except Exception as ex:
                            raise ValueError("Could not set " + evaporation.SECTION_NAME + " from: " + line + '\n' + str(ex))
        return evaporation


class WindSpeedReader:
    """wind speed parameters, stored as part of [TEMPERATURE] section"""

    SECTION_NAME = "WINDSPEED"

    @staticmethod
    def read(new_text):
        wind_speed = WindSpeed()
        fields = new_text.split()
        if len(fields) > 1:
            if fields[0].strip().upper() != wind_speed.SECTION_NAME:
                raise ValueError("Could not set " + wind_speed.SECTION_NAME + " from: " + new_text)
            wind_speed.source = WindSource[fields[1].upper()]
        if len(fields) > 2 and wind_speed.source == WindSource.MONTHLY:
            wind_speed.wind_speed_monthly = fields[2:]
        return wind_speed


class SnowMeltReader:
    """snow melt parameters"""

    SECTION_NAME = "SNOWMELT"

    @staticmethod
    def read(new_text):
        snow_melt = SnowMelt()
        fields = new_text.split()
        if len(fields) > 0:
            if fields[0].strip().upper() != snow_melt.SECTION_NAME:
                raise ValueError("Could not set " + snow_melt.SECTION_NAME + " from: " + new_text)
        if len(fields) > 1:
           snow_melt.snow_temp = fields[1]
        if len(fields) > 2:
           snow_melt.ati_weight = fields[2]
        if len(fields) > 3:
           snow_melt.negative_melt_ratio = fields[3]
        if len(fields) > 4:
           snow_melt.elevation = fields[4]
        if len(fields) > 5:
           snow_melt.latitude = fields[5]
        if len(fields) > 6:
           snow_melt.time_correction = fields[6]
        return snow_melt


class ArealDepletionReader:
    """areal depletion parameters"""

    SECTION_NAME = "ADC"

    @staticmethod
    def read(new_text):
        areal_depletion = ArealDepletion()
        for line in new_text.splitlines():
            fields = line.split()
            if len(fields) > 2:
                if fields[0].strip().upper() != areal_depletion.SECTION_NAME:
                    raise ValueError("Could not set " + areal_depletion.SECTION_NAME + " from: " + line)
                if fields[1].upper() == "IMPERVIOUS":
                    areal_depletion.adc_impervious = fields[2:]
                elif fields[1].upper() == "PERVIOUS":
                    areal_depletion.adc_pervious = fields[2:]
        return areal_depletion


class AdjustmentsReader(SectionReader):
    """Specifies optional monthly adjustments to be made to temperature, evaporation rate,
    rainfall intensity and hydraulic conductivity in each time period of a simulation."""

    SECTION_NAME = "[ADJUSTMENTS]"

    @staticmethod
    def read(new_text):
        adjustments = Adjustments()
        for line in new_text.splitlines():
            try:
                line = SectionReader.set_comment_check_section(adjustments, line)
                fields = line.split()
                if len(fields) > 12:
                    if fields[0].upper() == "TEMPERATURE":
                        adjustments.temperature = fields[1:]
                    elif fields[0].upper() == "EVAPORATION":
                        adjustments.evaporation = fields[1:]
                    elif fields[0].upper() == "RAINFALL":
                        adjustments.rainfall = fields[1:]
                    elif fields[0].upper() == "CONDUCTIVITY":
                        adjustments.soil_conductivity = fields[1:]
            except:
                print(adjustments.SECTION_NAME + " skipping input line: " + line)
        return adjustments


class ConduitReader(Link):
    """A conduit link (pipe or channel) in a SWMM model drainage system that conveys water from one node to another."""

    @staticmethod
    def read(new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        conduit = Conduit()
        new_text = SectionReader.set_comment_check_section(conduit, new_text)
        fields = new_text.split(None, 8)
        if len(fields) > 2:
            conduit.name, conduit.inlet_node, conduit.outlet_node = fields[0:3]
        if len(fields) > 3:
            conduit.length = fields[3]
        if len(fields) > 4:
            conduit.roughness = fields[4]
        if len(fields) > 5:
            conduit.inlet_offset = fields[5]
        if len(fields) > 6:
            conduit.outlet_offset = fields[6]
        if len(fields) > 7:
            conduit.initial_flow = fields[7]
        if len(fields) > 8:
            conduit.maximum_flow = fields[8]
        return conduit


class PumpReader(Link):
    """A pump link in a SWMM model"""

    @staticmethod
    def read(new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        pump = Pump()
        new_text = SectionReader.set_comment_check_section(pump, new_text)
        fields = new_text.split(None, 8)
        if len(fields) > 2:
            pump.name, pump.inlet_node, pump.outlet_node = fields[0:3]
        if len(fields) > 3:
            pump.pump_curve = fields[3]
        if len(fields) > 4:
            pump.initial_status = fields[4]
        if len(fields) > 5:
            pump.startup_depth = fields[5]
        if len(fields) > 6:
            pump.shutoff_depth = fields[6]
        return pump


class OrificeReader(Link):
    @staticmethod
    def read(new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        orifice = Orifice()
        new_text = SectionReader.set_comment_check_section(orifice, new_text)
        fields = new_text.split(None, 8)
        if len(fields) > 2:
            orifice.name, orifice.inlet_node, orifice.outlet_node = fields[0:3]
        if len(fields) > 3:
            orifice.setattr_keep_type("type", fields[3])
        if len(fields) > 4:
            orifice.setattr_keep_type("inlet_offset", fields[4])
        if len(fields) > 5:
            orifice.setattr_keep_type("discharge_coefficient", fields[5])
        if len(fields) > 6:
            orifice.setattr_keep_type("flap_gate", fields[6])
        if len(fields) > 7:
            orifice.setattr_keep_type("initial_flow", fields[7])
        if len(fields) > 8:
            orifice.setattr_keep_type("o_rate", fields[8])
        return orifice


class WeirReader(Link):
    @staticmethod
    def read(new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        weir = Weir()
        new_text = SectionReader.set_comment_check_section(weir, new_text)
        fields = new_text.split(None, 8)
        if len(fields) > 5:
            weir.name = fields[0]
            weir.inlet_node = fields[1]
            weir.outlet_node = fields[2]
            weir.setattr_keep_type("type", fields[3])
            weir.setattr_keep_type("inlet_offset", fields[4])
            weir.setattr_keep_type("discharge_coefficient", fields[5])
        if len(fields) > 6:
            weir.setattr_keep_type("flap_gate", fields[6])
        if len(fields) > 7:
            weir.setattr_keep_type("end_contractions", fields[7])
        if len(fields) > 8:
            weir.setattr_keep_type("end_coefficient", fields[8])
        if len(fields) > 9:
            weir.setattr_keep_type("can_surcharge", fields[9])
        if len(fields) > 10:
            weir.setattr_keep_type("road_width", fields[10])
        if len(fields) > 11:
            weir.setattr_keep_type("road_surface", fields[11])
        return weir


class OutletReader(Link):
    @staticmethod
    def read(new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        outlet = Outlet()
        new_text = SectionReader.set_comment_check_section(outlet, new_text)
        fields = new_text.split(None, 8)
        if len(fields) > 4:
            outlet.name = fields[0]
            outlet.inlet_node = fields[1]
            outlet.outlet_node = fields[2]
            outlet.setattr_keep_type("inlet_offset", fields[3])
            outlet.setattr_keep_type("curve_type", fields[4].replace('/', '_'))
        if outlet.curve_type in (OutletCurveType.TABULAR_DEPTH, OutletCurveType.TABULAR_HEAD):
            if len(fields) > 5:
                outlet.setattr_keep_type("rating_curve", fields[5])
            if len(fields) > 6:
                outlet.setattr_keep_type("flap_gate", fields[6])
        elif outlet.curve_type in (OutletCurveType.FUNCTIONAL_DEPTH, OutletCurveType.FUNCTIONAL_HEAD):
            if len(fields) > 5:
                outlet.setattr_keep_type("coefficient", fields[5])
            if len(fields) > 6:
                outlet.setattr_keep_type("exponent", fields[6])
            if len(fields) > 7:
                outlet.setattr_keep_type("flap_gate", fields[7])
        return outlet


class CrossSectionReader(SectionReader):
    """A cross section of a Conduit, Orifice, or Weir

    Attributes:
        link (str): name of the conduit, orifice, or weir this is a cross-section of.
        shape (CrossSectionShape): name of cross-section shape.
        geometry1 (str): full height of the cross-section (ft or m). For irregular, this is the cross-section name.
        geometry2 (str): auxiliary parameters (width, side slopes, etc.)
        geometry3 (str): auxiliary parameters (width, side slopes, etc.)
        geometry4 (str): auxiliary parameters (width, side slopes, etc.)
        barrels (str): number of barrels (i.e., number of parallel pipes of equal size, slope, and
                       roughness) associated with a conduit (default is 1).
        culvert_code (str): name of conduit inlet geometry if it is a culvert subject to possible inlet flow control
        curve (str): name of associated Shape Curve that defines how width varies with depth.
    """


    @staticmethod
    def read(new_text):
        cross_section = CrossSection()
        new_text = SectionReader.set_comment_check_section(cross_section, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            cross_section.link = fields[0]
        if len(fields) > 1:
            cross_section.setattr_keep_type("shape", fields[1])
        if cross_section.shape == CrossSectionShape.CUSTOM:
            if len(fields) > 2:
                cross_section.geometry1 = fields[2]
            if len(fields) > 3:
                cross_section.curve = fields[3]
            if len(fields) > 4:
                cross_section.barrels = fields[4]
                if len(fields) > 6 and fields[6].isdigit():  # Old interface saves CUSTOM barrels in this field.
                    cross_section.barrels = fields[6]
        # elif cross_section.shape == CrossSectionShape.IRREGULAR:
        #     if len(fields) > 2:
        #         cross_section.transect = fields[2]
        else:
            if len(fields) > 2:
                cross_section.geometry1 = fields[2]
            if len(fields) > 3:
                cross_section.geometry2 = fields[3]
            if len(fields) > 4:
                cross_section.geometry3 = fields[4]
            if len(fields) > 5:
                cross_section.geometry4 = fields[5]
            if len(fields) > 6:
                cross_section.barrels = fields[6]
            if len(fields) > 7:
                cross_section.culvert_code = fields[7]
        return cross_section


class ControlsReader(SectionReader):

    SECTION_NAME = "[CONTROLS]"

    @staticmethod
    def read(new_text):
        controls = Controls()
        start_search = new_text.find("RULE") + 1
        controls.value = new_text[0:start_search] + new_text[start_search:].replace("\nRULE", "\n\nRULE")
        return controls


class TransectsReader(SectionReader):

    SECTION_NAME = "[TRANSECTS]"
    DEFAULT_COMMENT = ";;Transect Data in HEC-2 format"

    @staticmethod
    def read(new_text):
        transects = Transects()
        transects.value = []
        item_lines = []
        line = ''
        found_non_comment = False
        for line in new_text.splitlines():
            if line.startswith(";;") or line.startswith('['):
                SectionReader.set_comment_check_section(transects, line)
            elif line.startswith(';'):
                if found_non_comment:  # This comment must be the start of the next one, so build the previous one
                    try:
                        transects.value.append(TransectReader.read('\n'.join(item_lines)))
                        item_lines = []
                        found_non_comment = False
                    except Exception as e:
                        print("Could not create object from: " + line + '\n' + str(e) + '\n' + str(traceback.print_exc()))
                item_lines.append(line)
            elif not line.strip():  # add blank row as a comment item in transects.value list
                comment = Section()
                comment.name = "Comment"
                comment.value = ''
                transects.value.append(comment)
            else:
                item_lines.append(line)
                found_non_comment = True

        if found_non_comment:  # Found a final one that has not been built yet, build it now
            try:
                transects.value.append(TransectReader.read('\n'.join(item_lines)))
            except Exception as e:
                print("Could not create object from: " + line + '\n' + str(e) + '\n' + str(traceback.print_exc()))
        return transects


class TransectReader(SectionReader):
    """the cross-section geometry of a natural channel or conduit with irregular shapes"""


    @staticmethod
    def read(new_text):
        transect = Transect()
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(transect, line)
            fields = line.split()
            if len(fields) > 2:
                if fields[0].upper() == "GR":
                    for elev_index in range(1, len(fields) - 1, 2):
                        transect.stations.append((fields[elev_index], fields[elev_index + 1]))
                elif len(fields) > 3:
                    if fields[0].upper() == "NC":
                        (transect.n_left, transect.n_right, transect.n_channel) = fields[1:4]
                    elif fields[0].upper() == "X1":
                        transect.name = fields[1]
                        transect.overbank_left = fields[3]
                        if len(fields) > 4:
                            transect.overbank_right = fields[4]
                        if len(fields) > 7:
                            transect.meander_modifier = fields[7]
                        if len(fields) > 8:
                            transect.stations_modifier = fields[8]
                        if len(fields) > 9:
                            transect.elevations_modifier = fields[9]
        return transect


class JunctionReader(SectionReader):
    """A Junction node"""

    @staticmethod
    def read(new_text):
        junction = Junction()
        new_text = SectionReader.set_comment_check_section(junction, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            junction.name = fields[0]
        if len(fields) > 1:
            junction.elevation = fields[1]
        if len(fields) > 2:
            junction.max_depth = fields[2]
        if len(fields) > 3:
            junction.initial_depth = fields[3]
        if len(fields) > 4:
            junction.surcharge_depth = fields[4]
        if len(fields) > 5:
            junction.ponded_area = fields[5]
        return junction


class OutfallReader(SectionReader):
    """Read outfall properties"""

    @staticmethod
    def read(new_text):
        outfall = Outfall()
        new_text = SectionReader.set_comment_check_section(outfall, new_text)
        fields = new_text.split()
        if len(fields) > 2:
            outfall.name = fields[0]
            outfall.setattr_keep_type("elevation", fields[1])
            outfall.setattr_keep_type("outfall_type", fields[2])
            gated_field = 4
            if outfall.outfall_type == OutfallType.FIXED:
                outfall.setattr_keep_type("fixed_stage", fields[3])
            elif outfall.outfall_type == OutfallType.TIDAL:
                outfall.setattr_keep_type("tidal_curve", fields[3])
            elif outfall.outfall_type == OutfallType.TIMESERIES:
                outfall.time_series_name = fields[3]
            else:
                gated_field = 3
            if len(fields) > gated_field:
                outfall.setattr_keep_type("tidal_gate", fields[gated_field])
            if len(fields) > gated_field + 1:
                outfall.route_to = fields[gated_field + 1]
        else:
            outfall = None
        return outfall


class DividerReader(SectionReader):
    """Read a flow divider node"""

    @staticmethod
    def read(new_text):
        divider = Divider()
        new_text = SectionReader.set_comment_check_section(divider, new_text)
        fields = new_text.split()
        if len(fields) > 3:
            divider.name = fields[0]
            divider.setattr_keep_type("elevation", fields[1])
            divider.diverted_link = fields[2]
            divider.setattr_keep_type("flow_divider_type", fields[3])
            if len(fields) > 4:
                if divider.flow_divider_type == FlowDividerType.OVERFLOW:
                    divider.setattr_keep_type("max_depth", fields[4])
                    if len(fields) > 5:
                        divider.setattr_keep_type("initial_depth", fields[5])
                    if len(fields) > 6:
                        divider.setattr_keep_type("surcharge_depth", fields[6])
                    if len(fields) > 7:
                        divider.setattr_keep_type("ponded_area", fields[7])
                elif divider.flow_divider_type == FlowDividerType.CUTOFF:
                    divider.setattr_keep_type("min_diversion_flow", fields[4])
                    if len(fields) > 5:
                        divider.setattr_keep_type("max_depth", fields[5])
                    if len(fields) > 6:
                        divider.setattr_keep_type("initial_depth", fields[6])
                    if len(fields) > 7:
                        divider.setattr_keep_type("surcharge_depth", fields[7])
                    if len(fields) > 8:
                        divider.setattr_keep_type("ponded_area", fields[8])
                elif divider.flow_divider_type == FlowDividerType.TABULAR:
                    divider.divider_curve = fields[4]
                    if len(fields) > 5:
                        divider.setattr_keep_type("max_depth", fields[5])
                    if len(fields) > 6:
                        divider.setattr_keep_type("initial_depth", fields[6])
                    if len(fields) > 7:
                        divider.setattr_keep_type("surcharge_depth", fields[7])
                    if len(fields) > 8:
                        divider.setattr_keep_type("ponded_area", fields[8])

                elif divider.flow_divider_type == FlowDividerType.WEIR:
                    divider.setattr_keep_type("min_diversion_flow", fields[4])
                    if len(fields) > 5:
                        divider.setattr_keep_type("weir_max_depth", fields[5])
                    if len(fields) > 6:
                        divider.setattr_keep_type("weir_coefficient", fields[6])
                    if len(fields) > 7:
                        divider.setattr_keep_type("max_depth", fields[7])
                    if len(fields) > 8:
                        divider.setattr_keep_type("initial_depth", fields[8])
                    if len(fields) > 9:
                        divider.setattr_keep_type("surcharge_depth", fields[9])
                    if len(fields) > 10:
                        divider.setattr_keep_type("ponded_area", fields[10])
        return divider


class StorageReader(SectionReader):
    """Read a storage unit from text"""

    @staticmethod
    def read(new_text):
        storage = StorageUnit()
        new_text = SectionReader.set_comment_check_section(storage, new_text)
        fields = new_text.split()
        if len(fields) > 4:
            storage.name = fields[0]
            storage.setattr_keep_type("elevation", fields[1])
            storage.setattr_keep_type("max_depth", fields[2])
            storage.setattr_keep_type("initial_depth", fields[3])
            storage.setattr_keep_type("storage_curve_type", fields[4])
            if len(fields) > 5:
                if storage.storage_curve_type == StorageCurveType.TABULAR:
                    storage.storage_curve = fields[5]
                    next_field = 6
                elif storage.storage_curve_type == StorageCurveType.FUNCTIONAL and len(fields) > 7:
                    storage.setattr_keep_type("coefficient", fields[5])
                    storage.setattr_keep_type("exponent", fields[6])
                    storage.setattr_keep_type("constant", fields[7])
                    next_field = 8

                if len(fields) > next_field:
                    storage.setattr_keep_type("ponded_area", fields[next_field])
                    next_field += 1
                if len(fields) > next_field:
                    storage.setattr_keep_type("evaporation_factor", fields[next_field])
                    next_field += 1
                if len(fields) > next_field:
                    storage.setattr_keep_type("seepage_suction_head", fields[next_field])
                    next_field += 1
                if len(fields) > next_field:
                    storage.setattr_keep_type("seepage_hydraulic_conductivity", fields[next_field])
                    next_field += 1
                if len(fields) > next_field:
                    storage.setattr_keep_type("seepage_initial_moisture_deficit", fields[next_field])
        return storage


class DirectInflowReader(SectionReader):
    """Defines characteristics of inflows added directly into a node"""


    @staticmethod
    def read(new_text):
        direct_inflow = DirectInflow()
        new_text = SectionReader.set_comment_check_section(direct_inflow, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            direct_inflow.node = fields[0]
        if len(fields) > 1:
            direct_inflow.constituent = fields[1]
        if len(fields) > 2:
            direct_inflow.timeseries = fields[2]
        if len(fields) > 3 and direct_inflow.constituent.upper() != "FLOW":
            direct_inflow.setattr_keep_type("format", DirectInflowType[fields[3]])
        if len(fields) > 4:
            direct_inflow.conversion_factor = fields[4]
        if len(fields) > 5:
            direct_inflow.scale_factor = fields[5]
        if len(fields) > 6:
            direct_inflow.baseline = fields[6]
        if len(fields) > 7:
            direct_inflow.baseline_pattern = fields[7]
        return direct_inflow


class DryWeatherInflowReader(SectionReader):
    """Specifies dry weather flow and its quality entering the drainage system at a specific node"""


    @staticmethod
    def read(new_text):
        dry_weather_inflow = DryWeatherInflow()
        new_text = SectionReader.set_comment_check_section(dry_weather_inflow, new_text)
        fields = new_text.split()
        if len(fields) > 2:
            dry_weather_inflow.node = fields[0]
            dry_weather_inflow.constituent = fields[1]
            dry_weather_inflow.average = fields[2]
            if len(fields) > 3:
                dry_weather_inflow.time_patterns = fields[3:]
        return dry_weather_inflow


class RDIInflowReader(SectionReader):
    """Defines characteristics of Rainfall-Dependent Infiltration/Inflows entering the system at a node"""


    @staticmethod
    def read(new_text):
        rdi_inflow = RDIInflow()
        new_text = SectionReader.set_comment_check_section(rdi_inflow, new_text)
        fields = new_text.split()
        if len(fields) > 2:
            rdi_inflow.node = fields[0]
            rdi_inflow.hydrograph_group = fields[1]
            rdi_inflow.sewershed_area = fields[2]
        return rdi_inflow


class TreatmentReader(SectionReader):
    """Define the treatment properties of a node using a treatment expression"""


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
    def read(new_text):
        treatment = Treatment()
        new_text = SectionReader.set_comment_check_section(treatment, new_text)
        fields = new_text.split()
        if len(fields) > 2:
            treatment.node = fields[0]
            treatment.pollutant = fields[1]
            treatment.function = ' '.join(fields[2:])
        return treatment


class AquiferReader(SectionReader):
    """Sub-surface groundwater area that models water infiltrating."""

    @staticmethod
    def read(new_text):
        aquifer = Aquifer()
        new_text = SectionReader.set_comment_check_section(aquifer, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            aquifer.name = fields[0]
        if len(fields) > 1:
            aquifer.porosity = fields[1]
        if len(fields) > 2:
            aquifer.wilting_point = fields[2]
        if len(fields) > 3:
            aquifer.field_capacity = fields[3]
        if len(fields) > 4:
            aquifer.conductivity = fields[4]
        if len(fields) > 5:
            aquifer.conductivity_slope = fields[5]
        if len(fields) > 6:
            aquifer.tension_slope = fields[6]
        if len(fields) > 7:
            aquifer.upper_evaporation_fraction = fields[7]
        if len(fields) > 8:
            aquifer.lower_evaporation_depth = fields[8]
        if len(fields) > 9:
            aquifer.lower_groundwater_loss_rate = fields[9]
        if len(fields) > 10:
            aquifer.bottom_elevation = fields[10]
        if len(fields) > 11:
            aquifer.water_table_elevation = fields[11]
        if len(fields) > 12:
            aquifer.unsaturated_zone_moisture = fields[12]
        if len(fields) > 13:
            aquifer.upper_evaporation_pattern = fields[13]
        return aquifer


class LIDControlReader(SectionReader):
    """Defines scale-independent LID controls that can be deployed within subcatchments"""

    LineTypes = (
        ("has_surface_layer",
         "SURFACE",
         "surface_layer_storage_depth",
         "surface_layer_vegetative_cover_fraction",
         "surface_layer_surface_roughness",
         "surface_layer_surface_slope",
         "surface_layer_swale_side_slope"),
        ("has_soil_layer",
         "SOIL",
         "soil_layer_thickness",
         "soil_layer_porosity",
         "soil_layer_field_capacity",
         "soil_layer_wilting_point",
         "soil_layer_conductivity",
         "soil_layer_conductivity_slope",
         "soil_layer_suction_head"),
        ("has_pavement_layer",
         "PAVEMENT",
         "pavement_layer_thickness",
         "pavement_layer_void_ratio",
         "pavement_layer_impervious_surface_fraction",
         "pavement_layer_permeability",
         "pavement_layer_clogging_factor"),
        ("has_storage_layer",
         "STORAGE",
         "storage_layer_height",
         "storage_layer_void_ratio",
         "storage_layer_filtration_rate",
         "storage_layer_clogging_factor"),
        ("has_underdrain_system",
         "DRAIN",
         "drain_coefficient",
         "drain_exponent",
         "drain_offset_height",
         "drain_delay"),
        ("has_drainmat_system",
         "DRAINMAT",
         "drainmat_thickness",
         "drainmat_void_fraction",
         "drainmat_roughness"))

    @staticmethod
    def read(new_text):
        lid_control = LIDControl()
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(lid_control, line)
            if line:
                fields = line.split()
                if len(fields) == 2:
                    if lid_control.name:
                        raise ValueError("LIDControlReader.read: LID name already set: " +
                                         lid_control.name + ", then found 2-element line: " + line)
                    lid_control.name = fields[0]
                    try:
                        lid_control.lid_type = LIDType[fields[1].upper()]
                    except:
                        raise ValueError("LIDControlReader.read: Unknown LID type in second field: " + line)
                elif len(fields) > 2:
                    if fields[0] != lid_control.name:
                        raise ValueError("LIDControlReader.read: LID name: {} != {}".format(fields[0], lid_control.name))
                    check_type = fields[1].upper()
                    found_type = False
                    for field_names in LIDControl.LineTypes:
                        if field_names[1].upper() == check_type:
                            found_type = True
                            setattr(lid_control, field_names[0], True)  # Set flag to show it has this
                            for (field_name, field_value) in zip(field_names[2:], fields[2:]):
                                lid_control.setattr_keep_type(field_name, field_value)
                            continue
                    if not found_type:
                        raise ValueError("LIDControlReader.read: Unknown line: " + line)
        return lid_control


class SnowPackReader(SectionReader):
    """Snow pack parameters"""

    LineTypes = (
        ("has_plowable",
         "PLOWABLE",
         "plowable_minimum_melt_coefficient",
         "plowable_maximum_melt_coefficient",
         "plowable_base_temperature",
         "plowable_fraction_free_water_capacity",
         "plowable_initial_snow_depth",
         "plowable_initial_free_water",
         "plowable_fraction_impervious_area"),
        ("has_impervious",
         "IMPERVIOUS",
         "impervious_minimum_melt_coefficient",
         "impervious_maximum_melt_coefficient",
         "impervious_base_temperature",
         "impervious_fraction_free_water_capacity",
         "impervious_initial_snow_depth",
         "impervious_initial_free_water",
         "impervious_depth_100_cover"),
        ("has_pervious",
         "PERVIOUS",
         "pervious_minimum_melt_coefficient",
         "pervious_maximum_melt_coefficient",
         "pervious_base_temperature",
         "pervious_fraction_free_water_capacity",
         "pervious_initial_snow_depth",
         "pervious_initial_free_water",
         "pervious_depth_100_cover"),
        ("has_removal",
         "REMOVAL",
         "depth_snow_removal_begins",
         "fraction_transferred_out_watershed",
         "fraction_transferred_impervious_area",
         "fraction_transferred_pervious_area",
         "fraction_converted_immediate_melt",
         "fraction_moved_another_subcatchment",
         "subcatchment_transfer"))

    @staticmethod
    def read(new_text):
        snow_pack = SnowPack()
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(snow_pack, line)
            if line:
                fields = line.split()
                if len(fields) > 2:
                    if not snow_pack.name:                      # If we have not found a name yet, use the first one we find
                        snow_pack.name = fields[0]
                    elif fields[0] != snow_pack.name:           # If we find a different name, complain
                        raise ValueError("SnowPackReader.read: name: " + fields[0] + " != " + snow_pack.name)
                    check_type = fields[1].upper()
                    found_type = False
                    for field_names in snow_pack.LineTypes:
                        if field_names[1].upper() == check_type:  # Find the group of fields this line is about
                            found_type = True
                            setattr(snow_pack, field_names[0], True)   # Set flag to show we have this group
                            for (field_name, field_value) in zip(field_names[2:], fields[2:]):
                                snow_pack.setattr_keep_type(field_name, field_value)
                            continue
                    if not found_type:
                        raise ValueError("SnowPackReader.read: Unknown line: " + line)
        return snow_pack


class SubcatchmentReader(SectionReader):
    """Subcatchment geometry, location, parameters, and time-series data"""

    @staticmethod
    def read(new_text):
        subcatchment = Subcatchment()
        fields = new_text.split()
        if len(fields) > 0:
            subcatchment.name = fields[0]
        if len(fields) > 1:
            subcatchment.rain_gage = fields[1]
        if len(fields) > 2:
            subcatchment.outlet = fields[2]
        if len(fields) > 3:
            subcatchment.area = fields[3]
        if len(fields) > 4:
            subcatchment.percent_impervious = fields[4]
        if len(fields) > 5:
            subcatchment.width = fields[5]
        if len(fields) > 6:
            subcatchment.percent_slope = fields[6]
        if len(fields) > 7:
            subcatchment.curb_length = fields[7]
        if len(fields) > 8:
            subcatchment.snow_pack = fields[8]
        return subcatchment


class HortonInfiltrationReader(SectionReader):
    """Horton Infiltration parameters"""

    @staticmethod
    def read(new_text):
        horton_infiltration = HortonInfiltration()
        new_text = SectionReader.set_comment_check_section(horton_infiltration, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            horton_infiltration.subcatchment = fields[0]
        if len(fields) > 1:
            horton_infiltration.max_rate = fields[1]
        if len(fields) > 2:
            horton_infiltration.min_rate = fields[2]
        if len(fields) > 3:
            horton_infiltration.decay = fields[3]
        if len(fields) > 4:
            horton_infiltration.dry_time = fields[4]
        if len(fields) > 5:
            horton_infiltration.max_volume = fields[5]
        return horton_infiltration


class GreenAmptInfiltrationReader(SectionReader):
    """Green-Ampt Infiltration parameters"""

    @staticmethod
    def read(new_text):
        green_ampt_infiltration = GreenAmptInfiltration()
        new_text = SectionReader.set_comment_check_section(green_ampt_infiltration, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            green_ampt_infiltration.subcatchment = fields[0]
        if len(fields) > 1:
            green_ampt_infiltration.suction = fields[1]
        if len(fields) > 2:
            green_ampt_infiltration.hydraulic_conductivity = fields[2]
        if len(fields) > 3:
            green_ampt_infiltration.initial_moisture_deficit = fields[3]
        return green_ampt_infiltration


class CurveNumberInfiltrationReader(SectionReader):
    """Curve Number Infiltration parameters"""

    @staticmethod
    def read(new_text):
        curve_number_infiltration = CurveNumberInfiltration()
        new_text = SectionReader.set_comment_check_section(curve_number_infiltration, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            curve_number_infiltration.subcatchment = fields[0]
        if len(fields) > 1:
            curve_number_infiltration.curve_number = fields[1]
        if len(fields) > 2:
            curve_number_infiltration.hydraulic_conductivity = fields[2]
        if len(fields) > 3:
            curve_number_infiltration.dry_days = fields[3]
        return curve_number_infiltration


class GroundwaterReader(SectionReader):
    """Link a subcatchment to an aquifer and to a drainage system node"""

    @staticmethod
    def read(new_text):
        groundwater = Groundwater()
        new_text = SectionReader.set_comment_check_section(groundwater, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            groundwater.subcatchment = fields[0]
        if len(fields) > 1:
            groundwater.aquifer = fields[1]
        if len(fields) > 2:
            groundwater.receiving_node = fields[2]
        if len(fields) > 3:
            groundwater.surface_elevation = fields[3]
        if len(fields) > 4:
            groundwater.groundwater_flow_coefficient = fields[4]
        if len(fields) > 5:
            groundwater.groundwater_flow_exponent = fields[5]
        if len(fields) > 6:
            groundwater.surface_water_flow_coefficient = fields[6]
        if len(fields) > 7:
            groundwater.surface_water_flow_exponent = fields[7]
        if len(fields) > 8:
            groundwater.surface_gw_interaction_coefficient = fields[8]
        if len(fields) > 9:
            groundwater.fixed_surface_water_depth = fields[9]
        if len(fields) > 10:
            groundwater.threshold_groundwater_elevation = fields[10]
        if len(fields) > 11:
            groundwater.bottom_elevation = fields[11]
        if len(fields) > 12:
            groundwater.water_table_elevation = fields[12]
        if len(fields) > 13:
            groundwater.unsaturated_zone_moisture = fields[13]
        return groundwater


class LIDUsageReader(SectionReader):
    """Specifies how an LID control will be deployed in a subcatchment"""


    @staticmethod
    def read(new_text):
        lid_usage = LIDUsage()
        fields = new_text.split()
        if len(fields) > 0:
            lid_usage.subcatchment_name = fields[0]
        if len(fields) > 1:
            lid_usage.control_name = fields[1]
        if len(fields) > 2:
            lid_usage.number_replicate_units = fields[2]
        if len(fields) > 3:
            lid_usage.area_each_unit = fields[3]
        if len(fields) > 4:
            lid_usage.top_width_overland_flow_surface = fields[4]
        if len(fields) > 5:
            lid_usage.percent_initially_saturated = fields[5]
        if len(fields) > 6:
            lid_usage.percent_impervious_area_treated = fields[6]
        if len(fields) > 7:
            lid_usage.send_outflow_pervious_area = fields[7]
        if len(fields) > 8:
            lid_usage.detailed_report_file = fields[8]
        return lid_usage


class CoverageReader(SectionReader):
    """Specifies the percentage of a subcatchments area that is covered by each category of land use."""


    @staticmethod
    def read(new_text):
        """ This method is not used when reading input files because there may be more than one on a line.
            See the method that reads the Coverages section below. """
        coverage = Coverage()
        fields = new_text.split()
        coverage.__init__(fields[0], fields[1], fields[2])
        return coverage


class CoveragesReader(SectionReader):
    """Specifies the percentage of a subcatchments area that is covered by each category of land use."""

    SECTION_NAME = "[COVERAGES]"
    DEFAULT_COMMENT = ";;Subcatchment  \tLand Use        \tPercent\n"\
                      ";;--------------\t----------------\t----------"

    @staticmethod
    def read(new_text):
        coverages = Coverages()
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(coverages, line)
            fields = line.split()
            if len(fields) > 2:
                subcatchment = fields[0]
                for landuse_index in range(1, len(fields) - 1, 2):
                    coverages.value.append(Coverage(subcatchment, fields[landuse_index], fields[landuse_index+1]))
        return coverages


class InitialLoadingReader(SectionReader):
    """Specifies a pollutant buildup that exists on a subcatchment at the start of a simulation."""

    @staticmethod
    def read(new_text):
        initial_loading = InitialLoading()
        new_text = SectionReader.set_comment_check_section(initial_loading, new_text)
        fields = new_text.split()
        if len(fields) > 2:
            initial_loading.subcatchment_name, initial_loading.pollutant_name, initial_loading.initial_buildup = fields[0:3]
        return initial_loading


class InitialLoadingsReader(SectionReader):
    """Specifies the pollutant buildup that exists on each subcatchment at the start of a simulation."""

    SECTION_NAME = "[LOADINGS]"
    DEFAULT_COMMENT = ";;Subcatchment  \tPollutant       \tBuildup\n"\
                      ";;--------------\t----------------\t----------"

    @staticmethod
    def read(new_text):
        initial_loadings = InitialLoadings()
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(initial_loadings, line)
            fields = line.split()
            if len(fields) > 2:
                subcatchment = fields[0]
                for index in range(1, len(fields) - 1, 2):
                    new_loading = InitialLoadingReader.read(subcatchment + ' ' + fields[index] + ' ' + fields[index+1])
                    initial_loadings.value.append(new_loading)
        return initial_loadings


class RainGageReader(SectionReader):
    """Read a rain gage from text"""

    @staticmethod
    def read(new_text):
        rain_gage = RainGage()
        new_text = SectionReader.set_comment_check_section(rain_gage, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            rain_gage.name = fields[0]
        if len(fields) > 1:
            rain_gage.setattr_keep_type("rain_format", fields[1])
        if len(fields) > 2:
            rain_gage.rain_interval = fields[2]
        if len(fields) > 3:
            rain_gage.snow_catch_factor = fields[3]
        if len(fields) > 5:
            if fields[4].upper() == "TIMESERIES":
                rain_gage.timeseries = fields[5]
            else:
                rain_gage.data_file_name = fields[5]
                if len(fields) > 6:
                    rain_gage.data_file_station_id = fields[6]
                if len(fields) > 7:
                    rain_gage.data_file_rain_units = fields[7]
        return rain_gage


class SubareasReader(SectionReader):
    """Read subarea information from text into project.subbasins"""

    @staticmethod
    def read(new_text, project):
        disposable_subareas = Section()
        disposable_subareas.SECTION_NAME = "[SUBAREAS]"
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(disposable_subareas, line)
            fields = line.split()
            if len(fields) > 5:
                subcatchment_name = fields[0]
                for subcatchment in project.subcatchments.value:
                    if subcatchment.name == subcatchment_name:
                        subcatchment.setattr_keep_type("n_imperv", fields[1])
                        subcatchment.setattr_keep_type("n_perv", fields[2])
                        subcatchment.setattr_keep_type("storage_depth_imperv", fields[3])
                        subcatchment.setattr_keep_type("storage_depth_perv", fields[4])
                        subcatchment.setattr_keep_type("percent_zero_impervious", fields[5])
                        subcatchment.subarea_routing = Routing.OUTLET
                        if len(fields) > 6:
                            routing = fields[6].upper()
                            if routing.startswith("I"):
                                subcatchment.subarea_routing = Routing.IMPERVIOUS
                            elif routing.startswith("P"):
                                subcatchment.subarea_routing = Routing.PERVIOUS
                        if len(fields) > 7:
                            subcatchment.setattr_keep_type("percent_routed", fields[7])


class TagsReader(SectionReader):
    """Read tag information from text into project objects that have tags"""

    @staticmethod
    def read(new_text, project):
        section_map = {"GAGE": [project.raingages.value],
                       "SUBCATCH": [project.subcatchments.value],
                       "NODE": [project.junctions.value, project.outfalls.value,
                                project.dividers.value, project.storage.value],
                       "LINK": [project.conduits.value, project.pumps.value, project.orifices.value,
                                project.weirs.value, project.outlets.value]}
        disposable_tags = Section()
        disposable_tags.SECTION_NAME = "[TAGS]"
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(disposable_tags, line)
            fields = line.split()
            if len(fields) > 2:
                object_type_name = fields[0].upper()
                object_name = fields[1].upper()
                tag = ' '.join(fields[2:])
                sections = section_map[object_type_name]
                found = False
                for section in sections:
                    for candidate in section:
                        if candidate.name.upper() == object_name:
                            candidate.tag = tag
                            found = True
                            # print "Tagged: " + type(candidate).__name__ + ' ' + candidate.name + ' = ' + tag
                            break
                    if found:
                        break
                if not found:
                    print "Tag not applied: " + line


class LossesReader(SectionReader):
    """Read LOSSES section from text into project.conduits"""

    @staticmethod
    def read(new_text, project):
        disposable_losses = Section()
        disposable_losses.SECTION_NAME = "[LOSSES]"
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(disposable_losses, line)
            fields = line.split()
            if len(fields) > 3:
                conduit_name = fields[0]
                for conduit in project.conduits.value:
                    if conduit.name == conduit_name:
                        conduit.setattr_keep_type("entry_loss_coefficient", fields[1])
                        conduit.setattr_keep_type("exit_loss_coefficient", fields[2])
                        conduit.setattr_keep_type("loss_coefficient", fields[3])
                        if len(fields) > 4:
                            conduit.setattr_keep_type("flap_gate", fields[4])
                        if len(fields) > 5:
                            conduit.setattr_keep_type("seepage", fields[5])


class UnitHydrographReader(SectionReader):
    """Specifies the shapes of the triangular unit hydrographs that determine the amount of
        rainfall-dependent infiltration/inflow (RDII) entering the drainage system"""

    @staticmethod
    def read(new_text):
        unit_hydrograph = UnitHydrograph()
        for line in new_text.splitlines():
            entry = None
            line = SectionReader.set_comment_check_section(unit_hydrograph, line)
            if line:
                fields = line.split()
                if unit_hydrograph.name and unit_hydrograph.name != "Unnamed" and unit_hydrograph.name != fields[0]:
                    raise ValueError("UnitHydrographReader.read: name: " + fields[0] + " != " +
                                     unit_hydrograph.name + "\nin line: " + line)
                if len(fields) == 2:
                    (unit_hydrograph.name, unit_hydrograph.rain_gage_name) = fields
                elif len(fields) > 5:
                    entry = UnitHydrographEntry()
                    entry.hydrograph_month = fields[1]
                    entry.term = fields[2]
                    entry.response_ratio = fields[3]
                    entry.time_to_peak = fields[4]
                    entry.recession_limb_ratio = fields[5]
                    if len(fields) > 6:
                        entry.initial_abstraction_depth = fields[6]
                    if len(fields) > 7:
                        entry.initial_abstraction_rate = fields[7]
                    if len(fields) > 8:
                        entry.initial_abstraction_amount = fields[8]
                else:
                    print("UnitHydrographReader.read skipped: " + line)
            if entry:
                unit_hydrograph.value.append(entry)
        return unit_hydrograph


class BackdropOptionsReader(SectionReader):
    """Identifies a backdrop image and dimensions for the network map"""

    SECTION_NAME = "[BACKDROP]"

    @staticmethod
    def read(new_text):
        backdrop_options = BackdropOptions()
        for line in new_text.splitlines():
            try:
                line = SectionReader.set_comment_check_section(backdrop_options, line)
                fields = line.split()
                if len(fields) > 1:
                    if fields[0].lower() == "dimensions" and len(fields) > 4:
                        backdrop_options.dimensions = (float(fields[1]), float(fields[2]), float(fields[3]), float(fields[4]))
                    elif fields[0].lower() == "offset" and len(fields) > 2:
                        backdrop_options.offset = (float(fields[1]), float(fields[2]))
                    elif fields[0].lower() == "scaling" and len(fields) > 2:
                        backdrop_options.scaling = (float(fields[1]), float(fields[2]))
                    else:
                        backdrop_options.setattr_keep_type(ProjectBase.format_as_attribute_name(fields[0]), fields[1])
            except:
                print("BackdropOptions skipping input line: " + line)
        return backdrop_options


class GeneralReader(SectionReader):
    """SWMM General Options"""

    SECTION_NAME = "[OPTIONS]"

    old_flow_routing = {
        "UF": FlowRouting.STEADY,
        "KW": FlowRouting.KINWAVE,
        "DW": FlowRouting.DYNWAVE}
    """Mapping from old flow routing names to FlowRouting enumeration"""

    section_comments = (";; Dates", ";; Time Steps", ";; Dynamic Wave")

    @staticmethod
    def read(new_text):
        """Read this section from the text representation"""
        general = General()

        # Skip the comments we insert automatically
        for comment in General.section_comments:
            new_text = new_text.replace(comment + '\n', '')

        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(general, line)
            if line.strip():
                # Set fields from metadata if this section has metadata
                tried_set = False
                for set_here in (general, general.dates, general.time_steps, general.dynamic_wave):
                    (attr_name, attr_value) = SectionReader.get_attr_name_value(set_here, line)
                    if attr_name:
                        try:
                            tried_set = True

                            if attr_name == "flow_routing" and GeneralReader.old_flow_routing.has_key(attr_value.upper()):
                                # Translate from old flow routing name to new flow routing name
                                attr_value = GeneralReader.old_flow_routing[attr_value.upper()]

                            if attr_name == "normal_flow_limited" and attr_value.upper() == "NO":
                                # Translate from old value NO to new value SLOPE
                                attr_value = "SLOPE"

                            set_here.setattr_keep_type(attr_name, attr_value)
                        except Exception as e:
                            print("options.General.text could not set " + attr_name + '\n' + str(e))
                if not tried_set:
                    print("options.General.text skipped: " + line)
        return general


class MapOptionsReader(SectionReader):
    """SWMM Map Options"""

    SECTION_NAME = "[MAP]"

    @staticmethod
    def read(new_text):
        map_options = MapOptions()
        for line in new_text.splitlines():
            try:
                line = SectionReader.set_comment_check_section(map_options, line)
                fields = line.split()
                if len(fields) > 1:
                    if fields[0].lower() == "dimensions" and len(fields) > 4:
                        map_options.dimensions = (float(fields[1]), float(fields[2]), float(fields[3]), float(fields[4]))
                    else:
                        map_options.setattr_keep_type(ProjectBase.format_as_attribute_name(fields[0]), fields[1])
            except:
                print("BackdropOptions skipping input line: " + line)
        return map_options


class ReportReader(SectionReader):
    """Report Options"""

    SECTION_NAME = "[REPORT]"

    DEFAULT_COMMENT = ";;Reporting Options"

    @staticmethod
    def read(new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """

        report = Report()  # Reset all values to defaults

        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(report, line)
            (attr_name, attr_value) = ReportReader.get_attr_name_value(report, line)
            if attr_name:
                if attr_name in Report.LISTS:
                    attr_value = attr_value.split()
                    existing_value = getattr(report, attr_name, Report.EMPTY_LIST)
                    if existing_value != Report.EMPTY_LIST:  # include values already set on other lines
                        attr_value = existing_value + attr_value
                report.setattr_keep_type(attr_name, attr_value)
        return report

