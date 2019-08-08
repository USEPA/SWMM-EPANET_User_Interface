from enum import Enum
from ui.inifile import ini_setting
from PyQt5.QtCore import QSettings
import core.epanet.options.hydraulics as hyd

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
    def __init__(self, file_name, project, program_setting):
        self.model = "epanet"
        self.project = project
        self.program_settings = program_setting
        ini_setting.__init__(self, file_name, self.model)

        # [Labels] label prefix
        self.model_object_keys = ["Junctions", "Reservoirs", "Tanks", "Pipes", "Pumps", "Valves", "Patterns", "Curves"]
        self.model_object_def_prefix = ["J", "R", "T", "P", "U", "V", "Ptn", "C"]

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
        self.parameters_def_values = ["GPM", "H_W", 1.0, 1.0, 40, 0.001, "CONTINUE", 1, 1.0, 0.5, "Yes",
                                      2, 10, 0.0]

        if self.config is None:
            self.init_config()

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

        self.node_numerical_preference_keys = ['Demand', 'Head', 'Pressure', 'Node Quality']
        self.node_numerical_preferences = {}
        for key in self.node_numerical_preference_keys:
            self.node_numerical_preferences[key] = 2
            if self.config:
                val, vtype = self.get_setting_value("Display Precision", key)
                if val is not None:
                    self.node_numerical_preferences[key] = val

        self.link_numerical_preference_keys = ['Flow', 'Velocity', 'Unit Headloss',
                                               'Friction Factor', 'Reaction Rate', 'Quality']
        self.link_numerical_preferences = {}
        for key in self.link_numerical_preference_keys:
            self.link_numerical_preferences[key] = 2
            if self.config:
                val, vtype = self.get_setting_value("Display Precision", key)
                if val is not None:
                    self.link_numerical_preferences[key] = val

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

    def init_config(self):
        # if a new qsettings has not been created such as when no project is created
        # then, create an empty qsettings
        if self.config is None:
            self.config = QSettings(QSettings.IniFormat, QSettings.UserScope, "EPA", self.model, None)
        '''
        self.config.setValue("Model/Name", self.model)
        for key in self.model_object_keys:
            self.config.setValue("Labels/" + key, self.model_object_prefix[key])
        for key in self.properties_keys:
            self.config.setValue("Defaults/" + key, self.properties_values[key])
        for key in self.parameters_keys:
            self.config.setValue("Defaults/" + key, self.parameters_values[key])
        '''

    def sync_defaults_label(self):
        """
        sync object label/prefix with internal qsettings
        """
        for key in self.model_object_keys:
            if self.config:
                self.config.setValue("Labels/" + key, self.model_object_prefix[key])
        if self.config:
            self.config.setValue("Labels/" + self.id_increment_key, str(self.id_increment))
            self.config.sync()

    def sync_defaults_property(self):
        """
        sync object properties with internal qsettings
        """
        for key in self.properties_keys:
            if self.config:
                self.config.setValue("Defaults/" + key, self.properties_values[key])
        if self.config:
            self.config.sync()

    def sync_defaults_parameter(self):
        """
        sync hydraulic parameters with internal qsettings
        """
        for key in self.parameters_keys:
            if self.config:
                self.config.setValue("Defaults/" + key, self.parameters_values[key])
        if self.project:
            self.sync_project_hydraulic_parameters()

    def sync_project_hydraulic_parameters(self):
        hydraulics_options = self.project.options.hydraulics
        for key in self.parameters_keys:
            val = self.parameters_values[key]
            if "flow unit" in key.lower():
                hydraulics_options.flow_units = hyd.FlowUnits[val]
            elif "headloss" in key.lower():
                #head_loss_underscore = self.cboHeadloss.currentText().replace('-', '_')
                hydraulics_options.head_loss = hyd.HeadLoss[val]
            elif "unbalanced" in key.lower():
                hydraulics_options.unbalanced = hyd.Unbalanced[val]
            elif "accuracy" in key.lower():
                hydraulics_options.accuracy = float(val)
            elif "check freq" in key.lower():
                hydraulics_options.check_frequency = int(val)
            elif "damp" in key.lower():
                hydraulics_options.damp_limit = float(val)
            elif "pattern" in key.lower():
                hydraulics_options.default_pattern = val
            elif "demand" in key.lower():
                hydraulics_options.demand_multiplier = float(val)
            elif "emitter" in key.lower():
                hydraulics_options.emitter_exponent = float(val)
            elif "max check" in key.lower():
                hydraulics_options.max_check = int(val)
            elif "trials" in key.lower():
                hydraulics_options.maximum_trials = int(val)
            elif "viscosity" in key.lower():
                hydraulics_options.viscosity = float(val)
            elif "gravity" in key.lower():
                hydraulics_options.specific_gravity = float(val)

    def sync_preferences(self):
        """
        sync preferences with internal qsettings
        """
        for key in self.node_numerical_preference_keys:
            if self.config:
                self.config.setValue("Display Precision/" + key, self.node_numerical_preferences[key])
        for key in self.link_numerical_preference_keys:
            if self.config:
                self.config.setValue("Display Precision/" + key, self.link_numerical_preferences[key])
        if self.config:
            self.config.sync()

    def apply_default_attributes(self, item):
        """
        Set default attributes for new model object
        Args:
            item: newly created model object
        """
        item_type = item.__class__.__name__
        if item_type == "Junction":
            item.elevation = self.config.value("Defaults/Node Elevation")
            if item.elevation is None:
                item.elevation = self.properties_values["Node Elevation"]
        elif item_type == "Tank":
            item.elevation = self.config.value("Defaults/Node Elevation")
            if item.elevation is None:
                item.elevation = self.properties_values["Node Elevation"]
            item.diameter = self.config.value("Defaults/Tank Diameter")
            if item.diameter is None:
                item.diameter = self.properties_values["Tank Diameter"]
            item.initial_level = self.config.value("Defaults/Tank Height")
            if item.initial_level is None:
                item.initial_level = self.properties_values["Tank Height"]
        elif item_type == "Pipe":
            if float(item.length) < 0.00000001:
                item.length = self.config.value("Defaults/Pipe Length")
                if item.length is None:
                    item.length = self.properties_values["Pipe Length"]
            item.diameter = self.config.value("Defaults/Tank Diameter")
            if item.diameter is None:
                item.diameter = self.properties_values["Tank Diameter"]
            item.roughness = self.config.value("Defaults/Pipe Roughness")
            if item.roughness is None:
                item.roughness = self.properties_values["Pipe Roughness"]




