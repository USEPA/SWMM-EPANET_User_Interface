/*
 *  swmm_output.i - SWIG interface description file for SWMM Output API
 *
 *  Created:    11/3/2017
 *  Author:     Michael E. Tryby
 *              US EPA - ORD/NRMRL
 *
*/

%module(package="swmm") output
%{
#include "swmm_output.h"

#define SWIG_FILE_WITH_INIT
%}

%include "typemaps.i"

/* DEFINE AND TYPEDEF MUST BE INCLUDED */
typedef void* SMO_Handle;


%include "swmm_output_enums.h"


/* TYPEMAPS FOR VOID POINTER */
/* Used for functions that output a new opaque pointer */
%typemap(in, numinputs=0) SMO_Handle* p_handle_out (void* retval)
{
 /* OUTPUT in */
    retval = NULL;
    $1 = &retval;
}
/* used for functions that take in an opaque pointer (or NULL)
and return a (possibly) different pointer */
%typemap(argout) SMO_Handle* p_handle_out
{
 /* OUTPUT argout */
    %append_output(SWIG_NewPointerObj(SWIG_as_voidptr(retval$argnum), $1_descriptor, 0));
}
%typemap(in) SMO_Handle* p_handle_inout (SMO_Handle retval)
{
   /* INOUT in */
   SWIG_ConvertPtr(obj0,SWIG_as_voidptrptr(&retval), 0, 0);
    $1 = &retval;
}
/* No need for special IN typemap for opaque pointers, it works anyway */


/* TYPEMAP FOR IGNORING INT ERROR CODE RETURN VALUE */
%typemap(out) int {
    $result = Py_None;
    Py_INCREF($result);
}


/* TYPEMAPS FOR DOUBLE ARGUMENT AS RETURN VALUE */
%typemap(in, numinputs=0) double* double_out (double temp) {
    $1 = &temp;
}
%typemap(argout) double* double_out {
    %append_output(PyFloat_FromDouble(*$1));
}


/* TYPEMAPS FOR INT ARGUMENT AS RETURN VALUE */
%typemap(in, numinputs=0) int* int_out (int temp) {
    $1 = &temp;
}
%typemap(argout) int* int_out {
    %append_output(PyInt_FromLong(*$1));
}


/* TYPEMAP FOR MEMORY MANAGEMENT AND ENCODING OF STRINGS */
%typemap(in, numinputs=0)char** string_out (char* temp), int* slen (int temp){
   $1 = &temp;
}
%typemap(argout)(char** string_out, int* slen) {
    if (*$1) {
        PyObject* o;
        o = PyUnicode_FromStringAndSize(*$1, *$2);

        $result = SWIG_Python_AppendOutput($result, o);
        free(*$1);
    }
}

/* TYPEMAPS FOR MEMORY MANAGEMNET OF FLOAT ARRAYS */
%typemap(in, numinputs=0)float** float_out (float* temp), int* int_dim (int temp){
   $1 = &temp;
}
%typemap(argout) (float** float_out, int* int_dim) {
    if (*$1) {
      PyObject *o = PyList_New(*$2);
      int i;
      float* temp = *$1;
      for(i=0; i<*$2; i++) {
        PyList_SetItem(o, i, PyFloat_FromDouble((double)temp[i]));
      }
      $result = SWIG_Python_AppendOutput($result, o);
      free(*$1);
    }
}


/* TYPEMAPS FOR MEMORY MANAGEMNET OF INT ARRAYS */
%typemap(in, numinputs=0)int** int_out (long* temp), int* int_dim (int temp){
   $1 = &temp;
}
%typemap(argout) (int** int_out, int* int_dim) {
    if (*$1) {
      PyObject *o = PyList_New(*$2);
      int i;
      long* temp = (long*)*$1;
      for(i=0; i<*$2; i++) {
        PyList_SetItem(o, i, PyInt_FromLong(temp[i]));
      }
      $result = SWIG_Python_AppendOutput($result, o);
      free(*$1);
    }
}


