import inspect
import traceback
from enum import Enum
from core.project_base import ProjectBase, Section, SectionAsList
from core.indexed_list import IndexedList
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressDialog


class InputFileReader(object):
    """ Base class for reading input files """
    def __init__(self):
        self.input_err_msg = ""

    def read_file(self, project, file_name):
        """ Read the contents of file_name into project. """
        self.input_err_msg = ""
        try:
            """
            with open(file_name, 'r') as inp_reader:
                project.file_name = file_name
                self.set_from_text_lines(project, inp_reader.readlines())
            """
            import codecs
            with codecs.open(file_name, 'r', 'utf-8') as inp_reader:
                project.file_name = file_name
                self.set_from_text_lines(project, inp_reader.readlines())
                """
                task = TaskOpenInput('open file', project, inp_reader.readlines(), self.read_section)
                task.begun.connect(lambda: print('reading begins...'))
                task.progressChanged.connect(lambda: print(task.progress()))
                task.taskCompleted.connect(lambda: self.finished_reading(project))
                task.run()
                """
        except Exception as e:
            # print("Error reading {0}: {1}\n{2}".format(file_name, str(e), str(traceback.print_exc())))
            try:
                with codecs.open(file_name, 'r', 'latin1') as inp_reader:
                    project.file_name = file_name
                    # self.set_from_text_lines(project, iter(inp_reader))
                    self.set_from_text_lines(project, inp_reader.readlines())
            except Exception as e:
                self.input_err_msg = "File is probably not a valid project or input file."
                print("Error reading {0}: {1}\n{2}".format(file_name, str(e), str(traceback.print_exc())))
                if ".net" in file_name:
                    self.input_err_msg += "\nPlease note: binary (.net) input file is deprecated (not supported)."

    def set_from_text_lines(self, project, lines_iterator):
        """Read a project file from lines of text.
            Args:
                project (ProjectBase): Project object to read data into
                lines_iterator (iterator): Lines of text formatted as input file.
        """
        winform = True
        project.sections = []
        project.section_order = []
        section_name = ""
        section_whole = []
        total_count = len(lines_iterator)
        if winform:
            progress = QProgressDialog('Reading input...', 'Cancel', 1, total_count)
            progress.setWindowModality(Qt.WindowModal)
        line_ctr = 1
        for line in lines_iterator:
            if winform:
                if line_ctr % 100 == 0:
                    progress.setValue(line_ctr)
                if progress.wasCanceled():
                    break
            if line.lstrip().startswith('['):
                if section_name:
                    project.section_order.append(section_name.upper())
                    self.read_section(project, section_name, '\n'.join(section_whole))
                section_name = line.strip()
                section_whole = [section_name]
            elif line.strip():
                section_whole.append(line.rstrip())
            line_ctr = line_ctr + 1
        if winform:
            progress.setValue(total_count)

        if section_name:
            project.section_order.append(section_name.upper())
            self.read_section(project, section_name, '\n'.join(section_whole))
        project.add_sections_from_attributes()  # if there are any sections not in the file, add them to list
        self.finished_reading(project)

    def finished_reading(self, project):
        print ("Finished reading " + project.file_name)

    def read_section(self, project, section_name, section_text):
        """ Read the section named section_name whose complete text is section_text into project. """

        old_section = project.find_section(section_name)
        #if old_section:
        #    project.sections.remove(old_section)
        new_section = None
        attr_name = project.format_as_attribute_name(section_name)

        # special case for section 'lid_controls', because of multi-line structure, must strip out comment lines
        if attr_name == "lid_controls":
            # strip comment lines from section_text
            section_text_list = section_text.split('\n')
            string_without_comments = ""
            for line in section_text_list:
                if line[0] != ";":
                    string_without_comments += line + '\n'
            section_text = string_without_comments[:-1]

        reader_name = "read_" + attr_name
        if hasattr(self, reader_name):
            reader = self.__getattribute__(reader_name)
            try:
                new_section = reader.read(section_text)
            except Exception as e:
                print("Exception calling " + reader_name + " for " + section_name + ":\n" + str(e) +
                      '\n' + str(traceback.print_exc()))

        if new_section is None:
            if not section_name == '[END]':
                self.input_err_msg += '\n' + 'Unrecognized keyword (' + section_name + ').'
            print("Default Section for " + section_name)
            new_section = Section()
            new_section.SECTION_NAME = section_name
            if not section_name == section_text:
                new_section.value = section_text

        if "REACTION" in new_section.SECTION_NAME.upper() and old_section:
            for vmdata in old_section.metadata:
                old_section.__setattr__(vmdata.attribute, new_section.__getattribute__(vmdata.attribute))
            if new_section.value and len(new_section.value) > 0:
                for spec in new_section.value:
                    old_section.value.append(spec)
        else:
            project.__setattr__(attr_name, new_section)

        if old_section is None: #new_section not in project.sections:
            project.sections.append(new_section)


