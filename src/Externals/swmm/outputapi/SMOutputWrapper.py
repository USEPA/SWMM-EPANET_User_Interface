"""

Wrapper for SWMM Output API.

Written for SWMM-EPANET User Interface project
2016
Mark Gray, RESPEC
for US EPA

Inspired by ENOutputWrapper by Bryant E. McDonnell 12/7/2015

"""

from ctypes import *

import Externals.swmm.outputapi.outputapi as _lib


# Subcatchment Attributes

from outputapi import rainfall_subcatch, snow_depth_subcatch, evap_loss, infil_loss,\
                      runoff_rate, gwoutflow_rate, gwtable_elev, soil_moisture, pollutant_conc_subcatch

SMO_subcatchAttributes = (rainfall_subcatch, snow_depth_subcatch, evap_loss, infil_loss,
                          runoff_rate, gwoutflow_rate, gwtable_elev, soil_moisture, pollutant_conc_subcatch)

SMO_subcatchAttributeNames = ("Precipitation", "Snow Depth", "Evaporation", "Infiltration",
                              "Runoff", "Groundwater Flow", "Groundwater Elevation", "Soil Moisture", "Concentration")

SMO_subcatchAttributeUnits = (('in/hr', 'mm/hr'),  # Precipitation
                              ('in', 'mm'),  # Snow Depth
                              ('in/day', 'mm/day'),  # Evaporation
                              ('in/hr', 'mm/hr'),  # Infiltration
                              ('CFS', 'CMS'),  # Runoff
                              ('CFS', 'CMS'),  # GW Flow
                              ('ft', 'm'),  # GW Elev
                              ('', ''),  # Soil Moisture
                              ('mg/L', 'mg/L'))  # Washoff

# Node Attributes

from outputapi import invert_depth,\
                      hydraulic_head,\
                      stored_ponded_volume,\
                      lateral_inflow,\
                      total_inflow,\
                      flooding_losses,\
                      pollutant_conc_node\

SMO_nodeAttributes = (invert_depth,
                      hydraulic_head,
                      stored_ponded_volume,
                      lateral_inflow,
                      total_inflow,
                      flooding_losses,
                      pollutant_conc_node)

SMO_nodeAttributeNames = ("Depth",
                          "Head",
                          "Volume",
                          "Lateral Inflow",
                          "Total Inflow",
                          "Flooding",
                          "TSS")

SMO_nodeAttributeUnits = (('ft', 'm'),  # Depth
                          ('ft', 'm'),  # Head
                          ('ft3', 'm3'),  # Volume
                          ('CFS', 'CMS'),  # Lateral Inflow
                          ('CFS', 'CMS'),  # Total Inflow
                          ('CFS', 'CMS'),  # Overflow
                          ('mg/L', 'mg/L'))  # Quality

# Link Attributes

from outputapi import flow_rate_link, flow_depth, flow_velocity, flow_volume, capacity, pollutant_conc_link
SMO_linkAttributes = (flow_rate_link, flow_depth, flow_velocity, flow_volume, capacity, pollutant_conc_link)
SMO_linkAttributeNames = ("Flow", "Depth", "Velocity", "Volume", "Capacity", "Concentration")
SMO_linkAttributeUnits = (('CFS', 'CMS'),    # Flow
                          ('ft', 'm'),       # Depth
                          ('fps', 'm/s'),    # Velocity
                          ('ft3', 'm3'),     # Volume.
                          ('', ''),          # Fraction Full
                          ('mg/L', 'mg/L'))  # Quality

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

