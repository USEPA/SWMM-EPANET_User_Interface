"""

Wrapper for EPANET Output API.

Author: Bryant E. McDonnell
Date: 12/7/2015
Language: Anglais

Refactored for inclusion in SWMM-EPANET User Interface project
2016
Mark Gray, RESPEC
for US EPA
2018
Tong Zhai
update to python 3

"""

from ctypes import *
import time, datetime
import Externals.epanet.outputapi.outputapi as _lib

# ctypes utility variable created once to avoid overhead of creating every time needed
_cint = c_int()

class ENR_categoryBase:
    """ This class is not used directly, it is as a base class with shared code for ENR_node_type and ENR_link_type.
        self.name stores the ID/name of the item and can be text or numeric.
        self.index stores the index of this item used when accessing the binary file.
        Code outside this module should not need to access self.index. """
    TypeLabel = "Base"

    def __init__(self, item_name, index):
        self.name = item_name
        self.index = index

    def __str__(self):
        return self.name

    @classmethod
    def read_all(cls, output):
        """ Read all items of this class from the output file into a dictionary.
            Intended to be called only in the constructor of the output file object.
            Args
            output (OutputObject): object that has already opened the desired output file.
            Returns (dictionary): Python dictionary of all objects of this type, keyed by name.
        """
        items = {}
        item_count = output._call_int(_lib.ENR_getNetSize, cls._count_flag)
        ctypes_name = _lib.String(((_lib.MAXID + 1) * '\0').encode())
        for index in range(1, item_count + 1):
            _lib.ENR_getElementName(output.ptrapi, cls._elementType, index, ctypes_name)
            try:
                # name = str(ctypes_name)
                name = ctypes_name.data.decode('utf-8')
                items[name] = cls(name, index)
            except Exception as e:
                # raise Exception("EPANET read_all output failed.")
                pass
        return items

    # def get_value(self, output, attribute, time_index):
    #     """ Purpose: Get a single result for particular item, time, and attribute.
    #         Args
    #         output: OutputObject that already has the desired output file open.
    #         attribute: attribute to get values of - must be an ENR_attribute from self.Attributes.
    #         time_index: time index to retrieve, 0 is the first time index.
    #     """
    #     ctypes_return = c_float()
    #     return_code = self._get_value(output.ptrapi, time_index, self.index, attribute.index, byref(ctypes_return))
    #     if return_code == 0:
    #         return ctypes_return.value
    #     else:
    #         print("Error in get_value({}, {}, {})".format(str(self.name), str(time_index), str(attribute.name)))
    #         output._raise_error(return_code)

    def get_series(self, output, attribute, start_index=0, end_index=-1):
        """
            Purpose: Get time series results for the requested attribute.
            Args
            output: OutputObject that already has the desired output file open.
            attribute: attribute to get values of - must be an ENR_attribute from self.Attributes.
            start_index: first time index to retrieve, default = 0 for first time index.
            end_index: last time index to retrieve, or -1 to get all values starting at start_index.
        """
        if end_index == -1:
            end_index = output.num_periods - 1
        if start_index < 0:
            raise Exception("get_series start_index " + str(start_index) + " cannot be less than zero.")
        if start_index >= output.num_periods:
            raise Exception("get_series start_index " + str(start_index) +
                            " must be less than number of time steps " + str(output.num_periods))
        if end_index < start_index:
            raise Exception("get_series end_index " + str(end_index) +
                            " less than start_index " + str(start_index))
        if end_index >= output.num_periods:
            raise Exception("get_series end_index " + str(end_index) +
                            " must be less than number of time steps " + str(output.num_periods))
        returned_length = c_int()
        error_new = c_int()
        ask_for_end = end_index
        # if output.newOutValueSeriesLengthIsEnd:
        #     ask_for_end += start_index + 1
        series_pointer = _lib.ENR_newOutValueSeries(output.ptrapi, start_index,
                                                    ask_for_end, byref(returned_length), byref(error_new))
        if error_new.value != 0:
            print("Error " + str(error_new.value) +
                  " allocating series start=" + str(start_index) + ", end=" + str(ask_for_end))
            output._raise_error(error_new.value)

        if self.index >= 0:
            error_get = self._get_series(output.ptrapi,
                                         self.index,
                                         attribute.index,
                                         start_index,
                                         returned_length.value,
                                         series_pointer)
        else:
            error_get = self._get_series(output.ptrapi,
                                         attribute.index,
                                         start_index,
                                         returned_length.value,
                                         series_pointer)

        if error_get != 0:
            print("Error reading series " + self.TypeLabel + " " + str(self.name) + ', att #' + str(attribute.index))
            output._raise_error(error_get)

        build_array = [series_pointer[i] for i in range(returned_length.value)]
        _lib.ENR_free(series_pointer)
        return build_array

    @classmethod
    def get_attribute_for_all_at_time(cls, output, attribute, time_index):
        """ Purpose: For all items of this type (nodes or links) at given time, get a particular attribute.
            Args
            output: OutputObject that already has the desired output file open.
            attribute: attribute to get values of - must be an ENR_attribute from self.Attributes.
            time_index: time index to retrieve, 0 is the first time index.
            Examples
            for node in output.nodes:
                values = node.get_all_attributes_at_time(output, time_index)
                for attribute in (node.AttributeDemand, node.AttributeHead):
                    print(attribute.name, attribute.str(values[attribute.index]))

        """
        returned_length = c_int()
        error_new = c_int()
        array_pointer = _lib.ENR_newOutValueArray(output.ptrapi,
                                                  _lib.ENR_getAttribute,
                                                  cls._elementType,
                                                  byref(returned_length),
                                                  byref(error_new))
        if error_new.value != 0:
            print("Error " + str(error_new.value) + " calling ENR_newOutValueArray for " + cls.TypeLabel)
            output._raise_error(error_new.value)

        error_get = cls._get_attribute(output.ptrapi, time_index, attribute.index, array_pointer)
        if error_get != 0:
            print("Error reading " + str(attribute.name) + " for all " + cls.TypeLabel + "s at " + str(time_index))
            output._raise_error(error_get)

        BldArray = [array_pointer[i] for i in range(returned_length.value)]
        _lib.ENR_free(array_pointer)
        return BldArray

    def get_all_attributes_at_time(self, output, time_index):
        """
        For one location at one time, get all attributes.

        Returns: List of attribute values in the same order as self.attributes.

        Examples

        output = ENOutputWrapper.OutputObject("Net1.out")
        for time_index in range(0, output.num_periods):
            for node in output.nodes:
                attribute_values = node.get_all_attributes_at_time(output, time_index)
                for value, definition in zip(attribute_values, node.attributes):
                    print("At node " + node.name + ", attribute " + definition.name +
                          " has value " + str(value) + " at time step " + time_index)
        """

        returned_length = c_int()
        error_new = c_int()
        array_pointer = _lib.ENR_newOutValueArray(output.ptrapi,
                                                  _lib.ENR_getResult,
                                                  self._elementType,
                                                  byref(returned_length),
                                                  byref(error_new))
        if error_new.value != 0:
            print("Error " + str(error_new.value) + " calling ENR_newOutValueArray for " + self.TypeLabel)
            output._raise_error(error_new.value)

        error_get = self._get_result(output.ptrapi, time_index, self.index, array_pointer)
        if error_get != 0:
            print("Error reading all attributes for " + self.name + " at " + str(time_index))
            output._raise_error(error_get)
        BldArray = [array_pointer[i] for i in range(returned_length.value)]
        _lib.ENR_free(array_pointer)
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
            if attribute.name.upper() == attribute_name.upper():
                return attribute
        return None


