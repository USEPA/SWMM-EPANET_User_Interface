"""

Wrapper for EPANET Output API.

Author: Bryant E. McDonnell
Date: 12/7/2015
Language: Anglais

Edited for inclusion in SWMM-EPANET User Interface project
26 April 2016
Mark Gray, RESPEC
for US EPA

"""

from ctypes import *

import Externals.epanet.output.outputapi as _lib

"""
#---- imported constants made available as local (not a good practice....)
##ENR_ElementType;
from outputapi import ENR_node, ENR_link

##ENR_ApiFunction;
from outputapi import ENR_getSeries,ENR_getAttribute,ENR_getResult

##ENR_ElementCount;
from outputapi import ENR_nodeCount,ENR_tankCount,ENR_linkCount,ENR_pumpCount,ENR_valveCount

##ENR_Unit;
from outputapi import ENR_flowUnits,ENR_pressUnits

##ENR_Time;
from outputapi import ENR_reportStart,ENR_reportStep,ENR_simDuration,ENR_numPeriods
"""
##ENR_NodeAttribute;
from Externals.epanet.output.outputapi import ENR_demand, ENR_head, ENR_pressure, ENR_quality
ENR_NodeAttributes= (ENR_demand,
                     ENR_head,
                     ENR_pressure,
                     ENR_quality)
ENR_NodeAttributeNames = ("Demand",
                          "Head",
                          "Pressure",
                          "Quality")
ENR_NodeAttributeUnits = (('CFS', 'LPS'), ('ft', 'm'), ('psi', 'm'), ('mg/L', 'mg/L'))
ENR_USFlowUnits = ('CFS', 'GPM', 'MGD', 'IMGD', 'AFD')
ENR_SIFlowUnits = ('LPS', 'LPM', 'MLD', 'CMH', 'CMD')
##ENR_LinkAttribute;
from Externals.epanet.output.outputapi import ENR_flow,ENR_velocity,ENR_headloss,ENR_avgQuality
from Externals.epanet.output.outputapi import ENR_status,ENR_setting,ENR_rxRate,ENR_frctnFctr
ENR_LinkAttributes= (ENR_flow,
                     ENR_velocity,
                     ENR_headloss,
                     ENR_avgQuality,
                     ENR_status,
                     ENR_setting,
                     ENR_rxRate,
                     ENR_frctnFctr)
ENR_LinkAttributeNames = ('Flow',
                          'Velocity',
                          'Unit Headloss',
                          'Quality',
                          'Status',
                          'Setting',
                          'Reaction Rate',
                          'Friction Factor')
ENR_LinkAttributeUnits = (('CFS', 'LPS'), ('fps', 'm/s'), ('ft/Kft', 'm/km'), ('mg/L', 'mg/L'),
                          ('', ''),('', ''), ('mg/L/d', 'mg/L/d'), ('', ''))
ENR_UnitsUS = 0
ENR_UnitsSI = 1
#---------------------------------------------------------------------------------------------


label  = _lib.String( (_lib.MAXID+1)*'\0')
errmsg = _lib.String( (_lib.MAXMSG+1)*'\0')
cint = c_int()

