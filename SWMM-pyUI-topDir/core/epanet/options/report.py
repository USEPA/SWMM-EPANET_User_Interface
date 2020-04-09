from enum import Enum
from core.project_base import Section
from core.metadata import Metadata


class StatusWrite(Enum):
    """Report writing options"""
    YES = 1
    NO = 2
    FULL = 3


class ReportOptions(Section):
    """Report Options"""

    SECTION_NAME = "[REPORT]"

    #     attribute, input_name
    metadata = Metadata((
        ("status",   "Status"),
        ("summary",  "Summary"),
        ("pagesize", "Page"),
        ("energy",   "Energy"),
        ("file",     "File")))

    metadata_lists = Metadata((
        ("nodes",   "Nodes"),
        ("links",   "Links"),
        ("elevation", "Elevation"),
        ("demand", "Demand"),
        ("head", "Head"),
        ("pressure", "Pressure"),
        ("quality", "Quality"),
        ("length", "Length"),
        ("diameter", "Diameter"),
        ("flow", "Flow"),
        ("velocity", "Velocity"),
        ("headloss", "Headloss"),
        ("position", "Position"),
        ("setting", "Setting"),
        ("reaction", "Reaction"),
        ("friction_factor", "F-Factor")))
    """Mapping between attribute name and name used in input file"""

    def __init__(self):
        Section.__init__(self)

        ## sets the number of lines written per page of the output report
        self.pagesize = ''

        ## supplies the name of a file to which the output report will be written;
        ## don't write by default"""
        self.file = ''                  # string

        ## determines whether a hydraulic status report should be generated
        self.status = StatusWrite.NO    # YES/NO/FULL

        ## determines whether a summary table of number of network components and key analysis options is generated
        self.summary = True             # YES/NO

        ## determines if a table reporting average energy usage and cost for each pump is provided;
        ## don't write by default"""
        self.energy = False             # YES/NO

        ## identifies which nodes will be reported on. List individual IDs or use NONE or ALL
        self.nodes = []

        ## identifies which links will be reported on. List individual IDs or use NONE or ALL
        self.links = []

        ## used to identify which quantities are reported on;
        ## don't write if blank
        self.parameters = []            # list of strings


    @property
    def page(self):
        """Alias for pagesize"""
        return self.pagesize

    @page.setter
    def page(self, new_value):
        """Alias for pagesize"""
        self.pagesize = new_value