class ENR_attribute():
    """ Attribute type for accessing and displaying attribute name, units, and string-formatted value.
        Attributes
        index (int): index within the outputapi library of this attribute, used internally for requesting this attribute
                     and used for finding this attribute in the array returned by get_all_attributes_at_time.
        name (str): human-readable label for this attribute.
        units: when creating, pass in a 2-element tuple with ('English', 'Metric') unit labels
               used by units() function to return the appropriate units for the system in use.
        str_format (str): preferred format for converting the values retrieved for this attribute into a string;
                          used in str(value) function.
     """
    def __init__(self, index, name, units, str_format='{:7.2f}'):
        self.index = index
        self.name = name
        self._units = units
        self.str_format = str_format

    def str(self, value):
        """Format a value using the string format of this attribute"""
        return self.str_format.format(value)

    def units(self, unit_system):
        """Retrieve the units label for this attribute for the specified unit system."""
        return self._units[unit_system]


class _ENR_attributeLinkStatus(ENR_attribute):
    """ Specialized version of ENR_attribute that overrides str method for displaying link status """
    def str(self, value):
        if value in [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]:
            return ('Closed', 'Closed', 'Closed', 'Open', 'Active', 'Open', 'Open', 'Open')[int(value)]
        else:
            return str(value)


class ENR_node_type(ENR_categoryBase):
    """
    A node of this type can be used to access values from an EPANET output file using the methods in ENR_categoryBase.
    Junctions, tanks, and reservoirs all use this same class.
    Attributes are defined at the class level and are shared by all nodes.
    API methods are private and are only used internally by methods in ENR_categoryBase.
    """
    TypeLabel = "Node"

    AttributeDemand   = ENR_attribute(_lib.ENR_demand,   "Demand",   ('', ''))
    AttributeHead     = ENR_attribute(_lib.ENR_head,     "Head",     ('ft', 'm'))
    AttributePressure = ENR_attribute(_lib.ENR_pressure, "Pressure", ('psi', 'm'))
    AttributeQuality  = ENR_attribute(_lib.ENR_quality,  "Quality",  ('mg/L', 'mg/L'))

    Attributes = (AttributeDemand, AttributeHead, AttributePressure, AttributeQuality)

    _count_flag = _lib.ENR_nodeCount
    # _get_value = _lib.ENR_getNodeValue
    _get_series = _lib.ENR_getNodeSeries
    _get_attribute = _lib.ENR_getNodeAttribute
    _get_result = _lib.ENR_getNodeResult
    _elementType = _lib.ENR_node


