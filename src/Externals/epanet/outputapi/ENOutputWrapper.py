"""

Wrapper for EPANET Output API.

Author: Bryant E. McDonnell
Date: 12/7/2015
Language: Anglais

Edited for inclusion in SWMM-EPANET User Interface project
April-May 2016
Mark Gray, RESPEC
for US EPA

"""

from ctypes import *

import Externals.epanet.outputapi.outputapi as _lib

# ENR_NodeAttribute
from Externals.epanet.outputapi.outputapi import ENR_demand, ENR_head, ENR_pressure, ENR_quality
# ENR_LinkAttribute
from Externals.epanet.outputapi.outputapi import ENR_flow,ENR_velocity,ENR_headloss,ENR_avgQuality
from Externals.epanet.outputapi.outputapi import ENR_status,ENR_setting,ENR_rxRate,ENR_frctnFctr

# ctypes utility variables created once to avoid overhead of creating every time they are needed
_label  = _lib.String((_lib.MAXID + 1) * '\0')
_errmsg = _lib.String((_lib.MAXMSG + 1) * '\0')
_cint = c_int()


class ENR_item:
    """ This class is not used directly, it is as a base class with shared code for ENR_node_type and ENR_link_type.
        self.id store the ID/name of the item which could be text or numeric.
        self.index store the index of this item used when accessing the binary file.
        Code outside this module should not need to access self.index. """
    TypeLabel = "Base"

    def __init__(self, item_id, index):
        self.id = item_id
        self.index = index

    def __str__(self):
        return self.id

    @classmethod
    def get_list(cls, output):
        """ Read the list of all items of this class from the output file.
            Args
            output (OutputObject): object that has already opened the desired output file.
            Returns (list): Python list of all objects of this type.
        """
        items = []
        _lib.ENR_getNetSize(output.ptrapi, cls._count_flag, byref(_cint))
        item_count = _cint.value
        for index in range(0, item_count - 1):
            cls._get_id(output.ptrapi, index, _label)
            items.append(cls(str(_label), index))
        return items

    def get_value(self, output, attribute, time_index):
        """ Purpose: Get a single result for particular item, time, and attribute.
            Args
            output: OutputObject that already has the desired output file open.
            attribute: attribute to get values of - must be an ENR_attribute from self.Attributes.
            time_index: time index to retrieve, 0 is the first time index.
        """
        ctypes_return = c_float()
        return_code = self._get_value(output.ptrapi, time_index, self.index, attribute.index, byref(ctypes_return))
        if return_code == 0:
            return ctypes_return.value
        else:
            print "Error in get_value({}, {}, {})".format(str(self.id), str(time_index), str(attribute.name))
            output.RaiseError(return_code)

    def get_value_formatted(self, output, attribute, time_index):
        val = self.get_value(output, attribute, time_index)
        if attribute == ENR_link_type.AttributeStatus and val in [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]:
            return ('Closed', 'Closed', 'Closed', 'Open', 'Active', 'Open', 'Open', 'Open')[int(val)]
        else:
            return '{:7.2f}'.format(val)

    def get_series(self, output, attribute, start_index=0, num_values=-1):
        """
            Purpose: Get time series results for the requested attribute.
            Args
            output: OutputObject that already has the desired output file open.
            attribute: attribute to get values of - must be an ENR_attribute from self.Attributes.
            start_index: first time index to retrieve, default = 0 for first time index.
            num_values: number of values to retrieve, or -1 to get all values starting at start_index.
        """
        if num_values == -1:
            num_values = output.numPeriods - start_index
        if start_index < 0 or start_index >= output.numPeriods:
            raise Exception("Start Time Index " + str(start_index) + \
                            " Outside Number of TimeSteps " + str(output.numPeriods))
        if num_values < 1 or start_index + num_values > output.numPeriods:
            raise Exception("Series Length " + str(num_values) + \
                            " Outside Number of TimeSteps " + str(output.numPeriods))
        returned_length = c_int()
        error_new = c_int()
        ask_for_length = num_values
        if output.newOutValueSeriesLengthIsEnd:
            ask_for_length += start_index + 1
        SeriesPtr = _lib.ENR_newOutValueSeries(output.ptrapi, start_index,
                                               ask_for_length, byref(returned_length), byref(error_new))
        if error_new.value != 0:
            print "Error " + str(error_new.value)\
                  + " allocating series start=" + str(start_index) + ", len=" + str(num_values)
            output.RaiseError(error_new.value)

        if self.index >= 0:
            error_get = self._get_series(output.ptrapi,
                                      self.index,
                                      attribute.index,
                                      start_index,
                                      returned_length.value,
                                      SeriesPtr)
        else:
            error_get = self._get_series(output.ptrapi,
                                      attribute.index,
                                      start_index,
                                      returned_length.value,
                                      SeriesPtr)

        if error_get != 0:
            print "Error reading series " + self.TypeLabel + " " + str(self.id) + ', att #' + str(attribute.index)
            output.RaiseError(error_get)

        build_array = [SeriesPtr[i] for i in range(returned_length.value)]
        _lib.ENR_free(SeriesPtr)
        return build_array

    @classmethod
    def get_attribute_for_all_at_time(cls, output, attribute, time_index):
        """ Purpose: For all items of this type (nodes or links) at given time, get a particular attribute.
            Args
            output: OutputObject that already has the desired output file open.
            attribute: attribute to get values of - must be an ENR_attribute from self.Attributes.
            time_index: time index to retrieve, 0 is the first time index.
        """
        returned_length = c_int()
        error_new = c_int()
        ValArrayPtr = _lib.ENR_newOutValueArray(output.ptrapi, _lib.ENR_getAttribute,
                                                cls._elementType, byref(returned_length), byref(error_new))
        if error_new.value != 0:
            print "Error " + str(error_new.value) + " calling ENR_newOutValueArray for " + cls.TypeLabel
            output.RaiseError(error_new.value)

        # ENR_getLinkAttribute.argtypes = [POINTER(ENResultsAPI), c_int, ENR_LinkAttribute, POINTER(c_float)]

        error_get = cls._get_attribute(output.ptrapi, time_index, attribute.index, ValArrayPtr)
        if error_get != 0:
            print "Error reading all attributes for " + cls.TypeLabel + " at " + str(time_index) + ', att ' + str(attribute.name)
            output.RaiseError(error_get)

        BldArray = [ValArrayPtr[i] for i in range(returned_length.value)]
        _lib.ENR_free(ValArrayPtr)
        return BldArray

    @classmethod
    def get_attribute_by_name(cls, attribute_name):
        """ Get an ENR_attribute from the list Attributes of this class, given the attribute name.
            Args:
            attribute_name: name of attribute, must match the name of an attribute in the Attributes of this class.
            Returns
            ENR_attribute object whose name == attribute_name, or None if no attribute's name matches exactly.
        """
        for attribute in cls.Attributes:
            if attribute.name == attribute_name:
                return attribute
        return None


