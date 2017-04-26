from core.project_base import Section
from enum import Enum


class BackdropOptions(Section):
    """Identifies a backdrop image and dimensions for the network map"""

    SECTION_NAME = "[BACKDROP]"

    def __init__(self):
        Section.__init__(self)

        self.dimensions = (0.0, 0.0, 0.0, 0.0)  # real
        """provides the X and Y coordinates of the lower-left and upper-right corners of the maps bounding rectangle"""

        self.file = "" 		                    # string
        """name of the file that contains the backdrop image"""

        self.units = ""      # "None"  # string
        self.offset = None   # (0.0, 0.0)  # real
        self.scaling = None  # (0.0, 0.0)  # real

