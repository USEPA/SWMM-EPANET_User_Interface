from core.project_base import Section
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

    def __init__(self):
        Section.__init__(self)

        self.dimensions = (0.0, 0.0, 0.0, 0.0)  # real
        """
        Coordinates of the map extent:
        X1 lower-left X coordinate of full map extent
        Y1 lower-left Y coordinate of full map extent
        X2 upper-right X coordinate of full map extent
        Y2 upper-right Y coordinate of full map extent
        """

        self.units = MapUnits.NONE
        """map units"""

    def setMapUnits(self, unit):
        if unit.upper() == 'FEET':
            self.units = MapUnits.FEET
        elif unit.upper() == 'METERS':
            self.units = MapUnits.METERS
        elif unit.upper() == 'DEGREES':
            self.units = MapUnits.DEGREES
        elif unit.upper() == 'NONE':
            self.units = MapUnits.NONE

