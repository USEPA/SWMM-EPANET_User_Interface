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

    def to_inp(self):
        """format contents of this item for writing to file"""
        return self.value

