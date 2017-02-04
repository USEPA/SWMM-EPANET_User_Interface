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
    def __init__(self, file_name, project):
        ini_setting.__init__(self, file_name)
        self.project = project
        self.model = "epanet"

        # [Labels] label prefix
        self.model_object_keys = ["Junctions", "Reservoirs", "Tanks", "Pumps", "Valves", "Patterns", "Curves"]
        self.model_object_def_prefix = ["J", "R", "T", "P", "V", "Ptn", "C"]

        self.id_increment_key = "ID Increment"
        self.id_def_increment = 1
        self.id_increment = 1

        # [Defaults]
        self.properties_keys = ["Node Elevation", "Tank Diameter", "Tank Height", "Pipe Length",
                           "Pipe Diameter", "Pipe Roughness", "Auto Length"]
        self.properties_def_values = [0, 50, 20, 1000, 12, 100, "Off"]

        # [Defaults]
        self.parameters_keys = ["Flow Units", "Headloss Formula", "Specific Gravity", "Relative Viscosity",
                           "Maximum Trials", "Accuracy", "If Unbalanced", "Default Pattern", "Demand Multiplier",
                           "Emitter Exponent", "Status Report", "Check Frequency", "Max Check", "Damp Limit"]
        self.parameters_def_values = ["GPM", "H_W", 1.0, 1.0, 40, 0.001, "Continue", 1, 1.0, 0.5, "Yes",
                                      "", "", ""]

        self.model_object_prefix = {}
        for key in self.model_object_keys:
            self.model_object_prefix[key] = self.model_object_def_prefix[self.model_object_keys.index(key)]
            if self.config:
                val, vtype = self.get_setting_value("Labels", key)
                if val is not None:
                    self.model_object_prefix[key] = val

        self.id_increment, vtype = self.get_setting_value("Labels", self.id_increment_key)
        if self.id_increment is None:
            self.id_increment = 1

        self.properties_values = {}
        for key in self.properties_keys:
            self.properties_values[key] = self.properties_def_values[self.properties_keys.index(key)]
            if self.config:
                val, vtype = self.get_setting_value("Defaults", key)
                if val is not None:
                    self.properties_values[key] = val

        self.parameters_values = {}
        for key in self.parameters_keys:
            self.parameters_values[key] = self.parameters_def_values[self.parameters_keys.index(key)]
            if self.config:
                val, vtype = self.get_setting_value("Defaults", key)
                if val is not None:
                    self.parameters_values[key] = val
