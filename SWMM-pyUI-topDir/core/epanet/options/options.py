from enum import Enum

from core.project_base import Section
from core.epanet.options.quality import QualityOptions
from core.epanet.options.hydraulics import HydraulicsOptions


class Options(Section):
    """EPANET Options"""

    SECTION_NAME = "[OPTIONS]"

    def __init__(self):
        Section.__init__(self)

        ## HydraulicsOptions: Hydraulics options
        self.hydraulics = HydraulicsOptions()

        ## QualityOptions: Water quality options
        self.quality = QualityOptions()

        ## str: Name of a file containing coordinates of the network's nodes, not written if not set
        self.map = ""


