from enum import Enum


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


class Curve:
    """Defines data curves and their X,Y points"""
    def __init__(self):
        self.Name = ""			# string
        """Curve ID Label"""

        self.Type = CurveType.PUMP			# PUMP, EFFICIENCY, VOLUME, or HEAD_LOSS
        """Curve type"""

        self.XValues = 0.0		# real array
        """X Values"""

        self.YValues = 0.0		# real array
        """Y Values"""


