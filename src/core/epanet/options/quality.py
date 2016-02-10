from enum import Enum

from core.inputfile import Section


class QualityAnalysisType(Enum):
    """Type of Water Quality Analysis"""
    NONE = 1
    CHEMICAL = 2
    AGE = 3
    TRACE = 4


class QualityOptions(Section):
    """EPANET Quality Options"""

    SECTION_NAME = "[OPTIONS]"

    def __init__(self):
        Section.__init__(self)

        self.quality = QualityAnalysisType.NONE
        """Type of water quality analysis to perform"""

        self.chemical_name = ""
        """Name of chemical to be analyzed in quality section"""

        self.mass_units = ""
        """Units of chemical to be analyzed in quality section"""

        self.diffusivity = 1.0
        """Molecular diffusivity of the chemical being analyzed relative to that of chlorine in water"""

        self.trace_node = ""
        """Node id to use in a quality trace"""

        self.tolerance = 0.0
        """Difference in water quality level below one parcel of water is essentially the same as another"""

    @property
    def text(self):
        """Contents of this item formatted for writing to file"""
        txt = " Quality            \t"
        if self.quality is None or self.quality == QualityAnalysisType.NONE:
            txt = ""
        elif self.quality == QualityAnalysisType.AGE:
            txt += "AGE"
        elif self.quality == QualityAnalysisType.TRACE:
            txt += "Trace"
            if self.trace_node:
                txt += " " + self.trace_node
        elif self.quality == QualityAnalysisType.CHEMICAL:
            if self.chemical_name:
                txt += self.chemical_name
            else:
                txt += "CHEMICAL"
        if txt and self.mass_units:
            txt += " " + self.mass_units
        if txt:
            txt += "\n"
        txt += " Diffusivity        \t" + str(self.diffusivity) + "\n"
        txt += " Tolerance          \t" + str(self.tolerance) + "\n"
        return txt

    @text.setter
    def text(self, new_text):
        """Read this section from the text representation"""
        self.quality = QualityAnalysisType.NONE  # default to NONE until found below
        self.chemical_name = ""
        self.mass_units = ""
        self.trace_node = ""

        for line in new_text.splitlines():
            line_list = line.split()
            if line_list:
                if str(line_list[0]).strip().upper() == "QUALITY":
                    quality_type = str(line_list[1]).strip().upper()
                    try:
                        self.quality = QualityAnalysisType[quality_type]
                    except:
                        self.quality = QualityAnalysisType.CHEMICAL
                        self.chemical_name = str(line_list[1])
                    if self.quality == QualityAnalysisType.TRACE:
                        self.trace_node = line_list[2]
                    elif len(line_list) > 2:
                        self.mass_units = line_list[2]
                elif str(line_list[0]).strip().upper() == "DIFFUSIVITY":
                    self.diffusivity = float(line_list[1])
                elif str(line_list[0]).strip().upper() == "TOLERANCE":
                    self.tolerance = float(line_list[1])
