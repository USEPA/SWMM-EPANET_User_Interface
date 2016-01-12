from enum import Enum


class CurveType(Enum):
    """Curve Type"""
    PUMP = 1
    EFFICIENCY = 2
    VOLUME = 3
    HEAD_LOSS = 4


class Curve:
    """Defines data curves and their X,Y points"""
    def __init__(self):
        self.Name = ""			# string
        """Curve ID Label"""

        self.Description = ""   # string
        """Curve description"""

        self.Type = CurveType.PUMP			# PUMP, EFFICIENCY, VOLUME, or HEAD_LOSS
        """Curve type"""

        self.XValues = 0.0		# real array
        """X Values"""

        self.YValues = 0.0		# real array
        """Y Values"""


