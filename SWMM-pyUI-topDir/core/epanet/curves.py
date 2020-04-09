import traceback
from enum import Enum
from core.project_base import Section


class CurveType(Enum):
    """Curve Type"""
    UNSET = 0
    PUMP = 1
    EFFICIENCY = 2
    VOLUME = 3
    HEADLOSS = 4


class Curve(Section):
    """Defines a data curve of X,Y points"""


    def __init__(self):
        Section.__init__(self)

        ## Curve name/ID/Label
        self.name = ''      # string

        ## Curve description
        self.description = ''   # string

        ## CurveType: Type of Curve
        self.curve_type = CurveType.UNSET    # PUMP, EFFICIENCY, VOLUME, or HEADLOSS

        ## X, Y Values
        self.curve_xy = []      # list of (x, y) tuples


