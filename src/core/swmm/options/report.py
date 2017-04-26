from core.project_base import Section
from core.metadata import Metadata


class Report(Section):
    """Report Options"""

    SECTION_NAME = "[REPORT]"

    DEFAULT_COMMENT = ";;Reporting Options"

    #    attribute,            input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("input", "INPUT"),
        ("continuity", "CONTINUITY"),
        ("flow_stats", "FLOWSTATS"),
        ("controls", "CONTROLS"),
        ("subcatchments", "SUBCATCHMENTS"),
        ("nodes", "NODES"),
        ("links", "LINKS"),
        ("lids", "LID")))
    """Mapping between attribute name and name used in input file"""

    LISTS = ("subcatchments", "nodes", "links", "lids")

    EMPTY_LIST = ["NONE"]
    ALL_LIST = ["ALL"]

    def __init__(self):
        Section.__init__(self)

        ## Whether report includes a summary of the input data
        self.input = False

        ## Whether to report continuity checks
        self.continuity = True

        ## Whether to report summary flow statistics
        self.flow_stats = True

        ## Whether to list all control actions taken during a simulation
        self.controls = False

        ## List of subcatchments whose results are to be reported, or ALL or NONE
        self.subcatchments = Report.ALL_LIST

        ## List of nodes whose results are to be reported, or ALL or NONE
        self.nodes = Report.ALL_LIST

        ## List of links whose results are to be reported, or ALL or NONE
        self.links = Report.ALL_LIST

        ## List of lid specifications whose results are to be reported.
        ## Includes LID control name, subcatchment id and file name.
        self.lids = []

