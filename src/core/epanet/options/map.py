from core.inputfile import Section


class MapOptions(Section):
    """EPANET Map Options"""

    SECTION_NAME = "[OPTIONS]"

    # @staticmethod
    # def default():
    #     return EPANETOptions(EPANETOptions.SECTION_NAME, None, None, -1)

    def __init__(self):
        Section.__init__(self)

        self.map = ""
        """Name of a file containing coordinates of the network's nodes"""
