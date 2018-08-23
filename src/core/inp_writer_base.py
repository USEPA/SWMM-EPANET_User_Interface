import inspect
import traceback
from enum import Enum
from core.project_base import ProjectBase, Section, SectionAsList


class InputFileWriterBase(object):
    """ Base class common to SWMM and EPANET.
        Creates and saves text version of model input file *.inp.
    """
    def as_text(self, project, derived_sections):
        """
        Text version of project, suitable for saving to *.inp file.
        Args:
            project (ProjectBase): Project data to serialize as text.
            derived_sections (dict): Section names and full text to insert or append to the ones in self.sections
        Returns:
            string containing data from the specified project in *.inp format.
        """
        if derived_sections:
            # Make a local copy that we remove items from as we use them
            derived_sections = derived_sections.copy()
        section_text_list = []
        try:
            if hasattr(project, "section_order"):
                section_order = project.section_order
            else:
                section_order = None
            for section in project.sections:
                attr_name = ''
                section_name = ''
                if hasattr(section, "SECTION_NAME"):
                    section_name = section.SECTION_NAME
                    if "subcentroid" in section_name.lower() or "sublink" in section_name.lower():
                        continue
                    attr_name = "write_" + project.format_as_attribute_name(section_name)
                if section_name and "CALIBRATION" in section_name.upper():
                    # EPANET doesn't recognize [CALIBRATIONS] section
                    # it is for internal use at run time
                    continue
                if hasattr(self, attr_name):
                    writer = self.__getattribute__(attr_name)
                elif hasattr(section, "value") and isinstance(section.value, str):
                    writer = SectionWriter()
                else:
                    writer = SectionWriterAsList(section_name, SectionWriter(), None)
                try:
                    section_text = writer.as_text(section).rstrip('\n')
                    if section_text and section_text != '[END]':                    # Skip adding blank sections
                        section_text_list.append(section_text)

                    # If we have a section order and derived sections to insert,
                    # insert any derived sections that come directly after this section.
                    if section_order and section_name and derived_sections:
                        try:
                            index = section_order.index(section_name.upper()) + 1
                            next_section = section_order[index]
                            while next_section:
                                next_derived_section = derived_sections.pop(next_section, None)
                                if next_derived_section:
                                    section_text_list.append(next_derived_section)
                                    index += 1
                                    next_section = section_order[index]
                                else:
                                    next_section = None
                        except:
                            pass
                except Exception as e1:
                    section_text_list.append(str(e1) + '\n' + str(traceback.print_exc()))
            for section_text in derived_sections.values(): #.items()
                section_text_list.append(section_text)
            return '\n\n'.join(section_text_list) + '\n'
        except Exception as e2:
            return str(e2) + '\n' + str(traceback.print_exc())

    def write_file(self, project, file_name):
        """
        Save text file version of project in *.inp file format in file_name.
        Args:
            project (ProjectBase): Project data to serialize as text.
            file_name (str): full path and file name to save in.
        Returns:
            string containing data from the specified project in *.inp format.
        """
        if file_name:
            with open(file_name, 'w') as writer:
                writer.writelines(self.as_text(project))
                # project.file_name = file_name


class SectionWriter(object):
    """ Base class for writing a section or sub-section or value to an input file """

    field_format = " {:19}\t{}"  # Default field format

    @staticmethod
    def as_text(section):
        """ Format contents of this section for writing to inp file.
            Args:
                section (Section): section of input sequence
        """
        if isinstance(section, str):
            return section
        txt = SectionWriter._get_text_using_metadata(section)
        if txt or txt == '':
            return txt
        if isinstance(section.value, str) and len(section.value) > 0:
            return section.value
        elif isinstance(section.value, (list, tuple)):
            text_list = []
            if hasattr(section, "SECTION_NAME") and section.SECTION_NAME:
                text_list.append(section.SECTION_NAME)
            if section.comment:
                text_list.append(section.comment)
            for item in section.value:
                text_list.append(str(item))
            return '\n'.join(text_list)
        elif section.value is None:
            return ''
        else:
            return str(section.value)

    @staticmethod
    def _get_text_using_metadata(section):
        """ Get input file representation of section using attributes represented in metadata, if any.
            Private method intended for use by subclasses.
            Returns empty string if the attributes in metadata have no values.
            Returns None if there is no appropriate metadata."""
        if hasattr(section, "metadata") and section.metadata:
            found_any = False
            text_list = []
            if hasattr(section, "SECTION_NAME"):
                text_list.append(section.SECTION_NAME)
            if section.comment:
                text_list.append(section.comment)
                if section.comment != getattr(section, "DEFAULT_COMMENT", ''):
                    found_any = True
            for metadata_item in section.metadata:
                attr_line = SectionWriter._get_attr_line(section, metadata_item.input_name, metadata_item.attribute)
                if attr_line:
                    text_list.append(attr_line)
                    found_any = True
            if found_any:
                return '\n'.join(text_list)
            return ''
        return None

    @staticmethod
    def _get_attr_line(section, label, attr_name):
        """ Generate one line of an input sequence which specifies the label and value of the attribute attr_name
        Args:
            section (Section): project section that may contain a value for the attribute named attr_name.
            label (str): label that will appear in the returned line.
            attr_name (str): name of attribute to get the value of. If attribute is not present, None is returned.
         """
        if label and attr_name and hasattr(section, attr_name):
            attr_value = getattr(section, attr_name)
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
                return SectionWriter.field_format.format(label, attr_value)
        else:
            return None

    @staticmethod
    def yes_no(true_false):
        if true_false:
            return "YES"
        else:
            return "NO"


