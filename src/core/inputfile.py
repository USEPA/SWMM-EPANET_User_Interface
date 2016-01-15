class InputFile(object):
    """Input File Reader and Writer"""

    def __init__(self):
        self.sections = []
        """List of sections in the file"""

    def read_file(self, filename):
        inp_reader = open(filename, 'r')
        section_index = 1
        section_name = ""
        section_whole = ""
        for line in iter(inp_reader):
            if line.startswith('['):
                if len(section_name) > 0:
                    self.add_section(section_name, section_whole, section_index)
                    section_index += 1
                section_name = line.rstrip()
                section_whole = line
            else:
                section_whole += line
        inp_reader.close()
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
        if section_attr is None:
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
                for row in section_text.splitlines()[1:]:
                    try:
                        make_one = list_class()
                        make_one.set_from_text(row)
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
                if hasattr(new_section, "set_from_text") & callable(new_section.set_from_text):
                    new_section.set_from_text(section_text)
        if new_section is not None:
            self.sections.append(new_section)
            if section_attr is not None:
                self.__setattr__(attr_name, new_section)

    def to_inp(self):
        build_str = ""
        for section in self.sections:
            build_str += section.to_inp()
        return build_str

    @staticmethod
    def printable_to_attribute(name):
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

    def set_from_text(self, text):
        self.value = text
        for line in text.splitlines():
            if not line.startswith((';', '[')):
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

        if isinstance(self.value, basestring):
            return self.value
        elif isinstance(self.value, (list, tuple)):
            inp = self.name + '\n'
            for item in self.value:
                if hasattr(item, "to_inp"):
                    inp += item.to_inp() + '\n'
                else:
                    inp += item + '\n'
            return inp
        else:
            return self.value