class ENR_link_type(ENR_categoryBase):
    """
    A link of this type can be used to access values from an EPANET output file using the methods in ENR_categoryBase.
    Pipes, pumps, and valves all use this same class.
    Attributes are defined at the class level and are shared by all links.
    API methods are private and are only used internally by methods in ENR_categoryBase.
    """
    TypeLabel = "Link"

    AttributeFlow           = ENR_attribute(_lib.ENR_flow,              'Flow',            ('', ''))
    AttributeVelocity       = ENR_attribute(_lib.ENR_velocity,          'Velocity',        ('fps', 'm/s'))
    AttributeHeadloss       = ENR_attribute(_lib.ENR_headloss,          'Unit Headloss',   ('ft/Kft', 'm/km'))
    AttributeQuality        = ENR_attribute(_lib.ENR_avgQuality,        'Quality',         ('mg/L', 'mg/L'))
    AttributeStatus         = _ENR_attributeLinkStatus(_lib.ENR_status, 'Status',          ('', ''))
    AttributeSetting        = ENR_attribute(_lib.ENR_setting,           'Setting',         ('', ''))
    AttributeReactionRate   = ENR_attribute(_lib.ENR_rxRate,            'Reaction Rate',   ('mg/L/d', 'mg/L/d'))
    AttributeFrictionFactor = ENR_attribute(_lib.ENR_frctnFctr,         'Friction Factor', ('', ''), '{:7.3f}')

    Attributes = (AttributeFlow, AttributeVelocity, AttributeHeadloss, AttributeQuality,
                  AttributeStatus, AttributeSetting, AttributeReactionRate, AttributeFrictionFactor)

    _count_flag = _lib.ENR_linkCount
    # _get_value = _lib.ENR_getLinkValue
    _get_series = _lib.ENR_getLinkSeries
    _get_attribute = _lib.ENR_getLinkAttribute
    _get_result = _lib.ENR_getLinkResult
    _elementType = _lib.ENR_link

ENR_USFlowUnits = ('CFS', 'GPM', 'MGD', 'IMGD', 'AFD')
ENR_SIFlowUnits = ('LPS', 'LPM', 'MLD', 'CMH', 'CMD')
ENR_PressureUnits = ('PSI', "meters", "kPa")

