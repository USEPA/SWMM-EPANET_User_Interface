# -*- coding: utf-8 -*-

#
#  __init__.py - SWMM output package
#
#  Date Created: August 9, 2018
#
#  Author:     Michael E. Tryby
#              US EPA - ORD/NRMRL
#

'''
A low level pythonic API for the swmm-output dll using SWIG.
'''


__author__ = "Michael Tryby"
__copyright__ = "None"
__credits__ = "Colleen Barr"
__license__ = "CC0 1.0 Universal"

__version__ = "0.4.0"
__date__ = "February 15, 2019"

__maintainer__ = "Michael Tryby"
__email__ = "tryby.michael@epa.gov"
__status  = "Development"


from enum import Enum
from aenum import extend_enum
from itertools import islice

from swmm.output import output as oapi


class Units(Enum):
    RAIN_INT   = 1
    SNOW_DEPTH = 2
    EVAP_RATE  = 3
    INFIL_RATE = 4
    FLOW_RATE  = 5
    ELEV       = 6
    PERCENT    = 7
    CONCEN     = 8
    HEAD       = 9
    VOLUME     = 10
    VELOCITY   = 11
    TEMP       = 12
    UNITLESS   = 13
    NONE       = 14


class OutputMetadata:
    '''
    Simple attribute name and unit lookup.
    '''
    _unit_labels_us_ = {
        Units.RAIN_INT:       "in/hr",
        Units.SNOW_DEPTH:     "in",
        Units.EVAP_RATE:      "in/day",
        Units.INFIL_RATE:     "in/hr",
        Units.ELEV:           "ft",
        Units.PERCENT:        "%",
        Units.HEAD:           "ft",
        Units.VOLUME:         "cu ft",
        Units.VELOCITY:       "ft/sec",
        Units.TEMP:           "deg F",
        Units.UNITLESS:       "unitless",
        Units.NONE:           "",

        oapi.FlowUnits.CFS:   "cu ft/sec",
        oapi.FlowUnits.GPM:   "gal/min",
        oapi.FlowUnits.MGD:   "M gal/day",

        oapi.ConcUnits.MG:    "mg/L",
        oapi.ConcUnits.UG:    "ug/L",
        oapi.ConcUnits.COUNT: "Count/L",
        oapi.ConcUnits.NONE:  ""
    }

    _unit_labels_si_ = {
        Units.RAIN_INT:       "mm/hr",
        Units.SNOW_DEPTH:     "mm",
        Units.EVAP_RATE:      "mm/day",
        Units.INFIL_RATE:     "mm/hr",
        Units.ELEV:           "m",
        Units.PERCENT:        "%",
        Units.HEAD:           "m",
        Units.VOLUME:         "cu m",
        Units.VELOCITY:       "m/sec",
        Units.TEMP:           "deg C",
        Units.UNITLESS:       "unitless",
        Units.NONE:           "",

        oapi.FlowUnits.CMS:   "cu m/sec",
        oapi.FlowUnits.LPS:   "L/sec",
        oapi.FlowUnits.MLD:   "M L/day",

        oapi.ConcUnits.MG:    "mg/L",
        oapi.ConcUnits.UG:    "ug/L",
        oapi.ConcUnits.COUNT: "Count/L",
        oapi.ConcUnits.NONE:  ""
    }


    def _build_pollut_metadata(self, output_handle):
        '''
        Builds metadata for pollutant attributes at runtime.
        '''
        # Get number of pollutants
        n = oapi.getprojectsize(output_handle)[oapi.ElementType.POLLUT]

        if n > 0:

            pollut_name = []
            pollut_units = []

            # Get pollutant names
            for i in range(0, n):
                pollut_name.append(oapi.getelementname(output_handle,
                                                       oapi.ElementType.POLLUT, i))
            # Get pollutant units
            for u in oapi.getunits(output_handle)[2:]:
                pollut_units.append(oapi.ConcUnits(u))

            # Create dictionary keys
            for i in range(1, n):
                symbolic_name = 'POLLUT_CONC_' + str(i)
                extend_enum(oapi.SubcatchAttribute, symbolic_name, 8 + i)
                extend_enum(oapi.NodeAttribute, symbolic_name, 6 + i)
                extend_enum(oapi.LinkAttribute, symbolic_name, 5 + i)

            # Update metadata dictionary with pollutant metadata
            for i, attr in enumerate(islice(oapi.SubcatchAttribute, 8, None)):
                self._metadata[attr] = (pollut_name[i], self._unit_labels[pollut_units[i]])

            for i, attr in enumerate(islice(oapi.NodeAttribute, 6, None)):
                self._metadata[attr] = (pollut_name[i], self._unit_labels[pollut_units[i]])

            for i, attr in enumerate(islice(oapi.LinkAttribute, 5, None)):
                self._metadata[attr] = (pollut_name[i], self._unit_labels[pollut_units[i]])


    def __init__(self, output_handle):
        # Get units from binary output file
        self.units = oapi.getunits(output_handle)

        # Determine prevailing unit system
        self._unit_system = oapi.UnitSystem(self.units[0])
        if self._unit_system == oapi.UnitSystem.US:
            self._unit_labels = type(self)._unit_labels_us_
        else:
            self._unit_labels = type(self)._unit_labels_si_

        # Set user flow units
        self._flow = oapi.FlowUnits(self.units[1])

        self._metadata = {
            oapi.SubcatchAttribute.RAINFALL:           ("Rainfall",                self._unit_labels[Units.RAIN_INT]),
            oapi.SubcatchAttribute.SNOW_DEPTH:         ("Snow Depth",              self._unit_labels[Units.SNOW_DEPTH]),
            oapi.SubcatchAttribute.EVAP_LOSS:          ("Evaporation Loss",        self._unit_labels[Units.EVAP_RATE]),
            oapi.SubcatchAttribute.INFIL_LOSS:         ("Infiltration Loss",       self._unit_labels[Units.INFIL_RATE]),
            oapi.SubcatchAttribute.RUNOFF_RATE:        ("Runoff Rate",             self._unit_labels[self._flow]),
            oapi.SubcatchAttribute.GW_OUTFLOW_RATE:    ("Groundwater Flow Rate",   self._unit_labels[self._flow]),
            oapi.SubcatchAttribute.GW_TABLE_ELEV:      ("Groundwater Elevation",   self._unit_labels[Units.ELEV]),
            oapi.SubcatchAttribute.SOIL_MOISTURE:      ("Soil Moisture",           self._unit_labels[Units.PERCENT]),
            oapi.SubcatchAttribute.POLLUT_CONC_0:      ("Pollutant Concentration", self._unit_labels[Units.NONE]),

            oapi.NodeAttribute.INVERT_DEPTH:           ("Invert Depth",            self._unit_labels[Units.ELEV]),
            oapi.NodeAttribute.HYDRAULIC_HEAD:         ("Hydraulic Head",          self._unit_labels[Units.HEAD]),
            oapi.NodeAttribute.PONDED_VOLUME:          ("Ponded Volume",           self._unit_labels[Units.VOLUME]),
            oapi.NodeAttribute.LATERAL_INFLOW:         ("Lateral Inflow",          self._unit_labels[self._flow]),
            oapi.NodeAttribute.TOTAL_INFLOW:           ("Total Inflow",            self._unit_labels[self._flow]),
            oapi.NodeAttribute.FLOODING_LOSSES:        ("Flooding Loss",           self._unit_labels[self._flow]),
            oapi.NodeAttribute.POLLUT_CONC_0:          ("Pollutant Concentration", self._unit_labels[Units.NONE]),

            oapi.LinkAttribute.FLOW_RATE:              ("Flow Rate",               self._unit_labels[self._flow]),
            oapi.LinkAttribute.FLOW_DEPTH:             ("Flow Depth",              self._unit_labels[Units.ELEV]),
            oapi.LinkAttribute.FLOW_VELOCITY:          ("Flow Velocity",           self._unit_labels[Units.VELOCITY]),
            oapi.LinkAttribute.FLOW_VOLUME:            ("Flow Volume",             self._unit_labels[Units.VOLUME]),
            oapi.LinkAttribute.CAPACITY:               ("Capacity",                self._unit_labels[Units.PERCENT]),
            oapi.LinkAttribute.POLLUT_CONC_0:          ("Pollutant Concentration", self._unit_labels[Units.NONE]),

            oapi.SystemAttribute.AIR_TEMP:             ("Temperature",             self._unit_labels[Units.TEMP]),
            oapi.SystemAttribute.RAINFALL:             ("Rainfall",                self._unit_labels[Units.RAIN_INT]),
            oapi.SystemAttribute.SNOW_DEPTH:           ("Snow Depth",              self._unit_labels[Units.SNOW_DEPTH]),
            oapi.SystemAttribute.EVAP_INFIL_LOSS:      ("Evap and Infil Losses",   self._unit_labels[Units.INFIL_RATE]),
            oapi.SystemAttribute.RUNOFF_FLOW:          ("Runoff Flow Rate",        self._unit_labels[self._flow]),
            oapi.SystemAttribute.DRY_WEATHER_INFLOW:   ("Dry Weather Inflow",      self._unit_labels[self._flow]),
            oapi.SystemAttribute.GW_INFLOW:            ("Groundwater Inflow",      self._unit_labels[self._flow]),
            oapi.SystemAttribute.RDII_INFLOW:          ("RDII Inflow",             self._unit_labels[self._flow]),
            oapi.SystemAttribute.DIRECT_INFLOW:        ("Direct Inflow",           self._unit_labels[self._flow]),
            oapi.SystemAttribute.TOTAL_LATERAL_INFLOW: ("Total Lateral Inflow",    self._unit_labels[self._flow]),
            oapi.SystemAttribute.FLOOD_LOSSES:         ("Flood Losses",            self._unit_labels[self._flow]),
            oapi.SystemAttribute.OUTFALL_FLOWS:        ("Outfall Flow",            self._unit_labels[self._flow]),
            oapi.SystemAttribute.VOLUME_STORED:        ("Volume Stored",           self._unit_labels[Units.VOLUME]),
            oapi.SystemAttribute.EVAP_RATE:            ("Evaporation Rate",        self._unit_labels[Units.EVAP_RATE])
        }

        self._build_pollut_metadata(output_handle)


    def get_attribute_metadata(self, attribute):
        '''
        Takes an attribute enum and returns the name and units in a tuple.
        '''
        return self._metadata[attribute]