class SectionWriterAsList(SectionWriter):
    """ Section writer that can serialize a section that contains a list of items. """
    def __init__(self, section_name, list_type_writer, section_comment):
        """
        Create a section writer that can serialize a section that contains a list of items.
        Args:
            section_name (str): Name of section. Square brackets will be added if not already present.
            list_type_writer (type or instance): Writer that can serialize items in the section.
            section_comment (str): Default comment lines that appear at the beginning of the section. Can be None.
        """
        if list_type_writer is None:
            print ("No list_type_writer specified for " + section_name)
        if not section_name.startswith("["):
            section_name = '[' + section_name + ']'
        self.SECTION_NAME = section_name.upper()
        SectionWriter.__init__(self)
        if isinstance(list_type_writer, type):
            self.list_type_writer = list_type_writer()
        else:
            self.list_type_writer = list_type_writer

        if section_comment:
            self.DEFAULT_COMMENT = section_comment

    def as_text(self, section):
        """ Format contents of this section for writing to inp file.
            Args:
                section (Section): section of input sequence that contains a list of items in its value attribute
        """
        if section.value or (section.comment and (not hasattr(section, "DEFAULT_COMMENT") or
                                                      section.comment != section.DEFAULT_COMMENT)):
            text_list = []
            if hasattr(section, "SECTION_NAME") and section.SECTION_NAME and section.SECTION_NAME != "Comment":
                text_list.append(section.SECTION_NAME)
            elif hasattr(self, "SECTION_NAME") and self.SECTION_NAME and self.SECTION_NAME != "Comment":
                text_list.append(self.SECTION_NAME)
            if section.comment:
                text_list.append(section.comment)
            elif hasattr(self, "DEFAULT_COMMENT") and self.DEFAULT_COMMENT:
                text_list.append(self.DEFAULT_COMMENT)
            if isinstance(section.value, str):
                text_list.append(section.value.rstrip('\n'))  # strip any newlines from end of each item
            else:
                for item in section.value:
                    if item is not None:
                        if hasattr(item, "description"):
                            if len(item.description) > 0 and section.SECTION_NAME != '[COORDINATES]' and \
                                                             section.SECTION_NAME != '[SUBAREAS]' and \
                                                             section.SECTION_NAME != '[LOSSES]' and \
                                                             section.SECTION_NAME != '[SYMBOLS]' and \
                                                             section.SECTION_NAME != '[STATUS]' and \
                                                             section.SECTION_NAME != '[EMITTERS]' and \
                                                             section.SECTION_NAME != '[PATTERNS]' and \
                                                             section.SECTION_NAME != '[CURVES]':
                                if item.description[0] == ';':
                                    text_list.append(item.description)
                                else:
                                    text_list.append(';' + item.description)
                        if isinstance(item, str):
                            item_str = item
                        else:
                            if hasattr(item, "SECTION_NAME") and item.SECTION_NAME == "Comment":  #xw9/13/2016
                                item_str = item.value
                            else:
                                item_str = self.list_type_writer.as_text(item)
                        if item_str is not None and item_str:
                            # Uncomment below to skip blank items unless they are a blank comment, those are purposely blank
                            # if item_str.strip() or isinstance(item, str) or
                            #  (isinstance(item, Section) and item.SECTION_NAME == "Comment"):
                            text_list.append(item_str.rstrip('\n'))  # strip any newlines from end of each item
            return '\n'.join(text_list)
        else:
            return ''
