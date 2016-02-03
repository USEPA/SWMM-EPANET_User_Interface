from core.inputfile import Section
from enum import Enum


class StatusWrite(Enum):
    """Report writing options"""
    YES = 1
    NO = 2
    FULL = 3


class StatusYesNo(Enum):
    """Report writing options"""
    YES = 1
    NO = 2


class ReportOptions(Section):
    """Report Options"""

    SECTION_NAME = "[REPORT]"

    def __init__(self):
        Section.__init__(self)

        self.pagesize = 0		# integer
        """sets the number of lines written per page of the output report"""

        self.file = ""			# string
        """supplies the name of a file to which the output report will be written"""
        """don't write by default"""

        self.status = StatusWrite.NO		# YES/NO/FULL
        """determines whether a hydraulic status report should be generated"""

        self.summary = StatusYesNo.YES		# YES/NO
        """determines whether a summary table of number of network components and key analysis options is generated"""

        self.energy = StatusYesNo.NO        # YES/NO
        """determines if a table reporting average energy usage and cost for each pump is provided"""
        """don't write by default"""

        self.parameters = ""		        # string -- note could be multiple parameter lines
        """used to identify which quantities are reported on"""
        """don't write by default"""