# Units of Measurement
#
# Units                  US Customary                           SI Metric
#    AREA_SUBCATCH          acres                 ac               hectares            ha
#    AREA_STOR              square feet           sq ft            square meters       sq m
#    AREA_POND              square feet           sq ft            square meters       sq m
#    CAP_SUC                inches                in               millimeters         mm
#    CONC                   milligrams/liter      mg/L             milligrams/liter    mg/L
#                           micrograms/liter      ug/L             micrograms/liter    ug/L
#                           counts/liter          Count/L          counts/liter        Count/L
#    INFIL_DECAY            1/hours               1/hrs            1/hours             1/hrs
#    POLLUT_DECAY           1/days                1/days           1/days              1/days
#    DEPRES_STOR            inches                in               millimeters         mm
#    DEPTH                  feet                  ft               meters              m
#    DIAM                   feet                  ft               meters              m
#    DISC_COEFF_ORIF        dimensionless         dimless          dimensionless       dimless
#    DISC_COEFF_WEIR        CFS/foot^n            CFS/ft^n         CMS/meter^n         CMS/m^n
#    ELEV                   feet                  ft               meters              m
#    EVAP_RATE              inches/day            in/day           millimeters/day     mm/day
#    FLOW_RATE              cubic feet/sec        CFS              cubic meter/sec     CMS
#                           gallons/minute        GPM              liter/sec           LPS
#                           million gallons/day   MGD              million liter/day   MLD
#    HEAD                   feet                  ft               meters              m
#    HYD_CONDUCT            inches/hour           in/hr            millimeters/hour    mm/hr
#    INFIL_RATE             inches/hour           in/hr            millimeters/hour    mm/hr
#    LEN                    feet                  ft               meters              m
#    MANN_N                 seconds/meter^1/3     sec/m^1/3        seconds/meter^1/3   sec/m^1/3
#    POLLUT_BUILDUP         mass/length           mass/len         mass/length         mass/len
#                           mass/acre             mass/ac          mass/hectare        mass/ha
#    RAIN_INTENSITY         inches/hour           in/hr            millimeters/hour    mm/hr
#    RAIN_VOLUME            inches                in               millimeters         mm
#    SLOPE_SUBCATCH         percent               percent          percent             percent
#    SLOPE_XSEC             rise/run              rise/run         rise/run            rise/run
#    STREET_CLEAN_INT       days                  days             days                days
#    VOLUME                 cubic feet            cu ft            cubic meters        cu m
#    WIDTH                  feet                  ft               meters              m
