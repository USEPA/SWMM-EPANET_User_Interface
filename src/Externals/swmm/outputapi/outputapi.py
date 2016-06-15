'''Wrapper for outputAPI.h

Generated with:
C:\OSGeo4W64\apps\Python27\Scripts\ctypesgen.py -a -l outputapi -o outputAPI.py outputAPI.h

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
        if isinstance(seq, basestring):
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
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
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
    def count(self, sub, start=0, end=sys.maxint):
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
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
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
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
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
    def startswith(self, prefix, start=0, end=sys.maxint):
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
        elif isinstance(sub, basestring):
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
        elif isinstance(other, basestring):
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
        if isinstance(obj, (str, unicode, UserString)):
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
        except OSError,e:
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
        print "SMOutputAPI-64.dll Not found in " + search_dir
        next_search_dir = os.path.dirname(search_dir)
        if next_search_dir == search_dir:
            break
        search_dir = next_search_dir
    print "Try loading SMOutputAPI-64 from " + search_dir
    _libs["outputapi"] = load_library(os.path.join(search_dir, "SMOutputAPI-64"))

# 1 libraries
# End libraries

# No modules

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 41
class struct_SMOutputAPI(Structure):
    pass

SMOutputAPI = struct_SMOutputAPI # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 41

enum_anon_1 = c_int # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 49

subcatchCount = 0 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 49

nodeCount = (subcatchCount + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 49

linkCount = (nodeCount + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 49

pollutantCount = (linkCount + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 49

SMO_elementCount = enum_anon_1 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 49

enum_anon_2 = c_int # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 55

flow_rate = 0 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 55

concentration = (flow_rate + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 55

SMO_unit = enum_anon_2 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 55

enum_anon_3 = c_int # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 62

getAttribute = 0 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 62

getResult = (getAttribute + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 62

SMO_apiFunction = enum_anon_3 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 62

enum_anon_4 = c_int # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 70

subcatch = 0 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 70

node = (subcatch + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 70

link = (node + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 70

_sys = (link + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 70

SMO_elementType = enum_anon_4 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 70

enum_anon_5 = c_int # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 77

reportStep = 0 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 77

numPeriods = (reportStep + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 77

SMO_time = enum_anon_5 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 77

enum_anon_6 = c_int # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 90

rainfall_subcatch = 0 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 90

snow_depth_subcatch = (rainfall_subcatch + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 90

evap_loss = (snow_depth_subcatch + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 90

infil_loss = (evap_loss + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 90

runoff_rate = (infil_loss + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 90

gwoutflow_rate = (runoff_rate + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 90

gwtable_elev = (gwoutflow_rate + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 90

soil_moisture = (gwtable_elev + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 90

pollutant_conc_subcatch = (soil_moisture + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 90

SMO_subcatchAttribute = enum_anon_6 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 90

enum_anon_7 = c_int # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 101

invert_depth = 0 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 101

hydraulic_head = (invert_depth + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 101

stored_ponded_volume = (hydraulic_head + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 101

lateral_inflow = (stored_ponded_volume + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 101

total_inflow = (lateral_inflow + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 101

flooding_losses = (total_inflow + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 101

pollutant_conc_node = (flooding_losses + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 101

SMO_nodeAttribute = enum_anon_7 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 101

enum_anon_8 = c_int # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 111

flow_rate_link = 0 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 111

flow_depth = (flow_rate_link + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 111

flow_velocity = (flow_depth + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 111

flow_volume = (flow_velocity + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 111

capacity = (flow_volume + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 111

pollutant_conc_link = (capacity + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 111

SMO_linkAttribute = enum_anon_8 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 111

enum_anon_9 = c_int # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

air_temp = 0 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

rainfall_system = (air_temp + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

snow_depth_system = (rainfall_system + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

evap_infil_loss = (snow_depth_system + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

runoff_flow = (evap_infil_loss + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

dry_weather_inflow = (runoff_flow + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

groundwater_inflow = (dry_weather_inflow + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

RDII_inflow = (groundwater_inflow + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

direct_inflow = (RDII_inflow + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

total_lateral_inflow = (direct_inflow + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

flood_losses = (total_lateral_inflow + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

outfall_flows = (flood_losses + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

volume_stored = (outfall_flows + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

evap_rate = (volume_stored + 1) # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

SMO_systemAttribute = enum_anon_9 # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 129

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 131
class struct_IDentry(Structure):
    pass

struct_IDentry.__slots__ = [
    'IDname',
    'nextID',
]
struct_IDentry._fields_ = [
    ('IDname', String),
    ('nextID', POINTER(struct_IDentry)),
]

idEntry = struct_IDentry # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 135

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 137
if hasattr(_libs['outputapi'], 'SMR_open'):
    SMR_open = _libs['outputapi'].SMR_open
    SMR_open.argtypes = [String, POINTER(POINTER(SMOutputAPI))]
    SMR_open.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 140
if hasattr(_libs['outputapi'], 'SMO_getProjectSize'):
    SMO_getProjectSize = _libs['outputapi'].SMO_getProjectSize
    SMO_getProjectSize.argtypes = [POINTER(SMOutputAPI), SMO_elementCount, POINTER(c_int)]
    SMO_getProjectSize.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 141
if hasattr(_libs['outputapi'], 'SMO_getUnits'):
    SMO_getUnits = _libs['outputapi'].SMO_getUnits
    SMO_getUnits.argtypes = [POINTER(SMOutputAPI), SMO_unit, POINTER(c_int)]
    SMO_getUnits.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 142
if hasattr(_libs['outputapi'], 'SMO_getStartTime'):
    SMO_getStartTime = _libs['outputapi'].SMO_getStartTime
    SMO_getStartTime.argtypes = [POINTER(SMOutputAPI), POINTER(c_double)]
    SMO_getStartTime.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 143
if hasattr(_libs['outputapi'], 'SMO_getTimes'):
    SMO_getTimes = _libs['outputapi'].SMO_getTimes
    SMO_getTimes.argtypes = [POINTER(SMOutputAPI), SMO_time, POINTER(c_int)]
    SMO_getTimes.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 146
if hasattr(_libs['outputapi'], 'SMO_getSubcatchIDs'):
    SMO_getSubcatchIDs = _libs['outputapi'].SMO_getSubcatchIDs
    SMO_getSubcatchIDs.argtypes = [POINTER(SMOutputAPI), POINTER(c_int)]
    SMO_getSubcatchIDs.restype = POINTER(struct_IDentry)

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 147
if hasattr(_libs['outputapi'], 'SMO_getNodeIDs'):
    SMO_getNodeIDs = _libs['outputapi'].SMO_getNodeIDs
    SMO_getNodeIDs.argtypes = [POINTER(SMOutputAPI), POINTER(c_int)]
    SMO_getNodeIDs.restype = POINTER(struct_IDentry)

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 148
if hasattr(_libs['outputapi'], 'SMO_getLinkIDs'):
    SMO_getLinkIDs = _libs['outputapi'].SMO_getLinkIDs
    SMO_getLinkIDs.argtypes = [POINTER(SMOutputAPI), POINTER(c_int)]
    SMO_getLinkIDs.restype = POINTER(struct_IDentry)

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 149
if hasattr(_libs['outputapi'], 'SMO_getPollutIDs'):
    SMO_getPollutIDs = _libs['outputapi'].SMO_getPollutIDs
    SMO_getPollutIDs.argtypes = [POINTER(SMOutputAPI), POINTER(c_int)]
    SMO_getPollutIDs.restype = POINTER(struct_IDentry)

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 152
if hasattr(_libs['outputapi'], 'SMO_newOutValueSeries'):
    SMO_newOutValueSeries = _libs['outputapi'].SMO_newOutValueSeries
    SMO_newOutValueSeries.argtypes = [POINTER(SMOutputAPI), c_int, c_int, POINTER(c_int), POINTER(c_int)]
    SMO_newOutValueSeries.restype = POINTER(c_float)

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 154
if hasattr(_libs['outputapi'], 'SMO_newOutValueArray'):
    SMO_newOutValueArray = _libs['outputapi'].SMO_newOutValueArray
    SMO_newOutValueArray.argtypes = [POINTER(SMOutputAPI), SMO_apiFunction, SMO_elementType, POINTER(c_int), POINTER(c_int)]
    SMO_newOutValueArray.restype = POINTER(c_float)

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 158
if hasattr(_libs['outputapi'], 'SMO_newOutTimeList'):
    SMO_newOutTimeList = _libs['outputapi'].SMO_newOutTimeList
    SMO_newOutTimeList.argtypes = [POINTER(SMOutputAPI), POINTER(c_int)]
    SMO_newOutTimeList.restype = POINTER(c_double)

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 159
if hasattr(_libs['outputapi'], 'SMO_getTimeList'):
    SMO_getTimeList = _libs['outputapi'].SMO_getTimeList
    SMO_getTimeList.argtypes = [POINTER(SMOutputAPI), POINTER(c_double)]
    SMO_getTimeList.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 162
if hasattr(_libs['outputapi'], 'SMO_getSubcatchSeries'):
    SMO_getSubcatchSeries = _libs['outputapi'].SMO_getSubcatchSeries
    SMO_getSubcatchSeries.argtypes = [POINTER(SMOutputAPI), c_int, SMO_subcatchAttribute, c_int, c_int, POINTER(c_float)]
    SMO_getSubcatchSeries.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 164
if hasattr(_libs['outputapi'], 'SMO_getNodeSeries'):
    SMO_getNodeSeries = _libs['outputapi'].SMO_getNodeSeries
    SMO_getNodeSeries.argtypes = [POINTER(SMOutputAPI), c_int, SMO_nodeAttribute, c_int, c_int, POINTER(c_float)]
    SMO_getNodeSeries.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 166
if hasattr(_libs['outputapi'], 'SMO_getLinkSeries'):
    SMO_getLinkSeries = _libs['outputapi'].SMO_getLinkSeries
    SMO_getLinkSeries.argtypes = [POINTER(SMOutputAPI), c_int, SMO_linkAttribute, c_int, c_int, POINTER(c_float)]
    SMO_getLinkSeries.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 168
if hasattr(_libs['outputapi'], 'SMO_getSystemSeries'):
    SMO_getSystemSeries = _libs['outputapi'].SMO_getSystemSeries
    SMO_getSystemSeries.argtypes = [POINTER(SMOutputAPI), SMO_systemAttribute, c_int, c_int, POINTER(c_float)]
    SMO_getSystemSeries.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 172
if hasattr(_libs['outputapi'], 'SMO_getSubcatchAttribute'):
    SMO_getSubcatchAttribute = _libs['outputapi'].SMO_getSubcatchAttribute
    SMO_getSubcatchAttribute.argtypes = [POINTER(SMOutputAPI), c_int, SMO_subcatchAttribute, POINTER(c_float)]
    SMO_getSubcatchAttribute.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 174
if hasattr(_libs['outputapi'], 'SMO_getNodeAttribute'):
    SMO_getNodeAttribute = _libs['outputapi'].SMO_getNodeAttribute
    SMO_getNodeAttribute.argtypes = [POINTER(SMOutputAPI), c_int, SMO_nodeAttribute, POINTER(c_float)]
    SMO_getNodeAttribute.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 176
if hasattr(_libs['outputapi'], 'SMO_getLinkAttribute'):
    SMO_getLinkAttribute = _libs['outputapi'].SMO_getLinkAttribute
    SMO_getLinkAttribute.argtypes = [POINTER(SMOutputAPI), c_int, SMO_linkAttribute, POINTER(c_float)]
    SMO_getLinkAttribute.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 178
if hasattr(_libs['outputapi'], 'SMO_getSystemAttribute'):
    SMO_getSystemAttribute = _libs['outputapi'].SMO_getSystemAttribute
    SMO_getSystemAttribute.argtypes = [POINTER(SMOutputAPI), c_int, SMO_systemAttribute, POINTER(c_float)]
    SMO_getSystemAttribute.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 182
if hasattr(_libs['outputapi'], 'SMO_getSubcatchResult'):
    SMO_getSubcatchResult = _libs['outputapi'].SMO_getSubcatchResult
    SMO_getSubcatchResult.argtypes = [POINTER(SMOutputAPI), c_int, c_int, POINTER(c_float)]
    SMO_getSubcatchResult.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 184
if hasattr(_libs['outputapi'], 'SMO_getNodeResult'):
    SMO_getNodeResult = _libs['outputapi'].SMO_getNodeResult
    SMO_getNodeResult.argtypes = [POINTER(SMOutputAPI), c_int, c_int, POINTER(c_float)]
    SMO_getNodeResult.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 186
if hasattr(_libs['outputapi'], 'SMO_getLinkResult'):
    SMO_getLinkResult = _libs['outputapi'].SMO_getLinkResult
    SMO_getLinkResult.argtypes = [POINTER(SMOutputAPI), c_int, c_int, POINTER(c_float)]
    SMO_getLinkResult.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 188
if hasattr(_libs['outputapi'], 'SMO_getSystemResult'):
    SMO_getSystemResult = _libs['outputapi'].SMO_getSystemResult
    SMO_getSystemResult.argtypes = [POINTER(SMOutputAPI), c_int, POINTER(c_float)]
    SMO_getSystemResult.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 191
if hasattr(_libs['outputapi'], 'SMO_free'):
    SMO_free = _libs['outputapi'].SMO_free
    SMO_free.argtypes = [POINTER(c_float)]
    SMO_free.restype = None

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 192
if hasattr(_libs['outputapi'], 'SMO_freeTimeList'):
    SMO_freeTimeList = _libs['outputapi'].SMO_freeTimeList
    SMO_freeTimeList.argtypes = [POINTER(c_double)]
    SMO_freeTimeList.restype = None

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 193
if hasattr(_libs['outputapi'], 'SMO_freeIDList'):
    SMO_freeIDList = _libs['outputapi'].SMO_freeIDList
    SMO_freeIDList.argtypes = [POINTER(struct_IDentry)]
    SMO_freeIDList.restype = None

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 196
if hasattr(_libs['outputapi'], 'SMO_close'):
    SMO_close = _libs['outputapi'].SMO_close
    SMO_close.argtypes = [POINTER(SMOutputAPI)]
    SMO_close.restype = c_int

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 197
if hasattr(_libs['outputapi'], 'SMO_errMessage'):
    SMO_errMessage = _libs['outputapi'].SMO_errMessage
    SMO_errMessage.argtypes = [c_int, String, c_int]
    SMO_errMessage.restype = c_int

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

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 27
try:
    MAXFNAME = 259
except:
    pass

# c:\\mingw\\lib64\\gcc\\x86_64-w64-mingw32\\4.8.3\\include\\stdbool.h: 34
try:
    true = 1
except:
    pass

# c:\\mingw\\lib64\\gcc\\x86_64-w64-mingw32\\4.8.3\\include\\stdbool.h: 35
try:
    false = 0
except:
    pass

# c:\\mingw\\lib64\\gcc\\x86_64-w64-mingw32\\4.8.3\\include\\stdbool.h: 48
try:
    __bool_true_false_are_defined = 1
except:
    pass

INT4 = c_int # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 31

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 34
try:
    ERR411 = 'Input Error 411: no memory allocated for results.'
except:
    pass

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 35
try:
    ERR412 = "Input Error 412: no results; binary file hasn't been opened."
except:
    pass

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 36
try:
    ERR421 = 'Input Error 421: invalid parameter code.'
except:
    pass

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 37
try:
    ERR434 = 'File Error  434: unable to open binary output file.'
except:
    pass

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 38
try:
    ERR435 = 'File Error  435: run terminated; no results in binary file.'
except:
    pass

# C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 39
try:
    ERR441 = 'Error 441: need to call SMR_open before calling this function'
except:
    pass

SMOutputAPI = struct_SMOutputAPI # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 41

IDentry = struct_IDentry # C:\\Users\\Public\\Python\\OutputAPIs\\SWMMoutputAPI\\outputAPI.h: 131

# No inserted files

