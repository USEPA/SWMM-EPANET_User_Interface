import inspect
import traceback
from enum import Enum


class InputFile(object):
    """Input File Reader and Writer"""

    def __init__(self):
        self.sections = []
        self.file_name = ""
        """List of sections in the file"""

    def get_text(self):
        section_text_list = []
        try:
            for section in self.sections:
                try:
                    section_text_list.append(section.get_text())
                except Exception as e1:
                    section_text_list.append(str(e1) + '\n' + str(traceback.print_exc()))
            return '\n'.join(section_text_list)
        except Exception as e2:
            return(str(e2) + '\n' + str(traceback.print_exc()))

    def set_text(self, new_text):
        self.set_from_text_lines(new_text.splitlines())

    def read_file(self, file_name):
        try:
            with open(file_name, 'r') as inp_reader:
                self.file_name = file_name
                self.set_from_text_lines(iter(inp_reader))
        except Exception as e:
            print("Error reading {0}: {1}\n{2}".format(file_name, str(e), str(traceback.print_exc())))

    def set_from_text_lines(self, lines_iterator):
        """Read as a project file from lines of text.
            Args:
                lines_iterator (iterator): Produces lines of text formatted as input file.
        """
        section_index = 1
        section_name = ""
        section_whole = ""
        for line in lines_iterator:
            if line.startswith('['):
                if section_name:
                    self.add_section(section_name, section_whole, section_index)
                    section_index += 1
                section_name = line.rstrip()
                section_whole = line
            else:
                section_whole += line
        if section_name:
            self.add_section(section_name, section_whole, section_index)
            section_index += 1

    def add_section(self, section_name, section_text, section_index):
        attr_name = InputFile.printable_to_attribute(section_name)
        try:
            section_attr = self.__getattribute__(attr_name)
        except:
            section_attr = None

        if section_attr is None:  # if there is not a class associated with this name, read it as generic Section
            new_section = Section()
            new_section.name = section_name
            new_section.index = section_index
            new_section.value = section_text
            new_section.value_original = section_text
        else:
            section_class = type(section_attr)
            if section_class is list:
                new_section = Section()
                new_section.name = section_name
                new_section.index = section_index
                new_section.value_original = section_text
                section_list = []
                list_class = section_attr[0]
                for row in section_text.splitlines()[1:]:  # process each row after the one with the section name
                    if row.startswith(';'):                # if row starts with semicolon, the whole row is a comment
                        comment = Section()
                        comment.name = "Comment"
                        comment.index = section_index
                        comment.value = row
                        comment.value_original = row
                        section_list.append(comment)
                    else:
                        try:
                            if row.strip():
                                make_one = list_class()
                                make_one.set_text(row)
                                section_list.append(make_one)
                        except Exception as e:
                            print("Could not create object from row: " + row + "\n" + str(e))
                new_section.value = section_list
            else:
                new_section = section_class()
                if hasattr(new_section, "index"):
                    new_section.index = section_index
                if hasattr(new_section, "value"):
                    new_section.value = section_text
                if hasattr(new_section, "value_original"):
                    new_section.value_original = section_text
                try:
                    new_section.set_text(section_text)
                except Exception as e:
                    print("Could not call set_text on " + attr_name + " (" + section_name + "):\n" + str(e))
        if new_section is not None:
            self.sections.append(new_section)
            if section_attr is not None:
                self.__setattr__(attr_name, new_section)

    def find_section(self, section_title):
        for section in self.sections:
            if hasattr(section, "SECTION_NAME"):
                this_section_name = section.SECTION_NAME
            else:
                this_section_name = section.name
            if str(this_section_name).replace('[', '').replace(']', '').lower() == section_title.lower():
                return section
        return None

    @staticmethod
    def printable_to_attribute(name):
        """@param name is as it appears in text input file, return it formatted as a class attribute name"""
        return name.lower().replace(' ', '_').replace('[', '').replace(']', '')


