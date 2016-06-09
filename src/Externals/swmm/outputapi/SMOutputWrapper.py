"""

Wrapper for SWMM Output API.

Written for SWMM-EPANET User Interface project
2016
Mark Gray, RESPEC
for US EPA

Inspired by ENOutputWrapper by Bryant E. McDonnell 12/7/2015

"""

from ctypes import *
import time, datetime
import Externals.swmm.outputapi.outputapi as _lib

# Subcatchment Attributes
from outputapi import rainfall_subcatch, snow_depth_subcatch, evap_loss, infil_loss,\
                      runoff_rate, gwoutflow_rate, gwtable_elev, soil_moisture, pollutant_conc_subcatch

# Node Attributes
from outputapi import invert_depth,\
                      hydraulic_head,\
                      stored_ponded_volume,\
                      lateral_inflow,\
                      total_inflow,\
                      flooding_losses,\
                      pollutant_conc_node\

# Link Attributes
from outputapi import flow_rate_link, flow_depth, flow_velocity, flow_volume, capacity, pollutant_conc_link

# System Attributes
from outputapi import air_temp,\
                      rainfall_system,\
                      snow_depth_system,\
                      evap_infil_loss,\
                      runoff_flow,\
                      dry_weather_inflow,\
                      groundwater_inflow,\
                      RDII_inflow,\
                      direct_inflow,\
                      total_lateral_inflow,\
                      flood_losses,\
                      outfall_flows,\
                      volume_stored,\
                      evap_rate


class SMO_categoryBase:
    """ This class is not used directly, it serves as a base class for
        SMO_subcatchment, SMO_node, SMO_link, and SMO_system.
        All but SMO_system use self.id to store an item id and self.index to store the index in the binary file"""
    TypeLabel = "Base"
    def __init__(self, id, index):
        self.id = id
        self.index = index

    def __str__(self):
        return self.id


class SMO_subcatchment(SMO_categoryBase):
    TypeLabel = "Subcatchment"
    Attributes = (rainfall_subcatch, snow_depth_subcatch, evap_loss, infil_loss,
                  runoff_rate, gwoutflow_rate, gwtable_elev, soil_moisture, pollutant_conc_subcatch)

    AttributeNames = ("Precipitation", "Snow Depth", "Evaporation", "Infiltration",
                      "Runoff", "Groundwater Flow", "Groundwater Elevation", "Soil Moisture", "Concentration")

    AttributeUnits = (('in/hr', 'mm/hr'),  # Precipitation
                      ('in', 'mm'),  # Snow Depth
                      ('in/day', 'mm/day'),  # Evaporation
                      ('in/hr', 'mm/hr'),  # Infiltration
                      ('CFS', 'CMS'),  # Runoff
                      ('CFS', 'CMS'),  # GW Flow
                      ('ft', 'm'),  # GW Elev
                      ('', ''),  # Soil Moisture
                      ('mg/L', 'mg/L'))  # Washoff

    get_ids = _lib.SMO_getSubcatchIDs
    get_series = _lib.SMO_getSubcatchSeries
    get_attribute = _lib.SMO_getSubcatchAttribute
    get_result = _lib.SMO_getSubcatchResult
    elementType = 0  # typedef enum {subcatch, node, link, sys} SMO_elementType


class SMO_node(SMO_categoryBase):
    TypeLabel = "Node"
    Attributes = (invert_depth,
                  hydraulic_head,
                  stored_ponded_volume,
                  lateral_inflow,
                  total_inflow,
                  flooding_losses,
                  pollutant_conc_node)

    AttributeNames = ("Depth",
                      "Head",
                      "Volume",
                      "Lateral Inflow",
                      "Total Inflow",
                      "Flooding",
                      "TSS")

    AttributeUnits = (('ft', 'm'),  # Depth
                          ('ft', 'm'),  # Head
                          ('ft3', 'm3'),  # Volume
                          ('CFS', 'CMS'),  # Lateral Inflow
                          ('CFS', 'CMS'),  # Total Inflow
                          ('CFS', 'CMS'),  # Overflow
                          ('mg/L', 'mg/L'))  # Quality

    get_ids = _lib.SMO_getNodeIDs
    get_series = _lib.SMO_getNodeSeries
    get_attribute = _lib.SMO_getNodeAttribute
    get_result = _lib.SMO_getNodeResult
    elementType = 1  # typedef enum {subcatch, node, link, sys} SMO_elementType


