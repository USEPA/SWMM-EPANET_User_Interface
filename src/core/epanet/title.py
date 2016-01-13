from core.inputfile import Section


class Title(Section):
    """EPANET descriptive title"""

    SECTION_NAME = "[TITLE]"

    # @staticmethod
    # def default():
    #     return Title(EPANETOptions.SECTION_NAME, None, None, -1)

    def __init__(self, name, value, default_value, index):
        self.title = ""
        """Descriptive title"""

        Section.__init__(self, name, value, default_value, index)

    def set_from_text(self, text):
        lines = text.splitlines()
        del lines[0]  # skip [TITLE] line
        self.title = '\n'.join(lines)

