from core.inputfile import Section
from enum import Enum


class BackdropUnits(Enum):
    """units of map dimensions"""
    FEET = 1
    METERS = 2
    DEGREES = 3
    NONE = 4


class BackdropOptions(Section):
    """Identifies a backdrop image and dimensions for the network map"""

    SECTION_NAME = "[BACKDROP]"

    @staticmethod
    def default():
        return BackdropOptions(BackdropOptions.SECTION_NAME, None, -1)

    def __init__(self, name, value, index):
        Section.__init__(self, name, value, None, index)
        # TODO: parse "value" argument to extract values for each field, after setting default values below
        # TODO: document valid values in docstrings below and/or implement each as an Enum or class

        self.dimensions = (0.0, 0.0, 0.0, 0.0)  # real
        """provides the X and Y coordinates of the lower-left and upper-right corners of the map’s bounding rectangle"""

        self.units = BackdropUnits.NONE			# FEET/METERS/DEGREES/NONE
        """specifies the units that the map’s dimensions are given in"""

        self.file = "" 		                    # string
        """name of the file that contains the backdrop image"""

        self.offset_x = 0.0			            # real
        """X distance that the upper-left corner of the backdrop image is offset from the map’s bounding rectangle"""

        self.offset_y = 0.0			            # real
        """Y distance that the upper-left corner of the backdrop image is offset from the map’s bounding rectangle"""
