from enum import Enum
from core.inputfile import Section


class StatusWrite(Enum):
    """Report writing options"""
    YES = 1
    NO = 2
    FULL = 3


class ReportOptions(Section):
    """Report Options"""

    SECTION_NAME = "[REPORT]"

    field_dict = {
        "Status": "status",
        "Summary": "summary",
        "Page": "pagesize",
        "Energy": "energy",
        "File": "file"}
    """Mapping from label used in file to field name"""

    def __init__(self):
        Section.__init__(self)

        self.pagesize = 0               # integer
        """sets the number of lines written per page of the output report"""

        self.file = ""                  # string
        """supplies the name of a file to which the output report will be written"""
        """don't write by default"""

        self.status = StatusWrite.NO    # YES/NO/FULL
        """determines whether a hydraulic status report should be generated"""

        self.summary = True             # YES/NO
        """determines whether a summary table of number of network components and key analysis options is generated"""

        self.energy = False             # YES/NO
        """determines if a table reporting average energy usage and cost for each pump is provided"""
        """don't write by default"""

        self.parameters = ""            # string -- could be multiple parameter lines
        """used to identify which quantities are reported on"""
        """don't write by default"""

    @property
    def page(self):
        """Alias for pagesize"""
        return self.pagesize

    @page.setter
    def page(self, new_value):
        """Alias for pagesize"""
        self.pagesize = new_value
