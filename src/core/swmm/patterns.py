from enum import Enum
from core.project_base import Section


class PatternType(Enum):
    """Pattern Type"""
    MONTHLY = 1
    DAILY = 2
    HOURLY = 3
    WEEKEND = 4


class Pattern(Section):
    """Pattern multipliers define how some base quantity is adjusted for each time period"""
    def __init__(self):
        Section.__init__(self)

        self.name = "Unnamed"
        """Pattern name"""

        self.pattern_type = PatternType.MONTHLY
        """Pattern type"""

        self.description = ''
        """Pattern description"""

        self.multipliers = []
        """Array of multipliers for this pattern"""

