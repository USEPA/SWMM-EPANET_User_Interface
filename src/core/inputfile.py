class InputFile(object):
    """Input File Reader and Writer"""

    def __init__(self, filename):
        if self.section_types is None:
            self.section_types = {}
        self.sections = []
        """List of sections in the file"""

        inp_reader = open(filename, 'r')
        sections_read = 0
        section_name = ""
        section_whole = ""
        for line in iter(inp_reader):
            if line.startswith('['):
                if len(section_name) > 0:
                    sections_read += 1
                    self.add_section(section_name, section_whole, sections_read)
                section_name = line.rstrip()
                section_whole = line
            else:
                section_whole += line
        inp_reader.close()
        if len(section_name) > 0:
            sections_read += 1
            self.add_section(section_name, section_whole, sections_read)

    def add_section(self, section_name, section_body, section_index):
        section_class = self.section_types.get(section_name)
        if section_class is None:
            section_class = Section
        if isinstance(section_class, list):
            section_list = []
            section_class = section_class[0]
            for row in section_body.splitlines():
                try:
                    make_one = section_class(section_name, row, None, section_index)
                except:
                    make_one = None
                if make_one is not None:
                    section_list.append(make_one)
            self.sections.append(Section(section_name, section_list))
        else:
            self.sections.append(section_class(section_name, section_body, None, section_index))

    def to_inp(self):
        build_str = ""
        for section in self.sections:
            build_str += section.to_inp()
        return build_str


class Section(object):
    """Any section or sub-section or value in an input file"""

    def __init__(self, name, value, value_default, index):
        self.name = name
        """Name of the item"""

        self.value = value
        """Current value of the item"""

        self.value_default = value_default
        """Default value of the item if not specified"""

        self.value_original = value
        """Original value of the item as read from a file during this session"""

        self.index = index
        """Index indicating the order in which this item was read
           (used for keeping items in the same order when written)"""

        if isinstance(value, str):
            self.set_from_text(value)

    def set_from_text(self, text):
        for line in text.splitlines():
            if not line.startswith(';', '['):
                line_list = line.split()
                for name_last_word in range(0, 1):
                    attr_name = ''.join(line_list[:name_last_word]).lower()
                    if hasattr(self, attr_name):
                        try:
                            setattr(self, attr_name, ' '.join(line_list[name_last_word + 1:]))
                        except:
                            raise Exception("Unable to set attribute " + attr_name +
                                            " to " + ' '.join(line_list[name_last_word + 1:]))

    def to_inp(self):
        """format contents of this item for writing to file"""
        return self.value

