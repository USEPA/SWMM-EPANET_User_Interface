from core.inputfile import Section


class Title(Section):
    """EPANET descriptive title"""

    SECTION_NAME = "[TITLE]"

    def __init__(self):
        Section.__init__(self)
        self.title = ""
        self.notes = ""
        """str: Descriptive title"""

    def get_text(self):
        """format contents of this item for writing to file"""
        return Title.SECTION_NAME + '\n' + self.title + '\n' + self.notes

    def set_text(self, new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        self.__init__()
        for line in new_text.splitlines()[1:]:  # include all after first [TITLE] line
            if len(self.title) == 0:
                self.title = line
            else:
                if len(self.notes) > 0:
                    self.notes += '\n'
                self.notes += line
