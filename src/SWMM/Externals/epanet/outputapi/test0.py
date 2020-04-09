"""example: direct call thougt ctypesgen generated module

"""
import ctypes

from Externals.epanet.outputapi import outputapi as _lib

label  = _lib.String( (_lib.MAXID+1)*'\0')
errmsg = _lib.String( (_lib.MAXMSG+1)*'\0')
k=ctypes.c_int()
x= ctypes.c_float()

addr=ctypes.c_void_p()
filename= "Net1.bin"
if _lib.ENR_open(ctypes.byref(addr), filename) ==0 :
    print "\nfile {0} successfuly opened\n".format(filename)
else:
    exit()

if _lib.ENR_getNetSize(addr, _lib.ENR_nodeCount, ctypes.byref(k)) ==0 :
    print "nodes:     {0}".format(k.value)

if _lib.ENR_getNetSize(addr, _lib.ENR_tankCount, ctypes.byref(k)) ==0 :
    print "tanks:     {0}".format(k.value)

if _lib.ENR_getNetSize(addr, _lib.ENR_linkCount, ctypes.byref(k)) ==0 :
    print "links:     {0}".format(k.value)

if _lib.ENR_getNetSize(addr, _lib.ENR_pumpCount, ctypes.byref(k)) ==0 :
    print "pumps:     {0}".format(k.value)

if _lib.ENR_getNetSize(addr, _lib.ENR_valveCount, ctypes.byref(k)) ==0 :
    print "valves:     {0}".format(k.value)



_lib.ENR_getTimes(addr, _lib.ENR_numPeriods, ctypes.byref(k))
numperiods= k.value

nodeIndex= 10
_lib.ENR_getNodeID(addr, nodeIndex, label)
print "\n\nHead at node  idx={0}  ID={1} ".format(nodeIndex, label)
for i in range(0, numperiods):
    _lib.ENR_getNodeValue(addr, i, 10, _lib.ENR_head, ctypes.byref(x))
    print x.value,
print "\n\n"


if _lib.ENR_close(ctypes.byref(addr)) == 0:
  print "\nfile {0} successfuly closed".format(filename)




