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
        self.curve_id = ""			# string
        """Curve ID Label"""

        self.description = ""   # string
        """Curve description"""

        self.curve_type = CurveType.PUMP			# PUMP, EFFICIENCY, VOLUME, or HEAD_LOSS
        """Curve type"""

        self.curve_xy = []		# list of (x, y) tuples
        """X, Y Values"""

    def to_inp(self):
        """format contents of this item for writing to file"""
        inp = str(self.curve_id)
        if len(self.description) > 0:
            inp += self.description + '\n'
        for xy in self.curve_xy:
            inp += '\t' + xy[0] + '\t' + xy[1] + '\n'
        """TODO: What is the rule for creating columns? Will any amount of whitespace work?"""
        return inp

    def set_from_text(self, text):
        fields = text.split()
        self.curve_id = fields[0]
        self.curve_xy.append((fields[1], fields[2]))

