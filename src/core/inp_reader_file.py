import inspect
import traceback
from enum import Enum
from core.project import Section, SectionAsListOf


class InputReaderFile(object):
    """Input File Reader"""

    @staticmethod
    def read_file(self, file_name):
        try:
            with open(file_name, 'r') as inp_reader:
                self.set_from_text_lines(iter(inp_reader))
                self.file_name = file_name
        except Exception as e:
            print("Error reading {0}: {1}\n{2}".format(file_name, str(e), str(traceback.print_exc())))

    @staticmethod
    def set_from_text_lines(project, lines_iterator):
        """Read as a project file from lines of text.
            Args:
                project (Project): Project object to read data into
                lines_iterator (iterator): Lines of text formatted as input file.
        """
        section_name = ""
        section_whole = []
        for line in lines_iterator:
            if line.lstrip().startswith('['):
                if section_name:
                    project.add_section(section_name, '\n'.join(section_whole))
                section_name = line.strip()
                section_whole = [section_name]
            elif line.strip():
                section_whole.append(line.rstrip())
        if section_name:
            project.add_section(section_name, '\n'.join(section_whole))
        InputReaderFile.add_sections_from_attributes(project)

    @staticmethod
    def add_sections_from_attributes(project):
        """Add the sections that are attributes of the class to the list of sections."""
        for attr_value in vars(project).values():
            if isinstance(attr_value, Section) and attr_value not in project.sections:
                project.sections.append(attr_value)

    @staticmethod
    def add_section(project, section_name, section_text):
        attr_name = project.format_as_attribute_name(section_name)
        try:
            section_attr = project.__getattribute__(attr_name)
        except:
            section_attr = None

        new_section = project.find_section(section_name)

        if section_attr is None:  # if there is not a class associated with this name, read it as generic Section
            print("Default Section for " + section_name)
            if new_section is None:
                new_section = Section()
                new_section.SECTION_NAME = section_name
                new_section.value = section_text
        else:
            section_class = type(section_attr)
            if new_section is None:  # This section has not yet been added to self.sections
                if section_class is SectionAsListOf or section_class is SectionAsListGroupByID:
                    new_section = section_attr  # Use the existing instance created during project init
                else:
                    try:
                        new_section = section_class()  # Create a new instance of this class
                    except Exception as e:
                        print("Could not create item of type " + str(section_class) + '\n' + str(e) +
                              '\n' + str(traceback.print_exc()))
        if new_section is not None:
            try:
                new_section.set_text(section_text)
            except Exception as e:
                print("Could not call set_text on " + attr_name + " (" + section_name + "):\n" + str(e) +
                      '\n' + str(traceback.print_exc()))
            if new_section not in project.sections:
                project.sections.append(new_section)
                if section_attr is not None:
                    project.__setattr__(attr_name, new_section)


