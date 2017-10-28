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


class SwmmOutputCategoryBase:
    """
    This class is not used directly, it is as a base class with shared code for
    SwmmOutputSubcatchment, SwmmOutputNode, SwmmOutputLink, and SwmmOutputSystem.
    self.name stores the ID/name of the item and can be text or numeric.
    self._index stores the index of this item used when accessing the binary file.
    Code outside this module should not need to access self._index.
    SwmmOutputSystem does not use self.name and self._index because it does not have multiple locations.
    """
    type_label = "Base"

    def __init__(self, item_name, index):
        self.name = item_name
        self._index = index

    def __str__(self):
        return self.name

    @classmethod
    def read_all(cls, output):
        """ Read all items of this type from the output file into a dictionary.
            Intended to be called only in the constructor of the output file object.
            Also add pollutants present in this output as attributes of this class.

            Args:
            output (SwmmOutputObject): object that has already opened the desired output file.
            Returns (dictionary): Python dictionary of all objects of this type, keyed by name.

            Notes:
            Not used for SwmmOutputSystem because it does not have a list of names/IDs to read,
            and it does not have pollutants as attributes to set.
        """
        items = {}
        item_count = output._call_int(_lib.SMO_getProjectSize, cls._count_flag)
        ctypes_name = _lib.String((_lib.MAXID + 1) * '\0')
        for index in range(0, item_count):
            _lib.SMO_getElementName(output.ptrapi, cls._element_type, index, ctypes_name, _lib.MAXID)
            name = str(ctypes_name)
            items[name] = cls(name, index)

        # Populate pollutants as attributes of this class
        if hasattr(cls, "_first_pollutant"):
            pollutant_index = cls._first_pollutant
            if len(cls.attributes) == pollutant_index:
                # pollutant_names = []
                for pollutant in output.pollutants.values():
                    cls.attributes.append(SwmmOutputAttribute(pollutant_index, pollutant.name,
                                                              (pollutant.units, pollutant.units)))
                    # pollutant_names.append(pollutant.name)
                    pollutant_index += 1
                # if pollutant_names:
                #     print(cls.type_label + " pollutants: " + ", ".join(pollutant_names))
            else:
                print "Not reading pollutants because len(cls.attributes) == " + str(len(cls.attributes)) +\
                      " and pollutant_index == " + str(pollutant_index)
        return items

    def get_series(self, output, attribute, start_index=0, num_values=-1):
        """
            Purpose: Get time series results for the requested attribute.
            Args
            output: SwmmOutputObject that already has the desired output file open.
            attribute: attribute to get values of - must be an SwmmOutputAttribute from self.Attributes.
            start_index: first time index to retrieve, default = 0 for first time index.
            num_values: number of values to retrieve, or -1 to get all values starting at start_index.
        """
        if num_values == -1:
            num_values = output.num_periods - start_index
        if start_index < 0 or start_index >= output.num_periods:
            raise Exception("Start Time Index " + str(start_index) +
                            " Outside Number of TimeSteps " + str(output.num_periods))
        if num_values < 1 or start_index + num_values > output.num_periods:
            raise Exception("Series Length " + str(num_values) +
                            " Outside Number of TimeSteps " + str(output.num_periods))
        returned_length = c_int()
        error_new = c_int()
        series_pointer = _lib.SMO_newOutValueSeries(output.ptrapi, start_index, num_values,
                                                    byref(returned_length), byref(error_new))
        if error_new.value != 0:
            print("Error " + str(error_new.value) +
                  " allocating series start=" + str(start_index) + ", len=" + str(num_values))
            output._raise_error(error_new.value)

        if self._index >= 0:
            error_get = self._get_series(output.ptrapi,
                                         self._index,
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
            print("Error reading series " + self.type_label + " " + str(self.name) + ', att #' + str(attribute.index))
            output._raise_error(error_get)

        build_array = [series_pointer[i] for i in range(returned_length.value)]
        _lib.SMO_free(series_pointer)
        return build_array

    @classmethod
    def get_attribute_for_all_at_time(cls, output, attribute, time_index):
        """ Purpose: For all items of this type (nodes or links) at given time, get a particular attribute.
            Args
            output: SwmmOutputObject that already has the desired output file open.
            attribute: attribute to get values of - must be an SwmmOutputAttribute from self.Attributes.
            time_index: time index to retrieve, 0 is the first time index.
        """
        returned_length = c_int()
        error_new = c_int()
        array_pointer = _lib.SMO_newOutValueArray(output.ptrapi, _lib.getAttribute,
                                                  cls._element_type, byref(returned_length), byref(error_new))
        if error_new.value != 0:
            print("Error " + str(error_new.value) + " calling ENR_newOutValueArray for " + cls.type_label)
            output._raise_error(error_new.value)

        error_get = cls._get_attribute(output.ptrapi, time_index, attribute.index, array_pointer)
        if error_get != 0:
            print("Error reading all attributes for " + cls.type_label +
                  " at " + str(time_index) + ', att ' + str(attribute.name))
            output._raise_error(error_get)

        BldArray = [array_pointer[i] for i in range(returned_length.value)]
        _lib.SMO_free(array_pointer)
        return BldArray

    @classmethod
    def get_attribute_by_name(cls, attribute_name):
        """ Get an SwmmOutputAttribute from the list attributes of this class, given the attribute name.
            Args:
            attribute_name: name of attribute, must match the name of an attribute in the attributes of this class.
            Returns
            SwmmOutputAttribute object whose name == attribute_name, or None if no attribute's name matches exactly.
        """
        for attribute in cls.attributes:
            if attribute.name == attribute_name:
                return attribute
        return None


class SwmmOutputAttribute():
    def __init__(self, index, name, units, str_format='{:7.2f}'):
        self.index = index
        self.name = name
        self._units = units
        self.str_format = str_format

    def str(self, value):
        """Format a value using the string format of this attribute"""
        return self.str_format.format(value)

    def units(self, unit_system):
        return self._units[unit_system]


class SwmmOutputSubcatchment(SwmmOutputCategoryBase):
    type_label = "Subcatchment"

    attribute_precipitation         = SwmmOutputAttribute(_lib.rainfall_subcatch,       "Precipitation",         ('in/hr', 'mm/hr'))
    attribute_snow_depth            = SwmmOutputAttribute(_lib.snow_depth_subcatch,     "Snow Depth",            ('in', 'mm'))
    attribute_evaporation           = SwmmOutputAttribute(_lib.evap_loss,               "Evaporation",           ('in/day', 'mm/day'))
    attribute_infiltration          = SwmmOutputAttribute(_lib.infil_loss,              "Infiltration",          ('in/hr', 'mm/hr'))
    attribute_runoff                = SwmmOutputAttribute(_lib.runoff_rate,             "Runoff",                ('CFS', 'CMS'))
    attribute_groundwater_flow      = SwmmOutputAttribute(_lib.gwoutflow_rate,          "Groundwater Flow",      ('CFS', 'CMS'))
    attribute_groundwater_elevation = SwmmOutputAttribute(_lib.gwtable_elev,            "Groundwater Elevation", ('ft', 'm'))
    attribute_soil_moisture         = SwmmOutputAttribute(_lib.soil_moisture,           "Soil Moisture",         ('', ''))

    attributes = [attribute_precipitation,
                  attribute_snow_depth,
                  attribute_evaporation,
                  attribute_infiltration,
                  attribute_runoff,
                  attribute_groundwater_flow,
                  attribute_groundwater_elevation,
                  attribute_soil_moisture]

    _count_flag = _lib.subcatchCount
    _get_series = _lib.SMO_getSubcatchSeries
    _get_attribute = _lib.SMO_getSubcatchAttribute
    _get_result = _lib.SMO_getSubcatchResult
    _element_type = _lib.subcatch  # typedef enum {subcatch, node, link, sys} SMO_elementType
    _first_pollutant = _lib.pollutant_conc_subcatch


class SwmmOutputNode(SwmmOutputCategoryBase):
    type_label = "Node"

    attribute_depth          = SwmmOutputAttribute(_lib.invert_depth,         "Depth",          ('ft', 'm'))
    attribute_head           = SwmmOutputAttribute(_lib.hydraulic_head,       "Head",           ('ft', 'm'))
    attribute_volume         = SwmmOutputAttribute(_lib.stored_ponded_volume, "Volume",         ('ft3', 'm3'))
    attribute_lateral_inflow = SwmmOutputAttribute(_lib.lateral_inflow,       "Lateral Inflow", ('CFS', 'CMS'))
    attribute_total_inflow   = SwmmOutputAttribute(_lib.total_inflow,         "Total Inflow",   ('CFS', 'CMS'))
    attribute_flooding       = SwmmOutputAttribute(_lib.flooding_losses,      "Flooding",       ('CFS', 'CMS'))

    attributes = [attribute_depth,
                  attribute_head,
                  attribute_volume,
                  attribute_lateral_inflow,
                  attribute_total_inflow,
                  attribute_flooding]

    _count_flag = _lib.nodeCount
    _get_series = _lib.SMO_getNodeSeries
    _get_attribute = _lib.SMO_getNodeAttribute
    _get_result = _lib.SMO_getNodeResult
    _element_type = _lib.node  # typedef enum {subcatch, node, link, sys} SMO_elementType
    _first_pollutant = _lib.pollutant_conc_node


class SwmmOutputLink(SwmmOutputCategoryBase):
    type_label = "Link"

    attribute_flow          = SwmmOutputAttribute(_lib.flow_rate_link,      "Flow",          ('CFS', 'CMS'))
    attribute_depth         = SwmmOutputAttribute(_lib.flow_depth,          "Depth",         ('ft', 'm'))
    attribute_velocity      = SwmmOutputAttribute(_lib.flow_velocity,       "Velocity",      ('fps', 'm/s'))
    attribute_volume        = SwmmOutputAttribute(_lib.flow_volume,         "Volume",        ('ft3', 'm3'))
    attribute_capacity      = SwmmOutputAttribute(_lib.capacity,            "Capacity",      ('', ''))

    attributes = [attribute_flow,
                  attribute_depth,
                  attribute_velocity,
                  attribute_volume,
                  attribute_capacity]

    _count_flag = _lib.linkCount
    _get_series = _lib.SMO_getLinkSeries
    _get_attribute = _lib.SMO_getLinkAttribute
    _get_result = _lib.SMO_getLinkResult
    _element_type = _lib.link  # typedef enum {subcatch, node, link, sys} SMO_elementType
    _first_pollutant = _lib.pollutant_conc_link


class SwmmOutputSystem(SwmmOutputCategoryBase):
    type_label = "System"

    attribute_temperature        = SwmmOutputAttribute(_lib.air_temp,             "Temperature",    ('deg F', 'deg C'))
    attribute_precipitation      = SwmmOutputAttribute(_lib.rainfall_system,      "Precipitation",  ('in/hr', 'mm/hr'))
    attribute_snow_depth         = SwmmOutputAttribute(_lib.snow_depth_system,    "Snow Depth",     ('in',    'mm'))
    attribute_infiltration       = SwmmOutputAttribute(_lib.evap_infil_loss,      "Infiltration",   ('in/hr', 'mm/hr'))
    attribute_runoff             = SwmmOutputAttribute(_lib.runoff_flow,          "Runoff",             ('CFS', 'CMS'))
    attribute_dry_weather_inflow = SwmmOutputAttribute(_lib.dry_weather_inflow,   "Dry Weather Inflow", ('CFS', 'CMS'))
    attribute_groundwater_inflow = SwmmOutputAttribute(_lib.groundwater_inflow,   "Groundwater Inflow", ('CFS', 'CMS'))
    attribute_rdii_inflow        = SwmmOutputAttribute(_lib.RDII_inflow,          "I&I Inflow",         ('CFS', 'CMS'))
    attribute_direct_inflow      = SwmmOutputAttribute(_lib.direct_inflow,        "Direct Inflow",      ('CFS', 'CMS'))
    attribute_total_inflow       = SwmmOutputAttribute(_lib.total_lateral_inflow, "Total Inflow",       ('CFS', 'CMS'))
    attribute_flooding           = SwmmOutputAttribute(_lib.flood_losses,         "Flooding",           ('CFS', 'CMS'))
    attribute_outflow            = SwmmOutputAttribute(_lib.outfall_flows,        "Outflow",            ('CFS', 'CMS'))
    attribute_storage            = SwmmOutputAttribute(_lib.volume_stored,        "Storage",            ('ft3', 'm3'))
    attribute_evaporation        = SwmmOutputAttribute(_lib.evap_rate,            "Evaporation", ('in/day', 'mm/day'))
    #attribute_pet                = SwmmOutputAttribute(_lib.pet,                  "PET",         ('in/day', 'mm/day'))

    attributes = (attribute_temperature,
                  attribute_precipitation,
                  attribute_snow_depth,
                  attribute_infiltration,
                  attribute_runoff,
                  attribute_dry_weather_inflow,
                  attribute_groundwater_inflow,
                  attribute_rdii_inflow,
                  attribute_direct_inflow,
                  attribute_total_inflow,
                  attribute_flooding,
                  attribute_outflow,
                  attribute_storage,
                  attribute_evaporation)

    _get_series = _lib.SMO_getSystemSeries
    _get_attribute = _lib.SMO_getSystemAttribute
    _get_result = _lib.SMO_getSystemResult
    _element_type = _lib._sys  # 3 typedef enum {subcatch, node, link, sys} SMO_elementType


class SwmmOutputPollutant(SwmmOutputCategoryBase):
    type_label = "Pollutant"
    all_units = ["mg/L", "ug/L", "count/L"]
    _count_flag = _lib.pollutantCount
    _element_type = _lib._sys  # This is recognized when getting names from the API. (There are no names for sys.)


swmm_output_object_types = (SwmmOutputSubcatchment, SwmmOutputNode, SwmmOutputLink, SwmmOutputSystem)
swmm_output_object_labels = [ot.type_label for ot in swmm_output_object_types]


def swmm_output_get_object_type(object_type_name):
    for object_type in swmm_output_object_types:
        if object_type.type_label == object_type_name:
            return object_type

SMO_USFlowUnits = ('CFS', 'GPM', 'MGD')
SMO_SIFlowUnits = ('CMS', 'LPS', 'MLD')
TempUnits = ('deg F', 'deg C')

SMO_UnitsUS = 0
SMO_UnitsSI = 1

cint = c_int()


class SwmmOutputObject(object):
    def __init__(self, output_file_name):
        """ Open the named file and maintain an internal pointer to be used to access contents of the file.
            Read header information from the file including units, times, and lists of nodes, links, subcatchments.
            Args
            output_file_name (str): full path and file name of EPANET binary output file to open
        """
        self._call_int_return = c_int()  # Private variable used only inside call_int
        self._call_double_return = c_double()  # Private variable used only inside call_double
        self.output_file_name = str(output_file_name)

        self.ptrapi = _lib.SMO_init()
        for attempt in [1, 2, 3, 4, 5]:  # wait to finish closing the file in case it just finished running the model

            ret = _lib.SMO_open(self.ptrapi, self.output_file_name)
            if ret == 0:
                break
            print("Error " + str(ret) + " opening " + self.output_file_name + " retrying...")
            time.sleep(1)
        if ret != 0:
            self._raise_error(ret)

        # self._measure_new_out_value_series()
        self._get_units()
        self._get_sizes()
        self._get_times()

        self.pollutants = SwmmOutputPollutant.read_all(self)
        for pollutant in self.pollutants.values():
            pollutant.units = SwmmOutputPollutant.all_units[
                self._call_int(_lib.SMO_getPollutantUnits, pollutant._index)]

        # Read all the model elements into dictionaries (also add pollutants to attributes)
        self.subcatchments = SwmmOutputSubcatchment.read_all(self)
        self.nodes = SwmmOutputNode.read_all(self)
        self.links = SwmmOutputLink.read_all(self)
        self.nodes_units = {}
        self.links_units = {}
        self.subcatchments_units = {}
        self.system = {'-1': SwmmOutputSystem('-1', -1)}
        self.all_items = (self.subcatchments, self.nodes, self.links, self.system)

    def build_units_dictionary(self):
       # output attributes
        for l_id in self.links.keys():
            for attr in self.links[l_id].attributes:
                self.links_units[attr.name] = attr._units[self.unit_system]
            break
       # output attributes
        for n_id in self.nodes.keys():
            for attr in self.nodes[n_id].attributes:
                self.nodes_units[attr.name] = attr._units[self.unit_system]
            break
        # sub attributes
        for s_id in self.subcatchments.keys():
            for attr in self.subcatchments[s_id].attributes:
                self.subcatchments_units[attr.name] = attr._units[self.unit_system]

    def _call(self, function, *args):
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
        self._call(function, *args_to_pass)                 # self.call(function, *args, byref(self._call_int_return))
        return self._call_int_return.value

    def _call_double(self, function, *args):
        """ Call an API method whose return value is an integer indicating an error if != 0
            and which also returns a double in the last argument (using byref).
            call_double handles the return value error flag by calling RaiseError if needed.
            Do not include the last argument (the return argument) in *args, it will be added internally
            The double value returned is the return value of call_double."""
        args_to_pass = list(args)
        args_to_pass.append(byref(self._call_double_return))  # When moving to Python 3.5+, can skip appending and use:
        self._call(function, *args_to_pass)                   # self.call(function, *args, byref(self._call_int_return))
        return self._call_double_return.value

    def _raise_error(self, ErrNo):
        # if _RetErrMessage(ErrNo , errmsg, err_max_char)==0:
        #     raise Exception(errmsg.value)
        # else:
        raise Exception("SWMM output error #{0}".format(ErrNo))

    # def _measure_new_out_value_series(self):
    #     """Test SMO_newOutValueSeries to see whether it treats the requested length as length or end.
    #         Sets self.newOutValueSeriesLengthIsEnd flag so we can adjust how we call this method."""
    #     returned_length = c_int()
    #     error_new = c_int()
    #     series_pointer = _lib.SMO_newOutValueSeries(self.ptrapi, 1, 2, byref(returned_length), byref(error_new))
    #     if error_new.value != 0:
    #         print("Error allocating series start to test ENR_newOutValueSeries: " + str(error_new.value))
    #         self._raise_error(error_new.value)
    #     self.newOutValueSeriesLengthIsEnd = (returned_length.value == 1)
    #     _lib.SMO_free(series_pointer)

    def _get_units(self):
        """
        Purpose: Reads flow unit index into self.flowUnits, sets self.unit_system and self.flowUnitsLabel
        """
        self.flowUnits = self._call_int(_lib.SMO_getUnits, _lib.flow_rate)
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
        self.nodeCount = self._call_int(_lib.SMO_getProjectSize, _lib.nodeCount)
        self.subcatchCount = self._call_int(_lib.SMO_getProjectSize, _lib.subcatchCount)
        self.linkCount = self._call_int(_lib.SMO_getProjectSize, _lib.linkCount)
        self.pollutantCount = self._call_int(_lib.SMO_getProjectSize, _lib.pollutantCount)

    def _get_times(self):
        """
        Purpose: Retrieve report and simulation time-related parameters and stores them in self.
        """
        RawReportStart = self._call_double(_lib.SMO_getStartTime)  # decimal (Julian) days since 12 AM on 12/30/1899
        self.StartDate = datetime.datetime(1899, 12, 30) + datetime.timedelta(RawReportStart)
        self.reportStep = self._call_int(_lib.SMO_getTimes, _lib.reportStep)
        self.num_periods = self._call_int(_lib.SMO_getTimes, _lib.numPeriods)
        self.simDuration = self.reportStep * self.num_periods
        self.EndDate = self.StartDate + datetime.timedelta(seconds=self.simDuration)
        # self.all_dates = pandas.date_range(start=self.StartDate, end=self.EndDate, periods=self.num_periods)

        # _lib.SMO_getTimes(self.ptrapi, _lib.SMO_simDuration, byref(cint))
        # self.simDuration = cint.value

    def get_items(self, object_type_label):
        """ Get the dictionary of items of the type whose type_label attribute is object_type_label.

            Args:
            object_type_label: can be "Subcatchment", "Node" or "Link". (System has no items.)

            Examples:
                for name, node in get_items("Node"):
                    print(name, str(node.get_series(output, SwmmOutputNode.attribute_depth, 0, 2)[1]))
        """
        for items in self.all_items:
            if items:
                # Check the first item to make sure its type label matches
                for item in items.values():
                    if item.type_label == object_type_label:
                        return items
                    else:  # these are not the items we want, skip to next items
                        break
        return {}

    def close(self):
        """
        Close the binary file.
        """
        self._call(_lib.SMO_close)

    def elapsed_hours_at_index(self, report_time_index):
        return (report_time_index * self.reportStep) / 3600.0

    def get_time(self, report_time_index):
        elapsed_hours = self.elapsed_hours_at_index(report_time_index)
        return self.StartDate + datetime.timedelta(hours=elapsed_hours)

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

    def get_time_series(self, type_label, object_id, attribute_name):
        #ToDo: need to debug get_series about not reading the first zero entry
        try:
            import pandas
            item = None
            if "SYSTEM" in type_label.upper():
                item = self.system.items()[0][1] # SwmmOutputSystem
            else:
                item = self.get_items(type_label)[object_id]  # SwmmOutputSubcatchment, Link, Node

            attribute = item.get_attribute_by_name(attribute_name)  # SwmmOutputAttribute
            y_values = item.get_series(self, attribute, 0, self.num_periods)

            #hack #1:
            y_values.insert(0, 0.0) #all rains Tser starts with zero
            x_values = []
            #hack #2, +1 is to end in the ending moment of a time step
            for time_index in range(0, self.num_periods + 1):
                elapsed_hours = self.elapsed_hours_at_index(time_index)
                # if elapsed_flag:
                #    x_values.append(elapsed_hours)
                # else:
                x_values.append(self.StartDate + datetime.timedelta(hours=elapsed_hours))
            # now make a time series data frame
            return pandas.Series(y_values, index=x_values)
        except Exception as ex:
            print str(ex)

    def get_item_unit(self, type_label, object_id, attribute_name):
        if "SYSTEM" in type_label.upper():
            item = self.system.items()[0][1]
        else:
            item = self.get_items(type_label)[object_id]  # SwmmOutputSubcatchment
        attribute = item.get_attribute_by_name(attribute_name)  # SwmmOutputAttribute

        lisPollutant = False
        for pname in self.pollutants:
            if pname.upper() == attribute_name.upper():
                lisPollutant = True
                break
        if lisPollutant:
            return self.pollutants[attribute_name].units
        else:
            return attribute.units(self.unit_system)

        # if attribute.index < len(item.attributes) - 1:
        #     return attribute.units(self.unit_system)
        # else:
        #     return self.pollutants[attribute_name].units
        #     pass

    def reportStepDays(self):
        return self.reportStep / 86400.0;
