from core.project_base import Section


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
        lines = new_text.replace(self.SECTION_NAME, '').strip().splitlines()
        if len(lines) > 0:
            self.title = lines[0]
        if len(lines) > 1:
            self.notes = '\n'.join(lines[1:])