class SectionReader(object):
    """Any section or sub-section or value in an input file"""

    def set_text(section, new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        section.__init__()  # Reset all values to defaults
        section.value = new_text
        for line in new_text.splitlines():
            SectionReader.set_text_line(section, line)

    @staticmethod
    def set_comment_check_section(section, line):
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
            if section.comment:
                # Compare with existing comment and decide whether to discard one or combine them
                omit_chars = " ;\t-_"
                this_stripped = SectionReader.omit_these(this_comment, omit_chars).upper()
                if len(this_stripped) == 0 and ("---" in this_comment) and not ("---" in section.comment):
                    section.comment += '\n'  # Add dashed line on a new line if self.comment does not already have one
                elif this_stripped in SectionReader.omit_these(section.comment, omit_chars).upper():
                    this_comment = ''  # Already have this comment, don't add it again
                elif hasattr(section, "DEFAULT_COMMENT") and section.comment == section.DEFAULT_COMMENT:
                    section.comment = ''  # Replace default comment with the one we are reading
                else:
                    section.comment += '\n'  # Separate from existing comment with newline
            section.comment += this_comment
        if line.startswith('['):
            if hasattr(section, "SECTION_NAME") and line.strip().upper() != section.SECTION_NAME.upper():
                raise ValueError("Cannot set " + section.SECTION_NAME + " from: " + line.strip())
            else:  # subsection does not have a SECTION_NAME or SECTION_NAME matches: no further processing needed
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
        return SectionReader.omit_these(string_one, omit_chars) == SectionReader.omit_these(string_two, omit_chars)

    @staticmethod
    def match_omit_nocase(string_one, string_two, omit_chars):
        """Compare strings after converting to upper case and removing omit_chars. True if they match.
            Args:
                string_one (str): One string to compare
                string_two (str): Other string to compare
                omit_chars (str): Characters to remove from both strings before comparing
        """
        return SectionReader.match_omit(string_one.upper(), string_two.upper(), omit_chars.upper())

    def matches(section, other):
        """Test whether this section and other have the same contents ignoring case, whitespace, order of lines.
        Args:
            other: a Section or anything with a get_text method or will be converted to string with str()
        """
        if other is None:
            return False
        if hasattr(other, "get_text"):
            other_str = other.get_text()
        else:
            other_str = str(other)
        this_str = section.get_text()
        # other_str and this_str are the raw versions, next we process out unimportant differences
        if other_str and this_str:  # Both are not empty
            # Split into lines, strip comments, and keep only lines that are not blank
            # this_sorted = [s for s in this_str.upper().splitlines() if (s.strip() and not s.startswith(';'))]
            # other_sorted = [s for s in other_str.upper().splitlines() if (s.strip() and not s.startswith(';'))]
            this_sorted = [s.split(';')[0].strip() for s in this_str.upper().splitlines() if s.split(';')[0].strip()]
            other_sorted = [s.split(';')[0].strip() for s in other_str.upper().splitlines() if s.split(';')[0].strip()]
            if len(this_sorted) != len(other_sorted):
                return False  # Different number of significant lines means they do not match.
            # sort lines because we don't care if the same options are in a different order
            this_sorted.sort()
            other_sorted.sort()
            for (this_line, other_line) in zip(this_sorted, other_sorted):
                # Compare each line by replacing any group of spaces and tabs with one space
                this_line_split = this_line.split()
                other_line_split = other_line.split()
                if len(this_line_split) != len(other_line_split):
                    return False  # Different number of significant columns in a line means they do not match
                this_line_joined = ' '.join(this_line_split)
                other_line_joined = ' '.join(other_line_split)
                if this_line_joined != other_line_joined:
                    # If whole line does not match, check for match of each field
                    for (this_field, other_field) in zip(this_line_split, other_line_split):
                        if this_field != other_field:
                            try:  # Check for match when converted to floating point numbers
                                this_float = float(this_field)
                                other_float = float(other_field)
                                if this_float != other_float:
                                    return False
                            except ValueError:
                                return False
        elif other_str or this_str:
            return False  # Only one is empty, so they don't match
        return True

    @staticmethod
    def set_text_line(section, line):
        """Set part of this section from one line of text.
            Args:
                line (str): One line of text formatted as input file.
        """
        line = SectionReader.set_comment_check_section(section, line)
        if line.strip():
            # Set fields from metadata if this section has metadata
            attr_name = ""
            attr_value = ""
            tried_set = False
            if hasattr(section, "metadata") and section.metadata:
                (attr_name, attr_value) = SectionReader.get_attr_name_value(line)
            else:  # This section does not have metadata, try to set its fields anyway
                line_list = line.split()
                if len(line_list) > 1:
                    if len(line_list) == 2:
                        test_attr_name = line_list[0].lower()
                        if hasattr(section, test_attr_name):
                            attr_name = test_attr_name
                            attr_value = line_list[1]
                    else:
                        for value_start in (1, 2):
                            for connector in ('', '_'):
                                test_attr_name = connector.join(line_list[:value_start]).lower()
                                if hasattr(section, test_attr_name):
                                    attr_name = test_attr_name
                                    attr_value = ' '.join(line_list[value_start:])
                                    break
            if attr_name:
                try:
                    tried_set = True
                    section.setattr_keep_type(attr_name, attr_value)
                except:
                    print("Section.text could not set " + attr_name)
            if not tried_set:
                print("Section.text skipped: " + line)

    @staticmethod
    def get_attr_name_value(section, line):
        """Search self.metadata for attribute with input_name matching start of line.
            Args:
                line (str): One line of text formatted as input file, with field name followed by field value.
            Returns:
                Attribute name from metadata and new attribute value from line as a tuple:
                (attr_name, attr_value) or (None, None) if not found.
        """
        if hasattr(section, "metadata") and section.metadata:
            lower_line = line.lower().strip()
            for meta_item in section.metadata:
                key = meta_item.input_name.lower()
                if len(lower_line) > len(key):
                    # if this line starts with this key followed by a space or tab
                    if lower_line.startswith(key) and lower_line[len(key)] in (' ', '\t'):
                        if hasattr(section, meta_item.attribute):
                            # return attribute name and value specified on this line
                            return (meta_item.attribute, line.strip()[len(key) + 1:].strip())
        return (None, None)

    @staticmethod
    def read_section_as_list_of(section, new_text):
        section.value = []
        for line in new_text.splitlines()[1:]:  # process each line after the first one [section name]
            if line.startswith(';') or not line.strip():  # if row starts with semicolon or is blank, add as a comment
                if section.value:  # If we have already added items to this section, add comment as a Section
                    comment = Section()
                    comment.SECTION_NAME = "Comment"
                    comment.value = line
                    section.value.append(comment)
                else:  # If we are still at the beginning of the section, set self.comment instead of adding a Section
                    section.set_comment_check_section(line)
            else:
                try:
                    if section.list_type is basestring:
                        make_one = line
                    else:
                        make_one = section.list_type()
                        make_one.set_text(line)
                    section.value.append(make_one)
                except Exception as e:
                    print("Could not create object from: " + line + '\n' + str(e) + '\n' + str(traceback.print_exc()))


    @staticmethod
    def read_section_as_list_group_by_id(section, new_text):
        """
        Read a Section that contains items which may each span more than one line.
        Each item includes zero or more comment lines and one or more lines with the first field being the item ID.

        Parse new_text into a section comment (column headers) followed by items of type self.list_type.
        section.value is created as a list of items of self.list_type.
        section.list_type was set by the SectionAsListOf constructor.
        Each item text is made into a self.list_type using a constructor that takes a string, then added to self.value.
            Args:
                new_text (str): Text of whole section to parse into comments and a list of items.
        """
        section.value = []
        lines = new_text.splitlines()
        section.set_comment_check_section(lines[0])  # Check first line against section name
        next_index = 1
        expected_comment_lines = section.comment.splitlines()
        for line_number in range(1, len(expected_comment_lines) + 1):  # Parse initial comment lines into self.comment
            if str(lines[line_number]).startswith(';'):
                # On multi-line initial comment, make sure last line is just dashes if the default comment was.
                # Otherwise it is kept out of the section comment and will be assigned to go with an item.
                if next_index < expected_comment_lines \
                        or len(Section.omit_these(lines[line_number], ";-_ \t")) == 0 \
                        or len(Section.omit_these(expected_comment_lines[line_number - 1], ";-_ \t")) > 0:
                    section.set_comment_check_section(lines[line_number])
                    next_index += 1
            else:
                break

        item_text = ""
        item_id = ""
        for line in lines[next_index:]:
            if line.startswith(';'):  # Found a comment, must be the start of a new item
                if len(item_id) > 0:
                    section.value.append(section.list_type(item_text))
                    item_text = ''
                elif item_text:
                    item_text += '\n'
                item_text += line
                item_id = ''
            else:
                id_split = line.split()
                if len(id_split) > 1:
                    new_item_id = id_split[0].strip()
                    if len(item_id) > 0:  # If we already read an ID that has not been saved to value yet
                        if new_item_id != item_id:  # If this item is not the same one we are already reading
                            try:  # then save the one we have been reading since we have read it all
                                section.value.append(section.list_type(item_text))
                            except Exception as ex:
                                raise Exception("Create: {}\nfrom string:{}\n{}\n{}".format(self.list_type.__name__,
                                                                                            item_text,
                                                                                            str(ex),
                                                                                            str(traceback.print_exc())))
                            item_text = ''  # clear the buffer after using it to create/append an item
                    item_id = new_item_id
                    if item_text:
                        item_text += '\n'
                    item_text += line
        if item_text:
            section.value.append(section.list_type(item_text))

