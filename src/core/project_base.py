import inspect
import traceback
from enum import Enum
from core.indexed_list import IndexedList
from .utility import ParseData


class ProjectBase(object):
    """
    Base class of SWMM and EPANET project classes that hold the data in an input sequence.
    Reading and writing the input sequence is handled in other classes.
    """

    def __init__(self):
        self.file_name = ""
        self.file_name_temporary = ""
        self.sections = []
        self.metric = False  # Both project types default to CFS, so metric defaults to False
        self.add_sections_from_attributes()

    def add_sections_from_attributes(self):
        """Add the sections that are attributes of the class to the list of sections."""
        for attr_value in vars(self).values():
            if isinstance(attr_value, Section) and attr_value not in self.sections:
                self.sections.append(attr_value)

    def find_section(self, section_name):
        """ Find an element of self.sections by name, ignoring square brackets and capitalization.
            Args:
                 section_name (str): Name of section to find.
        """
        compare_title = self.format_as_attribute_name(section_name).replace('_', '')
        if compare_title == 'timepatterns':
            compare_title = 'patterns'
        elif compare_title == 'unithydrographs':
            compare_title = 'hydrographs'
        elif compare_title == 'lidcontrols':
            compare_title = 'lid_controls'
        elif compare_title == 'lidusage':
            compare_title = 'lid_usage'

        for section in self.sections:
            this_section_name = ''
            if hasattr(section, "SECTION_NAME"):
                this_section_name = section.SECTION_NAME
            elif hasattr(section, "name"):
                this_section_name = section.name
            if this_section_name and self.format_as_attribute_name(str(this_section_name)) == compare_title:
                return section
        return None

    @staticmethod
    def format_as_attribute_name(name):
        """
        Format a name into a string that can be used as a Python attribute name.
        @param name (str) version of section or attribute name that may contain spaces (as in text input file)
        Returns (str) lowercase name with underscores instead of spaces and without square brackets.
        """
        return name.lower().replace(' ', '_').replace('[', '').replace(']', '')

    def all_nodes(self):
        lst_all = IndexedList([], ['name'])
        for section in self.nodes_groups():
            lst_all.extend(section.value)
        return lst_all

    def all_links(self):
        lst_all = IndexedList([], ['name'])
        for section in self.links_groups():
            lst_all.extend(section.value)
        return lst_all

    def find_link(self, link_name):
        for link_group in self.links_groups():
            if link_group and link_group.value:
                try:
                    return link_group.find_item(link_name)
                except:
                    return None

    def all_vertices(self, set_names=False):
        """ Return a list of Coordinate objects, one for each internal vertices of all links.
            If set_names is True, also set the name of each vertex to match its link. """
        lst_all = []
        for section in self.links_groups():
            for link in section.value:
                if set_names:
                    for vertex in link.vertices:
                        vertex.name = link.name
                lst_all.extend(link.vertices)
        return lst_all


class Section(object):
    """Any section or sub-section or value in an input sequence"""

    def __init__(self):
        """Initialize or reset section"""
        # if not hasattr(self, "name"):
        #     self.name = "Unnamed"

        if hasattr(self, "value") and type(self.value) is list:
            self.value = []
        else:
            self.value = ""
            """Current value of the item as it appears in an InputFile"""

        self.comment = ""
        """A user-specified header and/or comment about the section"""

        if hasattr(self, "DEFAULT_COMMENT"):
            self.comment = self.DEFAULT_COMMENT

    def setattr_keep_type(self, attr_name, attr_value):
        """ Set attribute attr_name = attr_value.
            If existing value of attr_name is int, float, bool, or Enum,
            try to remove spaces and convert attr_value to the same type before setting.
            Args:
                attr_name (str): Name of attribute of self to set.
                attr_value: New value to assign to attr_name.
        """
        try:
            old_value = getattr(self, attr_name, "")
            if type(old_value) == int:
                if isinstance(attr_value, str):
                    attr_value = attr_value.replace(' ', '')
                val, val_is_good = ParseData.intTryParse(attr_value)
                if val_is_good:
                    setattr(self, attr_name, val)
            elif type(old_value) == float:
                if isinstance(attr_value, str):
                    attr_value = attr_value.replace(' ', '')
                val, val_is_good = ParseData.floatTryParse(attr_value)
                if val_is_good:
                    setattr(self, attr_name, val)
            elif isinstance(old_value, Enum):
                val_is_good = True
                if not isinstance(attr_value, Enum):
                    enum_type = type(old_value)
                    try:
                        attr_value = enum_type[attr_value.replace('-', '_')]
                    except KeyError:
                        try:
                            attr_value = enum_type[attr_value.upper().replace('-', '_')]
                        except KeyError:
                            val_is_good = False
                            print("Did not find value '" + attr_value + "' in valid values for '" + attr_name + "'")
                if val_is_good:
                    setattr(self, attr_name, attr_value)
            elif type(old_value) == bool:
                if not isinstance(attr_value, bool):
                    attr_value = str(attr_value).upper() not in ("NO", "FALSE")
                setattr(self, attr_name, attr_value)
            else:
                setattr(self, attr_name, attr_value)
        except Exception as e:
            print("Exception setting {}: {}\n{}".format(attr_name, str(e), str(traceback.print_exc())))
            setattr(self, attr_name, attr_value)
            print(str(attr_name) + " now = " + str(getattr(self, attr_name)))

    def find_item(self, aName):
        if isinstance(self.value, list):
            for obj in self.value:
                if aName.upper() == obj.name.upper():
                    return obj
        return None

    def get_item(self, fname, fvalue):
        if not isinstance(self.value, list): return None
        if not self.value or len(self.value) == 0: return None
        if not hasattr(self.value[0], fname): return None
        for obj in self.value:
            if obj.__dict__[fname] == fvalue:
                return obj
        return None

class SectionAsList(Section):
    def __init__(self, section_name, section_comment=None):
        self.value = []
        if not section_name.startswith("["):
            section_name = '[' + section_name + ']'
        self.SECTION_NAME = section_name.upper()
        if section_comment:
            self.DEFAULT_COMMENT = section_comment
        Section.__init__(self)

    def find_item(self, aName):
        if aName:
            for obj in self.value:
                if aName.upper() == obj.name.upper():
                    return obj
        return None

    def get_item(self, fname, fvalue):
        if not self.value or len(self.value) == 0: return None
        if not hasattr(self.value[0], fname): return None
        for obj in self.value:
            if obj.__dict__[fname] == fvalue:
                return obj
        return None

# class SectionAsListGroupByID(SectionAsListOf):