class Section(object):
    """Any section or sub-section or value in an input file"""

    field_format = " {:19}\t{}"

    def __init__(self):
        self.name = "Unnamed"
        """Name of the item"""

        if hasattr(self, "SECTION_NAME"):
            self.name = self.SECTION_NAME

        self.value = ""
        """Current value of the item as it appears in an InputFile"""

        self.value_original = None
        """Original value of the item as read from an InputFile during this session"""

        self.index = -1
        """Index indicating the order in which this item was read
           (used for keeping items in the same order when written)"""

        self.comment = ""
        """A user-specified header and/or comment about the section"""

    def __str__(self):
        """Override default method to return string representation"""
        return self.get_text()

    def get_text(self):
        """Contents of this section formatted for writing to file"""
        txt = self._get_text_field_dict()
        if txt:
            return txt
        if isinstance(self.value, basestring):
            return self.value
        elif isinstance(self.value, (list, tuple)):
            text_list = [self.name]
            for item in self.value:
                text_list.append(str(item))
            return '\n'.join(text_list)
        elif self.value is None:
            return ''
        else:
            return str(self.value)

    def _get_text_field_dict(self):
        """ Get string representation of attributes represented in field_dict, if any.
            Private method intended for use by subclasses """
        if hasattr(self, "field_dict") and self.field_dict:
            text_list = []
            if self.name and self.name.startswith('['):
                text_list.append(self.name)
            for label, attr_name in self.field_dict.items():
                if label and attr_name and hasattr(self, attr_name):
                    attr_value = getattr(self, attr_name)
                    if isinstance(attr_value, Enum):
                        attr_value = attr_value.name
                    if attr_value:
                        text_list.append(self.field_format.format(label, attr_value))
            if text_list:
                return '\n'.join(text_list)
        return ''  # Did not find field values from field_dict to return

    def set_text(self, new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        self.value = new_text
        for line in new_text.splitlines():
            self.set_text_line(line)

    def set_text_line(self, line):
        """Set part of this section from one line of text.
            Args:
                line (str): One line of text formatted as input file.
        """
        # first split out any comment after a semicolon
        comment_split = str.split(line, ';', 1)
        if len(comment_split) == 2:
            line = comment_split[0]
            if self.comment:
                self.comment += '\n'
            self.comment += ';' + comment_split[1]

        if not line.startswith('[') and line.strip():
            # Set fields from field_dict if this section has one
            attr_name = ""
            attr_value = ""
            tried_set = False
            if hasattr(self, "field_dict") and self.field_dict:
                (attr_name, attr_value) = self.get_field_dict_value(line)
            else:  # This section does not have a field_dict, try to set its fields anyway
                line_list = line.split()
                if len(line_list) > 1:
                    if len(line_list) == 2:
                        test_attr_name = line_list[0].lower()
                        if hasattr(self, test_attr_name):
                            attr_name = test_attr_name
                            attr_value = line_list[1]
                    else:
                        for value_start in (1, 2):
                            for connector in ('', '_'):
                                test_attr_name = connector.join(line_list[:value_start]).lower()
                                if hasattr(self, test_attr_name):
                                    attr_name = test_attr_name
                                    attr_value = ' '.join(line_list[value_start:])
                                    break
            if attr_name:
                try:
                    tried_set = True
                    self.setattr_keep_type(attr_name, attr_value)
                except:
                    print("Section.text could not set " + attr_name)
            if not tried_set:
                print("Section.text skipped: " + line)

    def get_field_dict_value(self, line):
        """Search self.field_dict for attribute matching start of line.
            Args:
                line (str): One line of text formatted as input file, with field name followed by field value.
            Returns:
                Attribute name from field_dict and new attribute value from line as a tuple:
                (attr_name, attr_value) or (None, None) if not found.
        """
        if hasattr(self, "field_dict") and self.field_dict:
            lower_line = line.lower().strip()
            for dict_tuple in self.field_dict.items():
                key = dict_tuple[0]
                # if this line starts with this key followed by a space or tab
                if lower_line.startswith(key.lower()) and lower_line[len(key)] in (' ', '\t'):
                    test_attr_name = dict_tuple[1]
                    if hasattr(self, test_attr_name):
                        # return attribute name and value to be assigned
                        return(test_attr_name, line[len(key) + 1:].strip())
        return(None, None)

    def setattr_keep_type(self, attr_name, attr_value):
        """Set attribute attr_name = attr_value.
            If existing value of attr_name is int, float, bool, or Enum,
            try to remove spaces and convert attr_value to the same type before setting.
            Args:
                attr_name (str): Name of attribute of self to set.
                attr_value: New value to assign to attr_name.
        """
        try:
            old_value = getattr(self, attr_name, "")
            if isinstance(old_value, int):
                if isinstance(attr_value, str):
                    attr_value = attr_value.replace(' ', '')
                setattr(self, attr_name, int(attr_value))
            elif isinstance(old_value, float):
                if isinstance(attr_value, str):
                    attr_value = attr_value.replace(' ', '')
                setattr(self, attr_name, float(attr_value))
            elif isinstance(old_value, Enum):
                if not isinstance(attr_value, Enum):
                    try:
                        attr_value = type(old_value)[attr_value]
                    except KeyError:
                        attr_value = type(old_value)[attr_value.upper()]
                setattr(self, attr_name, attr_value)
            elif isinstance(old_value, bool):
                if not isinstance(attr_value, bool):
                    attr_value = str(attr_value).upper() not in ("NO", "FALSE")
                setattr(self, attr_name, attr_value)
            else:
                setattr(self, attr_name, attr_value)
        except:
            setattr(self, attr_name, attr_value)

