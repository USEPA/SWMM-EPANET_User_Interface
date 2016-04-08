from core.inputfile import Section
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

    def __init__(self):
        Section.__init__(self)

        self.input = False
        """Whether report includes a summary of the input data"""

        self.continuity = True
        """Whether to report continuity checks"""

        self.flow_stats = True
        """Whether to report summary flow statistics"""

        self.controls = False
        """Whether to list all control actions taken during a simulation"""

        self.subcatchments = Report.EMPTY_LIST
        """List of subcatchments whose results are to be reported, or ALL or NONE"""

        self.nodes = Report.EMPTY_LIST
        """List of nodes whose results are to be reported, or ALL or NONE"""

        self.links = Report.EMPTY_LIST
        """List of links whose results are to be reported, or ALL or NONE"""

        self.lids = Report.EMPTY_LIST
        """List of lid specifications whose results are to be reported.
        Includes LID control name, subcatchment id and file name."""

    def set_text(self, new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """

        self.__init__()  # Reset all values to defaults

        for line in new_text.splitlines():
            line = self.set_comment_check_section(line)
            (attr_name, attr_value) = self.get_attr_name_value(line)
            if attr_name:
                if attr_name in Report.LISTS:
                    attr_value = attr_value.split()
                    existing_value = getattr(self, attr_name, Report.EMPTY_LIST)
                    if existing_value != Report.EMPTY_LIST:  # include values already set on other lines
                        attr_value = existing_value + attr_value
                self.setattr_keep_type(attr_name, attr_value)