class SMO_link(SMO_categoryBase):
    TypeLabel = "Link"
    Attributes = (flow_rate_link, flow_depth, flow_velocity, flow_volume, capacity, pollutant_conc_link)
    AttributeNames = ("Flow", "Depth", "Velocity", "Volume", "Capacity", "Concentration")
    AttributeUnits = (('CFS', 'CMS'),    # Flow
                      ('ft', 'm'),       # Depth
                      ('fps', 'm/s'),    # Velocity
                      ('ft3', 'm3'),     # Volume.
                      ('', ''),          # Fraction Full
                      ('mg/L', 'mg/L'))  # Quality

    get_ids = _lib.SMO_getLinkIDs
    get_series = _lib.SMO_getLinkSeries
    get_attribute = _lib.SMO_getLinkAttribute
    get_result = _lib.SMO_getLinkResult
    elementType = 2  # typedef enum {subcatch, node, link, sys} SMO_elementType


class SMO_system(SMO_categoryBase):
    TypeLabel = "System"
    Attributes = (air_temp,
                  rainfall_system,
                  snow_depth_system,
                  evap_infil_loss,
                  runoff_flow,
                  dry_weather_inflow,
                  groundwater_inflow,
                  RDII_inflow,
                  direct_inflow,
                  total_lateral_inflow,
                  flood_losses,
                  outfall_flows,
                  volume_stored,
                  evap_rate)

    AttributeNames = ("Temperature",
                      "Precipitation",
                      "Snow Depth",
                      "Infiltration",
                      "Runoff",
                      "Dry Weather Inflow",
                      "Groundwater Inflow",
                      "I&I Inflow",
                      "Direct Inflow",
                      "Total Inflow",
                      "Flooding",
                      "Outflow",
                      "Storage",
                      "Evaporation")

    AttributeUnits = (('deg F','deg C'),
                      ('in/hr', 'mm/hr'),    # Precipitation
                      ('in', 'mm'),          # Snow Depth
                      ('in/hr', 'mm/hr'),    # Infiltration
                      ('CFS', 'CMS'),  # Runoff
                      ('CFS', 'CMS'),  # Dry Weather Inflow
                      ('CFS', 'CMS'),  # Groundwater Inflow
                      ('CFS', 'CMS'),  # RDII Inflow
                      ('CFS', 'CMS'),  # Direct Inflow
                      ('CFS', 'CMS'),  # Total Inflow
                      ('CFS', 'CMS'),  # Flooding
                      ('CFS', 'CMS'),  # Outflow
                      ('ft3', 'm3'),   # Volume
                      ('in/day', 'mm/day'))  # Evaporation

    get_series = _lib.SMO_getSystemSeries
    get_attribute = _lib.SMO_getSystemAttribute
    get_result = _lib.SMO_getSystemResult
    elementType = 3  # typedef enum {subcatch, node, link, sys} SMO_elementType

SMO_objectTypes = (SMO_subcatchment, SMO_node, SMO_link, SMO_system)
SMO_objectTypeLabels = [ot.TypeLabel for ot in SMO_objectTypes]


def SMO_getObjectType(object_type_name):
    for object_type in SMO_objectTypes:
        if object_type.TypeLabel == object_type_name:
            return object_type

SMO_USFlowUnits = ('CFS', 'GPM', 'MGD')
SMO_SIFlowUnits = ('CMS', 'LPS', 'MLD')
TempUnits = ('deg F','deg C')

SMO_UnitsUS = 0
SMO_UnitsSI = 1

cint = c_int()


# class OutputNode:
#
#     def __init__(self, output, node_id):
#         self.output = output
#         self.id = node_id
#
#     def get_series(self, attribute, start_index=0, num_values=-1):


