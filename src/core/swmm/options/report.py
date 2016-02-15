from core.inputfile import Section


class Report(Section):
    """Report Options"""

    SECTION_NAME = "[REPORT]"

    field_dict = {
     "CONTROLS": "controls",
     "INPUT": "input"}
    """Mapping from label used in file to field name"""

    def __init__(self):
        Section.__init__(self)

        self.input = False
        """Whether report includes a summary of the input data"""

        self.continuity = False
        """Whether to report continuity checks"""

        self.flow_stats = False
        """Whether to report summary flow statistics"""

        self.controls = False
        """Whether to list all control actions taken during a simulation"""

        self.subcatchments = ""
        """List of subcatchments whose results are to be reported, or ALL or NONE"""

        self.nodes = ""
        """List of nodes whose results are to be reported, or ALL or NONE"""

        self.links = ""
        """List of links whose results are to be reported, or ALL or NONE"""

