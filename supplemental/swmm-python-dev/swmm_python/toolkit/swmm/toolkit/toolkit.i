/*
 *  toolkit.i - SWIG interface description file for SWMM toolkit
 * 
 *  Created:    7/2/2018
 *  Author:     Michael E. Tryby
 *              US EPA - ORD/NRMRL
 *  
 *  Build command: 
 *    $ python setup.py build
 *
*/ 

%module(package="swmm") toolkit
%{
#include "swmm5.h"
#include "toolkitAPI.h"

#define SWIG_FILE_WITH_INIT
%}

%include "typemaps.i"

/* DEFINE AND TYPEDEF MUST BE INCLUDED */
typedef void* SWMM_ProjectHandle;


#ifdef WINDOWS
  #ifdef __cplusplus
  #define DLLEXPORT __declspec(dllexport) __cdecl
  #else
  #define DLLEXPORT __declspec(dllexport) __stdcall
  #endif
#else
  #define DLLEXPORT
#endif


/* TYPEMAPS FOR OPAQUE POINTER */
/* Used for functions that output a new opaque pointer */
%typemap(in, numinputs=0) SWMM_ProjectHandle* ph_out (SWMM_ProjectHandle retval)
{
 /* OUTPUT in */
    retval = NULL;
    $1 = &retval;
}
/* used for functions that take in an opaque pointer (or NULL)
and return a (possibly) different pointer */
%typemap(argout) SWMM_ProjectHandle* ph_out, SWMM_ProjectHandle* ph_inout 
{
 /* OUTPUT argout */
    %append_output(SWIG_NewPointerObj(SWIG_as_voidptr(retval$argnum), $1_descriptor, 0));
} 
%typemap(in) SWMM_ProjectHandle* ph_inout (SWMM_ProjectHandle retval)
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


/* GENERATES DOCUMENTATION */
%feature("autodoc", "2");


/* CUSTOM RENAME FOR THESE FUNCTIONS */
%rename(alloc_project) swmm_alloc_project;
int  DLLEXPORT  swmm_alloc_project(SWMM_ProjectHandle *ph_out);

%rename(free_project) swmm_free_project;
int  DLLEXPORT  swmm_free_project(SWMM_ProjectHandle *ph_inout);


/* RENAME REMAINING FUNCTIONS PYTHON STYLE */
%rename("%(regex:/^\w+_([a-zA-Z]+)_\w+$/\L\\1/)s") "";


/* INSERTS CUSTOM EXCEPTION HANDLING IN WRAPPER */
%exception
{
    char* err_msg;
    swmm_clearError_project(arg1);
    $function
    if (swmm_checkError_project(arg1, &err_msg))
    {
        PyErr_SetString(PyExc_Exception, err_msg);
        free(err_msg);
        SWIG_fail;
    }
}

// CANONICAL API
int  DLLEXPORT  swmm_run_project(SWMM_ProjectHandle ph, const char* f1, const char* f2, const char* f3);
int  DLLEXPORT  swmm_open_project(SWMM_ProjectHandle ph, const char* f1, const char* f2, const char* f3);
int  DLLEXPORT  swmm_start_project(SWMM_ProjectHandle ph, int saveFlag);
int  DLLEXPORT  swmm_step_project(SWMM_ProjectHandle ph, double* double_out);
int  DLLEXPORT  swmm_end_project(SWMM_ProjectHandle ph);
int  DLLEXPORT  swmm_report_project(SWMM_ProjectHandle ph);
int  DLLEXPORT  swmm_getMassBalErr_project(SWMM_ProjectHandle ph, float* runoffErr, float* flowErr, float* qualErr);
int  DLLEXPORT  swmm_close_project(SWMM_ProjectHandle ph);

/* DEPRECATING OLD ERROR HANDLING INTERFACE */
//int  DLLEXPORT  swmm_getError_project(SWMM_ProjectHandle ph, char* errMsg, int msgLen);
//int  DLLEXPORT  swmm_getWarnings_project(SWMM_ProjectHandle ph);