class OutputObject(object):

    def __init__(self, binfile):
        """
        1) Initializes the opaque pointer to enrapi struct.
        2) Opens the output file.
        """
        self.enrapi = c_void_p()
        ret = _lib.ENR_open(byref(self.enrapi), binfile)
        if ret != 0:
            self.RaiseError(ret)
        self._get_Units()
        self._get_NetSize()
        self._get_Times()

    def RaiseError(self, ErrNo):
        # if _RetErrMessage(ErrNo , errmsg, err_max_char)==0:
        #     raise Exception(errmsg.value)
        # else:
        raise Exception("Unknown error #{0}".format(ErrNo) )

    def _get_Units(self):
        """
        Purpose: Returns pressure and flow units
        """
        _lib.ENR_getUnits(self.enrapi, _lib.ENR_flowUnits, byref(cint))
        self.flowUnits = cint.value

        _lib.ENR_getUnits(self.enrapi, _lib.ENR_pressUnits, byref(cint))
        self.pressUnits = cint.value
        
    def _get_NetSize(self):
        """
        Populates object attributes with the water object counts
        """
        _lib.ENR_getNetSize(self.enrapi, _lib.ENR_nodeCount, byref(cint))
        self.nodeCount = cint.value

        _lib.ENR_getNetSize(self.enrapi, _lib.ENR_tankCount, byref(cint))
        self.tankCount = cint.value

        _lib.ENR_getNetSize(self.enrapi, _lib.ENR_linkCount, byref(cint))
        self.linkCount = cint.value

        _lib.ENR_getNetSize(self.enrapi, _lib.ENR_pumpCount, byref(cint))
        self.pumpCount = cint.value

        _lib.ENR_getNetSize(self.enrapi, _lib.ENR_valveCount, byref(cint))
        self.valveCount = cint.value

    def _get_Times(self):
        """
        Purpose: Returns report and simulation time related parameters.
        """
        
        _lib.ENR_getTimes(self.enrapi, _lib.ENR_reportStart, byref(cint))
        self.reportStart = cint.value

        _lib.ENR_getTimes(self.enrapi, _lib.ENR_reportStep, byref(cint))
        self.reportStep = cint.value
        
        _lib.ENR_getTimes(self.enrapi, _lib.ENR_simDuration, byref(cint))
        self.simDuration = cint.value

        _lib.ENR_getTimes(self.enrapi, _lib.ENR_numPeriods, byref(cint))
        self.numPeriods = cint.value

    def get_NodeID(self, index):
         """Retrieves the ID label of a node with a specified index.
       
         Arguments:
         index: node index"""
         _lib.ENR_getNodeID(self.enrapi, index, label)
         return str(label)

    def get_NodeIndex(self, NodeID):
        for index in range(0, self.nodeCount - 1):
            if self.get_NodeID(index) == NodeID:
                return index
        return -1

    def get_LinkID(self, index):
         """Retrieves the ID label of a link with a specified index.
       
         Arguments:
         index: link index"""
         _lib.ENR_getLinkID(self.enrapi, index, label)
         return str(label)

    def get_NodeValue(self, NodeInd, TimeInd,  NodeAttr):
        """
        Purpose: Get results for particular node, time, attribute.
        """
        xval= c_float()
        ierr= _lib.ENR_getNodeValue(self.enrapi, TimeInd, NodeInd, NodeAttr, byref(xval) )
        if ierr == 0:
            return xval.value
        else:
            self.RaiseError(ierr)
           
    def get_LinkValue(self, NodeInd, TimeInd,  NodeAttr):
        """
        Purpose: Get results for particular link, time, attribute.
        """
        xval= c_float()
        ierr= _lib.ENR_getLinkValue(self.enrapi, TimeInd, NodeInd, NodeAttr, byref(xval) )
        if ierr == 0:
            return xval.value
        else:
            self.RaiseError(ierr)




    def get_NodeSeries(self, NodeInd, NodeAttr, SeriesStartInd = 0, SeriesLen = -1):
        """
        Purpose: Get time series results for particular attribute. Specify series
        start and length using seriesStart and seriesLength respectively.

        SeriesLen = -1 Default input: Gets data from Series Start Ind to end
        
        """
        if SeriesLen > self.numPeriods :
            raise Exception("Outside Number of TimeSteps")
        elif SeriesLen == -1:
            SeriesLen = self.numPeriods
            
        sLength = c_int()
        ErrNo1 = c_int()            
        SeriesPtr =  _lib.ENR_newOutValueSeries(self.enrapi, SeriesStartInd,
                                                SeriesLen, byref(sLength), byref(ErrNo1))
        ErrNo2 = _lib.ENR_getNodeSeries(self.enrapi, 
                                        NodeInd,
                                        NodeAttr,
                                        SeriesStartInd,
                                        sLength.value,
                                        SeriesPtr)

        BldArray = [SeriesPtr[i] for i in range(sLength.value)]
        _lib.ENR_free(SeriesPtr)
        return BldArray

    def get_LinkSeries(self, LinkInd, LinkAttr, SeriesStartInd = 0, SeriesLen = -1):
        """
        Purpose: Get time series results for particular attribute. Specify series
        start and length using seriesStart and seriesLength respectively.

        SeriesLen = -1 Default input: Gets data from Series Start Ind to end
        
        """
        if SeriesLen > self.numPeriods :
            raise Exception("Outside Number of TimeSteps")
        elif SeriesLen == -1:
            SeriesLen = self.numPeriods
            
        sLength = c_int()
        ErrNo1 = c_int()            
        SeriesPtr =  _lib.ENR_newOutValueSeries(self.enrapi, SeriesStartInd,
                                                SeriesLen, byref(sLength), byref(ErrNo1))
        ErrNo2 = _lib.ENR_getLinkSeries(self.enrapi, LinkInd, LinkAttr,
                                        SeriesStartInd, sLength.value, SeriesPtr)
        BldArray = [SeriesPtr[i] for i in range(sLength.value)]
        ret = _lib.ENR_free(SeriesPtr)

        return BldArray


    def get_NodeAttribute(self, NodeAttr, TimeInd):
        """
        Purpose: For all nodes at given time, get a particular attribute
        """
        alength = c_int()
        ErrNo1 = c_int()
        ValArrayPtr = _lib.ENR_newOutValueArray(self.enrapi, _lib.ENR_getAttribute,
                                                _lib.ENR_node, byref(alength), byref(ErrNo1))
        ErrNo2 = _lib.ENR_getNodeAttribute(self.enrapi, TimeInd, NodeAttr, ValArrayPtr)
        BldArray = [ValArrayPtr[i] for i in range(alength.value)]
        _lib.ENR_free(ValArrayPtr)
        return BldArray

    def get_LinkAttribute(self, LinkAttr, TimeInd):
        """
        Purpose: For all links at given time, get a particular attribute
        """
        alength = c_int()
        ErrNo1 = c_int()
        ValArrayPtr = _lib.ENR_newOutValueArray(self.enrapi, _lib.ENR_getAttribute,
                                                _lib.ENR_link, byref(alength), byref(ErrNo1))
        ErrNo2 = _lib.ENR_getLinkAttribute(self.enrapi, TimeInd, LinkAttr, ValArrayPtr)
        BldArray = [ValArrayPtr[i] for i in range(alength.value)]
        _lib.ENR_free(ValArrayPtr)
        return BldArray


    def get_NodeResult(self, NodeInd, TimeInd):
        """
        Purpose: For a node at given time, get all attributes
        """
        alength = c_int()
        ErrNo1 = c_int()
        ValArrayPtr = _lib.ENR_newOutValueArray(self.enrapi, 
                                                _lib.ENR_getResult,
                                                _lib.ENR_node,
                                                byref(alength),
                                                byref(ErrNo1))
        ErrNo2 = _lib.ENR_getNodeResult(self.enrapi, TimeInd, NodeInd, ValArrayPtr)
        BldArray = [ValArrayPtr[i] for i in range(alength.value)]
        _lib.ENR_free(ValArrayPtr)
        return BldArray

    def get_LinkResult(self, LinkInd, TimeInd):
        """
        Purpose: For a link at given time, get all attributes
        """
        alength = c_int()
        ErrNo1 = c_int()
        ValArrayPtr = _lib.ENR_newOutValueArray(self.enrapi,
                                                _lib.ENR_getResult,
                                                _lib.ENR_link,
                                                byref(alength),
                                                byref(ErrNo1))
        ErrNo2 = _lib.ENR_getLinkResult(self.enrapi, TimeInd, LinkInd, ValArrayPtr)
        BldArray = [ValArrayPtr[i] for i in range(alength.value)]
        _lib.ENR_free(ValArrayPtr)
        return BldArray

    def CloseOutputFile(self):
        """
        Call to close binary file.
        """
        ret = _lib.ENR_close(byref(self.enrapi) )
        if ret != 0:
            raise Exception('Failed to Close *.out file')
        





    
    
    
