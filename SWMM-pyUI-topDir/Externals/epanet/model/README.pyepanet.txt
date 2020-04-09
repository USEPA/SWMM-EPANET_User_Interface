PyEPANET 0.1.0 – README.txt

------------------------------
RESPEC edits:
This README is about the files:
epanet2.py
epanet2toolkit.py
The library compiled for use by these under 64-bit Windows is: epanet2_amd64.dll

epanet2.py has been modified slightly for the SWMM/EPANET user interface project to allow specifying where the underlying library is when creating a class ENepanet object.
------------------------------

Copyright 2011 Sandia Corporation. Under the terms of Contract DE-AC04-94AL85000 there is a non-exclusive license for use of this work by or on behalf of the U.S. Government. Export of this program may require a license from the United States Government.
All rights reserved. This software is licensed for use under the BSD license.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
 * Neither the name of the Sandia Corporation nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

---------------------

The PyEPANET Package

This Python package is a wrapper around the EPANET Programmers Toolkit that refactors the EPANET functions into a more pythonic format. Specifically, using the EPANET library directly in Python requires knowing the ctypes package, and learning how to pass variables by reference within Python. This package does that for the user. This way, the user can get values the “normal” python way – as returned values.

__ Installing the EPANET DLL

  To use PyEPANET you must already have the EPANET2 DLL compiled and installed in a place Python knows about. On Linux/Unix/Mac OSX machines, this means somewhere searched by default (such as /usr/lib or /usr/local/lib) or within the LD_LIBRARY_PATH variable. On Windows, the DLL should be in the system directory, or within the site-packages/pyepanet directory, or within the directory where the program will be executed.

__ Constants and Strings

  The EPANET Programmers Toolkit help files are the best place to start when trying to learn what the functions do. However, the most basic help has been added as pydoc-style docstrings within the package, so “help (pyepanet)” should give the user a place to start. All the EN_ enumerated constants that are defined in the DLL are also defined in the package, for example, “pyepanet.EN_NODECOUNT” will provide the correct value for the “EN_NODECOUNT” constant.

  To get a list of appropriate constants, see the “opt*” constants defined in the PyEPANET package. For example, the “pyepanet.optComponentCounts” array will list the string values for all the constants having to do with component counts. Again, using “help (pyepanet)” will provide a list of all the constants.

__ Loading the EPANET DLL

  To create an EPANET object, do the following:
	import pyepanet
	MyNet = pyepanet.ENepanet()
	MyNet.ENopen(‘MyInputFile.inp’,’myOutput.rpt’)

  To get, for example, the number of nodes in the network, do the following:
	numNodes = MyNet.ENgetcount(pyepanet.EN_NODECOUNT)

  Remember to close the EPANET object with the following before loading a new file:
	MyNet.ENclose()

  To get a list of all the methods defined within the class, along with a brief description of both the method and its parameters, use “help (pyepanet.ENepanet)”

__ Additional Notes

  There is one non-standard method within the ENepanet() class. These are there if the user wants to use the EPANET DLL like an executable. 
	from pyepanet import ENepanet
	A = ENepanet()
	A.epanetExec(‘mynetwork.inp’,’mynetwork.rpt’,’mynetwork.bin’)

  This form automatically closes the EPANET data structure after running, and the user does not need to run the ENclose function.

