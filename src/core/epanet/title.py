from core.inputfile import Section


class Title(Section):
    """EPANET descriptive title"""

    SECTION_NAME = "[TITLE]"

    # @staticmethod
    # def default():
    #     return Title(EPANETOptions.SECTION_NAME, None, None, -1)

    def __init__(self):
        Section.__init__(self)
        self.title = ""
        """Descriptive title"""

    @property
    def text(self):
        """format contents of this item for writing to file"""
        return Title.SECTION_NAME + '\n' + self.title

    @text.setter
    def text(self, new_text):
        """read properties from text"""
        lines = new_text.splitlines()
        del lines[0]  # skip [TITLE] line
        self.title = '\n'.join(lines)
