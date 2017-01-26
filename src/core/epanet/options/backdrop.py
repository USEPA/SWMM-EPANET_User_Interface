from core.project_base import Section
from enum import Enum


class BackdropUnits(Enum):
    """units of map dimensions"""
    NONE = 0
    FEET = 1
    METERS = 2
    DEGREES = 3


class BackdropOptions(Section):
    """Identifies a backdrop image and dimensions for the network map"""

    SECTION_NAME = "[BACKDROP]"

    def __init__(self):
        Section.__init__(self)

        ## X and Y coordinates of the lower-left and upper-right corners of the map's bounding rectangle
        self.dimensions = ("0.0", "0.0", "10000.0", "10000.0")  # lst:X_Southwest, Y_Southwest, X_northeast, Y_northeast

        ## specifies the units that the map's dimensions are given in
        self.units = BackdropUnits.NONE			# FEET/METERS/DEGREES/NONE

        ## Name of the file that contains the backdrop image
        self.file = '' 		                    # str

        ## Distance the upper-left corner of the backdrop image is offset from the map's bounding rectangle (X, Y)
        self.offset = ("0.0", "0.0")            # lst of str (X_offset, Y_offset)

