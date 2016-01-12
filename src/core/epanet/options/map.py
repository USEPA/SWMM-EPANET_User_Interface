from core.inputfile import Section


class MapOptions(Section):
    """EPANET Map Options"""

    SECTION_NAME = "[OPTIONS]"

    # @staticmethod
    # def default():
    #     return EPANETOptions(EPANETOptions.SECTION_NAME, None, None, -1)

    def __init__(self, name, value, default_value, index):
        Section.__init__(self, name, value, None, index)
        # TODO: parse "value" argument to extract values for each field, after setting default values below
        # TODO: document valid values in docstrings below and/or implement each as an Enum or class

        self.map = ""
        """Name of a file containing coordinates of the network's nodes"""
