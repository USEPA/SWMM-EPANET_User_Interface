class InputFile(object):
    """Input File Reader and Writer"""

    def __init__(self):
        self.sections = []
        """List of sections in the file"""

    @property
    def text(self):
        section_text_list = []
        for section in self.sections:
            section_text_list.append(str(section.text))
        return '\n'.join(section_text_list)

    @text.setter
    def text(self, new_text):
        self.set_from_text_lines(new_text.splitlines())

    def read_file(self, filename):
        with open(filename, 'r') as inp_reader:
            self.set_from_text_lines(iter(inp_reader))

    def set_from_text_lines(self, lines_iterator):
        """Read as a project file from the lines of text in @param lines_iterator provides"""
        section_index = 1
        section_name = ""
        section_whole = ""
        for line in lines_iterator:
            if line.startswith('['):
                if len(section_name) > 0:
                    self.add_section(section_name, section_whole, section_index)
                    section_index += 1
                section_name = line.rstrip()
                section_whole = line
            else:
                section_whole += line
        if len(section_name) > 0:
            self.add_section(section_name, section_whole, section_index)
            section_index += 1

    def add_section(self, section_name, section_text, section_index):
        new_section = None
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
                            if len(row.strip()) > 0:
                                make_one = list_class()
                                make_one.text(row)
                                section_list.append(make_one)
                        except:
                            make_one = None
                new_section = Section()
                new_section.name = section_name
                new_section.index = section_index
                new_section.value = section_list
                new_section.value_original = section_text
            else:
                new_section = section_class()
                if hasattr(new_section, "index"):
                    new_section.index = section_index
                if hasattr(new_section, "value"):
                    new_section.value = section_text
                if hasattr(new_section, "value_original"):
                    new_section.value_original = section_text
                if hasattr(new_section, "text"):
                    new_section.text = section_text
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

    def __init__(self):
        self.name = "Unnamed"
        """Name of the item"""

        self.value = ""
        """Current value of the item as it appears in an InputFile"""

        self.value_original = None
        """Original value of the item as read from an InputFile during this session"""

        self.index = -1
        """Index indicating the order in which this item was read
           (used for keeping items in the same order when written)"""

        self.comment = ""
        """A user-specified header and/or comment about the section"""

    @property
    def text(self):
        """Contents of this item formatted for writing to file"""

        if isinstance(self.value, basestring):
            return self.value
        elif isinstance(self.value, (list, tuple)):
            inp = self.name + '\n'
            for item in self.value:
                if hasattr(item, "text"):
                    inp += item.text + '\n'
                else:
                    inp += item + '\n'
            return inp
        elif self.value is None:
            return ''
        else:
            return self.value

    @text.setter
    def text(self, new_text):
        """Read this section from the text representation"""

        self.value = new_text
        for line in new_text.splitlines():
            comment_split = str.split(line, ';', 1)
            if len(comment_split) == 2:
                line = comment_split[0]
                if len(self.comment) > 0:
                    self.comment += '\n'
                self.comment += ';' + comment_split[1]
            if not line.startswith('['):
                if len(line.strip()) > 0:
                    line_list = line.split()
                    for name_last_word in range(0, 1):
                        attr_name = ''.join(line_list[:name_last_word]).lower()
                        if hasattr(self, attr_name):
                            try:
                                setattr(self, attr_name, ' '.join(line_list[name_last_word + 1:]))
                            except:
                                raise Exception("Unable to set attribute " + attr_name +
                                                " to " + ' '.join(line_list[name_last_word + 1:]))