/* TYPEMAP FOR ENUMERATED TYPES */
%typemap(in) EnumeratedType (int val, int ecode = 0) {
    if (PyObject_HasAttrString($input,"value")) {
        PyObject* o;
        o = PyObject_GetAttrString($input, "value");
        ecode = SWIG_AsVal_int(o, &val);
    }
    else {
        SWIG_exception_fail(SWIG_ArgError(ecode), "in method '" "$symname" "', argument " "$argnum"" of type '" "$ltype""'");
    }

    $1 = ($1_type)(val);
}
%apply EnumeratedType {SMO_unit, SMO_elementType, SMO_time, SMO_subcatchAttribute,
SMO_nodeAttribute, SMO_linkAttribute, SMO_systemAttribute};


/* RENAME FUNCTIONS PYTHON STYLE */
%rename("%(regex:/^\w+_([a-zA-Z]+)/\L\\1/)s") "";

/* GENERATES DOCUMENTATION */
%feature("autodoc", "2");


/* INSERTS CUSTOM EXCEPTION HANDLING IN WRAPPER */
%exception
{
    char* err_msg;
    SMO_clearError(arg1);
    $function
    if (SMO_checkError(arg1, &err_msg))
    {
        PyErr_SetString(PyExc_Exception, err_msg);
        SWIG_fail;
    }
}

/* INSERT EXCEPTION HANDLING FOR THESE FUNCTIONS */

int SMO_open(SMO_Handle p_handle, const char* path);

int SMO_getVersion(SMO_Handle p_handle, int* int_out);
int SMO_getProjectSize(SMO_Handle p_handle, int** int_out, int* int_dim);
int SMO_getUnits(SMO_Handle p_handle, int** int_out, int* int_dim);
//int SMO_getFlowUnits(SMO_Handle p_handle, int* int_out);
//int SMO_getPollutantUnits(SMO_Handle p_handle, int** int_out, int* int_dim);
int SMO_getStartDate(SMO_Handle p_handle, double* double_out);
int SMO_getTimes(SMO_Handle p_handle, SMO_time code, int* int_out);
int SMO_getElementName(SMO_Handle p_handle, SMO_elementType type,
    int elementIndex, char** string_out, int* slen);

int SMO_getSubcatchSeries(SMO_Handle p_handle, int subcatchIndex,
    SMO_subcatchAttribute attr, int startPeriod, int endPeriod, float** float_out, int* int_dim);
int SMO_getNodeSeries(SMO_Handle p_handle, int nodeIndex, SMO_nodeAttribute attr,
    int startPeriod, int endPeriod, float** float_out, int* int_dim);
int SMO_getLinkSeries(SMO_Handle p_handle, int linkIndex, SMO_linkAttribute attr,
    int startPeriod, int endPeriod, float** float_out, int* int_dim);
int SMO_getSystemSeries(SMO_Handle p_handle, SMO_systemAttribute attr,
    int startPeriod, int endPeriod, float** float_out, int* int_dim);

int SMO_getSubcatchAttribute(SMO_Handle p_handle, int timeIndex,
    SMO_subcatchAttribute attr, float** float_out, int* int_dim);
int SMO_getNodeAttribute(SMO_Handle p_handle, int timeIndex,
    SMO_nodeAttribute attr, float** float_out, int* int_dim);
int SMO_getLinkAttribute(SMO_Handle p_handle, int timeIndex,
    SMO_linkAttribute attr, float** float_out, int* int_dim);
int SMO_getSystemAttribute(SMO_Handle p_handle, int timeIndex,
    SMO_systemAttribute attr, float** float_out, int* int_dim);

int SMO_getSubcatchResult(SMO_Handle p_handle, int timeIndex,
    int subcatchIndex, float** float_out, int* int_dim);
int SMO_getNodeResult(SMO_Handle p_handle, int timeIndex,
    int nodeIndex, float** float_out, int* int_dim);
