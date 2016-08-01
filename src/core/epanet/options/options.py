from enum import Enum

from core.project_base import Section
from core.epanet.options.quality import QualityOptions
from core.epanet.options.hydraulics import HydraulicsOptions


class Options(Section):
    """EPANET Options"""

    SECTION_NAME = "[OPTIONS]"

    section_comments = (";; Hydraulics", ";; Water Quality")

    def __init__(self):
        Section.__init__(self)

        self.hydraulics = HydraulicsOptions()
        """HydraulicsOptions: Hydraulics options"""

        self.quality = QualityOptions()
        """QualityOptions: Water quality options"""

        self.map = ""
        """str: Name of a file containing coordinates of the network's nodes, not written if not set"""

    def get_text(self):
        """Contents of this item formatted for writing to file"""
        text_list = [self.SECTION_NAME]
        if self.map:
            text_list.append(" MAP                \t" + self.map)
        if self.hydraulics is not None:
            text_list.append(Options.section_comments[0])
            text_list.append(self.hydraulics.get_text())
        if self.quality is not None:
            text_list.append(Options.section_comments[1])
            text_list.append(self.quality.get_text())
        return '\n'.join(text_list)

    def set_text(self, new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        self.__init__()
        # Skip the comments we insert automatically
        for comment in Options.section_comments:
            new_text = new_text.replace(comment + '\n', '')
        self.hydraulics.set_text(new_text)
        self.quality.set_text(new_text)
        for line in new_text.splitlines():
            line_list = line.split()
            if line_list:
                if str(line_list[0]).strip().upper() == "MAP":
                    self.map = ' '.join(line_list[1:])
