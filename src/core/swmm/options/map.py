from core.inputfile import Section
from enum import Enum


class MapUnits(Enum):
    """Options for map units"""
    FEET = 1
    METERS = 2
    DEGREES = 3
    NONE = 4


class MapOptions(Section):
    """SWMM Map Options"""

    SECTION_NAME = "[MAP]"

    # @staticmethod
    # def default():
    #     return SWMMOptions(SWMMOptions.SECTION_NAME, None, None, -1)

    def __init__(self, name, value, default_value, index):
        Section.__init__(self, name, value, None, index)
        # TODO: parse "value" argument to extract values for each field, after setting default values below

        self.dimensions = []
        """
        Coordinates of the map extent:
        X1 lower-left X coordinate of full map extent
        Y1 lower-left Y coordinate of full map extent
        X2 upper-right X coordinate of full map extent
        Y2 upper-right Y coordinate of full map extent
        """

        self.units = MapUnits.FEET
        """map units"""
