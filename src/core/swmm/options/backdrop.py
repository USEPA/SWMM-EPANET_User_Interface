from core.inputfile import Section
from enum import Enum


class BackdropOptions(Section):
    """Identifies a backdrop image and dimensions for the network map"""

    SECTION_NAME = "[BACKDROP]"

    def __init__(self):
        Section.__init__(self)
        # TODO: parse "value" argument to extract values for each field, after setting default values below
        # TODO: document valid values in docstrings below and/or implement each as an Enum or class

        self.dimensions = (0.0, 0.0, 0.0, 0.0)  # real
        """provides the X and Y coordinates of the lower-left and upper-right corners of the maps bounding rectangle"""

        self.file = "" 		                    # string
        """name of the file that contains the backdrop image"""
