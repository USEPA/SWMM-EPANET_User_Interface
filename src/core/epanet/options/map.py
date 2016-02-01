from core.inputfile import Section


class MapOptions(Section):
    """EPANET Map Options"""

    SECTION_NAME = "[MAP]"

    def __init__(self):
        Section.__init__(self)

        self.map = ""
        """Name of a file containing coordinates of the network's nodes"""
        """Don't write by default"""
