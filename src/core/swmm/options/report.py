from core.inputfile import Section


class Report(Section):
    """Report Options"""

    SECTION_NAME = "[REPORT]"

    field_dict = {
     "INPUT": "input",
     "CONTINUITY": "continuity",
     "FLOWSTATS": "flow_stats",
     "CONTROLS": "controls",
     "SUBCATCHMENTS": "subcatchments",  # ALL / NONE / <list of subcatchment names>
     "NODES": "nodes",                  # ALL / NONE / <list of node names>
     "LINKS": "links"}                  # ALL / NONE / <list of link names>
    """Mapping from label used in file to field name"""

    LISTS = ("subcatchments", "nodes", "links")

    EMPTY_LIST = ["NONE"]

    def __init__(self):
        Section.__init__(self)

        self.comment = ";;Reporting Options"

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

    def set_text(self, new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """

        self.__init__()  # Reset all values to defaults

        for line in new_text.splitlines():
            (attr_name, attr_value) = self.get_field_dict_value(line)
            if attr_name:
                if attr_name in Report.list_attributes:
                    attr_value = attr_value.split()
                    existing_value = getattr(self, attr_name, Report.EMPTY_LIST)
                    if existing_value != Report.EMPTY_LIST:  # include values already set on other lines
                        attr_value = existing_value + attr_value
                self.setattr_keep_type(attr_name, attr_value)