SMO_systemAttributes = (air_temp,
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

SMO_systemAttributeNames = ("Temperature",
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

SMO_systemAttributeUnits = (('deg F','deg C'),
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
        ret = _lib.SMR_open(str(output_file_name), byref(self.ptrapi))
        if ret != 0:
            self.RaiseError(ret)
        # TODO: recompile dll so we can use this new argument order:
        # self.call(_lib.SMR_open, str(output_file_name))
        self._get_units()
        self._get_sizes()
        self._get_times()
        self.subcatchment_ids = self._read_linked_ids(_lib.SMO_getSubcatchIDs)
        self.node_ids = self._read_linked_ids(_lib.SMO_getNodeIDs)
        self.link_ids = self._read_linked_ids(_lib.SMO_getLinkIDs)

    def call(self, function, *args):
        """ Call any API method whose return value is an integer which indicates an error if != 0
            Handle the nonzero value by calling RaiseError."""
        try:
            ret = function(self.ptrapi, *args)
            if ret != 0:
                self.RaiseError(ret)
        except Exception as ex:
            print str(ex)
            raise Exception("SWMM output error calling " + str(function) + ": " + str(ex))

    def call_int(self, function, *args):
        """ Call an API method whose return value is an integer indicating an error if != 0
            and which also returns an integer in the last argument (using byref).
            call_int handles the return value error flag by calling RaiseError if needed.
            Do not include the last argument used as a return in *args, it will be added internally
            and the integer is the return value of call_int."""
        args_to_pass = list(args)
        args_to_pass.append(byref(self._call_int_return))  # When moving to Python 3.5+, can skip appending and use:
        self.call(function, *args_to_pass)                 # self.call(function, *args, byref(self._call_int_return))
        return self._call_int_return.value

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
        err = _lib.SMO_getProjectSize(self.ptrapi, _lib.nodeCount, byref(cint))
        if err != 0:
            print "Error in SMO_getProjectSize(nodeCount)"
            self.RaiseError(err)
        self.nodeCount = self.call_int(_lib.SMO_getProjectSize, _lib.nodeCount)
        self.subcatchCount = self.call_int(_lib.SMO_getProjectSize, _lib.subcatchCount)
        self.linkCount = self.call_int(_lib.SMO_getProjectSize, _lib.linkCount)
        self.pollutantCount = self.call_int(_lib.SMO_getProjectSize, _lib.pollutantCount)

    def _get_times(self):
        """
        Purpose: Retrieve report and simulation time-related parameters and stores them in self.
        """

        self.reportStart = 0  # TODO: read report start time from output
        # _lib.SMO_getTimes(self.ptrapi, _lib.SMO_reportStart, byref(cint))
        # self.reportStart = cint.value

        self.reportStep = self.call_int(_lib.SMO_getTimes, _lib.reportStep)
        self.numPeriods = self.call_int(_lib.SMO_getTimes, _lib.numPeriods)
        self.simDuration = self.reportStep * self.numPeriods

        # _lib.SMO_getTimes(self.ptrapi, _lib.SMO_simDuration, byref(cint))
        # self.simDuration = cint.value


    def _read_linked_ids(self, get_ids):
        """ Read a linked list of struct IDentry (char* IDname, IDentry* nextID).
            get_ids must be _lib.SMO_getNodeIDs or _lib.SMO_getLinkIDs or an entry point following the same pattern
            Returns a Python list of all the IDs."""
        ids = []
        c_return = get_ids(self.ptrapi, byref(cint))
        if cint.value != 0:
            print "Error reading IDs"
            self.RaiseError(cint.value)
        while c_return:
            ids.append(str(c_return.contents.IDname.data))
            print "Read ID " + ids[-1]
            c_return = c_return.contents.nextID
        return ids

    def get_NodeIndex(self, node_id):
        """Retrieves the index of the node with the specified ID.

        Arguments:
        node_id: node ID label"""
        try:
            return self.node_ids.index(node_id)
        except:
            return -1

    def get_LinkIndex(self, link_id):
        """Retrieves the index of the link with the specified ID.

        Arguments:
        link_id: link ID label"""
        try:
            return self.link_ids.index(link_id)
        except:
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

    def _get_series(self, function, item_index, attribute, start_index=0, num_values=-1):
        """
        Purpose: Get time series results for particular attribute. Specify series
        start and length using start_index and num_values respectively.

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
        SeriesPtr = _lib.SMO_newOutValueSeries(self.ptrapi, start_index,
                                               num_values, byref(sLength), byref(ErrNo1))
        if ErrNo1.value != 0:
            print "Error allocating series " + str(function) + ', ' + str(item_index) + ', ' + str(attribute)
            self.RaiseError(ErrNo1.value)

        ErrNo2 = function(self.ptrapi,
                          item_index,
                          attribute,
                          start_index,
                          sLength.value,
                          SeriesPtr)
        if ErrNo2 != 0:
            print "Error reading series " + str(function) + ', ' + str(item_index) + ', ' + str(attribute)
            self.RaiseError(ErrNo2)

        BldArray = [SeriesPtr[i] for i in range(sLength.value)]
        _lib.SMO_free(SeriesPtr)
        return BldArray

    def get_NodeSeries(self, node_index, attribute, start_index=0, num_values=-1):
        """
        Purpose: Get time series results from the given node.
        node_index is from zero-indexed nodes in output file, same indexes as self.node_ids.
        attribute must be an integer from SMO_nodeAttributes.
        start_index is the first time index to retrieve, default = 0.
        num_values is the number of values to retrieve, default of -1 gets all values starting at start_index.
        """
        return self._get_series(_lib.SMO_getNodeSeries, node_index, attribute, start_index, num_values)

    def get_LinkSeries(self, link_index, attribute, start_index=0, num_values=-1):
        """
        Purpose: Get time series results from the given link.
        link_index is from zero-indexed links in output file, same indexes as self.link_ids.
        attribute must be an integer from SMO_linkAttributes.
        start_index is the first time index to retrieve, default = 0.
        num_values is the number of values to retrieve, default of -1 gets all values starting at start_index.
        """
        return self._get_series(_lib.SMO_getLinkSeries, link_index, attribute, start_index, num_values)

    # TODO: SMO_getSubcatchSeries, SMO_getSystemSeries

    def _get_attribute(self, function, item_type, attribute, time_index):
        """
        Purpose: For all nodes at given time, get a particular attribute
        """
        alength = c_int()
        ErrNo1 = c_int()
        ValArrayPtr = _lib.SMO_newOutValueArray(self.ptrapi, _lib.SMO_getAttribute,
                                                item_type, byref(alength), byref(ErrNo1))
        ErrNo2 = function(self.ptrapi, time_index, attribute, ValArrayPtr)
        BldArray = [ValArrayPtr[i] for i in range(alength.value)]
        _lib.SMO_free(ValArrayPtr)
        return BldArray

    def get_NodeAttribute(self, attribute, time_index):
        """ Purpose: For all nodes at given time, get a particular attribute """
        return self._get_attribute(_lib.SMO_getNodeAttribute, _lib.SMO_node, attribute, time_index)

    def get_LinkAttribute(self, attribute, time_index):
        """ Purpose: For all links at given time, get a particular attribute """
        return self._get_attribute(_lib.SMO_getLinkAttribute, _lib.SMO_link, attribute, time_index)

    def _get_result(self, function, item_type, ItemInd, TimeInd):
        """
        Purpose: For a node at given time, get all attributes
        """
        alength = c_int()
        ErrNo1 = c_int()
        ValArrayPtr = _lib.SMO_newOutValueArray(self.ptrapi,
                                                _lib.SMO_getResult,
                                                item_type,
                                                byref(alength),
                                                byref(ErrNo1))
        ErrNo2 = function(self.ptrapi, TimeInd, ItemInd, ValArrayPtr)
        BldArray = [ValArrayPtr[i] for i in range(alength.value)]
        _lib.SMO_free(ValArrayPtr)
        return BldArray

    def get_NodeResult(self, NodeInd, TimeInd):
        """
        Purpose: For a node at given time, get all attributes
        """
        return self._get_result(_lib.SMO_getNodeResult, _lib.SMO_node, NodeInd, TimeInd)

    def get_LinkResult(self, LinkInd, TimeInd):
        """
        Purpose: For a link at given time, get all attributes
        """
        return self._get_result(_lib.SMO_getLinkResult, _lib.SMO_link, LinkInd, TimeInd)

    def CloseOutputFile(self):
        """
        Call to close binary file.
        """
        ret = _lib.SMO_close(byref(self.ptrapi))
        if ret != 0:
            raise Exception('Failed to Close *.out file')

    def elapsed_hours_at_index(self, report_time_index):
        return (self.reportStart + report_time_index * self.reportStep) / 3600

    def get_time_string(self, report_time_index):
        total_hours = self.elapsed_hours_at_index(report_time_index)
        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)
        return '{:02d}:{:02d}'.format(hours, minutes)
