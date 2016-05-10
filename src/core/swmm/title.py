from core.inputfile import Section


class Title(Section):
    """SWMM descriptive title"""

    SECTION_NAME = "[TITLE]"

    def __init__(self):
        Section.__init__(self)
        self.title = ""
        """str: Descriptive title"""

    def get_text(self):
        """format contents of this item for writing to file"""
        return Title.SECTION_NAME + '\n' + self.title

    def set_text(self, new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        self.__init__()
        # Skip section name and blank lines/spaces/tabs at beginning or end
        lines = new_text.replace(self.SECTION_NAME, '').strip().splitlines()
        if len(lines) > 0:
            self.title = '\n'.join(lines)
