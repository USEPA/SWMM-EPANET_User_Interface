from enum import Enum
from core.inputfile import Section


class StatusYesNo(Enum):
    """Report writing options"""
    YES = 1
    NO = 2


class Report(Section):
    """Report Options"""

    SECTION_NAME = "[REPORT]"

    field_dict = {
     "CONTROLS": "controls",
     "INPUT": "input"}
    """Mapping from label used in file to field name"""

    def __init__(self):
        Section.__init__(self)

        self.input = StatusYesNo.NO
        """Whether report includes a summary of the input data"""

        self.continuity = StatusYesNo.NO
        """Whether to report continuity checks"""

        self.flow_stats = StatusYesNo.NO
        """Whether to report summary flow statistics"""

        self.controls = StatusYesNo.NO
        """Whether to list all control actions taken during a simulation"""

        self.subcatchments = ""
        """List of subcatchments whose results are to be reported, or ALL or NONE"""

        self.nodes = ""
        """List of nodes whose results are to be reported, or ALL or NONE"""

        self.links = ""
        """List of links whose results are to be reported, or ALL or NONE"""

