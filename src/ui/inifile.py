from PyQt5.QtCore import QSettings
from .model_utility import ParseData
import os


class ini_setting:
    """
    class for managing .ini file and project defaults
    """
    release_mode = False

    def __init__(self, file_name, model):
        """
        constructor: read setting values into a QSetting object
        Args:
            file_name: ini file name
        """
        self.file_name = file_name
        self.model = model
        self.error_msg = ""
        self.groups_with_values = {} # all values read
        self.groups = {} # group names and key names
        self.config = None
        try:
            self.config = QSettings(QSettings.IniFormat, QSettings.UserScope, "EPA", self.model, None)
            if (not os.path.isfile(self.file_name) and file_name):
                from shutil import copyfile
                copyfile(self.config.fileName(), file_name)
                # self.create_ini_file(file_name)
            else:
                self.file_name = self.config.fileName()
            self.build_setting_map()
            print("Read project settings from " + self.file_name)
        except Exception as exINI:
            self.config = None
            self.error_msg = "Reading Error" + ":\n" + str(exINI)

    def create_ini_file(self, file_name):
        """
        Specify .ini file path after instantiation
        if setting is not yet instantiated:
            a new setting is instantiated
            if the new setting has no key:
                a new ini file is created
        Args:
            file_name: the full path to an ini file
        Returns: True if successful; False if failed
        """
        if os.path.isfile(self.file_name): return False
        if self.config is None:
            try:
                self.config = QSettings(file_name, QSettings.IniFormat)
                if len(self.config.allKeys()) == 0:
                    # this is a brand new ini file
                    self.config.setValue("Model/Name", self.model)
                    self.config.sync()
                    print("created ini file: " + file_name)
                else:
                    print("Read settings from ini file: " + file_name)
                self.file_name = file_name
                return True
            except Exception as exINI:
                self.config = None
                self.error_msg = "Reading Error" + ":\n" + str(exINI)
                return False

    def get_setting_value(self, group, key):
        """
        Get the value of a ini setting, assuming all settings are grouped
        Args:
            group: the string name of a group or section
            key: the string name of a key
        Returns:
            a list of two elements, first being the value, second being the value type
        """
        rval = [None, None]
        if len(self.groups) == 0:
            return rval
        if not group in self.groups:
            return rval

        self.config.beginGroup(group)
        qvar = self.config.value(key)
        if qvar is None:
            self.config.endGroup()
            return rval
        str_val = str(qvar)
        if len(str_val) > 0:
            tval, tval_is_good = ParseData.intTryParse(str_val)
            if tval_is_good:
                rval[0] = tval
                rval[1] = "integer"
                self.config.endGroup()
                return rval
            tval, tval_is_good = ParseData.floatTryParse(str_val)
            if tval_is_good:
                rval[0] = tval
                rval[1] = "float"
                self.config.endGroup()
                return rval
            rval[0] = str_val
            rval[1] = "string"
            self.config.endGroup()
            return rval
        elif str_val == "":
            rval[0] = ""
            rval[1] = "string"
        else:
            str_list = qvar.toStringList().join(",")
            if len(str_list) > 0:
                rval[0] = str_list.strip(",").split(",")
                rval[1] = "stringlist"
                self.config.endGroup()
                return rval

        self.config.endGroup()
        return rval

    def build_setting_map(self):
        """
        Build a setting group-key-value mapping dictionary as below:
        self.groups_with_values
        [group_name] -> [key_name] -> [value, value_type]

        Also create group dictionary keyed on group name, pointing to its list of keys
        so we can get setting values on a as needed basis
        self.groups
        [group_name] -> [key names]
        """
        self.groups.clear()
        self.groups_with_values.clear()
        for group in self.config.childGroups():
            self.config.beginGroup(group)
            self.groups_with_values[group] = {}
            self.groups[group] = []
            for key in self.config.childKeys():
                self.groups[group].append(key)
                val, vtype = self.get_setting_value(group, key)
                self.groups_with_values[group][key] = val
                # print group + "::" + key + "::" + self.config.value(key).toString()
            self.config.endGroup()

    def read_ini_file_cp(self):
        self.config.read(self.file_name)
        for section in self.config.sections():
            dict1 = self.config_section_map(section)
            pass
        pass

    def config_section_map(self, section):
        dict1 = {}
        for option in self.config.options(section):
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    print ("skip: %s" % option)
                pass
            except:
                print ("exception on %s!" % option)
                dict1[option] = None
        return dict1


