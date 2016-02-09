from enum import Enum

from core.inputfile import Section
from core.epanet.options.quality import QualityOptions
from core.epanet.options.hydraulics import HydraulicsOptions

class Options(Section):
    """EPANET Options"""

    SECTION_NAME = "[OPTIONS]"

    def __init__(self):
        Section.__init__(self)

        self.hydraulics = HydraulicsOptions()
        """Hydraulics options"""

        self.quality = QualityOptions()
        """Water quality options"""

        self.map = ""
        """Name of a file containing coordinates of the network's nodes, not written if not set"""

    @property
    def text(self):
        """Contents of this item formatted for writing to file"""
        text_list = [self.SECTION_NAME]
        if self.hydraulics is not None:
            text_list.append(self.hydraulics.text)
        if self.quality is not None:
            text_list.append(self.quality.text)
        if self.map:
            text_list.append(" MAP                \t" + self.map)
        return '\n'.join(text_list)

    @text.setter
    def text(self, new_text):
        """Read this section from the text representation"""
        self.hydraulics.text = new_text
        self.quality.text = new_text