class ENR_attribute():
    def __init__(self, index, name, units):
        self.index = index
        self.name = name
        self._units = units

    def units(self, unit_system):
        return self._units[unit_system]


class ENR_node_type(ENR_item):
    TypeLabel = "Node"

    AttributeDemand   = ENR_attribute(ENR_demand,   "Demand",   ('CFS', 'LPS'))
    AttributeHead     = ENR_attribute(ENR_head,     "Head",     ('ft', 'm'))
    AttributePressure = ENR_attribute(ENR_pressure, "Pressure", ('psi', 'm'))
    AttributeQuality  = ENR_attribute(ENR_quality,  "Quality",  ('mg/L', 'mg/L'))

    Attributes = (AttributeDemand, AttributeHead, AttributePressure, AttributeQuality)

    _count_flag = _lib.ENR_nodeCount
    _get_id = _lib.ENR_getNodeID
    _get_value = _lib.ENR_getNodeValue
    _get_series = _lib.ENR_getNodeSeries
    _get_attribute = _lib.ENR_getNodeAttribute
    _get_result = _lib.ENR_getNodeResult
    _elementType = _lib.ENR_node


class ENR_link_type(ENR_item):
    TypeLabel = "Link"

    AttributeFlow           = ENR_attribute(ENR_flow,       'Flow',            ('CFS', 'LPS'))
    AttributeVelocity       = ENR_attribute(ENR_velocity,   'Velocity',        ('fps', 'm/s'))
    AttributeHeadloss       = ENR_attribute(ENR_headloss,   'Unit Headloss',   ('ft/Kft', 'm/km'))
    AttributeQuality        = ENR_attribute(ENR_avgQuality, 'Quality',         ('mg/L', 'mg/L'))
    AttributeStatus         = ENR_attribute(ENR_status,     'Status',          ('', ''))
    AttributeSetting        = ENR_attribute(ENR_setting,    'Setting',         ('', ''))
    AttributeReactionRate   = ENR_attribute(ENR_rxRate,     'Reaction Rate',   ('mg/L/d', 'mg/L/d'))
    AttributeFrictionFactor = ENR_attribute(ENR_frctnFctr,  'Friction Factor', ('', ''))

    Attributes = (AttributeFlow, AttributeVelocity, AttributeHeadloss, AttributeQuality,
                  AttributeStatus, AttributeSetting, AttributeReactionRate, AttributeFrictionFactor)

    _count_flag = _lib.ENR_linkCount
    _get_id = _lib.ENR_getLinkID
    _get_value = _lib.ENR_getLinkValue
    _get_series = _lib.ENR_getLinkSeries
    _get_attribute = _lib.ENR_getLinkAttribute
    _get_result = _lib.ENR_getLinkResult
    _elementType = _lib.ENR_link


