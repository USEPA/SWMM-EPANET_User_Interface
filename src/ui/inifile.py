from PyQt4.QtCore import QSettings
from model_utility import ParseData

class ini_setting:
    """
    class for managing .ini file and project defaults
    """
    def __init__(self, file_name):
        """
        constructor
        Args:
            project: model project instance
            file_name: ini file name
            model: model type, either "swmm" or "epanet"
        """
        self.file_name = file_name
        self.error_msg = ""
        try:
            self.config = QSettings(self.file_name, QSettings.IniFormat)
            print("Read project settings from " + self.file_name)
        except Exception as exINI:
            self.config = None
            self.error_msg = "Reading Error" + ":\n" + str(exINI)

        self.sections = {} # all values read
        self.groups = {} # group names and key names

        if self.config is not None:
            # only create group dictionary keyed on group name, pointing to its list of keys
            # so we can get setting values on a as needed basis
            for group in self.config.childGroups():
                self.config.beginGroup(group)
                self.groups[group] = []
                for key in self.config.childKeys():
                    self.groups[group].append(key)
                    #print group + "::" + key + "::" + self.config.value(key).toString()
                self.config.endGroup()

    def get_setting(self, group, key):
        """
        Get the value of a ini setting
        Args:
            group: the string name of a group or section
            key: the string name of a key
        Returns:
            a list of two elements, first being the value, second being the value type
        """
        rval = [None, None]
        if len(self.groups) == 0:
            return rval
        self.config.beginGroup(group)
        qvar = self.config.value(key)
        str_val = qvar.toString()
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
        [group_name] -> [key_name] -> [value, value_type]
        """
        for group in self.config.childGroups():
            self.config.beginGroup(group)
            self.sections[group] = {}
            for key in self.config.childKeys():
                self.sections[group][key] = self.get_setting(group, key)
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
                    print "skip: %s" % option
                pass
            except:
                print "exception on %s!" % option
                dict1[option] = None
        return dict1


