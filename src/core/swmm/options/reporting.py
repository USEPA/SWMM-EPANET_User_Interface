import core.inputfile


class Reporting(core.inputfile.Section):
    """Report Options"""

    SECTION_NAME = "[REPORT]"

    @staticmethod
    def default():
        return ReportOptions(ReportOptions.SECTION_NAME, None, -1)

    def __init__(self, name, value, index):
        core.inputfile.Section.__init__(self, name, value, None, index)
        # TODO: parse "value" argument to extract values for each field, after setting default values below
        # TODO: document valid values in docstrings below and/or implement each as an Enum or class

        self.input = False
        """Whether report includes a summary of the input data"""

        self.continuity = True
        """Whether to report continuity checks"""

        self.flow_stats = True
        """Whether to report summary flow statistics"""

        self.controls = False
        """Whether to list all control actions taken during a simulation"""

        self.subcatchments = {}
        """List of subcatchments whose results are to be reported"""

        self.nodes = {}
        """List of nodes whose results are to be reported"""

        self.links = {}
        """List of links whose results are to be reported"""
