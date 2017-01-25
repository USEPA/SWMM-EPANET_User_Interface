from enum import Enum
from ui.inifile import ini_setting

class EPROPERTY_JUNCTION(Enum):
    """junction property index"""
    ELEV = 2 # Elevation
    DEMAND = 3 # Demand
    PATTERN = 4 # Demand pattern
    DMNDCAT = 5 # Demand categories
    EMITTER = 6 # Emitter coeff.
    INITQUAL = 7 # Init.quality
    SRCQUAL = 8 # Source quality
    SRCPAT = 9 # Source pattern
    SRCTYPE = 10 # Source type


class EPROPERTY_RES(Enum):
    HEAD = 2 # Head
    PATTERN = 3 # Head pattern
    INITQUAL = 4 # Init.quality
    SRCQUAL = 5 # Source quality
    SRCPAT = 6 # Source pattern
    SRCTYPE = 7 # Source type


class EPROPERTY_TANK(Enum):
    ELEV = 2 # Elevation
    INITLVL = 3 # Init.level
    MINLVL = 4 # Min.level
    MAXLVL = 5 # Max.level
    DIAM = 6 # Diameter
    MINVOL = 7 # Min.volume
    VCURVE = 8 # Volume curve
    MIXMODEL = 9 # Mixing model
    MIXFRAC = 10 # Mixing fraction
    KBULK = 11 # Bulk coeff.
    INITQUAL = 12 # Init.quality
    SRCQUAL = 13 # Source quality
    SRCPAT = 14 # Source pattern
    SRCTYPE = 15 # Source type


class EPROPERTY_PIPE(Enum):
    LEN = 2 # Length
    DIAM = 3 # Diameter
    ROUGH = 4 # Roughness coeff.
    MLOSS = 5 # Minor loss coeff.
    STATUS = 6 # Status
    KBULK = 7 # Bulk coeff.
    KWALL = 8 # Wall coeff.


class DefaultsEPANET(ini_setting):
    def __init__(self, file_name, project, qsetting):
        ini_setting.__init__(self, file_name, qsetting)
        self.project = project
        self.model = "epanet"