class SectionReader(object):
    """ Read a section or sub-section or value in an input file """

    def __init__(self):
        """Initialize section reader"""
        self.section_type = Section

    def read(self, new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        section = self.section_type()
        section.value = new_text
        for line in new_text.splitlines():
            self.set_text_line(section, line)
        return section

    @staticmethod
    def set_comment_check_section(section, line):
        """ Set comment to text after a semicolon and return the rest of the line.
            If the line is a section header (starts with open square bracket) then check against SECTION_NAME.
            If it matches, return empty string. If it does not match, raise ValueError.
            Args:
                section (Section): Section of input file to populate
                line (str): Text to search for a comment or section name.
        """
        comment_split = line.split(';', 1)
        if len(comment_split) == 2:  # Found a comment
            line = comment_split[0]
            this_comment = ';' + comment_split[1]
            #if section.value:
            if hasattr(section, "comment") and section.comment:
                # # Compare with existing comment and decide whether to discard one or combine them
                # omit_chars = " ;\t-_"
                # this_stripped = SectionReader.omit_these(this_comment, omit_chars).upper()
                # if len(this_stripped) == 0 and ("---" in this_comment) and not ("---" in section.comment):
                #     section.comment += '\n'  # Add dashed line on a new line if comment does not already have one
                # elif this_stripped in SectionReader.omit_these(section.comment, omit_chars).upper():
                #     this_comment = ''  # Already have this comment, don't add it again
                # elif hasattr(section, "DEFAULT_COMMENT") and section.comment == section.DEFAULT_COMMENT:
                #     section.comment = ''  # Replace default comment with the one we are reading
                # else:
                if not this_comment.lower() in section.comment.lower():
                    section.comment += '\n' + this_comment  # Separate from existing comment with newline
            elif hasattr(section, "description"):
                if not this_comment.lower() in section.description.lower():
                    if len(section.description) == 0:
                        section.description = this_comment
                    else:
                        section.description += '\n' + this_comment  # Separate from existing comment with newline
            else:
                section.comment = this_comment
                # section.description = this_comment
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
    def set_text_line(section, line):
        """Set part of this section from one line of text.
            Args:
                section (Section): Section of input file to populate
                line (str): One line of text formatted as input file.
        """
        line = SectionReader.set_comment_check_section(section, line)
        if line.strip():
            # Set fields from metadata if this section has metadata
            attr_name = ""
            attr_value = ""
            tried_set = False
            if hasattr(section, "metadata") and section.metadata:
                (attr_name, attr_value) = SectionReader.get_attr_name_value(section, line)
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
        """Search metadata of section for attribute with input_name matching start of line.
            Args:
                section (Section): data class
                line (str): One line of text formatted as input file, with field name followed by field value.
            Returns:
                Attribute name from metadata and new attribute value from line as a tuple:
                (attr_name, attr_value) or (None, None) if not found.
        """
        search_metadata = []
        if hasattr(section, "metadata") and section.metadata:
            search_metadata.append(section.metadata)
        # if hasattr(self, "metadata") and self.metadata:
        #     search_metadata.append(self.metadata)
        if search_metadata:
            lower_line = line.lower().strip()
            for metadata in search_metadata:
                for meta_item in metadata:
                    key = meta_item.input_name.lower()
                    if len(lower_line) > len(key):
                        # if this line starts with this key followed by a space or tab
                        if lower_line.startswith(key) and lower_line[len(key)] in (' ', '\t'):
                            if hasattr(section, meta_item.attribute):
                                # return attribute name and value specified on this line
                                return meta_item.attribute, line.strip()[len(key) + 1:].strip()
        return None, None


class SectionReaderAsList(SectionReader):
    """ Section reader that reads a section that contain a list of items """
    def __init__(self, section_name, list_type_reader, default_comment=None):
        if not section_name.startswith("["):
            section_name = '[' + section_name + ']'
        self.SECTION_NAME = section_name.upper()
        SectionReader.__init__(self)
        if isinstance(list_type_reader, type):
            self.list_type_reader = list_type_reader()
        else:
            self.list_type_reader = list_type_reader
        if default_comment:
            self.DEFAULT_COMMENT = default_comment

    def _init_section(self):
        section = self.section_type()
        # Set new section's SECTION_NAME if it has not already been set
        if not hasattr(section, "SECTION_NAME") and hasattr(self, "SECTION_NAME") and self.SECTION_NAME:
            section.SECTION_NAME = self.SECTION_NAME

        # TODO: figure out best way to tell whether this section can be indexed by name. For now we hard code names:
        index_these = ["[COORDINATES]", "[POLYGONS]", "[VERTICES]", "[SYMBOLS]", "[RAINGAGES]", "[SUBCATCHMENTS]",
                       "[HYDROGRAPHS]", "[LID_CONTROLS]", "[AQUIFERS]", "[SNOWPACKS]",
                       "[JUNCTIONS]", "[OUTFALLS]", "[DIVIDERS]", "[STORAGE]",
                       "[CONDUITS]", "[PUMPS]", "[ORIFICES]", "[WEIRS]", "[LANDUSES]", "[POLLUTANTS]",
                       "[PATTERNS]", "[CURVES]", "[TIMESERIES]", "[LABELS]", "[EVENTS]"]
        if hasattr(section, "SECTION_NAME") and section.SECTION_NAME in index_these:
            section.value = IndexedList([], ['name'])
        else:
            section.value = []
        return section

    def read(self, new_text):
        section = self._init_section()
        comment = ''
        keep_per_item_comment = True
        new_text = new_text.encode('ascii', errors='ignore')  # strip out non-ascii characters
        new_text = str(new_text, 'utf-8', 'ignore')
        if new_text.startswith('[LANDUSE'):
            keep_per_item_comment = True
        new_text = new_text.lstrip()  # xw20170328, remove heading white spaces indluing /n /t and spaces
        for line in new_text.splitlines()[1:]:  # process each line after the first one [section name]
            # if row starts with semicolon or is blank, add as a comment
            if line.lstrip().startswith(';') or not line.strip():
                if section.value or len(comment) > 0:  # If we have already added items to this section, add comment as a Section
                    # comment += line  xw20170327
                    if len(comment) > 0:  # xw20170327, added \n for multiple lines of comments within a section
                        comment += "\n" + line
                    else:
                        comment += line
                else:  # If we are still at the beginning of the section, set comment instead of adding a Section
                    if line.startswith(';;'):
                        self.set_comment_check_section(section, line)
                    elif keep_per_item_comment and line.startswith(';'):
                        comment = line
            else:
                if keep_per_item_comment and comment:
                    line = line + ' ' + comment
                    comment = ''
                self.read_item(section, line)
        return section

    def read_item(self, section, text):
        try:
            if self.list_type_reader:
                make_one = self.list_type_reader.read(text)
                if len(section.value) == 0:
                    if hasattr(make_one, "name"):
                        section.value = IndexedList([], ['name'])
            else:
                make_one = text

            if make_one is not None:
                section.value.append(make_one)
        except Exception as e:
            print("Could not create object from: " + text + '\n' + str(e) + '\n' + str(traceback.print_exc()))


class SectionReaderAsListGroupByID(SectionReaderAsList):
    """
    Reader for a section that contains items which may each span more than one line.
    Each item includes zero or more comment lines and one or more lines with the first field being the item ID.
    """

    def read(self, new_text):
        """
        Read a Section that contains items which may each span more than one line.
        Each item includes zero or more comment lines and one or more lines with the first field being the item ID.

        Parse new_text into a section comment (column headers) followed by items created by self.list_type_reader.
        section.value is created as a list of items read from new_text.
            Args:
                new_text (str): Text of whole section to parse into comments and a list of items.
            Returns:
                new self.section_type with value attribute populated from items in new_text.
        """
        section = self._init_section()
        lines = new_text.splitlines()
        self.set_comment_check_section(section, lines[0])  # Check first line against section name
        next_index = 1
        # expected_comment_lines = section.comment.splitlines()
        # for line_number in range(1, len(expected_comment_lines) + 1):  # Parse initial comment lines into comment
        #     if str(lines[line_number]).startswith(';'):
        #         # On multi-line initial comment, make sure last line is just dashes if the default comment was.
        #         # Otherwise it is kept out of the section comment and will be assigned to go with an item.
        #         if next_index < expected_comment_lines \
        #                 or len(Section.omit_these(lines[line_number], ";-_ \t")) == 0 \
        #                 or len(Section.omit_these(expected_comment_lines[line_number - 1], ";-_ \t")) > 0:
        #             self.set_comment_check_section(section, lines[line_number])
        #             next_index += 1
        #     else:
        #         break

        for next_index in range(1, len(lines) - 1):
            if not lines[next_index].strip().startswith(';'):
                break

        # If last comment line is not just a separator line, it is kept as the first item comment.
        if len(SectionReader.omit_these(lines[next_index-1], ";-_ \t")) > 0:
            next_index -= 1

        item_text = ""
        item_name = ""
        for line in lines[next_index:]:
            if line.startswith(';'):  # Found a comment, must be the start of a new item
                if len(item_name) > 0:
                    self.read_item(section, item_text)
                    item_text = ''
                elif item_text:
                    item_text += '\n'
                item_text += line
                item_name = ''
            else:
                id_split = line.split()
                if len(id_split) > 1:
                    new_item_name = id_split[0].strip()
                    if len(item_name) > 0:  # If we already read an ID that has not been saved to value yet
                        if new_item_name != item_name:  # If this item is not the same one we are already reading
                            self.read_item(section, item_text)
                            item_text = ''  # clear the buffer after using it to create/append an item
                    item_name = new_item_name
                    if item_text:
                        item_text += '\n'
                    item_text += line
        if item_text:
            self.read_item(section, item_text)
        return section
