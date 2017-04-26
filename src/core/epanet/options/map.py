from core.project_base import Section


class MapOptions(Section):
    """EPANET Map Options"""

    SECTION_NAME = "[OPTIONS]"

    def __init__(self):
        Section.__init__(self)

        ## Name of a file containing coordinates of the network's nodes;
        ## Don't write by default
        self.map = ""
        ## crs information
        self.crs_name = None
        self.crs_unit = None
