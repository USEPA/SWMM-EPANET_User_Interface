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

        self.pagesize = ''
        """sets the number of lines written per page of the output report"""

        self.file = ''                  # string
        """supplies the name of a file to which the output report will be written"""
        """don't write by default"""

        self.status = StatusWrite.NO    # YES/NO/FULL
        """determines whether a hydraulic status report should be generated"""

        self.summary = True             # YES/NO
        """determines whether a summary table of number of network components and key analysis options is generated"""

        self.energy = False             # YES/NO
        """determines if a table reporting average energy usage and cost for each pump is provided"""
        """don't write by default"""

        # self.nodes = []
        """identifies which nodes will be reported on. List individual IDs or use NONE or ALL"""

        # self.links = []
        """identifies which links will be reported on. List individual IDs or use NONE or ALL"""

        self.parameters = []            # list of strings
        """used to identify which nodes, links, and quantities are reported on"""
        """don't write if blank"""

    @property
    def page(self):
        """Alias for pagesize"""
        return self.pagesize

    @page.setter
    def page(self, new_value):
        """Alias for pagesize"""
        self.pagesize = new_value

    def get_text(self):
        txt = Section.get_text(self)
        if self.parameters:
            txt += '\n' + '\n'.join(self.parameters)
        return txt
    #     # [self.SECTION_NAME]
    #     # self._get_attr_line("Status", "status")
    #     # Section.__getattribute__()
    #     # txt.append("Status\t" + self.status.name)
    #     # if self.file:
    #     #     txt.append("File\t" + str(self.file))
    #     # if self.pagesize:
    #     #     txt.append("Pagesize\t" + str(self.pagesize))
    #     # if self.pagesize:
    #     #     txt.append("Pagesize\t" + str(self.pagesize))
    #     # if self.file:
    #     #     txt.append("File\t" + str(self.file))
    #     # txt.append(Section.get_text(self))  # Get text for the global variables using metadata
    #     if self.nodes:
    #         txt += '\n' + self.field_format.format("Nodes", ' '.join()
    #     return '\n'.join(txt)

    # def set_text(self, new_text):
    #     """Read this section from the text representation"""
    #     Section.set_text(self, new_text)  # Initialize, and set values using metadata
    #     # Custom code to set nodes and links since they may be split across lines
    #     self.nodes = []
    #     self.links = []
    #     for line in new_text.splitlines():
    #         (attr_name, attr_value) = new_text.split(None, 1)
    #         attr_name = attr_name.upper()
    #         if attr_name == "NODES":
    #             self.nodes.extend(attr_value.split())
    #         elif attr_name == "LINKS":
    #             self.links.extend(attr_value.split())
    #         elif attr_name in ()
    #         elif attr_name == "STATUS":
    #             self.status = attr_value
    #         elif attr_name == "SUMMARY":
    #             self.setattr_keep_type("summary", attr_value)
    #         elif attr_name == "PAGESIZE" or attr_name == "PAGE":
    #             self.pagesize = attr_value
    #         elif attr_name == "ENERGY":
    #             self.setattr_keep_type("energy", attr_value)
    #         else:
    #             self.parameters.extend(line)


    def set_text_line(self, line):
        """Set part of this section from one line of text.
            Args:
                line (str): One line of text formatted as input file.
        """
        line = self.set_comment_check_section(line)
        if line.strip():
            # Set fields from metadata
            (attr_name, attr_value) = self.get_attr_name_value(line)
            if attr_name:  # Set fields from metadata
                try:
                    self.setattr_keep_type(attr_name, attr_value)
                    return
                except:
                    print("Section report could not set " + attr_name)
            else:
                self.parameters.append(line)
