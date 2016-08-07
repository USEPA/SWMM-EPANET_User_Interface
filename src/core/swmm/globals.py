from enum import Enum

class ObjectType(Enum):
    SUBCATCHMENTS = 0
    NODES = 1
    LINKS = 2
    SYS = 3
    UNKNOWN = 4

class MiscConstants():
    """
    # Miscellaneous global constants
    """
    FLOWTOL         = 0.005             #Zero flow tolerance
    MISSING         = -1.0e10           #Missing value
    NOXY            = -9999999          #Missing map coordinate

    #NOPOINT: TPoint = (X: -9999999; Y: -9999999)
    #NORECT: TRect   = (Left: -9999999; Top: -9999999; Right: -9999999; Bottom: -9999999)

    NODATE          = -693594   # 1/1/0001
    NA              = '#N/A'
    NONE            = 0
    NOVIEW          = 0
    PLUS            = 1
    MINUS           = 2
    DefMeasError    = 5
    DefIDIncrement  = 1
    DefMaxTrials    = 8
    DefMinSurfAreaUS = '12.557' #(ft2)
    DefMinSurfAreaSI = '1.14'   #(m2)
    DefHeadTolUS     = '0.005'  #(ft)
    DefHeadTolSI     = '0.0015' #(m)

class EUnitSystem(Enum):
    usUS = 0
    usSI = 1

class ERunStatus(Enum):
    rsSuccess = 0
    rsWarning = 1
    rsError = 2
    rsWrongVersion = 3
    rsFailed = 4
    rsShutdown = 5
    rsStopped = 6
    rsImportError = 7
    rsNone = 8

#TArrowStyle = (asNone, asOpen, asFilled, asFancy);
#TMapUnits = (muFeet, muMeters, muDegrees, muNone);
#TInputFileType = (iftNone, iftNET, iftINP);