ENR_USFlowUnits = ('CFS', 'GPM', 'MGD', 'IMGD', 'AFD')
ENR_SIFlowUnits = ('LPS', 'LPM', 'MLD', 'CMH', 'CMD')

ENR_UnitsUS = 0
ENR_UnitsSI = 1
#---------------------------------------------------------------------------------------------


class OutputObject(object):

    def __init__(self, output_file_name):
        """ Open the named file and maintain an internal pointer to be used to access contents of the file.
            Read header information from the file including units, times, and lists of nodes and links.
            Args
            output_file_name (str): full path and file name of EPANET binary output file to open
        """
        self.ptrapi = c_void_p()
        self.output_file_name = str(output_file_name)
        ret = _lib.ENR_open(byref(self.ptrapi), self.output_file_name)
        if ret != 0:
            self.RaiseError(ret)
        self.measure_newOutValueSeries()
        self._get_Units()
        self._get_NetSize()
        self._get_Times()
        self.nodes = ENR_node_type.get_list(self)
        self.links = ENR_link_type.get_list(self)

    def RaiseError(self, ErrNo):
        # if _RetErrMessage(ErrNo , errmsg, err_max_char)==0:
        #     raise Exception(errmsg.value)
        # else:
        raise Exception("EPANET output error #{0}".format(ErrNo) )

    def measure_newOutValueSeries(self):
        """Test SMO_newOutValueSeries to see whether it treats the requested length as length or end.
            Sets self.newOutValueSeriesLengthIsEnd flag so we can adjust how we call this method."""
        sLength = c_int()
        ErrNo1 = c_int()
        SeriesPtr = _lib.ENR_newOutValueSeries(self.ptrapi, 1, 2, byref(sLength), byref(ErrNo1))
        self.newOutValueSeriesLengthIsEnd = (sLength.value == 1)
        _lib.ENR_free(SeriesPtr)

    def _get_Units(self):
        """
        Purpose: Read pressure and flow units into self.unit_system, self.flowUnitsLabel, self.pressUnits
        """
        _lib.ENR_getUnits(self.ptrapi, _lib.ENR_flowUnits, byref(_cint))
        self.flowUnits = _cint.value
        if self.flowUnits < len(ENR_USFlowUnits):
            self.unit_system = ENR_UnitsUS
            self.flowUnitsLabel = ENR_USFlowUnits[self.flowUnits]
        else:
            self.unit_system = ENR_UnitsSI
            self.flowUnitsLabel = ENR_SIFlowUnits[self.flowUnits - len(ENR_USFlowUnits)]

        _lib.ENR_getUnits(self.ptrapi, _lib.ENR_pressUnits, byref(_cint))
        self.pressUnits = _cint.value
        
    def _get_NetSize(self):
        """
        Populates object attributes with the water object counts
        """
        _lib.ENR_getNetSize(self.ptrapi, _lib.ENR_tankCount, byref(_cint))
        self.tankCount = _cint.value

        _lib.ENR_getNetSize(self.ptrapi, _lib.ENR_pumpCount, byref(_cint))
        self.pumpCount = _cint.value

        _lib.ENR_getNetSize(self.ptrapi, _lib.ENR_valveCount, byref(_cint))
        self.valveCount = _cint.value

    def _get_Times(self):
        """
        Purpose: Read report and simulation time related parameters.
        Populate self attributes: reportStart, reportStep, simDuration, numPeriods
        """
        
        _lib.ENR_getTimes(self.ptrapi, _lib.ENR_reportStart, byref(_cint))
        self.reportStart = _cint.value

        _lib.ENR_getTimes(self.ptrapi, _lib.ENR_reportStep, byref(_cint))
        self.reportStep = _cint.value
        
        _lib.ENR_getTimes(self.ptrapi, _lib.ENR_simDuration, byref(_cint))
        self.simDuration = _cint.value

        _lib.ENR_getTimes(self.ptrapi, _lib.ENR_numPeriods, byref(_cint))
        self.numPeriods = _cint.value

    def get_itemById(self, item_list, item_id):
        """Retrieve the item from item_list with the specified ID.
        Arguments:
        item_id: ID label of item to find"""
        for item in item_list:
            if item.id == item_id:
                return item
        else:
            return None

    # def get_indexById(self, item_list, item_id):
    #     """Retrieve the item from item_list with the specified ID.
    #     Arguments:
    #     item_id: ID label of item to find"""
    #     item = self.get_itemById(item_list, item_id)
    #     if item:
    #         return item.index
    #     else:
    #         return -1

    # def get_NodeResult(self, NodeInd, TimeInd):
    #     """
    #     Purpose: For a node at given time, get all attributes
    #     """
    #     alength = c_int()
    #     ErrNo1 = c_int()
    #     ValArrayPtr = _lib.ENR_newOutValueArray(self.ptrapi,
    #                                             _lib.ENR_getResult,
    #                                             _lib.ENR_node,
    #                                             byref(alength),
    #                                             byref(ErrNo1))
    #     ErrNo2 = _lib.ENR_getNodeResult(self.ptrapi, TimeInd, NodeInd, ValArrayPtr)
    #     BldArray = [ValArrayPtr[i] for i in range(alength.value)]
    #     _lib.ENR_free(ValArrayPtr)
    #     return BldArray
    #
    # def get_LinkResult(self, LinkInd, TimeInd):
    #     """
    #     Purpose: For a link at given time, get all attributes
    #     """
    #     alength = c_int()
    #     ErrNo1 = c_int()
    #     ValArrayPtr = _lib.ENR_newOutValueArray(self.ptrapi,
    #                                             _lib.ENR_getResult,
    #                                             _lib.ENR_link,
    #                                             byref(alength),
    #                                             byref(ErrNo1))
    #     ErrNo2 = _lib.ENR_getLinkResult(self.ptrapi, TimeInd, LinkInd, ValArrayPtr)
    #     BldArray = [ValArrayPtr[i] for i in range(alength.value)]
    #     _lib.ENR_free(ValArrayPtr)
    #     return BldArray

    def CloseOutputFile(self):
        """
        Call to close binary file.
        """
        ret = _lib.ENR_close(byref(self.ptrapi) )
        if ret != 0:
            raise Exception('Failed to Close file ' + self.output_file_name)

    def elapsed_hours_at_index(self, report_time_index):
        return (report_time_index * self.reportStep) / 3600

    def get_time_string(self, report_time_index):
        total_hours = self.elapsed_hours_at_index(report_time_index)
        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)
        return '{:02d}:{:02d}'.format(hours, minutes)

    def get_date_string(self, report_time_index):
        # current date = self.StartDate plus elapsed hours
        total_hours = self.elapsed_hours_at_index(report_time_index)
        report_date = self.StartDate + datetime.timedelta(hours=total_hours)
        return report_date.strftime("%Y-%m-%d %H:%M")
