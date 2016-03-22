import inspect
import traceback
from enum import Enum


class InputFile(object):
    """Input File Reader and Writer"""

    def __init__(self):
        self.file_name = ""
        self.sections = []
        self.add_sections_from_attributes()

    def get_text(self):
        section_text_list = []
        try:
            for section in self.sections:
                try:
                    section_text = section.get_text().rstrip('\n')
                    if section_text:                               # Skip adding blank sections
                        section_text_list.append(section_text)
                except Exception as e1:
                    section_text_list.append(str(e1) + '\n' + str(traceback.print_exc()))
            return '\n\n'.join(section_text_list) + '\n'
        except Exception as e2:
            return(str(e2) + '\n' + str(traceback.print_exc()))

    def set_text(self, new_text):
        self.set_from_text_lines(new_text.splitlines())

    def read_file(self, file_name):
        try:
            with open(file_name, 'r') as inp_reader:
                self.set_from_text_lines(iter(inp_reader))
                self.file_name = file_name
        except Exception as e:
            print("Error reading {0}: {1}\n{2}".format(file_name, str(e), str(traceback.print_exc())))

    def write_file(self, file_name):
        if file_name:
            with open(file_name, 'w') as writer:
                writer.writelines(self.get_text())
                self.file_name = file_name

    def set_from_text_lines(self, lines_iterator):
        """Read as a project file from lines of text.
            Args:
                lines_iterator (iterator): Produces lines of text formatted as input file.
        """
        self.__init__()
        self.sections = []
        section_index = 1
        section_name = ""
        section_whole = []
        for line in lines_iterator:
            if line.startswith('['):
                if section_name:
                    self.add_section(section_name, '\n'.join(section_whole), section_index)
                    section_index += 1
                section_name = line.rstrip()
                section_whole = [section_name]
            elif line.strip():
                section_whole.append(line.rstrip())
        if section_name:
            self.add_section(section_name, '\n'.join(section_whole), section_index)
            section_index += 1
        self.add_sections_from_attributes()

    def add_sections_from_attributes(self):
        """Add the sections that are attributes of the class to the list of sections."""
        for attr_value in vars(self).itervalues():
            if isinstance(attr_value, Section) and attr_value not in self.sections:
                self.sections.append(attr_value)

    def add_section(self, section_name, section_text, section_index):
        attr_name = InputFile.printable_to_attribute(section_name)
        try:
            section_attr = self.__getattribute__(attr_name)
        except:
            section_attr = None

        new_section = self.find_section(section_name)

        if section_attr is None:  # if there is not a class associated with this name, read it as generic Section
            if new_section is None:
                new_section = Section()
                new_section.name = section_name
                new_section.index = section_index
                new_section.value = section_text
                new_section.value_original = section_text
        else:
            section_class = type(section_attr)
            if new_section is None:                 # This section has not yet been added to self.sections
                if section_class is SectionAsListOf or section_class is SectionAsListGroupByID:
                    new_section = section_attr      # Use the existing instance created during project init
                else:
                    try:
                        new_section = section_class()   # Create a new instance of this class
                    except Exception as e:
                        print("Could not create item of type " + str(section_class) + '\n' + str(e) +
                              '\n' + str(traceback.print_exc()))
        if new_section is not None:
            if hasattr(new_section, "index"):
                new_section.index = section_index
            if hasattr(new_section, "value_original"):
                new_section.value_original = section_text
            try:
                new_section.set_text(section_text)
            except Exception as e:
                print("Could not call set_text on " + attr_name + " (" + section_name + "):\n" + str(e) +
                      '\n' + str(traceback.print_exc()))
            if new_section not in self.sections:
                self.sections.append(new_section)
                if section_attr is not None:
                    self.__setattr__(attr_name, new_section)

    def find_section(self, section_title):
        """ Find an element of self.sections, ignoring square brackets and capitalization.
            Args:
                 section_title (str): Title of section to find.
        """
        compare_title = InputFile.printable_to_attribute(section_title)
        for section in self.sections:
            if hasattr(section, "SECTION_NAME"):
                this_section_name = section.SECTION_NAME
            else:
                this_section_name = section.name
            if InputFile.printable_to_attribute(str(this_section_name)) == compare_title:
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
        """Initialize or reset section"""
        if hasattr(self, "SECTION_NAME"):
            self.name = self.SECTION_NAME
        elif not hasattr(self, "name"):
            self.name = "Unnamed"

        if hasattr(self, "value") and type(self.value) is list:
            self.value = []
        else:
            self.value = ""
            """Current value of the item as it appears in an InputFile"""

        self.value_original = None
        """Original value of the item as read from an InputFile during this session"""

        self.index = -1
        """Index indicating the order in which this item was read
           (used for keeping items in the same order when written)"""

        self.comment = ""
        """A user-specified header and/or comment about the section"""
        
        if hasattr(self, "DEFAULT_COMMENT"):
            self.comment = self.DEFAULT_COMMENT

    def __str__(self):
        """Override default method to return string representation"""
        return self.get_text()

    def get_text(self):
        """Contents of this section formatted for writing to file"""
        txt = self._get_text_field_dict()
        if txt or txt == '':
            return txt
        if isinstance(self.value, basestring) and len(self.value) > 0:
            return self.value
        elif isinstance(self.value, (list, tuple)):
            text_list = [self.name]
            if self.comment:
                text_list.append(self.comment)
            for item in self.value:
                text_list.append(str(item))
            return '\n'.join(text_list)
        elif self.value is None:
            return ''
        else:
            return str(self.value)

    def _get_text_field_dict(self):
        """ Get string representation of attributes represented in field_dict, if any.
            Private method intended for use by subclasses
            Returns None if there is no field_dict, empty string if there is, but no attributes have values."""
        if hasattr(self, "field_dict") and self.field_dict:
            found_any = False
            text_list = []
            if self.name and self.name.startswith('['):
                text_list.append(self.name)
            if self.comment:
                text_list.append(self.comment)
                if self.comment != getattr(self, "DEFAULT_COMMENT", ''):
                    found_any = True
            for label, attr_name in self.field_dict.items():
                attr_line = self._get_attr_line(label, attr_name)
                if attr_line:
                    text_list.append(attr_line)
                    found_any = True
            if found_any:
                return '\n'.join(text_list)
            else:
                return ''
        return None  # Did not find field values from field_dict to return

    def _get_attr_line(self, label, attr_name):
        if label and attr_name and hasattr(self, attr_name):
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, Enum):
                attr_value = attr_value.name.replace('_', '-')
            if isinstance(attr_value, bool):
                if attr_value:
                    attr_value = "YES"
                else:
                    attr_value = "NO"
            if isinstance(attr_value, list):
                attr_value = ' '.join(attr_value)
            if attr_value or attr_value == 0:
                return (self.field_format.format(label, attr_value))
        else:
            return None

    def set_text(self, new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        self.__init__()  # Reset all values to defaults
        self.value = new_text
        for line in new_text.splitlines():
            self.set_text_line(line)

    def set_comment_check_section(self, line):
        """ Split any comment after a semicolon into self.comment and return the rest of the line.
            If the line is a section header (starts with open square bracket) then check against self.SECTION_NAME.
            If it matches, return empty string. If it does not match, raise ValueError.
            Args:
                line (str): Text to search for a comment or section name.
        """
        comment_split = str.split(line, ';', 1)
        if len(comment_split) == 2:  # Found a comment
            line = comment_split[0]
            this_comment = ';' + comment_split[1]
            if self.comment:
                # Compare with existing comment and decide whether to discard one or combine them
                omit_chars = " ;\t-_"
                this_stripped = self.omit_these(this_comment, omit_chars).upper()
                if len(this_stripped) == 0 and ("---" in this_comment) and not ("---" in self.comment):
                    self.comment += '\n'    # Add dashed line on a new line if self.comment does not already have one
                elif this_stripped in self.omit_these(self.comment, omit_chars).upper():
                    this_comment = ''       # Already have this comment, don't add it again
                elif hasattr(self, "DEFAULT_COMMENT") and self.comment == self.DEFAULT_COMMENT:
                    self.comment = ''       # Replace default comment with the one we are reading
                else:
                    self.comment += '\n'    # Separate from existing comment with newline
            self.comment += this_comment
        if line.startswith('['):
            if hasattr(self, "SECTION_NAME") and line.strip().upper() != self.SECTION_NAME:
                raise ValueError("Cannot set " + self.SECTION_NAME + " from: " + line.strip())
            else:
                line = ''
        return line  # Return the portion of the line that was not in the comment and was not a section header

    @staticmethod
    def omit_these(original, omit_chars):
        """Return original with any characters in omit_chars removed.
            Args:
                original (str): Text to search
                omit_chars (str): Characters to remove from original
        """
        return ''.join(c for c in original if c not in omit_chars)

    @staticmethod
    def match_omit(string_one, string_two, omit_chars):
        """Compare strings after removing omit_chars from both. True if they match.
            Args:
                string_one (str): One string to compare
                string_two (str): Other string to compare
                omit_chars (str): Characters to remove from both strings before comparing
        """
        return Section.omit_these(string_one, omit_chars) == Section.omit_these(string_two, omit_chars)

    @staticmethod
    def match_omit_nocase(string_one, string_two, omit_chars):
        """Compare strings after converting to upper case and removing omit_chars. True if they match.
            Args:
                string_one (str): One string to compare
                string_two (str): Other string to compare
                omit_chars (str): Characters to remove from both strings before comparing
        """
        return Section.match_omit(string_one.upper(), string_two.upper(), omit_chars.upper())

    def set_text_line(self, line):
        """Set part of this section from one line of text.
            Args:
                line (str): One line of text formatted as input file.
        """
        line = self.set_comment_check_section(line)
        if line.strip():
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
            if type(old_value) == int:
                if isinstance(attr_value, str):
                    attr_value = attr_value.replace(' ', '')
                setattr(self, attr_name, int(attr_value))
            elif type(old_value) == float:
                if isinstance(attr_value, str):
                    attr_value = attr_value.replace(' ', '')
                setattr(self, attr_name, float(attr_value))
            elif isinstance(old_value, Enum):
                if not isinstance(attr_value, Enum):
                    try:
                        attr_value = type(old_value)[attr_value.replace('-', '_')]
                    except KeyError:
                        attr_value = type(old_value)[attr_value.upper().replace('-', '_')]
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


class SectionAsListOf(Section):
    def __init__(self, section_name, list_type, section_comment=None):
        if not section_name.startswith("["):
            section_name = '[' + section_name + ']'
        self.SECTION_NAME = section_name.upper()
        if section_comment:
            self.DEFAULT_COMMENT = section_comment
        Section.__init__(self)
        self.list_type = list_type

    def set_text(self, new_text):
        self.value = []
        for line in new_text.splitlines()[1:]:            # process each line after the first one [section name]
            if line.startswith(';') or not line.strip():  # if row starts with semicolon or is blank, add as a comment
                if self.value:  # If we have already added items to this section, add comment as a Section
                    comment = Section()
                    comment.name = "Comment"
                    comment.value = line
                    self.value.append(comment)
                else:  # If we are still at the beginning of the section, set self.comment instead of adding a Section
                    self.set_comment_check_section(line)
            else:
                try:
                    if self.list_type is basestring:
                        make_one = line
                    else:
                        make_one = self.list_type()
                        make_one.set_text(line)
                    self.value.append(make_one)
                except Exception as e:
                    print("Could not create object from: " + line + '\n' + str(e) + '\n' + str(traceback.print_exc()))

    def get_text(self):
        """Contents of this section formatted for writing to file"""
        if self.value \
           or (self.comment and (not hasattr(self, "DEFAULT_COMMENT") or self.comment != self.DEFAULT_COMMENT)):
            text_list = [self.name]
            if self.comment:
                text_list.append(self.comment)
            for item in self.value:
                item_str = str(item)
                # Skip blank items unless they are a blank comment, those are purposely blank lines
                # if item_str.strip() or isinstance(item, basestring) or (isinstance(item, Section) and item.name == "Comment"):
                text_list.append(item_str.rstrip('\n'))  # strip any newlines from end of each item
            return '\n'.join(text_list)
        else:
            return ''


class SectionAsListGroupByID(SectionAsListOf):

    def set_text(self, new_text):
        """
        Parse new_text into a section comment (column headers) followed by items of type self.list_type.
        Each item includes zero or more comment lines and one or more lines with the first field being the item ID.
        new_text is split into items (comment plus lines starting with the same ID).
        self.value is created as a list of self.list_type.
        Each item text is made into an item_type using a constructor that takes a string, then added to self.value.
            Args:
                new_text (str): Text of whole section to parse into comments and a list of items.
        """
        self.value = []
        lines = new_text.splitlines()
        self.set_comment_check_section(lines[0])                  # Check first line against section name
        next_index = 1
        expected_comment_lines = self.comment.splitlines()
        for line_number in range(1, len(expected_comment_lines) + 1):  # Parse initial comment lines into self.comment
            if str(lines[line_number]).startswith(';'):
                # On multi-line initial comment, make sure last line is just dashes if the default comment was.
                # Otherwise it is kept out of the section comment and will be assigned to go with an item.
                if next_index < expected_comment_lines \
                   or len(Section.omit_these(lines[line_number], ";-_ \t")) == 0 \
                   or len(Section.omit_these(expected_comment_lines[line_number - 1], ";-_ \t")) > 0:
                    self.set_comment_check_section(lines[line_number])
                    next_index += 1
            else:
                break

        item_text = ""
        item_id = ""
        for line in lines[next_index:]:
            if line.startswith(';'):    # Found a comment, must be the start of a new item
                if item_text:
                    self.value.append(self.list_type(item_text))
                item_text = line
                item_id = ""
            else:
                id_split = line.split()
                if len(id_split) > 1:
                    new_item_id = id_split[0].strip()
                    if len(item_id) > 0:            # If we already read an ID that has not been saved to value yet
                        if new_item_id != item_id:  # If this item is not the same one we are already reading
                            try:                    # then save the one we have been reading since we have read it all
                                self.value.append(self.list_type(item_text))
                            except Exception as ex:
                                raise Exception("Create: {}\nfrom string:{}\n{}\n{}".format(self.list_type.__name__,
                                                                                            item_text,
                                                                                            str(ex),
                                                                                            str(traceback.print_exc())))
                            item_text = ""          # clear the buffer after using it to create/append an item
                    item_id = new_item_id
                    if item_text:
                        item_text += '\n'
                    item_text += line
        if item_text:
            self.value.append(self.list_type(item_text))

