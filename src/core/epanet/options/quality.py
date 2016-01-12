from enum import Enum

from core.inputfile import Section


class Quality(Enum):
    """Type of Water Quality Analysis"""
    NONE = 1
    CHEMICAL = 2
    AGE = 3
    TRACE = 4


class QualityOptions(Section):
    """EPANET Quality Options"""

    SECTION_NAME = "[OPTIONS]"

    # @staticmethod
    # def default():
    #     return QualityOptions(EPANETOptions.SECTION_NAME, None, None, -1)

    def __init__(self, name, value, default_value, index):
        Section.__init__(self, name, value, None, index)
        # TODO: parse "value" argument to extract values for each field, after setting default values below
        # TODO: document valid values in docstrings below and/or implement each as an Enum or class

        self.quality = Quality.NONE
        """Type of water quality analysis to perform"""

        self.chemical_name = ""
        """Name of chemical to be analyzed in quality section"""

        self.mass_units = ""
        """Units of chemical to be analyzed in quality section"""

        self.relative_diffusivity = 1.0
        """Molecular diffusivity of the chemical being analyzed relative to that of chlorine in water"""

        self.trace_node = ""
        """Node id to use in a quality trace"""

        self.tolerance = 0.01
        """Difference in water quality level below one parcel of water is essentially the same as another"""