ENR_UnitsUS = 0
ENR_UnitsSI = 1


class OutputObject(object):

    def __init__(self, output_file_name):
        """ Open the named file and maintain an internal pointer to be used to access contents of the file.
            Read header information from the file including units, times, and lists of nodes and links.
            Args
            output_file_name (str): full path and file name of EPANET binary output file to open
        """
        self._call_int_return = c_int()  # Private variable used only inside call_int
        self._call_double_return = c_double()  # Private variable used only inside call_double
        self.output_file_name = str(output_file_name)
        self.ptrapi = _lib.ENR_init()
        ret = _lib.ENR_open(self.ptrapi, c_char_p(self.output_file_name.encode()))
        if ret > 400:
            self._raise_error(ret)
        file_version = self._call_int(_lib.ENR_getVersion)
        print("ENR opened {} Version {}".format(output_file_name, str(file_version)))
        self.dates = []
        self.times = []
        self._get_times()
        if self.simDuration > 0:
            self._measure_new_out_value_series()
        self._get_units()
        self.nodes = ENR_node_type.read_all(self)
        self.links = ENR_link_type.read_all(self)
        self.all_items = (self.nodes, self.links)
        self.nodes_units = {}
        self.links_units = {}

    def build_units_dictionary(self):
       # output attributes
        for l_id in self.links.keys():
            for attr in self.links[l_id].Attributes:
                self.links_units[attr.name] = attr._units[self.unit_system]
            break
       # output attributes
        for n_id in self.nodes.keys():
            for attr in self.nodes[n_id].Attributes:
                self.nodes_units[attr.name] = attr._units[self.unit_system]
            break

    def get_items(self, object_type_label):
        """ Get the dictionary of items of the type whose TypeLabel attribute is object_type_label.

            Args:
            object_type_label: can be "Node" or "Link".

            Examples:
                for name, node in get_items("Node"):
                    print(name, str(node.get_series(output, ENR_node_type.AttributePressure, 0, 2)[1]))
        """
        for items in self.all_items:
            if items:
                # Check the first item to make sure its type label matches
                for item in items.values():
                    if item.TypeLabel.upper() == object_type_label.upper():
                        return items
                    else:  # these are not the items we want, skip to next items
                        break
        return {}

    def call(self, function, *args):
        """ Call any API method whose return value is an integer which indicates an error if != 0
            Handle the nonzero value by calling RaiseError."""
        try:
            ret = function(self.ptrapi, *args)
            if ret != 0:
                self._raise_error(ret)
        except Exception as ex:
            print(str(ex))
            raise Exception("SWMM output error calling " + str(function) + ": " + str(ex))

    def _call_int(self, function, *args):
        """ Call an API method whose return value is an integer indicating an error if != 0
            and which also returns an integer in the last argument (using byref).
            call_int handles the return value error flag by calling RaiseError if needed.
            Do not include the last argument (the return argument) in *args, it will be added internally.
            The integer value returned is the return value of call_int."""
        args_to_pass = list(args)
        args_to_pass.append(byref(self._call_int_return))  # When moving to Python 3.5+, can skip appending and use:
        self.call(function, *args_to_pass)                 # self.call(function, *args, byref(self._call_int_return))
        return self._call_int_return.value

    def _call_double(self, function, *args):
        """ Call an API method whose return value is an integer indicating an error if != 0
            and which also returns a double in the last argument (using byref).
            call_double handles the return value error flag by calling RaiseError if needed.
            Do not include the last argument (the return argument) in *args, it will be added internally
            The double value returned is the return value of call_double."""
        args_to_pass = list(args)
        args_to_pass.append(byref(self._call_double_return))  # When moving to Python 3.5+, can skip appending and use:
        self.call(function, *args_to_pass)                   # self.call(function, *args, byref(self._call_int_return))
        return self._call_double_return.value

    def _raise_error(self, ErrNo):
        # if _RetErrMessage(ErrNo , errmsg, err_max_char)==0:
        #     raise Exception(errmsg.value)
        # else:
        raise Exception("EPANET output error #{0}".format(ErrNo) )

    def _measure_new_out_value_series(self):
        """Test ENR_newOutValueSeries to see whether it treats the requested length as length or end.
            Sets self.newOutValueSeriesLengthIsEnd flag so we can adjust how we call this method."""

        returned_length = c_int()
        error_new = c_int()

        try:
            series_pointer = _lib.ENR_newOutValueSeries(self.ptrapi, 0, 1, byref(returned_length), byref(error_new))
            if error_new.value != 0:
                print("Error allocating series start to test ENR_newOutValueSeries: " + str(error_new.value))
                self._raise_error(error_new.value)
            self.newOutValueSeriesLengthIsEnd = (returned_length.value == 1)
            _lib.ENR_free(series_pointer)
        except Exception as ex:
            print(str(ex))
            raise Exception("SWMM output error calling ENR_newOutValueSeries: " + str(ex))

    def _get_units(self):
        """
        Purpose: Read pressure and flow units, populate:
                 self.unit_system, self.flowUnitsLabel, ENR_link_type.AttributeFlow._units,
                  self.pressUnitsLabel
        """
        flow_units_index = self._call_int(_lib.ENR_getUnits, _lib.ENR_flowUnits)
        if flow_units_index < len(ENR_USFlowUnits):
            self.unit_system = ENR_UnitsUS
            self.flowUnitsLabel = ENR_USFlowUnits[flow_units_index]
        else:
            self.unit_system = ENR_UnitsSI
            self.flowUnitsLabel = ENR_SIFlowUnits[flow_units_index - len(ENR_USFlowUnits)]

        self.pressUnits = self._call_int(_lib.ENR_getUnits, _lib.ENR_pressUnits)
        self.pressUnitsLabel = ENR_PressureUnits[self.pressUnits]

        # Set private units attributes to match project units
        ENR_node_type.AttributePressure._units = (self.pressUnitsLabel, self.pressUnitsLabel)
        ENR_node_type.AttributeDemand._units = (self.flowUnitsLabel, self.flowUnitsLabel)
        ENR_link_type.AttributeFlow._units = (self.flowUnitsLabel, self.flowUnitsLabel)

    # def _get_sizes(self):
    #     """
    #     Populates object attributes with the water object counts
    #     """
    #     self.tankCount = self._call_int(_lib.ENR_getNetSize, _lib.ENR_tankCount)
    #     self.pumpCount = self._call_int(_lib.ENR_getNetSize, _lib.ENR_pumpCount)
    #     self.valveCount = self._call_int(_lib.ENR_getNetSize, _lib.ENR_valveCount)

    def _get_times(self):
        """
        Purpose: Read report and simulation time related parameters.
        Populate self attributes: reportStart, reportStep, simDuration, num_periods
        """
        self.reportStart = self._call_int(_lib.ENR_getTimes, _lib.ENR_reportStart)
        self.reportStep  = self._call_int(_lib.ENR_getTimes, _lib.ENR_reportStep)
        self.simDuration = self._call_int(_lib.ENR_getTimes, _lib.ENR_simDuration)
        #ToDo: num_periods is one more than specified ?!
        self.num_periods = self._call_int(_lib.ENR_getTimes, _lib.ENR_numPeriods)

        #let's save the time step series once as all constituents share this time series
        #x_values = []
        # hack #2, +1 is to end in the ending moment of a time step
        # this is called only once so as to be applied to all constituents' time series
        for time_index in range(0, self.num_periods):
            elapsed_hours = self.elapsed_hours_at_index(time_index)
            #self.dates.append(self.reportStart + datetime.timedelta(hours=elapsed_hours))
            self.times.append(elapsed_hours)

        pass

    def get_pump_energy_usage_statistics(self):
        """ Read pump energy usage statistics for all pumps.
            Returns: dictionary (keyed by each pump's link name) of PumpEnergy instances """
        all_pump_energy = {}
        pump_count = self._call_int(_lib.ENR_getNetSize, _lib.ENR_pumpCount)
        if pump_count:
            link_index_return = c_int()
            returned_length = c_int()
            error_new = c_int()
            array_pointer = _lib.ENR_newOutValueArray(self.ptrapi,
                                                      _lib.ENR_getEnergy,
                                                      _lib.ENR_link,
                                                      byref(returned_length),
                                                      byref(error_new))
            if error_new.value != 0:
                print("Error " + str(error_new.value) + " calling ENR_newOutValueArray for getEnergy")
                self._raise_error(error_new.value)

            for pump_index in range(1, pump_count + 1):
                self.call(_lib.ENR_getEnergyUsage, pump_index, byref(link_index_return), array_pointer)
                link_index = link_index_return.value
                for link in self.links:
                    if self.links[link].index == link_index:
                        all_pump_energy[self.links[link].name] = PumpEnergy(self.links[link].name,
                                                                array_pointer[1], array_pointer[2], array_pointer[3],
                                                                array_pointer[4], array_pointer[5], array_pointer[6])
                        break
            _lib.ENR_free(array_pointer)
        return all_pump_energy

    def get_reaction_summary(self):
        """ Read reaction summary (network-wide average reaction rates and average source mass inflow)
            Returns: four floating-point numbers: bulk, wall, tank, source """
        returned_length = c_int()
        error_new = c_int()
        array_pointer = _lib.ENR_newOutValueArray(self.ptrapi,
                                                  _lib.ENR_getReacts,
                                                  _lib.ENR_link,
                                                  byref(returned_length),
                                                  byref(error_new))
        if error_new.value != 0:
            print("Error " + str(error_new.value) + " calling ENR_newOutValueArray for getReacts")
            self._raise_error(error_new.value)

        self.call(_lib.ENR_getNetReacts, array_pointer)
        bulk = array_pointer[1]
        wall = array_pointer[2]
        tank = array_pointer[3]
        source = array_pointer[4]
        _lib.ENR_free(array_pointer)
        return bulk, wall, tank, source

    def close(self):
        """
        Close binary file.
        """
        try:
            ret = _lib.ENR_close(self.ptrapi)
            if ret != 0:
                raise Exception('Failed to Close file ' + self.output_file_name)
        finally:
            self.ptrapi = None

    def elapsed_hours_at_index(self, report_time_index):
        return (report_time_index * self.reportStep) / 3600

    def get_time_string(self, report_time_index):
        total_hours = self.elapsed_hours_at_index(report_time_index)
        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)
        return '{:02d}:{:02d}'.format(hours, minutes)

    # def get_date_string(self, report_time_index):
    #     # current date = self.StartDate plus elapsed hours
    #     total_hours = self.elapsed_hours_at_index(report_time_index)
    #     report_date = self.StartDate + datetime.timedelta(hours=total_hours)
    #     return report_date.strftime("%Y-%m-%d %H:%M")

    def get_time_series(self, type_label, object_id, attribute_name):
        # ToDo: need to debug get_series about not reading the first zero entry
        try:
            import pandas as pd
            item = None
            if "SYSTEM" in type_label.upper():
                item = self.system.items()[0][1]  # SwmmOutputSystem
            else:
                item = self.get_items(type_label)[object_id]  # SwmmOutputSubcatchment, Link, Node

            attribute = item.get_attribute_by_name(attribute_name)  # SwmmOutputAttribute
            #ToDo: this is a hack here, due to num_periods is off by 1 too many
            y_values = item.get_series(self, attribute, 0, self.num_periods - 1)

            # now make a time series data frame
            #return pd.Series(y_values, index=self.dates)
            return pd.Series(y_values, index=self.times)
        except Exception as ex:
            print (str(ex))


class PumpEnergy:
    def __init__(self, link, utilization, efficiency, kw_per_flow, average_kw, peak_kw, cost_per_day):
        self.link = link
        self.utilization = utilization
        self.efficiency = efficiency
        self.kw_per_flow = kw_per_flow
        self.average_kw = average_kw
        self.peak_kw = peak_kw
        self.cost_per_day = cost_per_day

    def __str__(self):
        return "name: " + self.link + '\n' +\
            "utilization: " + str(self.utilization) + '\n' +\
            "efficiency: " + str(self.efficiency) + '\n' +\
            "kw_per_flow: " + str(self.kw_per_flow) + '\n' +\
            "average_kw: " + str(self.average_kw) + '\n' +\
            "peak_kw: " + str(self.peak_kw) + '\n' +\
            "cost_per_day: " + str(self.cost_per_day) + '\n'
