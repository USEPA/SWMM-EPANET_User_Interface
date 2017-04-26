from enum import Enum
from core.project_base import Section


class CurveType(Enum):
    """Curve Type"""
    STORAGE = 1
    SHAPE = 2
    DIVERSION = 3
    TIDAL = 4
    PUMP1 = 5
    PUMP2 = 6
    PUMP3 = 7
    PUMP4 = 8
    RATING = 9
    CONTROL = 10


class Curve(Section):
    """Defines data curves and their X,Y points"""


    def __init__(self):
        Section.__init__(self)

        self.name = "Unnamed"      # string
        """Curve name/ID/Label"""

        self.curve_type = CurveType.PUMP1
        """Curve type"""

        self.curve_xy = []      # list of (x, y) tuples
        """X, Y Values"""