int SMO_getLinkResult(SMO_Handle p_handle, int timeIndex,
    int linkIndex, float** float_out, int* int_dim);
int SMO_getSystemResult(SMO_Handle p_handle, int timeIndex,
    int dummyIndex, float** float_out, int* int_dim);

%exception;

/* NO EXCEPTION HANDLING FOR THESE FUNCTIONS */
int SMO_init(SMO_Handle* p_handle_out);
int SMO_close(SMO_Handle* p_handle_inout);
void SMO_free(void** array);

void SMO_clearError(SMO_Handle p_handle);
int SMO_checkError(SMO_Handle p_handle, char** msg_buffer);


/* CODE ADDED DIRECTLY TO SWIGGED INTERFACE MODULE */
%pythoncode%{
import enum

import aenum

class UnitSystem(enum.Enum):
    US = SMO_US
    SI = SMO_SI

class FlowUnits(enum.Enum):
    CFS = SMO_CFS
    GPM = SMO_GPM
    MGD = SMO_MGD
    CMS = SMO_CMS
    LPS = SMO_LPS
    MLD = SMO_MLD

class ConcUnits(enum.Enum):
    MG = SMO_MG
    UG = SMO_UG
    COUNT = SMO_COUNT
    NONE = SMO_NONE

class ElementType(enum.IntEnum):
    SUBCATCH = SMO_subcatch
    NODE = SMO_node
    LINK = SMO_link
    POLLUT = SMO_pollut
    SYSTEM = SMO_sys

class Time(enum.Enum):
    REPORT_STEP = SMO_reportStep
    NUM_PERIODS = SMO_numPeriods

class SubcatchAttribute(aenum.Enum):
    RAINFALL = SMO_rainfall_subcatch
    SNOW_DEPTH = SMO_snow_depth_subcatch
    EVAP_LOSS = SMO_evap_loss
    INFIL_LOSS = SMO_infil_loss
    RUNOFF_RATE = SMO_runoff_rate
    GW_OUTFLOW_RATE = SMO_gwoutflow_rate
    GW_TABLE_ELEV = SMO_gwtable_elev
    SOIL_MOISTURE = SMO_soil_moisture
    POLLUT_CONC_0 = SMO_pollutant_conc_subcatch

class NodeAttribute(aenum.Enum):
    INVERT_DEPTH = SMO_invert_depth
    HYDRAULIC_HEAD = SMO_hydraulic_head
    PONDED_VOLUME = SMO_stored_ponded_volume
    LATERAL_INFLOW = SMO_lateral_inflow
    TOTAL_INFLOW = SMO_total_inflow
    FLOODING_LOSSES = SMO_flooding_losses
    POLLUT_CONC_0 = SMO_pollutant_conc_node

class LinkAttribute(aenum.Enum):
    FLOW_RATE = SMO_flow_rate_link
    FLOW_DEPTH = SMO_flow_depth
    FLOW_VELOCITY = SMO_flow_velocity
    FLOW_VOLUME = SMO_flow_volume
    CAPACITY = SMO_capacity
    POLLUT_CONC_0 = SMO_pollutant_conc_link

class SystemAttribute(enum.Enum):
    AIR_TEMP = SMO_air_temp
    RAINFALL = SMO_rainfall_system
    SNOW_DEPTH = SMO_snow_depth_system
    EVAP_INFIL_LOSS = SMO_evap_infil_loss
    RUNOFF_FLOW = SMO_runoff_flow
    DRY_WEATHER_INFLOW = SMO_dry_weather_inflow
    GW_INFLOW = SMO_groundwater_inflow
    RDII_INFLOW = SMO_RDII_inflow
    DIRECT_INFLOW = SMO_direct_inflow
    TOTAL_LATERAL_INFLOW = SMO_total_lateral_inflow
    FLOOD_LOSSES = SMO_flood_losses
    OUTFALL_FLOWS = SMO_outfall_flows
    VOLUME_STORED = SMO_volume_stored
    EVAP_RATE = SMO_evap_rate

%}