//// NEW TOOLKIT API
//int  DLLEXPORT  swmm_getSimulationUnit_project(SWMM_ProjectHandle ph, int type, int *value);
//int  DLLEXPORT  swmm_getSimulationAnalysisSetting_project(SWMM_ProjectHandle ph, int type, int *value);
//int  DLLEXPORT  swmm_getSimulationParam_project(SWMM_ProjectHandle ph, int type, double *value);
//int  DLLEXPORT  swmm_countObjects_project(SWMM_ProjectHandle ph, int type, int *count);
//int  DLLEXPORT  swmm_getObjectId_project(SWMM_ProjectHandle ph, int type, int index, char *id);
//int  DLLEXPORT  swmm_getNodeType_project(SWMM_ProjectHandle ph, int index, int *Ntype);
//int  DLLEXPORT  swmm_getLinkType_project(SWMM_ProjectHandle ph, int index, int *Ltype);
//int  DLLEXPORT  swmm_getLinkConnections_project(SWMM_ProjectHandle ph, int index, int *Node1, int *Node2);
//int  DLLEXPORT  swmm_getLinkDirection_project(SWMM_ProjectHandle ph, int index, signed char *value);
//int  DLLEXPORT  swmm_getSubcatchOutConnection_project(SWMM_ProjectHandle ph, int index, int *type, int *ObjIndex );
//int  DLLEXPORT  swmm_getNodeParam_project(SWMM_ProjectHandle ph, int index, int Param, double *value);
//int  DLLEXPORT  swmm_setNodeParam_project(SWMM_ProjectHandle ph, int index, int Param, double value);
//int  DLLEXPORT  swmm_getLinkParam_project(SWMM_ProjectHandle ph, int index, int Param, double *value);
//int  DLLEXPORT  swmm_setLinkParam_project(SWMM_ProjectHandle ph, int index, int Param, double value);
//int  DLLEXPORT  swmm_getSubcatchParam_project(SWMM_ProjectHandle ph, int index, int Param, double *value);
//int  DLLEXPORT  swmm_setSubcatchParam_project(SWMM_ProjectHandle ph, int index, int Param, double value);
//int  DLLEXPORT  swmm_getSimulationDateTime_project(SWMM_ProjectHandle ph, int timetype, int *year, int *month, int *day, int *hours, int *minutes, int *seconds);
//int  DLLEXPORT  swmm_setSimulationDateTime_project(SWMM_ProjectHandle ph, int timetype, char *dtimestr);

//// Active Simulation Results API
//int  DLLEXPORT  swmm_getCurrentDateTimeStr_project(SWMM_ProjectHandle ph, char *dtimestr);
//int  DLLEXPORT  swmm_getNodeResult_project(SWMM_ProjectHandle ph, int index, int type, double *result);
//int  DLLEXPORT  swmm_getLinkResult_project(SWMM_ProjectHandle ph, int index, int type, double *result);
//int  DLLEXPORT  swmm_getSubcatchResult_project(SWMM_ProjectHandle ph, int index, int type, double *result);
//int  DLLEXPORT  swmm_getNodeStats_project(SWMM_ProjectHandle ph, int index, SM_NodeStats *nodeStats);
//int  DLLEXPORT  swmm_getNodeTotalInflow_project(SWMM_ProjectHandle ph, int index, double *value);
//int  DLLEXPORT  swmm_getStorageStats_project(SWMM_ProjectHandle ph, int index, SM_StorageStats *storageStats);\
//int  DLLEXPORT  swmm_getOutfallStats_project(SWMM_ProjectHandle ph, int index, SM_OutfallStats *outfallStats);
////void DLLEXPORT swmm_freeOutfallStats(SM_OutfallStats *outfallStats);
//int  DLLEXPORT  swmm_getLinkStats_project(SWMM_ProjectHandle ph, int index, SM_LinkStats *linkStats);
//int  DLLEXPORT  swmm_getPumpStats_project(SWMM_ProjectHandle ph, int index, SM_PumpStats *pumpStats);
//int  DLLEXPORT  swmm_getGagePrecip_project(SWMM_ProjectHandle ph, int index, double *rainfall, double *snowfall, double *total);
//int  DLLEXPORT  swmm_getSubcatchStats_project(SWMM_ProjectHandle ph, int index, SM_SubcatchStats *subcatchStats);
////void DLLEXPORT swmm_freeSubcatchStats(SM_SubcatchStats *subcatchStats);
//int  DLLEXPORT  swmm_getSystemRoutingStats_project(SWMM_ProjectHandle ph, SM_RoutingTotals *routingTot);
//int  DLLEXPORT  swmm_getSystemRunoffStats_project(SWMM_ProjectHandle ph, SM_RunoffTotals *runoffTot);

//// Setters API
//int  DLLEXPORT  swmm_setLinkSetting_project(SWMM_ProjectHandle ph, int index, double setting);
//int  DLLEXPORT  swmm_setNodeInflow_project(SWMM_ProjectHandle ph, int index, double flowrate);
//int  DLLEXPORT  swmm_setOutfallStage_project(SWMM_ProjectHandle ph, int index, double stage);
//int  DLLEXPORT  swmm_setGagePrecip_project(SWMM_ProjectHandle ph, int index, double value);

%exception;

/* NO EXCEPTION HANDLING FOR THESE FUNCTIONS */
void DLLEXPORT  swmm_clearError_project(SWMM_ProjectHandle ph);
int  DLLEXPORT  swmm_checkError_project(SWMM_ProjectHandle ph, char** msg_buffer);
