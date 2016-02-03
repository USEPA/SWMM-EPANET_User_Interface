from core.inputfile import Section


class Title(Section):
    """SWMM descriptive title"""

    SECTION_NAME = "[TITLE]"

    # @staticmethod
    # def default():
    #     return Title(SWMMOptions.SECTION_NAME, None, None, -1)

    def __init__(self):
        Section.__init__(self)

        self.title = ""
        """Descriptive title"""