class OutputObject(object):
    def __init__(self, output_file_name):
        """
        1) Initializes the opaque pointer to ptrapi struct.
        2) Opens the output file.
        """
        self.ptrapi = c_void_p()
        self._call_int_return = c_int()  # Private variable used only inside call_int
        self._call_double_return = c_double()  # Private variable used only inside call_double
        ret = _lib.SMR_open(str(output_file_name), byref(self.ptrapi))
        if ret != 0:
            self.RaiseError(ret)
        # TODO: recompile dll so we can use this new argument order:
        # self.call(_lib.SMR_open, str(output_file_name))
        self.measure_newOutValueSeries()
        self._get_units()
        self._get_sizes()
        self._get_times()
        self.subcatchments = self._read_linked_ids(SMO_subcatchment)
        self.nodes = self._read_linked_ids(SMO_node)
        self.links = self._read_linked_ids(SMO_link)
        self.system = [SMO_system('-1', -1)]
        self.all_items = (self.subcatchments, self.nodes, self.links, self.system)
        # self.subcatchment_ids = [item.id for item in self.subcatchments]
        # self.node_ids = [item.id for item in self.nodes]
        # self.link_ids = [item.id for item in self.links]
        # self.all_ids = (self.subcatchment_ids, self.node_ids, self.link_ids, [-1])

    def get_items(self, objectTypeLabel):
        """ Get the list of items of the type whose TypeLabel attribute is objectTypeLabel.

            Args:
            objectTypeLabel: can be "Subcatchment", "Node" or "Link". (System has no items.)

            Examples:
                for node get_items("Node"):
                    print node.id
        """
        for items in self.all_items:
            if items and items[0].TypeLabel == objectTypeLabel:
                return items
        return []

    def call(self, function, *args):
        """ Call any API method whose return value is an integer which indicates an error if != 0
            Handle the nonzero value by calling RaiseError."""
        try:
            ret = function(self.ptrapi, *args)
            if ret != 0:
                self.RaiseError(ret)
        except Exception as ex:
            print(str(ex))
            raise Exception("SWMM output error calling " + str(function) + ": " + str(ex))

    def call_int(self, function, *args):
        """ Call an API method whose return value is an integer indicating an error if != 0
            and which also returns an integer in the last argument (using byref).
            call_int handles the return value error flag by calling RaiseError if needed.
            Do not include the last argument (the return argument) in *args, it will be added internally.
            The integer value returned is the return value of call_int."""
        args_to_pass = list(args)
        args_to_pass.append(byref(self._call_int_return))  # When moving to Python 3.5+, can skip appending and use:
        self.call(function, *args_to_pass)                 # self.call(function, *args, byref(self._call_int_return))
        return self._call_int_return.value

    def call_double(self, function, *args):
        """ Call an API method whose return value is an integer indicating an error if != 0
            and which also returns a double in the last argument (using byref).
            call_double handles the return value error flag by calling RaiseError if needed.
            Do not include the last argument (the return argument) in *args, it will be added internally
            The double value returned is the return value of call_double."""
        args_to_pass = list(args)
        args_to_pass.append(byref(self._call_double_return))  # When moving to Python 3.5+, can skip appending and use:
        self.call(function, *args_to_pass)                   # self.call(function, *args, byref(self._call_int_return))
        return self._call_double_return.value

    def measure_newOutValueSeries(self):
        """Test SMO_newOutValueSeries to see whether it treats the requested length as length or end.
            Sets self.newOutValueSeriesLengthIsEnd flag so we can adjust how we call this method."""
        sLength = c_int()
        ErrNo1 = c_int()
        SeriesPtr = _lib.SMO_newOutValueSeries(self.ptrapi, 1, 2, byref(sLength), byref(ErrNo1))
        _lib.SMO_free(SeriesPtr)
        self.newOutValueSeriesLengthIsEnd = (sLength.value == 1)

    def RaiseError(self, ErrNo):
        # if _RetErrMessage(ErrNo , errmsg, err_max_char)==0:
        #     raise Exception(errmsg.value)
        # else:
        raise Exception("SWMM output error #{0}".format(ErrNo))

    def _get_units(self):
        """
        Purpose: Reads flow unit index into self.flowUnits, sets self.unit_system and self.flowUnitsLabel
        """
        self.flowUnits = self.call_int(_lib.SMO_getUnits, _lib.flow_rate)
        if self.flowUnits < len(SMO_USFlowUnits):
            self.unit_system = SMO_UnitsUS
            self.flowUnitsLabel = SMO_USFlowUnits[self.flowUnits]
        else:
            self.unit_system = SMO_UnitsSI
            self.flowUnitsLabel = SMO_SIFlowUnits[self.flowUnits - len(SMO_USFlowUnits)]

        # _lib.SMO_getUnits(self.ptrapi, _lib.concentration, byref(cint))
        # self.concentrationUnits = cint.value

    def _get_sizes(self):
        """
        Populates object attributes with the water object counts
        """
        self.nodeCount = self.call_int(_lib.SMO_getProjectSize, _lib.nodeCount)
        self.subcatchCount = self.call_int(_lib.SMO_getProjectSize, _lib.subcatchCount)
        self.linkCount = self.call_int(_lib.SMO_getProjectSize, _lib.linkCount)
        self.pollutantCount = self.call_int(_lib.SMO_getProjectSize, _lib.pollutantCount)

    def _get_times(self):
        """
        Purpose: Retrieve report and simulation time-related parameters and stores them in self.
        """
        RawReportStart = self.call_double(_lib.SMO_getStartTime)  # decimal (Julian) days since 12 AM on 12/30/1899
        self.StartDate = datetime.datetime(1899, 12, 30) + datetime.timedelta(RawReportStart)
        self.reportStep = self.call_int(_lib.SMO_getTimes, _lib.reportStep)
        self.numPeriods = self.call_int(_lib.SMO_getTimes, _lib.numPeriods)
        self.simDuration = self.reportStep * self.numPeriods

        # _lib.SMO_getTimes(self.ptrapi, _lib.SMO_simDuration, byref(cint))
        # self.simDuration = cint.value

    def _read_linked_ids(self, objectType):
        """ Read a linked list of struct IDentry (char* IDname, IDentry* nextID).
            category._get_ids must be SMO_getNodeIDs SMO_getLinkIDs, or SMO_getSubcatchIDs.
            Returns a Python list of objects of type category, one for each IDs."""
        items = []
        index = 0
        id_head = objectType.get_ids(self.ptrapi, byref(cint))
        next_id = id_head
        if cint.value != 0:
            print "Error reading IDs for " + objectType.TypeLabel
            self.RaiseError(cint.value)
        while next_id:
            items.append(objectType(str(next_id.contents.IDname.data), index))
            print "Read # " + str(index) + " ID = " + items[-1].id
            next_id = next_id.contents.nextID
            index += 1
        _lib.SMO_freeIDList(id_head)
        return items

    def get_itemById(self, item_list, item_id):
        """Retrieve the item from item_list with the specified ID.
        Arguments:
        item_id: ID label of item to find"""
        for item in item_list:
            if item.id == item_id:
                return item
        else:
            return None

    def get_indexById(self, item_list, item_id):
        """Retrieve the item from item_list with the specified ID.
        Arguments:
        item_id: ID label of item to find"""
        item = self.get_itemById(item_list, item_id)
        if item:
            return item.index
        else:
            return -1

    # def get_NodeValue(self, NodeInd, TimeInd, NodeAttr):
    #     """
    #     Purpose: Get results for particular node, time, attribute.
    #     """
    #     xval = c_float()
    #     err = _lib.getNodeValue(self.ptrapi, TimeInd, NodeInd, NodeAttr, byref(xval))
    #     if err == 0:
    #         return xval.value
    #     else:
    #         print "Error in get_NodeValue({}, {}, {})".format(str(NodeInd), str(TimeInd), str(NodeAttr))
    #         self.RaiseError(err)
    #
    # def get_LinkValue(self, NodeInd, TimeInd, NodeAttr):
    #     """
    #     Purpose: Get results for particular link, time, attribute.
    #     """
    #     xval = c_float()
    #     err = _lib.getLinkValue(self.ptrapi, TimeInd, NodeInd, NodeAttr, byref(xval))
    #     if err == 0:
    #         return xval.value
    #     else:
    #         self.RaiseError(err)

    def _get_series(self, function, item_index, attribute_index, start_index=0, num_values=-1):
        """
        Purpose: Get time series results for the requested attribute.
        Specify series start index and num_values or accept defaults to get all values.
        item_index = -1 for item type that does not have an index (System)
        num_values = -1 Default input: Gets data from start_index to end

        """
        if num_values == -1:
            num_values = self.numPeriods - start_index
        if start_index < 0 or start_index >= self.numPeriods:
            raise Exception("Start Time Index " + str(start_index) +\
                            " Outside Number of TimeSteps " + str(self.numPeriods))
        if num_values < 1 or start_index + num_values > self.numPeriods:
            raise Exception("Series Length " + str(num_values) +\
                            " Outside Number of TimeSteps " + str(self.numPeriods))
        sLength = c_int()
        ErrNo1 = c_int()
        ask_for_length = num_values
        if self.newOutValueSeriesLengthIsEnd:
            ask_for_length += start_index + 1
        SeriesPtr = _lib.SMO_newOutValueSeries(self.ptrapi, start_index,
                                               ask_for_length, byref(sLength), byref(ErrNo1))
        if ErrNo1.value != 0:
            print "Error " + str(ErrNo1.value) + " allocating series start=" + str(start_index) + ", len=" + str(num_values)
            self.RaiseError(ErrNo1.value)

        if item_index >= 0:
            ErrNo2 = function(self.ptrapi,
                              item_index,
                              attribute_index,
                              start_index,
                              sLength.value,
                              SeriesPtr)
        else:
            ErrNo2 = function(self.ptrapi,
                              attribute_index,
                              start_index,
                              sLength.value,
                              SeriesPtr)

        if ErrNo2 != 0:
            print "Error reading series " + str(function) + ', ' + str(item_index) + ', ' + str(attribute_index)
            self.RaiseError(ErrNo2)

        BldArray = [SeriesPtr[i] for i in range(sLength.value)]
        _lib.SMO_free(SeriesPtr)
        return BldArray

    def get_series_by_name(self, objectTypeLabel, object_id, attribute_name, start_index, num_steps):
        """ Get a time-series of values and the units label.
            Args:
            objectTypeLabel: "Node", "Link", "Subcatchment", or "System"
            object_id: identifier of the node, link, or subcatchment. (Not used for System.)
            variable_name: name of attribute, from appropriate SMO_*Attributes array
            Returns
        """
        items = self.get_items(objectTypeLabel)
        if items:
            item = self.get_itemById(items, object_id)
            attribute_index = item.Attributes[item.AttributeNames.index(attribute_name)]
            units = item.AttributeUnits[attribute_index][self.unit_system]
            return self._get_series(item.get_series, item.index, attribute_index, start_index, num_steps), units

    def get_SubcatchmentSeries(self, subcatchment_index, attribute, start_index=0, num_values=-1):
        """
        Purpose: Get time series results from the given Subcatchment.
        subcatchment_index is from zero-indexed subcatchments in output file, same indexes as self.subcatchments.
        attribute must be an integer from SMO_subcatchment.Attributes.
        start_index is the first time index to retrieve, default = 0.
        num_values is the number of values to retrieve, default of -1 gets all values starting at start_index.
        """
        return self._get_series(SMO_subcatchment.get_series, subcatchment_index, attribute, start_index, num_values)

    def get_NodeSeries(self, node_index, attribute, start_index=0, num_values=-1):
        """
        Purpose: Get time series results from the given node.
        node_index is from zero-indexed nodes in output file, same indexes as self.nodes.
        attribute must be an integer from SMO_node.Attributes.
        start_index is the first time index to retrieve, default = 0.
        num_values is the number of values to retrieve, default of -1 gets all values starting at start_index.
        """
        return self._get_series(SMO_node.get_series, node_index, attribute, start_index, num_values)

    def get_LinkSeries(self, link_index, attribute, start_index=0, num_values=-1):
        """
        Purpose: Get time series results from the given link.
        link_index is from zero-indexed links in output file, same indexes as self.links.
        attribute must be an integer from SMO_link.Attributes.
        start_index is the first time index to retrieve, default = 0.
        num_values is the number of values to retrieve, default of -1 gets all values starting at start_index.
        """
        return self._get_series(SMO_link.get_series, link_index, attribute, start_index, num_values)

    def get_SystemSeries(self, attribute, start_index=0, num_values=-1):
        """
        Purpose: Get time series results for the given system attribute.
        attribute must be an integer from SMO_system.Attributes.
        start_index is the first time index to retrieve, default = 0.
        num_values is the number of values to retrieve, default of -1 gets all values starting at start_index.
        """
        return self._get_series(SMO_system.get_series, -1, attribute, start_index, num_values)

    def get_AttributeOfAllObjects(self, item_list, attribute_index, time_index):
        """
        Get the specified attribute for all objects of this type at the given time_index.

        Args:
            item_list: one of the lists in self.items (self.subcatchments, self.nodes, self.links, self.system)
            attribute_index: index of attribute in Attributes and AttributeNames of the type of items in item_list
        """
        alength = c_int()
        ErrNo1 = c_int()
        item = item_list[0]
        ValArrayPtr = _lib.SMO_newOutValueArray(self.ptrapi, _lib.SMO_getAttribute, item.elementType,
                                                byref(alength), byref(ErrNo1))
        ErrNo2 = item.get_attribute(self.ptrapi, time_index, attribute_index, ValArrayPtr)
        BldArray = [ValArrayPtr[i] for i in range(alength.value)]
        _lib.SMO_free(ValArrayPtr)
        return BldArray

    def get_AllAttributes(self, item, time_index):
        """
        Purpose: For an item (SMO_subcatchment, SMO_node, SMO_link, or SMO_system) at given time, get all attributes
        """
        alength = c_int()
        ErrNo1 = c_int()
        ValArrayPtr = _lib.SMO_newOutValueArray(self.ptrapi,
                                                _lib.SMO_getResult,
                                                item.elementType,
                                                byref(alength),
                                                byref(ErrNo1))
        ErrNo2 = item.get_result(self.ptrapi, time_index, item.index, ValArrayPtr)
        BldArray = [ValArrayPtr[i] for i in range(alength.value)]
        _lib.SMO_free(ValArrayPtr)
        return BldArray

    def CloseOutputFile(self):
        """
        Call to close binary file.
        """
        ret = _lib.SMO_close(byref(self.ptrapi))
        if ret != 0:
            raise Exception('Failed to Close *.out file')

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
