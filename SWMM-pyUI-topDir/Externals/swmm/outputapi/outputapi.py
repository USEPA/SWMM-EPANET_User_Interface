'''Wrapper for outputAPI.h

Generated with:
C:\OSGeo4W64\apps\Python27\Scripts\ctypesgen.py -a -l outputapi -o outputapi.py outputAPI.h

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, str):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, str):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, str):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=float("inf")):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=float("inf")):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=float("inf")):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=float("inf")):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=float("inf")):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=float("inf")):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=float("inf")):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, str):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, str):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, bytes, UserString)):
            if isinstance(obj, bytes):
                self.data = obj
            else:
                self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError as e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname

        else:
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries

if sys.platform == "linux2":
    _libs["outputapi"] = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(os.path.realpath(__file__)), "SMOutputAPI-64.so"))
else:
    search_dir = os.path.dirname(os.path.realpath(__file__))
    while search_dir and not os.path.isfile(os.path.join(search_dir, "SMOutputAPI-64.dll")):
        print ("SMOutputAPI-64.dll Not found in " + search_dir + "\n")
        next_search_dir = os.path.dirname(search_dir)
        if next_search_dir == search_dir:
            break
        search_dir = next_search_dir
    print ("Try loading SMOutputAPI-64 from " + search_dir + "\n")
    _libs["outputapi"] = load_library(os.path.join(search_dir, "SMOutputAPI-64"))

# 1 libraries
# End libraries

# No modules

# outputAPI.h: 33
class struct_SMOutputAPI(Structure):
    pass

SMOutputAPI = struct_SMOutputAPI # outputAPI.h: 33

enum_anon_1 = c_int # outputAPI.h: 41

subcatchCount = 0 # outputAPI.h: 41

nodeCount = (subcatchCount + 1) # outputAPI.h: 41

linkCount = (nodeCount + 1) # outputAPI.h: 41

pollutantCount = (linkCount + 1) # outputAPI.h: 41

SMO_elementCount = enum_anon_1 # outputAPI.h: 41

enum_anon_2 = c_int # outputAPI.h: 47

flow_rate = 0 # outputAPI.h: 47

concentration = (flow_rate + 1) # outputAPI.h: 47

SMO_unit = enum_anon_2 # outputAPI.h: 47

enum_anon_3 = c_int # outputAPI.h: 54

getAttribute = 0 # outputAPI.h: 54

getResult = (getAttribute + 1) # outputAPI.h: 54

SMO_apiFunction = enum_anon_3 # outputAPI.h: 54

enum_anon_4 = c_int # outputAPI.h: 62

subcatch = 0 # outputAPI.h: 62

node = (subcatch + 1) # outputAPI.h: 62

link = (node + 1) # outputAPI.h: 62

_sys = (link + 1) # outputAPI.h: 62

SMO_elementType = enum_anon_4 # outputAPI.h: 62

enum_anon_5 = c_int # outputAPI.h: 69

reportStep = 0 # outputAPI.h: 69

numPeriods = (reportStep + 1) # outputAPI.h: 69

SMO_time = enum_anon_5 # outputAPI.h: 69

enum_anon_6 = c_int # outputAPI.h: 82

rainfall_subcatch = 0 # outputAPI.h: 82

snow_depth_subcatch = (rainfall_subcatch + 1) # outputAPI.h: 82

evap_loss = (snow_depth_subcatch + 1) # outputAPI.h: 82

infil_loss = (evap_loss + 1) # outputAPI.h: 82

runoff_rate = (infil_loss + 1) # outputAPI.h: 82

gwoutflow_rate = (runoff_rate + 1) # outputAPI.h: 82

gwtable_elev = (gwoutflow_rate + 1) # outputAPI.h: 82

soil_moisture = (gwtable_elev + 1) # outputAPI.h: 82

pollutant_conc_subcatch = (soil_moisture + 1) # outputAPI.h: 82

SMO_subcatchAttribute = enum_anon_6 # outputAPI.h: 82

enum_anon_7 = c_int # outputAPI.h: 93

invert_depth = 0 # outputAPI.h: 93

hydraulic_head = (invert_depth + 1) # outputAPI.h: 93

stored_ponded_volume = (hydraulic_head + 1) # outputAPI.h: 93

lateral_inflow = (stored_ponded_volume + 1) # outputAPI.h: 93

total_inflow = (lateral_inflow + 1) # outputAPI.h: 93

flooding_losses = (total_inflow + 1) # outputAPI.h: 93

pollutant_conc_node = (flooding_losses + 1) # outputAPI.h: 93

SMO_nodeAttribute = enum_anon_7 # outputAPI.h: 93

enum_anon_8 = c_int # outputAPI.h: 103

flow_rate_link = 0 # outputAPI.h: 103

flow_depth = (flow_rate_link + 1) # outputAPI.h: 103

flow_velocity = (flow_depth + 1) # outputAPI.h: 103

flow_volume = (flow_velocity + 1) # outputAPI.h: 103

capacity = (flow_volume + 1) # outputAPI.h: 103

pollutant_conc_link = (capacity + 1) # outputAPI.h: 103

SMO_linkAttribute = enum_anon_8 # outputAPI.h: 103

enum_anon_9 = c_int # outputAPI.h: 121

air_temp = 0 # outputAPI.h: 121

rainfall_system = (air_temp + 1) # outputAPI.h: 121

snow_depth_system = (rainfall_system + 1) # outputAPI.h: 121

evap_infil_loss = (snow_depth_system + 1) # outputAPI.h: 121

runoff_flow = (evap_infil_loss + 1) # outputAPI.h: 121

dry_weather_inflow = (runoff_flow + 1) # outputAPI.h: 121

groundwater_inflow = (dry_weather_inflow + 1) # outputAPI.h: 121

RDII_inflow = (groundwater_inflow + 1) # outputAPI.h: 121

direct_inflow = (RDII_inflow + 1) # outputAPI.h: 121

total_lateral_inflow = (direct_inflow + 1) # outputAPI.h: 121

flood_losses = (total_lateral_inflow + 1) # outputAPI.h: 121

outfall_flows = (flood_losses + 1) # outputAPI.h: 121

volume_stored = (outfall_flows + 1) # outputAPI.h: 121

evap_rate = (volume_stored + 1) # outputAPI.h: 121

SMO_systemAttribute = enum_anon_9 # outputAPI.h: 121

# outputAPI.h: 138
if hasattr(_libs['outputapi'], 'SMO_init'):
    SMO_init = _libs['outputapi'].SMO_init
    SMO_init.argtypes = []
    SMO_init.restype = POINTER(SMOutputAPI)

# outputAPI.h: 139
if hasattr(_libs['outputapi'], 'SMO_open'):
    SMO_open = _libs['outputapi'].SMO_open
    SMO_open.argtypes = [POINTER(SMOutputAPI), String]
    SMO_open.restype = c_int

# outputAPI.h: 141
if hasattr(_libs['outputapi'], 'SMO_getProjectSize'):
    SMO_getProjectSize = _libs['outputapi'].SMO_getProjectSize
    SMO_getProjectSize.argtypes = [POINTER(SMOutputAPI), SMO_elementCount, POINTER(c_int)]
    SMO_getProjectSize.restype = c_int

# outputAPI.h: 142
if hasattr(_libs['outputapi'], 'SMO_getResultCount'):
    SMO_getResultCount = _libs['outputapi'].SMO_getResultCount
    SMO_getResultCount.argtypes = [POINTER(SMOutputAPI), SMO_elementType, POINTER(c_int)]
    SMO_getResultCount.restype = c_int

# outputAPI.h: 144
if hasattr(_libs['outputapi'], 'SMO_getUnits'):
    SMO_getUnits = _libs['outputapi'].SMO_getUnits
    SMO_getUnits.argtypes = [POINTER(SMOutputAPI), SMO_unit, POINTER(c_int)]
    SMO_getUnits.restype = c_int

# outputAPI.h: 145
if hasattr(_libs['outputapi'], 'SMO_getPollutantUnits'):
    SMO_getPollutantUnits = _libs['outputapi'].SMO_getPollutantUnits
    SMO_getPollutantUnits.argtypes = [POINTER(SMOutputAPI), c_int, POINTER(c_int)]
    SMO_getPollutantUnits.restype = c_int

# outputAPI.h: 147
if hasattr(_libs['outputapi'], 'SMO_getStartTime'):
    SMO_getStartTime = _libs['outputapi'].SMO_getStartTime
    SMO_getStartTime.argtypes = [POINTER(SMOutputAPI), POINTER(c_double)]
    SMO_getStartTime.restype = c_int

# outputAPI.h: 148
if hasattr(_libs['outputapi'], 'SMO_getTimes'):
    SMO_getTimes = _libs['outputapi'].SMO_getTimes
    SMO_getTimes.argtypes = [POINTER(SMOutputAPI), SMO_time, POINTER(c_int)]
    SMO_getTimes.restype = c_int

# outputAPI.h: 150
if hasattr(_libs['outputapi'], 'SMO_getElementName'):
    SMO_getElementName = _libs['outputapi'].SMO_getElementName
    SMO_getElementName.argtypes = [POINTER(SMOutputAPI), SMO_elementType, c_int, String, c_int]
    SMO_getElementName.restype = c_int

# outputAPI.h: 153
if hasattr(_libs['outputapi'], 'SMO_newOutValueSeries'):
    SMO_newOutValueSeries = _libs['outputapi'].SMO_newOutValueSeries
    SMO_newOutValueSeries.argtypes = [POINTER(SMOutputAPI), c_long, c_long, POINTER(c_long), POINTER(c_int)]
    SMO_newOutValueSeries.restype = POINTER(c_float)

# outputAPI.h: 155
if hasattr(_libs['outputapi'], 'SMO_newOutValueArray'):
    SMO_newOutValueArray = _libs['outputapi'].SMO_newOutValueArray
    SMO_newOutValueArray.argtypes = [POINTER(SMOutputAPI), SMO_apiFunction, SMO_elementType, POINTER(c_long), POINTER(c_int)]
    SMO_newOutValueArray.restype = POINTER(c_float)

# outputAPI.h: 158
if hasattr(_libs['outputapi'], 'SMO_getSubcatchSeries'):
    SMO_getSubcatchSeries = _libs['outputapi'].SMO_getSubcatchSeries
    SMO_getSubcatchSeries.argtypes = [POINTER(SMOutputAPI), c_int, SMO_subcatchAttribute, c_long, c_long, POINTER(c_float)]
    SMO_getSubcatchSeries.restype = c_int

# outputAPI.h: 160
if hasattr(_libs['outputapi'], 'SMO_getNodeSeries'):
    SMO_getNodeSeries = _libs['outputapi'].SMO_getNodeSeries
    SMO_getNodeSeries.argtypes = [POINTER(SMOutputAPI), c_int, SMO_nodeAttribute, c_long, c_long, POINTER(c_float)]
    SMO_getNodeSeries.restype = c_int

# outputAPI.h: 162
if hasattr(_libs['outputapi'], 'SMO_getLinkSeries'):
    SMO_getLinkSeries = _libs['outputapi'].SMO_getLinkSeries
    SMO_getLinkSeries.argtypes = [POINTER(SMOutputAPI), c_int, SMO_linkAttribute, c_long, c_long, POINTER(c_float)]
    SMO_getLinkSeries.restype = c_int

# outputAPI.h: 164
if hasattr(_libs['outputapi'], 'SMO_getSystemSeries'):
    SMO_getSystemSeries = _libs['outputapi'].SMO_getSystemSeries
    SMO_getSystemSeries.argtypes = [POINTER(SMOutputAPI), SMO_systemAttribute, c_long, c_long, POINTER(c_float)]
    SMO_getSystemSeries.restype = c_int

# outputAPI.h: 167
if hasattr(_libs['outputapi'], 'SMO_getSubcatchAttribute'):
    SMO_getSubcatchAttribute = _libs['outputapi'].SMO_getSubcatchAttribute
    SMO_getSubcatchAttribute.argtypes = [POINTER(SMOutputAPI), c_long, SMO_subcatchAttribute, POINTER(c_float)]
    SMO_getSubcatchAttribute.restype = c_int

# outputAPI.h: 169
if hasattr(_libs['outputapi'], 'SMO_getNodeAttribute'):
    SMO_getNodeAttribute = _libs['outputapi'].SMO_getNodeAttribute
    SMO_getNodeAttribute.argtypes = [POINTER(SMOutputAPI), c_long, SMO_nodeAttribute, POINTER(c_float)]
    SMO_getNodeAttribute.restype = c_int

# outputAPI.h: 171
if hasattr(_libs['outputapi'], 'SMO_getLinkAttribute'):
    SMO_getLinkAttribute = _libs['outputapi'].SMO_getLinkAttribute
    SMO_getLinkAttribute.argtypes = [POINTER(SMOutputAPI), c_long, SMO_linkAttribute, POINTER(c_float)]
    SMO_getLinkAttribute.restype = c_int

# outputAPI.h: 173
if hasattr(_libs['outputapi'], 'SMO_getSystemAttribute'):
    SMO_getSystemAttribute = _libs['outputapi'].SMO_getSystemAttribute
    SMO_getSystemAttribute.argtypes = [POINTER(SMOutputAPI), c_long, SMO_systemAttribute, POINTER(c_float)]
    SMO_getSystemAttribute.restype = c_int

# outputAPI.h: 176
if hasattr(_libs['outputapi'], 'SMO_getSubcatchResult'):
    SMO_getSubcatchResult = _libs['outputapi'].SMO_getSubcatchResult
    SMO_getSubcatchResult.argtypes = [POINTER(SMOutputAPI), c_long, c_int, POINTER(c_float)]
    SMO_getSubcatchResult.restype = c_int

# outputAPI.h: 178
if hasattr(_libs['outputapi'], 'SMO_getNodeResult'):
    SMO_getNodeResult = _libs['outputapi'].SMO_getNodeResult
    SMO_getNodeResult.argtypes = [POINTER(SMOutputAPI), c_long, c_int, POINTER(c_float)]
    SMO_getNodeResult.restype = c_int

# outputAPI.h: 180
if hasattr(_libs['outputapi'], 'SMO_getLinkResult'):
    SMO_getLinkResult = _libs['outputapi'].SMO_getLinkResult
    SMO_getLinkResult.argtypes = [POINTER(SMOutputAPI), c_long, c_int, POINTER(c_float)]
    SMO_getLinkResult.restype = c_int

# outputAPI.h: 182
if hasattr(_libs['outputapi'], 'SMO_getSystemResult'):
    SMO_getSystemResult = _libs['outputapi'].SMO_getSystemResult
    SMO_getSystemResult.argtypes = [POINTER(SMOutputAPI), c_long, c_int, POINTER(c_float)]
    SMO_getSystemResult.restype = c_int

# outputAPI.h: 185
if hasattr(_libs['outputapi'], 'SMO_free'):
    SMO_free = _libs['outputapi'].SMO_free
    SMO_free.argtypes = [POINTER(c_float)]
    SMO_free.restype = None

# outputAPI.h: 187
if hasattr(_libs['outputapi'], 'SMO_close'):
    SMO_close = _libs['outputapi'].SMO_close
    SMO_close.argtypes = [POINTER(SMOutputAPI)]
    SMO_close.restype = c_int

# outputAPI.h: 188
if hasattr(_libs['outputapi'], 'SMO_errMessage'):
    SMO_errMessage = _libs['outputapi'].SMO_errMessage
    SMO_errMessage.argtypes = [c_int, String, c_int]
    SMO_errMessage.restype = None

# <command-line>: 1
try:
    _REENTRANT = 1
except:
    pass

__const = c_int # <command-line>: 5

# <command-line>: 8
try:
    CTYPESGEN = 1
except:
    pass

# outputAPI.h: 13
try:
    MAXFILENAME = 259
except:
    pass

# outputAPI.h: 14
try:
    MAXELENAME = 31
except:
    pass

# outputAPI.h: 17
try:
    ERR410 = 'Error 410: SMO_init() has not been called'
except:
    pass

# outputAPI.h: 18
try:
    ERR411 = 'Error 411: SMO_open() has not been called'
except:
    pass

# outputAPI.h: 19
try:
    ERR414 = 'Error 414: memory allocation failure'
except:
    pass

# outputAPI.h: 21
try:
    ERR421 = 'Input Error 421: invalid parameter code'
except:
    pass

# outputAPI.h: 22
try:
    ERR422 = 'Input Error 422: reporting period index out of range'
except:
    pass

# outputAPI.h: 23
try:
    ERR423 = 'Input Error 423: element index out of range'
except:
    pass

# outputAPI.h: 24
try:
    ERR424 = 'Input Error 424: no memory allocated for results'
except:
    pass

# outputAPI.h: 26
try:
    ERR434 = 'File Error 434: unable to open binary output file'
except:
    pass

# outputAPI.h: 27
try:
    ERR435 = 'File Error 435: invalid file - not created by SWMM'
except:
    pass

# outputAPI.h: 28
try:
    ERR436 = 'File Error 436: invalid file - contains no results'
except:
    pass

# outputAPI.h: 29
try:
    ERR437 = 'File Error 437: invalid file - model run issued warnings'
except:
    pass

# outputAPI.h: 31
try:
    ERR440 = 'ERROR 440: an unspecified error has occurred'
except:
    pass

MAXID = 31

SMOutputAPI = struct_SMOutputAPI # outputAPI.h: 33

# No inserted files

