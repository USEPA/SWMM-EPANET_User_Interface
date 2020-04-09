# import ctypes
#
# from Externals.epanet.outputapi import outputapi as _lib
#
# label  = _lib.String( (_lib.MAXID+1)*'\0')
# errmsg = _lib.String( (_lib.MAXMSG+1)*'\0')
# count = ctypes.c_int()
# val = ctypes.c_float()
#
#
# class EnOutErr(Exception):
#   pass
#
# def errcheck(ierr):
#   if ierr==0:
#      return
#   if _lib.ENR_errMessage(ierr, errmsg, _lib.MAXMSG+1)==0:
#      raise EnOutErr(str(errmsg))
#   else:
#      raise EnOutErr("Unknown error #{0}".format(ierr) )
#
#
# def open(filename):
#     addr=ctypes.c_void_p()
#     errcheck(_lib.ENR_open(ctypes.byref(addr), filename)  )
#     return addr
#
# def close(addr):
#     errcheck(_lib.ENR_close(ctypes.byref(addr)) )
#
# def getnumnodes(addr):
#     count= ctypes.c_int()
#     errcheck(_lib.ENR_getNetSize(addr, _lib.ENR_nodeCount, ctypes.byref(count)) )
#     return count.value
#
# def getnumtanks(addr):
#     count= ctypes.c_int()
#     errcheck(_lib.ENR_getNetSize(addr, _lib.ENR_tankCount, ctypes.byref(count)) )
#     return count.value
#
# def getnumlinks(addr):
#     count= ctypes.c_int()
#     errcheck(_lib.ENR_getNetSize(addr, _lib.ENR_linkCount, ctypes.byref(count)) )
#     return count.value
#
# def getnumpumps(addr):
#     count= ctypes.c_int()
#     errcheck(_lib.ENR_getNetSize(addr, _lib.ENR_pumpCount, ctypes.byref(count)) )
#     return count.value
#
# def getnumvalves(addr):
#     count= ctypes.c_int()
#     errcheck(_lib.ENR_getNetSize(addr, _lib.ENR_valveCount, ctypes.byref(count)) )
#     return count.value
#
# def getnumperiods(addr):
#     count= ctypes.c_int()
#     errcheck(_lib.ENR_getTimes(addr, _lib.ENR_numPeriods,
# 			       ctypes.byref(count)) )
#     return count.value
#
# def getnodehead(addr, timeidx, nodeidx):
#     val= ctypes.c_float()
#     errcheck(_lib.ENR_getNodeValue(addr, timeidx, nodeidx, _lib.ENR_head, ctypes.byref(val)) )
#     return val.value
#
# def getnodeid(addr, index):
#     """Retrieves the ID label of a node with a specified index.
#
#     Arguments:
#     index: node index"""
#     errcheck(_lib.ENR_getNodeID(addr, index, label ) )
#     return str(label)
#
#
#
